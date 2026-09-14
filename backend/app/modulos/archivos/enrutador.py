from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.nucleo.ajustes import ajustes
from app.nucleo.dependencias import requerir_perfil
from app.modulos.archivos.cliente_cdn import eliminar_imagen, subir_imagen
from app.modulos.archivos.esquemas import ImagenSubidaSalida

enrutador = APIRouter(
    prefix="/archivos",
    tags=["archivos"],
    dependencies=[Depends(requerir_perfil("ADMINISTRADOR"))],
)

@enrutador.post(
    "/imagen", response_model=ImagenSubidaSalida, status_code=status.HTTP_201_CREATED
)
async def subir(archivo: UploadFile = File(...)) -> ImagenSubidaSalida:
    contenido = await archivo.read()
    limite = ajustes.tamanio_maximo_mb * 1024 * 1024
    if len(contenido) > limite:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"La imagen supera el limite de {ajustes.tamanio_maximo_mb} MB",
        )
    resultado = subir_imagen(contenido)
    return ImagenSubidaSalida(
        url=resultado["url"],
        id_cdn=resultado["id_cdn"],
        simulado=resultado.get("simulado", False),
    )

@enrutador.delete("/imagen/{id_cdn:path}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_cdn: str) -> None:
    eliminado = eliminar_imagen(id_cdn)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar la imagen",
        )
