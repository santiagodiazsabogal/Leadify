"""
api/acceso.py
=============
El login de Leadify del lado del servidor. Una cuenta = una empresa (constructora o inmobiliaria).

    POST   /api/cuentas         {usuario, correo, clave}   -> 201 {correo}
    POST   /api/sesion          {correo, clave, recordar}  -> 200 Sesion + cookie
    GET    /api/sesion                                     -> 200 Sesion | 401
    DELETE /api/sesion                                     -> 204
    POST   /api/sesion/google                              -> 503 (apagado)

Errores: {"detail": {"codigo": <CodigoError del front>, "mensaje": ..., "campos"?: {...}}}.

SIN CONFIRMACIÓN DE CORREO NI REVISIÓN: la cuenta nace aprobada y el front entra en el acto. Tampoco hay
recuperación de contraseña por correo: Render (plan gratuito) bloquea el SMTP.

SEGURIDAD
  * Contraseña con scrypt (N=2^14, r=8, p=1; sal de 16 bytes por cuenta). Nunca sale del servidor.
  * Sesión = token aleatorio en una cookie HttpOnly, Secure, SameSite=Lax y Path=/api. En la base solo va su
    SHA-256. "Recordarme" = cookie de 30 días; sin él, la cookie muere con el navegador y la sesión dura
    máximo 12 h en el servidor.
  * El front llama a /api/... en SU MISMO dominio (Vercel reenvía esas rutas a Render: frontend/vercel.json),
    así la cookie es de primera parte. Las peticiones que cambian algo exigen que, si viene un `Origin`, sea
    uno permitido (FRONT_URL, ORIGENES_ACCESO o localhost).
  * Los mensajes no revelan si un correo existe (salvo "correo_ocupado" al registrarse, inevitable).
    Entrar con un correo inexistente cuesta lo mismo que con uno real: se calcula un hash igual.
  * Topes: 5 fallos por correo en 15 min (en la base) y 20 registros por IP por hora (en memoria).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import math
import os
import re
import secrets
import threading
import time
from collections import deque
from datetime import timedelta
from typing import Any, Deque, Dict, Optional, Protocol
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from api.almacen_acceso import CorreoOcupado, UsuarioOcupado, ahora, iso, publica

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/api", include_in_schema=False)

COOKIE = "leadify_sesion"
SESION_RECORDADA = timedelta(days=30)
SESION_TEMPORAL = timedelta(hours=12)
INTENTOS_MAX = 5
INTENTOS_VENTANA = timedelta(minutes=15)
REGISTROS_POR_IP_HORA = 20

CLAVE_MIN, CLAVE_MAX = 10, 128
USUARIO_MIN, USUARIO_MAX = 3, 30

MENSAJES = {
    "datos_invalidos": "Revisa los datos marcados.",
    "credenciales": "El correo o la contraseña no coinciden.",
    "usuario_ocupado": "Ese nombre de usuario ya está en uso.",
    "correo_ocupado": "Ese correo ya tiene una cuenta. Entra con tu contraseña.",
    "demasiados_intentos": "Demasiados intentos. Espera unos minutos y vuelve a intentarlo.",
    "no_disponible": "El acceso todavía no está disponible.",
    "origen": "Petición no permitida.",
}


class AlmacenAcceso(Protocol):
    def crear_cuenta(self, usuario: str, correo: str, clave_hash: str) -> Dict[str, Any]: ...
    def por_correo(self, correo: str) -> Optional[Dict[str, Any]]: ...
    def crear_sesion(self, hash_: str, cuenta_id: str, recordar: bool, expira) -> None: ...
    def sesion(self, hash_: str) -> Optional[Dict[str, Any]]: ...
    def borrar_sesion(self, hash_: str) -> None: ...
    def registrar_fallo(self, correo: str) -> None: ...
    def contar_fallos(self, correo: str, desde) -> int: ...
    def limpiar_fallos(self, correo: str) -> None: ...
    def limpiar_vencidos(self) -> None: ...


_almacen: Optional[AlmacenAcceso] = None
_ultima_limpieza = 0.0


def configurar_almacen(almacen: Optional[AlmacenAcceso]) -> None:
    global _almacen
    _almacen = almacen


def _error(status: int, codigo: str, campos: Optional[Dict[str, str]] = None) -> HTTPException:
    detalle: Dict[str, Any] = {"codigo": codigo, "mensaje": MENSAJES.get(codigo, MENSAJES["datos_invalidos"])}
    if campos:
        detalle["campos"] = campos
    return HTTPException(status, detalle)


def _alm() -> AlmacenAcceso:
    global _ultima_limpieza
    if _almacen is None:
        raise _error(503, "no_disponible")
    if time.time() - _ultima_limpieza > 3600:          # una vez por hora: sesiones e intentos vencidos
        _ultima_limpieza = time.time()
        try:
            _almacen.limpiar_vencidos()
        except Exception as exc:                        # limpiar nunca debe tumbar un login
            logger.warning("acceso: no se pudo limpiar lo vencido: %s", exc)
    return _almacen


# ---------------------------------------------------------------------------
# Validación (la misma de frontend/src/auth/validacion.ts; el servidor no confía en el navegador)
# ---------------------------------------------------------------------------

_RE_USUARIO = re.compile(r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$")
_RE_CORREO = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")


def normalizar_correo(c: str) -> str:
    return (c or "").strip().lower()


def validar_usuario(u: str) -> Optional[str]:
    u = (u or "").strip().lower()
    if not u:
        return "Escribe un nombre de usuario."
    if len(u) < USUARIO_MIN:
        return f"Usa al menos {USUARIO_MIN} caracteres."
    if len(u) > USUARIO_MAX:
        return f"Usa máximo {USUARIO_MAX} caracteres."
    if not _RE_USUARIO.match(u):
        return "Usa minúsculas, números, puntos o guiones, sin espacios ni tildes."
    return None


def validar_correo(c: str) -> Optional[str]:
    c = normalizar_correo(c)
    if not c:
        return "Escribe tu correo."
    if len(c) > 254 or not _RE_CORREO.match(c):
        return "Escribe un correo válido, como nombre@empresa.com."
    return None


def validar_clave(clave: str, usuario: str = "", correo: str = "") -> Optional[str]:
    if not clave:
        return "Escribe una contraseña."
    if len(clave) < CLAVE_MIN:
        return f"Usa al menos {CLAVE_MIN} caracteres."
    if len(clave) > CLAVE_MAX:
        return f"Usa máximo {CLAVE_MAX} caracteres."
    baja = clave.lower()
    u = (usuario or "").strip().lower()
    local = normalizar_correo(correo).split("@")[0]
    if (u and u in baja) or (len(local) >= 4 and local in baja):
        return "No uses tu usuario ni tu correo dentro de la contraseña."
    if len(set(clave)) == 1:
        return "Evita repetir el mismo carácter."
    return None


# ---------------------------------------------------------------------------
# Contraseñas y tokens
# ---------------------------------------------------------------------------

_SCRYPT = {"n": 2 ** 14, "r": 8, "p": 1}


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _b64d(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def hash_clave(clave: str) -> str:
    sal = secrets.token_bytes(16)
    dk = hashlib.scrypt(clave.encode(), salt=sal, dklen=32, maxmem=64 * 1024 * 1024, **_SCRYPT)
    return f"scrypt${_SCRYPT['n']}${_SCRYPT['r']}${_SCRYPT['p']}${_b64(sal)}${_b64(dk)}"


def verificar_clave(clave: str, guardado: Optional[str]) -> bool:
    try:
        alg, n, r, p, sal, dk = (guardado or "").split("$")
        if alg != "scrypt":
            return False
        calc = hashlib.scrypt(clave.encode(), salt=_b64d(sal), dklen=len(_b64d(dk)), n=int(n), r=int(r), p=int(p),
                              maxmem=64 * 1024 * 1024)
        return hmac.compare_digest(calc, _b64d(dk))
    except (ValueError, TypeError):
        return False


# Para que entrar con un correo inexistente tarde lo mismo que con uno real.
_HASH_SENUELO = hash_clave(secrets.token_urlsafe(16))


def _sha(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Origen, cookie y topes
# ---------------------------------------------------------------------------

ORIGENES_DEFECTO = ("https://leadify-kappa.vercel.app",)


def _origenes_permitidos() -> set:
    permitidos = set(ORIGENES_DEFECTO)
    for o in [os.environ.get("FRONT_URL") or ""] + (os.environ.get("ORIGENES_ACCESO") or "").split(","):
        o = o.strip().rstrip("/")
        if o:
            permitidos.add(o)
    return permitidos


def _exigir_origen(request: Request) -> None:
    origen = (request.headers.get("origin") or "").rstrip("/")
    if not origen:
        return                                   # mismo origen sin Origin (o un cliente que no es navegador)
    host = urlparse(origen).hostname or ""
    if host in ("localhost", "127.0.0.1") or origen in _origenes_permitidos():
        return
    raise _error(403, "origen")


def _ip(request: Request) -> str:
    """La IP de quien usa el login, para el tope por IP.

    Estas rutas llegan por el reenvío de Vercel: para Render la conexión viene de un servidor de Vercel, y
    sin estas cabeceras el tope bloquearía a todo el mundo a la vez. Se pueden falsificar llamando directo a
    Render, pero solo sirve para esquivar el tope por IP, que es secundario: el que importa es por correo.
    """
    for nombre in ("x-vercel-forwarded-for", "x-forwarded-for", "cf-connecting-ip"):
        valor = (request.headers.get(nombre) or "").split(",")[0].strip()
        if valor:
            return valor
    return request.client.host if request.client else "desconocida"


_tope_lock = threading.Lock()
_ventanas: Dict[str, Deque[float]] = {}


def _tope(llave: str, tope: int, segundos: int) -> None:
    t = time.time()
    with _tope_lock:
        if len(_ventanas) > 5000:
            for k in [k for k, v in _ventanas.items() if not v or t - v[-1] >= segundos]:
                del _ventanas[k]
        v = _ventanas.setdefault(llave, deque())
        while v and t - v[0] >= segundos:
            v.popleft()
        if len(v) >= tope:
            espera = max(1, math.ceil(segundos - (t - v[0])))
            raise HTTPException(429, {"codigo": "demasiados_intentos", "mensaje": MENSAJES["demasiados_intentos"]},
                                headers={"Retry-After": str(espera)})
        v.append(t)


def reiniciar_topes() -> None:
    with _tope_lock:
        _ventanas.clear()


def _cookie_segura(request: Request) -> bool:
    # En local (http://localhost) el navegador no guarda cookies Secure servidas por http.
    return not (request.url.scheme == "http" and (request.url.hostname or "") in ("localhost", "127.0.0.1"))


def _poner_cookie(request: Request, response: Response, token: str, recordar: bool) -> None:
    response.set_cookie(COOKIE, token, max_age=int(SESION_RECORDADA.total_seconds()) if recordar else None,
                        httponly=True, secure=_cookie_segura(request), samesite="lax", path="/api")


def _quitar_cookie(request: Request, response: Response) -> None:
    response.delete_cookie(COOKIE, path="/api", httponly=True, secure=_cookie_segura(request), samesite="lax")


def _no_store(response: Response) -> None:
    response.headers["Cache-Control"] = "no-store"


def _sesion_json(cuenta: Dict[str, Any], expira) -> Dict[str, Any]:
    return {"cuenta": publica(cuenta), "expiraEn": iso(expira)}


def instalar_manejadores(app) -> None:
    """Si la base no responde (red, pooler, credenciales), el login dice "no disponible" en vez de un 500."""
    try:
        import psycopg
        from psycopg_pool import PoolTimeout
    except ImportError:                                 # sin psycopg instalado no hay Postgres que fallar
        return

    async def _base_caida(request: Request, exc: Exception):
        logger.error("acceso: la base de cuentas no responde: %s: %s", type(exc).__name__, exc)
        return JSONResponse(status_code=503, headers={"Cache-Control": "no-store"},
                            content={"detail": {"codigo": "no_disponible", "mensaje": MENSAJES["no_disponible"]}})

    app.add_exception_handler(psycopg.OperationalError, _base_caida)
    app.add_exception_handler(PoolTimeout, _base_caida)


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------

class EntradaRegistro(BaseModel):
    usuario: str = Field(max_length=60)
    correo: str = Field(max_length=300)
    clave: str = Field(max_length=300)


class EntradaSesion(BaseModel):
    correo: str = Field(max_length=300)
    clave: str = Field(max_length=300)
    recordar: bool = False


@router.post("/cuentas", status_code=201)
def crear_cuenta(datos: EntradaRegistro, request: Request, response: Response):
    _exigir_origen(request)
    _no_store(response)
    almacen = _alm()
    _tope(f"registro-ip:{_ip(request)}", REGISTROS_POR_IP_HORA, 3600)
    usuario = datos.usuario.strip().lower()
    correo = normalizar_correo(datos.correo)
    campos = {k: v for k, v in {"usuario": validar_usuario(usuario), "correo": validar_correo(correo),
                                "clave": validar_clave(datos.clave, usuario, correo)}.items() if v}
    if campos:
        raise _error(422, "datos_invalidos", campos)
    try:
        almacen.crear_cuenta(usuario, correo, hash_clave(datos.clave))
    except CorreoOcupado:
        raise _error(409, "correo_ocupado")
    except UsuarioOcupado:
        raise _error(409, "usuario_ocupado")
    logger.info("acceso: cuenta nueva %s", usuario)
    return {"correo": correo}


@router.post("/sesion")
def entrar(datos: EntradaSesion, request: Request, response: Response):
    _exigir_origen(request)
    _no_store(response)
    almacen = _alm()
    correo = normalizar_correo(datos.correo)
    if validar_correo(correo) or not datos.clave:
        raise _error(401, "credenciales")
    if almacen.contar_fallos(correo, ahora() - INTENTOS_VENTANA) >= INTENTOS_MAX:
        raise _error(429, "demasiados_intentos")
    cuenta = almacen.por_correo(correo)
    ok = verificar_clave(datos.clave, cuenta["clave_hash"] if cuenta else _HASH_SENUELO)
    if not ok or not cuenta:
        almacen.registrar_fallo(correo)
        raise _error(401, "credenciales")
    almacen.limpiar_fallos(correo)
    token = secrets.token_urlsafe(32)
    expira = ahora() + (SESION_RECORDADA if datos.recordar else SESION_TEMPORAL)
    almacen.crear_sesion(_sha(token), str(cuenta["id"]), datos.recordar, expira)
    _poner_cookie(request, response, token, datos.recordar)
    return _sesion_json(cuenta, expira)


@router.get("/sesion")
def sesion_actual(request: Request, response: Response):
    _no_store(response)
    almacen = _alm()                                     # sin base: 503, para que el front sepa por qué
    token = request.cookies.get(COOKIE)
    s = almacen.sesion(_sha(token)) if token else None
    if not s:
        r = JSONResponse(status_code=401, content={"detail": {"codigo": "sin_sesion", "mensaje": "No hay sesión."}},
                         headers={"Cache-Control": "no-store"})
        if token:
            _quitar_cookie(request, r)
        return r
    return _sesion_json(s["cuenta"], s["expira"])


@router.delete("/sesion", status_code=204)
def salir(request: Request):
    _exigir_origen(request)
    token = request.cookies.get(COOKIE)
    if token and _almacen is not None:
        _almacen.borrar_sesion(_sha(token))
    r = Response(status_code=204, headers={"Cache-Control": "no-store"})
    _quitar_cookie(request, r)
    return r


@router.post("/sesion/google")
def entrar_con_google(request: Request):
    # Apagado: exige un cliente OAuth y la verificación del ID token (firma, iss, aud, exp, nonce).
    _exigir_origen(request)
    raise _error(503, "no_disponible")
