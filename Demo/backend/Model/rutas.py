"""
Model/rutas.py
==============
Única fuente de verdad de **dónde vive cada archivo** del backend.

Antes cada módulo calculaba sus rutas con `os.path.dirname(__file__)` y las
colgaba de la raíz del repo. Con el backend repartido en paquetes eso deja de
funcionar —`modelo.py` ya no está al lado de `proyectos_model.json`— y, peor,
cada módulo tendría su propia idea de dónde buscar. Ese es exactamente el tipo
de desfase silencioso que describe el invariante 1 del CLAUDE.md, aplicado a
rutas en vez de a ids.

Convención:
    Model/data_projects/   datos de ENTRADA: el catálogo, los clientes
                           simulados y el historial con el que se entrenó.
                           Se versionan: hacen que `recomendar()` funcione
                           recién clonado, sin scrapear ni entrenar.
    salidas/               datos de SALIDA de una consulta concreta. Cambian
                           en cada llamada y están en .gitignore.
    frontend/public/recursos/imagenes_proyectos/<id_proyecto>/
                           los binarios pesados, del lado del front, que es
                           quien los sirve. El id del proyecto **es** el
                           nombre de la carpeta.
"""

from __future__ import annotations

import os
from argparse import ArgumentTypeError

# Model/ -> backend/ -> raíz del repo
DIR_MODEL = os.path.dirname(os.path.abspath(__file__))
DIR_BACKEND = os.path.dirname(DIR_MODEL)
DIR_RAIZ = os.path.dirname(DIR_BACKEND)

DIR_DATA_PROJECTS = os.path.join(DIR_MODEL, "data_projects")
DIR_SIMULACION = os.path.join(DIR_MODEL, "simulacion")
DIR_SALIDAS = os.path.join(DIR_BACKEND, "salidas")

# El front es quien sirve las imágenes, así que viven en sus recursos.
DIR_FRONTEND = os.path.join(DIR_RAIZ, "frontend")
DIR_RECURSOS_FRONT = os.path.join(DIR_FRONTEND, "public", "recursos")
DIR_IMAGENES = os.path.join(DIR_RECURSOS_FRONT, "imagenes_proyectos")

# --- Entradas (versionadas) ------------------------------------------------
RUTA_CATALOGO = os.path.join(DIR_DATA_PROJECTS, "proyectos_bogota.json")
RUTA_SEED_MANUAL = os.path.join(DIR_DATA_PROJECTS, "proyectos_seed.json")
RUTA_MODELO = os.path.join(DIR_DATA_PROJECTS, "proyectos_model.json")
RUTA_HISTORIAL = os.path.join(DIR_DATA_PROJECTS, "historial_simulado.json")
RUTA_CLIENTES = os.path.join(DIR_DATA_PROJECTS, "clientes_simulados.json")
RUTA_LOCALIDADES_GEO = os.path.join(DIR_DATA_PROJECTS, "localidades_bogota.json")
# El grafo de barrios (§3 del CLAUDE.md) sale de tres archivos:
#   - el TXT con los vecinos de cada sector catastral, calculado sobre la capa
#     oficial de IDECA. Es la fuente de las aristas y no se edita a mano.
#   - la geometría simplificada de esos sectores (Datos Abiertos Bogotá), que
#     permite ubicar un proyecto en su barrio por coordenada.
#   - el JSON compilado que lee el modelo: nodos, aristas y centroides.
RUTA_BARRIOS_VECINOS_TXT = os.path.join(DIR_DATA_PROJECTS, "barrios_bogota_vecinos.txt")
RUTA_BARRIOS_GEO = os.path.join(DIR_DATA_PROJECTS, "barrios_bogota_geo.json")
RUTA_BARRIOS_GRAFO = os.path.join(DIR_DATA_PROJECTS, "barrios_bogota.json")
RUTA_USUARIO_DEMO = os.path.join(DIR_DATA_PROJECTS, "usuario_ejemplo.json")
RUTA_USUARIO_MINIMO = os.path.join(DIR_DATA_PROJECTS, "usuario_minimo.json")

# Catálogo DEMO de arriendo (vivienda/oficina/bodega), separado a propósito
# del catálogo de venta: no comparten contrato (arriendo no tiene VIS ni
# cuota de hipoteca) y uno no debe poder pisar al otro.
RUTA_ARRIENDO = os.path.join(DIR_DATA_PROJECTS, "inmuebles_arriendo_bogota.json")

# --- Salidas (regeneradas en cada consulta) --------------------------------
RUTA_LLAMATIVOS = os.path.join(DIR_SALIDAS, "proyectos_listos_llamativos.json")
RUTA_RESPUESTA = os.path.join(DIR_SALIDAS, "respuesta.json")


def asegurar_salidas():
    """Crea `backend/salidas/` si no existe. La llaman los que escriben ahí."""
    os.makedirs(DIR_SALIDAS, exist_ok=True)
    return DIR_SALIDAS


class RutaFueraDelProyecto(ArgumentTypeError, ValueError):
    """La ruta recibida por consola apunta fuera de la carpeta del proyecto."""


_CARPETAS_AJENAS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def _archivos_del_proyecto():
    """Los archivos que hay hoy dentro de `Demo/`, sin dependencias ni caché."""
    for carpeta, subcarpetas, archivos in os.walk(os.path.realpath(DIR_RAIZ)):
        subcarpetas[:] = [s for s in subcarpetas if s not in _CARPETAS_AJENAS]
        for archivo in archivos:
            yield os.path.join(carpeta, archivo)


def ruta_del_proyecto(texto):
    """Resuelve la ruta de un archivo que llega por consola a uno que YA existe en el proyecto.

    En vez de dejar que una ruta escrita a mano llegue a `open()`, se busca entre los archivos de `Demo/` el que ella
    señala y se devuelve ese. Lo que no es un archivo del proyecto (`../../x`, otro disco, uno que no existe) se
    rechaza. Sirve como `type=` de argparse.
    """
    pedido = os.path.normcase(os.path.realpath(texto))
    for conocido in _archivos_del_proyecto():
        if os.path.normcase(conocido) == pedido:
            return conocido
    raise RutaFueraDelProyecto(f"Tiene que ser un archivo que exista dentro del proyecto ({os.path.realpath(DIR_RAIZ)}): {texto}")
