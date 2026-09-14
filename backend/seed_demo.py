"""
Seed de datos de demostración para Food Store.

Ejecutar desde backend/:
    python seed_demo.py

Es idempotente: si los datos ya existen, los omite.
Las tablas de catálogo base (perfiles, estados, formas de pago, unidades)
las maneja carga_inicial.py — este script agrega solo los datos de negocio.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/foodstore_new")

from sqlmodel import Session, select

from app.nucleo.proteccion import cifrar_clave
from app.persistencia.carga_inicial import ejecutar_carga_inicial
from app.persistencia.motor import crear_tablas, motor
import sqlalchemy as sa
from sqlmodel import SQLModel
from app.persistencia.entidades import (
    Articulo,
    ArticuloCategoria,
    Categoria,
    Cobro,
    ComposicionArticulo,
    Componente,
    Cuenta,
    CuentaPerfil,
    Domicilio,
    Orden,
    PartidaOrden,
    BitacoraOrden,
    Perfil,
    UnidadMedida,
)
from app.persistencia.motor import motor

# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------

CUENTAS_DEMO = [
    {"correo": "inventario@foodstore.com",  "clave": "Inventario1!", "nombre": "María Inventario",   "perfil": "INVENTARIO"},
    {"correo": "despacho@foodstore.com",    "clave": "Despacho1!",   "nombre": "Carlos Despacho",    "perfil": "DESPACHO"},
    {"correo": "comprador@foodstore.com",   "clave": "Comprador1!",  "nombre": "Ana García",         "perfil": "COMPRADOR"},
    {"correo": "comprador2@foodstore.com",  "clave": "Comprador1!",  "nombre": "Luis Martínez",      "perfil": "COMPRADOR"},
    {"correo": "comprador3@foodstore.com",  "clave": "Comprador1!",  "nombre": "Sofía Rodríguez",    "perfil": "COMPRADOR"},
    {"correo": "comprador4@foodstore.com",  "clave": "Comprador1!",  "nombre": "Tomás Fernández",    "perfil": "COMPRADOR"},
    {"correo": "comprador5@foodstore.com",  "clave": "Comprador1!",  "nombre": "Valentina López",    "perfil": "COMPRADOR"},
    {"correo": "comprador6@foodstore.com",  "clave": "Comprador1!",  "nombre": "Diego Sánchez",      "perfil": "COMPRADOR"},
    {"correo": "comprador7@foodstore.com",  "clave": "Comprador1!",  "nombre": "Camila Torres",      "perfil": "COMPRADOR"},
    {"correo": "comprador8@foodstore.com",  "clave": "Comprador1!",  "nombre": "Martín Pérez",       "perfil": "COMPRADOR"},
    {"correo": "comprador9@foodstore.com",  "clave": "Comprador1!",  "nombre": "Lucía Gómez",        "perfil": "COMPRADOR"},
    {"correo": "comprador10@foodstore.com", "clave": "Comprador1!",  "nombre": "Nicolás Díaz",       "perfil": "COMPRADOR"},
]

# Jerarquía: (nombre, padre_nombre | None)
CATEGORIAS_DEMO = [
    ("Comidas", None),
        ("Hamburguesas",    "Comidas"),
        ("Pizzas",          "Comidas"),
        ("Sandwichs",       "Comidas"),
        ("Ensaladas",       "Comidas"),
        ("Wraps",           "Comidas"),
        ("Minutas",         "Comidas"),
    ("Bebidas", None),
        ("Bebidas frías",   "Bebidas"),
        ("Bebidas calientes","Bebidas"),
        ("Jugos naturales", "Bebidas frías"),
        ("Gaseosas",        "Bebidas frías"),
    ("Postres", None),
        ("Helados",         "Postres"),
        ("Tortas",          "Postres"),
        ("Alfajores",       "Postres"),
    ("Extras", None),
        ("Salsas",          "Extras"),
        ("Porciones",       "Extras"),
]

COMPONENTES_DEMO = [
    # Panes (existencias en gramos)
    {"denominacion": "Pan brioche",          "existencias": 24000, "genera_alergia": True},
    {"denominacion": "Pan árabe",            "existencias": 12000, "genera_alergia": True},
    {"denominacion": "Pan lactal",           "existencias": 10000, "genera_alergia": True},
    {"denominacion": "Tortilla de trigo",    "existencias": 10000, "genera_alergia": True},
    # Carnes
    {"denominacion": "Medallón de carne",    "existencias": 60000, "genera_alergia": False},
    {"denominacion": "Pechuga de pollo",     "existencias": 45000, "genera_alergia": False},
    {"denominacion": "Panceta ahumada",      "existencias": 8000,  "genera_alergia": False},
    {"denominacion": "Jamón cocido",         "existencias": 15000, "genera_alergia": False},
    {"denominacion": "Chorizo",              "existencias": 18000, "genera_alergia": False},
    {"denominacion": "Salame",               "existencias": 7500,  "genera_alergia": False},
    # Lácteos / quesos
    {"denominacion": "Queso cheddar",        "existencias": 15000, "genera_alergia": True},
    {"denominacion": "Mozzarella",           "existencias": 60000, "genera_alergia": True},
    {"denominacion": "Queso azul",           "existencias": 3000,  "genera_alergia": True},
    {"denominacion": "Crema de leche",       "existencias": 6000,  "genera_alergia": True},
    {"denominacion": "Queso provolone",      "existencias": 6000,  "genera_alergia": True},
    # Verduras
    {"denominacion": "Lechuga",              "existencias": 18000, "genera_alergia": False},
    {"denominacion": "Tomate",               "existencias": 24000, "genera_alergia": False},
    {"denominacion": "Cebolla morada",       "existencias": 8000,  "genera_alergia": False},
    {"denominacion": "Pepino encurtido",     "existencias": 6000,  "genera_alergia": False},
    {"denominacion": "Rúcula",               "existencias": 5000,  "genera_alergia": False},
    {"denominacion": "Pimiento rojo",        "existencias": 6000,  "genera_alergia": False},
    {"denominacion": "Champiñones",          "existencias": 8000,  "genera_alergia": False},
    {"denominacion": "Espinaca",             "existencias": 6000,  "genera_alergia": False},
    {"denominacion": "Aceitunas",            "existencias": 3000,  "genera_alergia": False},
    # Salsas y condimentos
    {"denominacion": "Mayonesa",             "existencias": 8000,  "genera_alergia": True},
    {"denominacion": "Ketchup",              "existencias": 8000,  "genera_alergia": False},
    {"denominacion": "Mostaza",              "existencias": 6000,  "genera_alergia": False},
    {"denominacion": "Salsa BBQ",            "existencias": 7500,  "genera_alergia": False},
    {"denominacion": "Salsa de tomate",      "existencias": 40000, "genera_alergia": False},
    {"denominacion": "Aderezo César",        "existencias": 5000,  "genera_alergia": True},
    {"denominacion": "Chimichurri",          "existencias": 4000,  "genera_alergia": False},
    {"denominacion": "Alioli",               "existencias": 3000,  "genera_alergia": True},
    # Bases / masas
    {"denominacion": "Masa de pizza",        "existencias": 40000,  "genera_alergia": True},
    {"denominacion": "Papas fritas",         "existencias": 100000, "genera_alergia": False},
    {"denominacion": "Arroz blanco",         "existencias": 45000,  "genera_alergia": False},
    # Huevos y otros
    {"denominacion": "Huevo",                "existencias": 33000, "genera_alergia": True},
    {"denominacion": "Chocolate",            "existencias": 15000, "genera_alergia": True},
    {"denominacion": "Helado vainilla",      "existencias": 15000, "genera_alergia": True},
    {"denominacion": "Bizcochuelo",          "existencias": 12000, "genera_alergia": True},
    {"denominacion": "Dulce de leche",       "existencias": 12000, "genera_alergia": True},
    {"denominacion": "Coco rallado",         "existencias": 3000,  "genera_alergia": False},
    {"denominacion": "Galletita marinera",   "existencias": 12000, "genera_alergia": True},
]

_U = "https://images.unsplash.com/photo-"

# (titulo, descripcion, precio, existencias, disponible, [categorias], imagen_url, [(componente, gramos, extraible)])
ARTICULOS_DEMO = [
    # ---- HAMBURGUESAS ----
    {
        "titulo": "Hamburguesa Clásica",
        "descripcion": "Medallón de carne, queso cheddar, lechuga, tomate y mayonesa en pan brioche.",
        "precio": "1800.00", "existencias": 80, "disponible": True,
        "imagen": f"{_U}1568901346375-23c9450c58cd?w=800&q=80",
        "categorias": ["Hamburguesas"],
        "composicion": [
            ("Pan brioche", 80, False), ("Medallón de carne", 150, False),
            ("Queso cheddar", 30, True), ("Lechuga", 20, True),
            ("Tomate", 30, True), ("Mayonesa", 20, True),
        ],
    },
    {
        "titulo": "Hamburguesa Doble BBQ",
        "descripcion": "Doble medallón, panceta ahumada, cebolla caramelizada y salsa BBQ.",
        "precio": "2600.00", "existencias": 60, "disponible": True,
        "categorias": ["Hamburguesas"],
        "composicion": [
            ("Pan brioche", 80, False), ("Medallón de carne", 300, False),
            ("Panceta ahumada", 40, True), ("Cebolla morada", 20, True),
            ("Queso cheddar", 30, True), ("Salsa BBQ", 25, True),
        ],
    },
    {
        "titulo": "Hamburguesa Veggie",
        "descripcion": "Medallón de vegetales, queso, tomate, lechuga y pepino encurtido.",
        "precio": "1600.00", "existencias": 40, "disponible": True,
        "categorias": ["Hamburguesas"],
        "composicion": [
            ("Pan brioche", 80, False), ("Lechuga", 30, True),
            ("Tomate", 40, True), ("Queso cheddar", 30, True),
            ("Pepino encurtido", 20, True), ("Mayonesa", 20, True),
        ],
    },
    {
        "titulo": "Hamburguesa Blue Cheese",
        "descripcion": "Medallón de carne, queso azul, rúcula, cebolla caramelizada y alioli.",
        "precio": "2400.00", "existencias": 35, "disponible": True,
        "categorias": ["Hamburguesas"],
        "composicion": [
            ("Pan brioche", 80, False), ("Medallón de carne", 150, False),
            ("Queso azul", 30, True), ("Rúcula", 20, True),
            ("Cebolla morada", 20, True), ("Alioli", 20, True),
        ],
    },
    {
        "titulo": "Hamburguesa Pollo Crispy",
        "descripcion": "Pechuga de pollo crocante, coleslaw, pepino y mayonesa especiada.",
        "precio": "2000.00", "existencias": 50, "disponible": True,
        "categorias": ["Hamburguesas"],
        "composicion": [
            ("Pan brioche", 80, False), ("Pechuga de pollo", 150, False),
            ("Lechuga", 20, True), ("Mayonesa", 20, True),
            ("Pepino encurtido", 15, True),
        ],
    },
    {
        "titulo": "Hamburguesa Especial de la Casa",
        "descripcion": "Doble medallón, panceta, queso provolone fundido, huevo frito y chimichurri.",
        "precio": "3200.00", "existencias": 25, "disponible": True,
        "categorias": ["Hamburguesas"],
        "composicion": [
            ("Pan brioche", 80, False), ("Medallón de carne", 300, False),
            ("Panceta ahumada", 40, True), ("Queso provolone", 40, True),
            ("Huevo", 55, True), ("Chimichurri", 20, True),
        ],
    },
    # ---- PIZZAS ----
    {
        "titulo": "Pizza Margarita",
        "descripcion": "Salsa de tomate, mozzarella fresca y albahaca.",
        "precio": "2200.00", "existencias": 50, "disponible": True,
        "categorias": ["Pizzas"],
        "composicion": [
            ("Masa de pizza", 200, False), ("Salsa de tomate", 80, False),
            ("Mozzarella", 150, True),
        ],
    },
    {
        "titulo": "Pizza Napolitana",
        "descripcion": "Mozzarella, rodajas de tomate fresco, ajo y rúcula al final.",
        "precio": "2500.00", "existencias": 45, "disponible": True,
        "categorias": ["Pizzas"],
        "composicion": [
            ("Masa de pizza", 200, False), ("Salsa de tomate", 80, False),
            ("Mozzarella", 150, True), ("Tomate", 60, True), ("Rúcula", 20, True),
        ],
    },
    {
        "titulo": "Pizza Jamón y Morrones",
        "descripcion": "Salsa de tomate, mozzarella, jamón cocido y morrones asados.",
        "precio": "2700.00", "existencias": 40, "disponible": True,
        "categorias": ["Pizzas"],
        "composicion": [
            ("Masa de pizza", 200, False), ("Salsa de tomate", 80, False),
            ("Mozzarella", 150, True), ("Jamón cocido", 60, True),
            ("Pimiento rojo", 30, True),
        ],
    },
    {
        "titulo": "Pizza Fugazzeta",
        "descripcion": "Doble masa, mozzarella y cebolla abundante.",
        "precio": "2600.00", "existencias": 35, "disponible": True,
        "categorias": ["Pizzas"],
        "composicion": [
            ("Masa de pizza", 400, False), ("Mozzarella", 200, False),
            ("Cebolla morada", 80, True),
        ],
    },
    {
        "titulo": "Pizza Cuatro Quesos",
        "descripcion": "Mozzarella, cheddar, provolone y queso azul.",
        "precio": "3000.00", "existencias": 30, "disponible": True,
        "categorias": ["Pizzas"],
        "composicion": [
            ("Masa de pizza", 200, False), ("Salsa de tomate", 80, False),
            ("Mozzarella", 80, True), ("Queso cheddar", 40, True),
            ("Queso provolone", 40, True), ("Queso azul", 30, True),
        ],
    },
    {
        "titulo": "Pizza Vegetariana",
        "descripcion": "Tomate, champiñones, pimiento, aceitunas y rúcula.",
        "precio": "2400.00", "existencias": 30, "disponible": True,
        "categorias": ["Pizzas"],
        "composicion": [
            ("Masa de pizza", 200, False), ("Salsa de tomate", 80, False),
            ("Mozzarella", 120, True), ("Champiñones", 40, True),
            ("Pimiento rojo", 30, True), ("Aceitunas", 20, True),
        ],
    },
    # ---- SANDWICHS ----
    {
        "titulo": "Sandwich Club",
        "descripcion": "Pan lactal tostado, jamón, huevo duro, lechuga, tomate y mayonesa.",
        "precio": "1400.00", "existencias": 70, "disponible": True,
        "categorias": ["Sandwichs"],
        "composicion": [
            ("Pan lactal", 40, False), ("Jamón cocido", 60, True),
            ("Huevo", 55, True), ("Lechuga", 20, True),
            ("Tomate", 30, True), ("Mayonesa", 20, True),
        ],
    },
    {
        "titulo": "Choripán",
        "descripcion": "Chorizo a las brasas con chimichurri y tomate.",
        "precio": "1300.00", "existencias": 60, "disponible": True,
        "categorias": ["Sandwichs"],
        "composicion": [
            ("Pan lactal", 40, False), ("Chorizo", 120, False),
            ("Chimichurri", 20, True), ("Tomate", 30, True),
        ],
    },
    {
        "titulo": "Lomito Completo",
        "descripcion": "Medallón de carne, jamón, queso, huevo, lechuga, tomate y mayonesa.",
        "precio": "2200.00", "existencias": 45, "disponible": True,
        "categorias": ["Sandwichs"],
        "composicion": [
            ("Pan brioche", 80, False), ("Medallón de carne", 150, False),
            ("Jamón cocido", 40, True), ("Queso cheddar", 30, True),
            ("Huevo", 55, True), ("Lechuga", 20, True),
            ("Tomate", 30, True), ("Mayonesa", 20, True),
        ],
    },
    # ---- WRAPS ----
    {
        "titulo": "Wrap de Pollo",
        "descripcion": "Tortilla con pechuga grillada, lechuga, tomate, cheddar y aderezo César.",
        "precio": "1700.00", "existencias": 55, "disponible": True,
        "categorias": ["Wraps"],
        "composicion": [
            ("Tortilla de trigo", 50, False), ("Pechuga de pollo", 150, False),
            ("Lechuga", 30, True), ("Tomate", 30, True),
            ("Queso cheddar", 20, True), ("Aderezo César", 25, True),
        ],
    },
    {
        "titulo": "Wrap Veggie",
        "descripcion": "Tortilla con espinaca, champiñones, pimiento, queso y alioli.",
        "precio": "1500.00", "existencias": 40, "disponible": True,
        "categorias": ["Wraps"],
        "composicion": [
            ("Tortilla de trigo", 50, False), ("Espinaca", 30, True),
            ("Champiñones", 40, True), ("Pimiento rojo", 30, True),
            ("Queso cheddar", 20, True), ("Alioli", 20, True),
        ],
    },
    # ---- ENSALADAS ----
    {
        "titulo": "Ensalada César",
        "descripcion": "Lechuga romana, croutones, parmesano y aderezo César.",
        "precio": "1200.00", "existencias": 60, "disponible": True,
        "categorias": ["Ensaladas"],
        "composicion": [
            ("Lechuga", 150, False), ("Queso cheddar", 30, True),
            ("Aderezo César", 25, True),
        ],
    },
    {
        "titulo": "Ensalada Mediterránea",
        "descripcion": "Rúcula, tomate cherry, aceitunas, queso provolone y aceite de oliva.",
        "precio": "1300.00", "existencias": 45, "disponible": True,
        "categorias": ["Ensaladas"],
        "composicion": [
            ("Rúcula", 80, False), ("Tomate", 60, True),
            ("Aceitunas", 30, True), ("Queso provolone", 40, True),
        ],
    },
    # ---- MINUTAS ----
    {
        "titulo": "Milanesa con Papas",
        "descripcion": "Milanesa de carne rebozada con papas fritas.",
        "precio": "2100.00", "existencias": 50, "disponible": True,
        "categorias": ["Minutas"],
        "composicion": [
            ("Medallón de carne", 200, False), ("Papas fritas", 200, False),
            ("Ketchup", 20, True), ("Mayonesa", 20, True),
        ],
    },
    {
        "titulo": "Huevos Revueltos con Jamón",
        "descripcion": "Dos huevos revueltos con jamón y tostadas de pan lactal.",
        "precio": "1000.00", "existencias": 40, "disponible": True,
        "categorias": ["Minutas"],
        "composicion": [
            ("Huevo", 110, False), ("Jamón cocido", 60, True),
            ("Pan lactal", 40, False),
        ],
    },
    # ---- PORCIONES ----
    {
        "titulo": "Papas Fritas",
        "descripcion": "Porción de papas fritas crocantes con ketchup y mayonesa.",
        "precio": "900.00", "existencias": 120, "disponible": True,
        "categorias": ["Porciones"],
        "composicion": [
            ("Papas fritas", 200, False), ("Ketchup", 20, True), ("Mayonesa", 20, True),
        ],
    },
    {
        "titulo": "Papas con Queso y Panceta",
        "descripcion": "Papas fritas bañadas en queso fundido y panceta crocante.",
        "precio": "1300.00", "existencias": 70, "disponible": True,
        "categorias": ["Porciones"],
        "composicion": [
            ("Papas fritas", 200, False), ("Queso cheddar", 50, True),
            ("Panceta ahumada", 30, True),
        ],
    },
    # ---- SALSAS ----
    {
        "titulo": "Porción de Chimichurri",
        "descripcion": "Salsa criolla casera, perfecta para acompañar.",
        "precio": "300.00", "existencias": 200, "disponible": True,
        "categorias": ["Salsas"],
        "composicion": [("Chimichurri", 60, False)],
    },
    {
        "titulo": "Porción de Alioli",
        "descripcion": "Alioli casero de ajo y aceite de oliva.",
        "precio": "300.00", "existencias": 200, "disponible": True,
        "categorias": ["Salsas"],
        "composicion": [("Alioli", 60, False)],
    },
    # ---- BEBIDAS FRÍAS ----
    {
        "titulo": "Agua Mineral 500ml",
        "descripcion": "Agua mineral sin gas.",
        "precio": "400.00", "existencias": 300, "disponible": True,
        "categorias": ["Bebidas frías"],
        "composicion": [],
    },
    {
        "titulo": "Gaseosa 500ml",
        "descripcion": "Cola, naranja o lima limón a elección.",
        "precio": "600.00", "existencias": 300, "disponible": True,
        "categorias": ["Gaseosas"],
        "composicion": [],
    },
    {
        "titulo": "Limonada Natural",
        "descripcion": "Limones exprimidos, agua y azúcar. Opción con jengibre.",
        "precio": "800.00", "existencias": 80, "disponible": True,
        "categorias": ["Jugos naturales"],
        "composicion": [],
    },
    {
        "titulo": "Jugo de Naranja 400ml",
        "descripcion": "Naranja exprimida al momento, sin azúcar agregada.",
        "precio": "900.00", "existencias": 80, "disponible": True,
        "categorias": ["Jugos naturales"],
        "composicion": [],
    },
    # ---- BEBIDAS CALIENTES ----
    {
        "titulo": "Café con Leche",
        "descripcion": "Café espresso con leche vaporizada.",
        "precio": "500.00", "existencias": 150, "disponible": True,
        "categorias": ["Bebidas calientes"],
        "composicion": [],
    },
    {
        "titulo": "Té o Mate Cocido",
        "descripcion": "Surtido de tés o mate cocido con leche.",
        "precio": "400.00", "existencias": 150, "disponible": True,
        "categorias": ["Bebidas calientes"],
        "composicion": [],
    },
    # ---- POSTRES ----
    {
        "titulo": "Lava Cake de Chocolate",
        "descripcion": "Volcán de chocolate con centro fundente, servido con helado de vainilla.",
        "precio": "1100.00", "existencias": 30, "disponible": True,
        "categorias": ["Tortas"],
        "composicion": [
            ("Chocolate", 60, False), ("Huevo", 110, False),
            ("Crema de leche", 30, False), ("Helado vainilla", 100, True),
        ],
    },
    {
        "titulo": "Helado Artesanal (2 bochas)",
        "descripcion": "Sabores del día: vainilla, chocolate o frutilla.",
        "precio": "900.00", "existencias": 60, "disponible": True,
        "categorias": ["Helados"],
        "composicion": [("Helado vainilla", 200, False)],
    },
    {
        "titulo": "Alfajor Triple de Maicena",
        "descripcion": "Tres tapas de maicena con dulce de leche y coco rallado.",
        "precio": "600.00", "existencias": 80, "disponible": True,
        "categorias": ["Alfajores"],
        "composicion": [
            ("Galletita marinera", 30, False), ("Dulce de leche", 40, False),
            ("Coco rallado", 15, False),
        ],
    },
    {
        "titulo": "Torta de Chocolate",
        "descripcion": "Bizcochuelo húmedo de chocolate con ganache y crema.",
        "precio": "1400.00", "existencias": 20, "disponible": True,
        "categorias": ["Tortas"],
        "composicion": [
            ("Bizcochuelo", 120, False), ("Chocolate", 60, False),
            ("Crema de leche", 40, False),
        ],
    },
    {
        "titulo": "Panqueques con Dulce de Leche",
        "descripcion": "Tres panqueques con dulce de leche y crema batida.",
        "precio": "1000.00", "existencias": 35, "disponible": True,
        "categorias": ["Postres"],
        "composicion": [
            ("Huevo", 55, False), ("Dulce de leche", 60, False),
            ("Crema de leche", 30, True),
        ],
    },
]

DOMICILIOS_POR_COMPRADOR = {
    "comprador@foodstore.com": [
        {"via": "Av. Corrientes", "altura": "1234", "localidad": "CABA", "provincia": "Buenos Aires", "codigo_postal": "1043", "es_predeterminado": True},
        {"via": "Calle Florida", "altura": "456", "localidad": "Palermo", "provincia": "Buenos Aires", "codigo_postal": "1425", "es_predeterminado": False},
    ],
    "comprador2@foodstore.com": [
        {"via": "Av. Santa Fe", "altura": "3200", "localidad": "Recoleta", "provincia": "Buenos Aires", "codigo_postal": "1425", "es_predeterminado": True},
    ],
    "comprador3@foodstore.com": [
        {"via": "Av. Rivadavia", "altura": "5678", "localidad": "Caballito", "provincia": "Buenos Aires", "codigo_postal": "1406", "es_predeterminado": True},
    ],
    "comprador4@foodstore.com": [
        {"via": "Av. Cabildo", "altura": "2100", "localidad": "Belgrano", "provincia": "Buenos Aires", "codigo_postal": "1428", "es_predeterminado": True},
    ],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _t(dias_atras: int = 0, horas_atras: int = 0) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=dias_atras, hours=horas_atras)


def _agregar_bitacora(sesion, orden_id, ejecutado_por, transiciones, ts_base):
    for i, (prev, sig) in enumerate(transiciones):
        sesion.add(BitacoraOrden(
            orden_id=orden_id, estado_previo=prev, estado_siguiente=sig,
            ejecutado_por=ejecutado_por,
            registrado_en=ts_base + timedelta(minutes=i * 15),
        ))


# ---------------------------------------------------------------------------
# Seed principal
# ---------------------------------------------------------------------------

def seed() -> None:
    print("▶ Recreando esquema (drop schema cascade + create)...")
    with motor.connect() as conn:
        conn.execute(sa.text("DROP SCHEMA public CASCADE"))
        conn.execute(sa.text("CREATE SCHEMA public"))
        conn.commit()
    SQLModel.metadata.create_all(motor)
    print("▶ Ejecutando carga_inicial (catálogos base)...")
    ejecutar_carga_inicial()

    with Session(motor) as sesion:
        perfil_por_nombre: dict[str, Perfil] = {
            p.nombre: p for p in sesion.exec(select(Perfil)).all()
        }
        um_por_simbolo: dict[str, UnidadMedida] = {
            u.simbolo: u for u in sesion.exec(select(UnidadMedida)).all()
        }

        # --- Cuentas --------------------------------------------------------
        print("▶ Creando cuentas...")
        cuenta_por_correo: dict[str, Cuenta] = {
            c.correo: c for c in sesion.exec(select(Cuenta)).all()
        }
        for datos in CUENTAS_DEMO:
            if datos["correo"] not in cuenta_por_correo:
                nueva = Cuenta(
                    correo=datos["correo"],
                    clave_hash=cifrar_clave(datos["clave"]),
                    nombre_completo=datos["nombre"],
                    habilitado=True,
                )
                sesion.add(nueva)
                sesion.flush()
                sesion.add(CuentaPerfil(
                    cuenta_id=nueva.id,
                    perfil_id=perfil_por_nombre[datos["perfil"]].id,
                ))
                cuenta_por_correo[datos["correo"]] = nueva
                print(f"  + Cuenta: {datos['correo']} ({datos['perfil']})")

        # --- Categorías (jerárquicas) ----------------------------------------
        print("▶ Creando categorías...")
        cat_por_nombre: dict[str, Categoria] = {
            c.etiqueta: c for c in sesion.exec(select(Categoria)).all()
        }
        for nombre, padre_nombre in CATEGORIAS_DEMO:
            if nombre not in cat_por_nombre:
                padre_id = cat_por_nombre[padre_nombre].id if padre_nombre else None
                nueva = Categoria(etiqueta=nombre, padre_id=padre_id)
                sesion.add(nueva)
                sesion.flush()
                cat_por_nombre[nombre] = nueva
                print(f"  + Categoría: {nombre} (padre: {padre_nombre or 'raíz'})")

        # --- Componentes ----------------------------------------------------
        print("▶ Creando componentes...")
        comp_por_nombre: dict[str, Componente] = {
            c.denominacion: c for c in sesion.exec(select(Componente)).all()
        }
        for datos in COMPONENTES_DEMO:
            if datos["denominacion"] not in comp_por_nombre:
                nuevo = Componente(**datos)
                sesion.add(nuevo)
                sesion.flush()
                comp_por_nombre[datos["denominacion"]] = nuevo
                print(f"  + Componente: {datos['denominacion']}")

        # --- Artículos ------------------------------------------------------
        print("▶ Creando artículos...")
        art_por_titulo: dict[str, Articulo] = {
            a.titulo: a for a in sesion.exec(
                select(Articulo).where(Articulo.eliminado_en.is_(None))
            ).all()
        }
        for datos in ARTICULOS_DEMO:
            if datos["titulo"] not in art_por_titulo:
                articulo = Articulo(
                    titulo=datos["titulo"],
                    descripcion=datos["descripcion"],
                    precio_unitario=Decimal(datos["precio"]),
                    existencias=datos["existencias"],
                    disponible=datos["disponible"],
                )
                sesion.add(articulo)
                sesion.flush()
                art_por_titulo[datos["titulo"]] = articulo

                for nombre_cat in datos["categorias"]:
                    if nombre_cat in cat_por_nombre:
                        sesion.add(ArticuloCategoria(
                            articulo_id=articulo.id,
                            categoria_id=cat_por_nombre[nombre_cat].id,
                        ))

                for denom, gramos, extraible in datos["composicion"]:
                    comp = comp_por_nombre.get(denom)
                    if comp:
                        sesion.add(ComposicionArticulo(
                            articulo_id=articulo.id,
                            componente_id=comp.id,
                            extraible=extraible,
                            cantidad=Decimal(str(gramos)),
                        ))

                print(f"  + Artículo: {datos['titulo']}")

        sesion.flush()

        # --- Domicilios -----------------------------------------------------
        print("▶ Creando domicilios...")
        for correo, lista_doms in DOMICILIOS_POR_COMPRADOR.items():
            cuenta = cuenta_por_correo.get(correo)
            if not cuenta:
                continue
            doms_existentes = sesion.exec(
                select(Domicilio).where(Domicilio.cuenta_id == cuenta.id)
            ).all()
            if not doms_existentes:
                for d in lista_doms:
                    sesion.add(Domicilio(cuenta_id=cuenta.id, **d))
                    print(f"  + Domicilio {correo}: {d['via']} {d['altura']}")
                sesion.flush()

        # --- Órdenes --------------------------------------------------------
        print("▶ Creando órdenes...")

        admin = cuenta_por_correo.get("admin@foodstore.com") or sesion.exec(
            select(Cuenta).where(Cuenta.correo == "admin@foodstore.com")
        ).first()

        def _dom(correo):
            c = cuenta_por_correo.get(correo)
            if not c:
                return None
            return sesion.exec(
                select(Domicilio).where(Domicilio.cuenta_id == c.id)
            ).first()

        def _nueva_orden(correo, estado_final, transiciones, ts_base, partidas_datos,
                         descuento=Decimal("0.00"), tipo_entrega="DOMICILIO"):
            cuenta = cuenta_por_correo[correo]
            dom = _dom(correo)
            subtotal = sum(Decimal(str(p["precio"])) * p["unidades"] for p in partidas_datos)
            costo_envio = Decimal("500.00") if tipo_entrega == "DOMICILIO" else Decimal("0.00")
            total = subtotal - descuento + costo_envio
            orden = Orden(
                cuenta_id=cuenta.id,
                domicilio_id=dom.id if dom else None,
                tipo_entrega=tipo_entrega,
                estado_actual=estado_final,
                forma_pago_codigo="EFECTIVO" if tipo_entrega == "LOCAL" else "MERCADOPAGO",
                subtotal=subtotal,
                descuento=descuento,
                costo_envio=costo_envio,
                total=total,
                registrada_en=ts_base,
                actualizada_en=ts_base + timedelta(hours=1),
            )
            sesion.add(orden)
            sesion.flush()
            for p in partidas_datos:
                art = p["articulo"]
                sesion.add(PartidaOrden(
                    orden_id=orden.id,
                    articulo_id=art.id,
                    titulo_capturado=art.titulo,
                    precio_capturado=Decimal(str(p["precio"])),
                    unidades=p["unidades"],
                    subtotal_snap=Decimal(str(p["precio"])) * p["unidades"],
                ))
            _agregar_bitacora(sesion, orden.id, admin.id, transiciones, ts_base)
            return orden

        # Verificar si ya hay órdenes
        ordenes_existentes = sesion.exec(select(Orden)).first()
        if not ordenes_existentes:
            # Atajos de artículos
            A = art_por_titulo

            ENTREGADO = [
                (None, "PENDIENTE"), ("PENDIENTE", "CONFIRMADO"),
                ("CONFIRMADO", "EN_PREPARACION"), ("EN_PREPARACION", "ENTREGADO"),
            ]
            EN_PREP = [
                (None, "PENDIENTE"), ("PENDIENTE", "CONFIRMADO"),
                ("CONFIRMADO", "EN_PREPARACION"),
            ]
            CONFIRMADO = [(None, "PENDIENTE"), ("PENDIENTE", "CONFIRMADO")]
            PENDIENTE = [(None, "PENDIENTE")]
            CANCELADO = [(None, "PENDIENTE"), ("PENDIENTE", "CANCELADO")]

            # comprador 1 — historial rico
            _nueva_orden("comprador@foodstore.com", "ENTREGADO", ENTREGADO, _t(10),
                [{"articulo": A["Hamburguesa Clásica"], "precio": "1800.00", "unidades": 2},
                 {"articulo": A["Gaseosa 500ml"], "precio": "600.00", "unidades": 2}])
            _nueva_orden("comprador@foodstore.com", "ENTREGADO", ENTREGADO, _t(7),
                [{"articulo": A["Pizza Margarita"], "precio": "2200.00", "unidades": 1},
                 {"articulo": A["Pizza Napolitana"], "precio": "2500.00", "unidades": 1},
                 {"articulo": A["Gaseosa 500ml"], "precio": "600.00", "unidades": 2}],
                descuento=Decimal("500.00"))
            _nueva_orden("comprador@foodstore.com", "ENTREGADO", ENTREGADO, _t(3),
                [{"articulo": A["Hamburguesa Doble BBQ"], "precio": "2600.00", "unidades": 1},
                 {"articulo": A["Papas Fritas"], "precio": "900.00", "unidades": 1},
                 {"articulo": A["Agua Mineral 500ml"], "precio": "400.00", "unidades": 1}])
            _nueva_orden("comprador@foodstore.com", "EN_PREPARACION", EN_PREP, _t(horas_atras=2),
                [{"articulo": A["Hamburguesa Especial de la Casa"], "precio": "3200.00", "unidades": 1},
                 {"articulo": A["Papas con Queso y Panceta"], "precio": "1300.00", "unidades": 1},
                 {"articulo": A["Limonada Natural"], "precio": "800.00", "unidades": 2}])
            _nueva_orden("comprador@foodstore.com", "CANCELADO", CANCELADO, _t(1),
                [{"articulo": A["Hamburguesa Clásica"], "precio": "1800.00", "unidades": 1}])

            # comprador 2
            _nueva_orden("comprador2@foodstore.com", "ENTREGADO", ENTREGADO, _t(5),
                [{"articulo": A["Pizza Cuatro Quesos"], "precio": "3000.00", "unidades": 1},
                 {"articulo": A["Helado Artesanal (2 bochas)"], "precio": "900.00", "unidades": 2},
                 {"articulo": A["Gaseosa 500ml"], "precio": "600.00", "unidades": 1}])
            _nueva_orden("comprador2@foodstore.com", "ENTREGADO", ENTREGADO, _t(2),
                [{"articulo": A["Lomito Completo"], "precio": "2200.00", "unidades": 2},
                 {"articulo": A["Papas Fritas"], "precio": "900.00", "unidades": 2}])
            _nueva_orden("comprador2@foodstore.com", "CONFIRMADO", CONFIRMADO, _t(horas_atras=3),
                [{"articulo": A["Wrap de Pollo"], "precio": "1700.00", "unidades": 2},
                 {"articulo": A["Jugo de Naranja 400ml"], "precio": "900.00", "unidades": 2}])

            # comprador 3
            _nueva_orden("comprador3@foodstore.com", "ENTREGADO", ENTREGADO, _t(4),
                [{"articulo": A["Ensalada César"], "precio": "1200.00", "unidades": 1},
                 {"articulo": A["Wrap Veggie"], "precio": "1500.00", "unidades": 1},
                 {"articulo": A["Agua Mineral 500ml"], "precio": "400.00", "unidades": 2}])
            _nueva_orden("comprador3@foodstore.com", "PENDIENTE", PENDIENTE, _t(horas_atras=1),
                [{"articulo": A["Hamburguesa Veggie"], "precio": "1600.00", "unidades": 2},
                 {"articulo": A["Limonada Natural"], "precio": "800.00", "unidades": 1}])

            # comprador 4 — retira en local
            _nueva_orden("comprador4@foodstore.com", "ENTREGADO", ENTREGADO, _t(3),
                [{"articulo": A["Choripán"], "precio": "1300.00", "unidades": 3},
                 {"articulo": A["Papas Fritas"], "precio": "900.00", "unidades": 2},
                 {"articulo": A["Gaseosa 500ml"], "precio": "600.00", "unidades": 3}],
                tipo_entrega="LOCAL")
            _nueva_orden("comprador4@foodstore.com", "EN_PREPARACION", EN_PREP, _t(horas_atras=1),
                [{"articulo": A["Milanesa con Papas"], "precio": "2100.00", "unidades": 2},
                 {"articulo": A["Café con Leche"], "precio": "500.00", "unidades": 2}],
                tipo_entrega="LOCAL")

            # comprador 5 — solo una orden pendiente
            _nueva_orden("comprador5@foodstore.com", "PENDIENTE", PENDIENTE, _t(horas_atras=0),
                [{"articulo": A["Pizza Vegetariana"], "precio": "2400.00", "unidades": 1},
                 {"articulo": A["Lava Cake de Chocolate"], "precio": "1100.00", "unidades": 2}])

            print("  + Órdenes de múltiples compradores creadas")

        sesion.commit()

    print("\n✅ Seed completado.")
    print("\nCuentas disponibles:")
    print("  admin@foodstore.com           / Admin1234!    (ADMINISTRADOR)")
    print("  inventario@foodstore.com      / Inventario1!  (INVENTARIO)")
    print("  despacho@foodstore.com        / Despacho1!    (DESPACHO)")
    print("  comprador@foodstore.com       / Comprador1!   (COMPRADOR)  — 5 órdenes")
    print("  comprador2@foodstore.com      / Comprador1!   (COMPRADOR)  — 3 órdenes")
    print("  comprador3@foodstore.com      / Comprador1!   (COMPRADOR)  — 2 órdenes")
    print("  comprador4@foodstore.com      / Comprador1!   (COMPRADOR)  — 2 órdenes LOCAL")
    print("  comprador5@foodstore.com      / Comprador1!   (COMPRADOR)  — 1 orden pendiente")
    print("  comprador6-10@foodstore.com   / Comprador1!   (COMPRADOR)  — sin órdenes")


if __name__ == "__main__":
    seed()
