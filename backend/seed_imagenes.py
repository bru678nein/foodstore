"""
Asigna imágenes a los artículos subiendo desde URL a Cloudinary.

Requiere NUBE_CDN, API_KEY_CDN y API_SECRET_CDN en el .env.

Ejecutar desde backend/:
    python -X utf8 seed_imagenes.py

Es idempotente: omite artículos que ya tienen imagen.
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from sqlmodel import Session, select

from app.nucleo.ajustes import ajustes
from app.persistencia.entidades.articulo import Articulo, ArticuloImagen
from app.persistencia.motor import motor

# ---------------------------------------------------------------------------
# Mapa título → URL de Unsplash (foto específica, estable)
# ---------------------------------------------------------------------------
_U = "https://images.unsplash.com/photo-"

IMAGENES = {
    # Hamburguesas
    "Hamburguesa Clásica":            f"{_U}1568901346375-23c9450c58cd?w=800&q=80",
    "Hamburguesa Doble BBQ":          f"{_U}1607013251379-e6eecfffe234?w=800&q=80",
    "Hamburguesa Veggie":             f"{_U}1525059696034-4967a8e1dca2?w=800&q=80",
    "Hamburguesa Blue Cheese":        f"{_U}1586190848861-99aa4a171e90?w=800&q=80",
    "Hamburguesa Pollo Crispy":       f"{_U}1626645738196-c2a7c87a8f58?w=800&q=80",
    "Hamburguesa Especial de la Casa":f"{_U}1553979459-d1b5a3b40c87?w=800&q=80",
    # Pizzas
    "Pizza Margarita":                f"{_U}1565299624946-b28f40a0ae38?w=800&q=80",
    "Pizza Napolitana":               f"{_U}1574071318508-1cdbab80d002?w=800&q=80",
    "Pizza Jamón y Morrones":         f"{_U}1513104890138-7c749659a591?w=800&q=80",
    "Pizza Fugazzeta":                f"{_U}1571407970349-bc81e7e96d47?w=800&q=80",
    "Pizza Cuatro Quesos":            f"{_U}1528137871618-79d2021a68f4?w=800&q=80",
    "Pizza Vegetariana":              f"{_U}1590947132387-155cc02f3212?w=800&q=80",
    # Sandwichs
    "Sandwich Club":                  f"{_U}1528735602780-2552fd46c7af?w=800&q=80",
    "Choripán":                       f"{_U}1529193591184-b1d58069ecdd?w=800&q=80",
    "Lomito Completo":                f"{_U}1551782045-984481fdcb7b?w=800&q=80",
    # Wraps
    "Wrap de Pollo":                  f"{_U}1626700051175-6818013e1d4f?w=800&q=80",
    "Wrap Veggie":                    f"{_U}1512621776951-a57141f2eefd?w=800&q=80",
    # Ensaladas
    "Ensalada César":                 f"{_U}1550304943-4f24f54ddde9?w=800&q=80",
    "Ensalada Mediterránea":          f"{_U}1540189549336-e6e99eb4b8db?w=800&q=80",
    # Minutas
    "Milanesa con Papas":             f"{_U}1598103442097-8b74394b95c8?w=800&q=80",
    "Huevos Revueltos con Jamón":     f"{_U}1525351484163-7529414344d8?w=800&q=80",
    # Porciones
    "Papas Fritas":                   f"{_U}1576107232684-1279f814dc98?w=800&q=80",
    "Papas con Queso y Panceta":      f"{_U}1630384060421-cb20d0e0649d?w=800&q=80",
    # Salsas
    "Porción de Chimichurri":         f"{_U}1472476443507-c7b10a27f4b3?w=800&q=80",
    "Porción de Alioli":              f"{_U}1534482421-64566f976cfa?w=800&q=80",
    # Bebidas
    "Agua Mineral 500ml":             f"{_U}1548839140-29a749e1cf4d?w=800&q=80",
    "Gaseosa 500ml":                  f"{_U}1581006852452-9e6648e4c6a0?w=800&q=80",
    "Limonada Natural":               f"{_U}1621506289937-a8e4df240d0b?w=800&q=80",
    "Jugo de Naranja 400ml":          f"{_U}1622597467836-f3285f2131b8?w=800&q=80",
    "Café con Leche":                 f"{_U}1509042239860-f550ce710b93?w=800&q=80",
    "Té o Mate Cocido":               f"{_U}1556679343-c7306c1976bc?w=800&q=80",
    # Postres
    "Lava Cake de Chocolate":         f"{_U}1578985545062-69928b1d9587?w=800&q=80",
    "Helado Artesanal (2 bochas)":    f"{_U}1563805042-7684c019e1cb?w=800&q=80",
    "Alfajor Triple de Maicena":      f"{_U}1558961363-fa8fdf82db35?w=800&q=80",
    "Torta de Chocolate":             f"{_U}1567620905732-2d1ec7ab7445?w=800&q=80",
    "Panqueques con Dulce de Leche":  f"{_U}1528207776565-b52e7b2d0481?w=800&q=80",
}


def _configurar_cloudinary() -> bool:
    if not (ajustes.nube_cdn and ajustes.api_key_cdn and ajustes.api_secret_cdn):
        print("ERROR: Falta NUBE_CDN, API_KEY_CDN o API_SECRET_CDN en el .env")
        return False
    try:
        import cloudinary
        import cloudinary.uploader  # noqa: F401
    except ImportError:
        print("ERROR: instalá cloudinary con: pip install cloudinary")
        return False

    import cloudinary
    cloudinary.config(
        cloud_name=ajustes.nube_cdn,
        api_key=ajustes.api_key_cdn,
        api_secret=ajustes.api_secret_cdn,
        secure=True,
    )
    return True


def seed_imagenes() -> None:
    if not _configurar_cloudinary():
        return

    import cloudinary.uploader

    with Session(motor) as sesion:
        articulos = sesion.exec(
            select(Articulo).where(Articulo.eliminado_en.is_(None))
        ).all()

        # índice de los que ya tienen imagen
        con_imagen = set(
            row[0] for row in sesion.exec(
                select(ArticuloImagen.articulo_id)
            ).all()
        )

        pendientes = [a for a in articulos if a.id not in con_imagen and a.titulo in IMAGENES]

        if not pendientes:
            print("Todos los artículos ya tienen imagen.")
            return

        print(f"Subiendo imágenes para {len(pendientes)} artículos...\n")

        for articulo in pendientes:
            url_origen = IMAGENES[articulo.titulo]
            try:
                resp = cloudinary.uploader.upload(
                    url_origen,
                    folder="foodstore",
                    public_id=f"articulo_{articulo.id}",
                    overwrite=True,
                )
                sesion.add(ArticuloImagen(
                    articulo_id=articulo.id,
                    url_imagen=resp["secure_url"],
                    id_cdn=resp["public_id"],
                    posicion=0,
                ))
                sesion.flush()
                print(f"  OK  {articulo.titulo}")
                time.sleep(0.3)  # respetar rate limit de Cloudinary
            except Exception as e:
                print(f"  ERR {articulo.titulo}: {e}")

        sesion.commit()

    print("\nImagenes cargadas. Reinicia el backend para ver los cambios.")


if __name__ == "__main__":
    seed_imagenes()
