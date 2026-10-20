"""
api/almacen_acceso.py
=====================
Dónde viven las cuentas del login. Dos implementaciones con la MISMA interfaz:

  * `AlmacenPostgres`: producción. Tablas del esquema `acceso`
    (Database/migraciones/20261020120200_cuentas_login.sql). Se conecta con `DATABASE_URL`
    (variable de entorno de Render; nunca en el repo).
  * `AlmacenMemoria`: pruebas y local sin base. No persiste.

Este módulo solo guarda y lee: las reglas (validación, hash de la clave, topes) están en `api/acceso.py`.
"""

from __future__ import annotations

import threading
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


class CorreoOcupado(Exception):
    pass


class UsuarioOcupado(Exception):
    pass


def ahora() -> datetime:
    return datetime.now(timezone.utc)


def iso(d: Optional[datetime]) -> str:
    if d is None:
        return ""
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def publica(fila: Dict[str, Any]) -> Dict[str, Any]:
    """La cuenta con la forma del contrato del front (`Cuenta`). Nunca incluye el hash de la clave."""
    return {
        "id": str(fila["id"]),
        "usuario": fila["usuario"],
        "correo": fila["correo"],
        "estado": fila["estado"],
        "tipo": fila.get("tipo"),
        "metodos": ["correo"],
        "creadaEn": iso(fila.get("creada_en")),
    }


class AlmacenMemoria:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.cuentas: Dict[str, Dict[str, Any]] = {}
        self.sesiones: Dict[str, Dict[str, Any]] = {}
        self.intentos: List[Dict[str, Any]] = []

    def crear_cuenta(self, usuario: str, correo: str, clave_hash: str) -> Dict[str, Any]:
        with self._lock:
            if any(c["correo"] == correo for c in self.cuentas.values()):
                raise CorreoOcupado(correo)
            if any(c["usuario"] == usuario for c in self.cuentas.values()):
                raise UsuarioOcupado(usuario)
            fila = {"id": str(uuid.uuid4()), "usuario": usuario, "correo": correo, "clave_hash": clave_hash,
                    "estado": "aprobada", "tipo": None, "creada_en": ahora()}
            self.cuentas[fila["id"]] = fila
            return dict(fila)

    def por_correo(self, correo: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return next((dict(c) for c in self.cuentas.values() if c["correo"] == correo), None)

    def crear_sesion(self, hash_: str, cuenta_id: str, recordar: bool, expira: datetime) -> None:
        with self._lock:
            self.sesiones[hash_] = {"cuenta_id": str(cuenta_id), "recordar": recordar, "expira": expira}

    def sesion(self, hash_: str) -> Optional[Dict[str, Any]]:
        """{"cuenta": fila, "expira": datetime} si la sesión existe y no venció."""
        with self._lock:
            s = self.sesiones.get(hash_)
            if not s or s["expira"] <= ahora():
                self.sesiones.pop(hash_, None)
                return None
            c = self.cuentas.get(s["cuenta_id"])
            return {"cuenta": dict(c), "expira": s["expira"]} if c else None

    def borrar_sesion(self, hash_: str) -> None:
        with self._lock:
            self.sesiones.pop(hash_, None)

    def registrar_fallo(self, correo: str) -> None:
        with self._lock:
            self.intentos.append({"correo": correo, "en": ahora()})

    def contar_fallos(self, correo: str, desde: datetime) -> int:
        with self._lock:
            return sum(1 for i in self.intentos if i["correo"] == correo and i["en"] >= desde)

    def limpiar_fallos(self, correo: str) -> None:
        with self._lock:
            self.intentos = [i for i in self.intentos if i["correo"] != correo]

    def limpiar_vencidos(self) -> None:
        with self._lock:
            n = ahora()
            self.sesiones = {h: s for h, s in self.sesiones.items() if s["expira"] > n}
            self.intentos = [i for i in self.intentos if i["en"] > n - timedelta(days=1)]


_COLUMNAS = "id, usuario, correo, clave_hash, estado, tipo, creada_en"


class AlmacenPostgres:
    """Postgres con psycopg 3 y un pool chico de conexiones.

    `prepare_threshold=None`: sin sentencias preparadas, para que funcione igual detrás de un pooler en
    modo transacción (Supavisor) que en conexión directa o modo sesión."""

    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 5) -> None:
        from psycopg.rows import dict_row
        from psycopg_pool import ConnectionPool

        self.pool = ConnectionPool(
            dsn, min_size=min_size, max_size=max_size, open=True, timeout=10,
            kwargs={"row_factory": dict_row, "prepare_threshold": None, "autocommit": True},
        )

    def cerrar(self) -> None:
        self.pool.close()

    def _uno(self, sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        with self.pool.connection() as con:
            return con.execute(sql, params).fetchone()

    def _ejecutar(self, sql: str, params: tuple = ()) -> None:
        with self.pool.connection() as con:
            con.execute(sql, params)

    def crear_cuenta(self, usuario: str, correo: str, clave_hash: str) -> Dict[str, Any]:
        import psycopg

        try:
            fila = self._uno(
                f"insert into acceso.cuentas (usuario, correo, clave_hash) values (%s, %s, %s) returning {_COLUMNAS}",
                (usuario, correo, clave_hash))
        except psycopg.errors.UniqueViolation as exc:
            restriccion = getattr(getattr(exc, "diag", None), "constraint_name", "") or ""
            if "correo" in restriccion:
                raise CorreoOcupado(correo) from exc
            raise UsuarioOcupado(usuario) from exc
        return dict(fila)  # type: ignore[arg-type]

    def por_correo(self, correo: str) -> Optional[Dict[str, Any]]:
        return self._uno(f"select {_COLUMNAS} from acceso.cuentas where correo = %s", (correo,))

    def crear_sesion(self, hash_: str, cuenta_id: str, recordar: bool, expira: datetime) -> None:
        self._ejecutar("insert into acceso.sesiones (hash, cuenta_id, recordar, expira) values (%s, %s, %s, %s)",
                       (hash_, str(cuenta_id), recordar, expira))

    def sesion(self, hash_: str) -> Optional[Dict[str, Any]]:
        f = self._uno(
            "select s.expira as sesion_expira, " + ", ".join("c." + x.strip() for x in _COLUMNAS.split(",")) +
            " from acceso.sesiones s join acceso.cuentas c on c.id = s.cuenta_id where s.hash = %s and s.expira > now()",
            (hash_,))
        if not f:
            return None
        expira = f.pop("sesion_expira")
        return {"cuenta": f, "expira": expira}

    def borrar_sesion(self, hash_: str) -> None:
        self._ejecutar("delete from acceso.sesiones where hash = %s", (hash_,))

    def registrar_fallo(self, correo: str) -> None:
        self._ejecutar("insert into acceso.intentos (correo) values (%s)", (correo,))

    def contar_fallos(self, correo: str, desde: datetime) -> int:
        f = self._uno("select count(*)::int as n from acceso.intentos where correo = %s and en >= %s", (correo, desde))
        return int(f["n"]) if f else 0

    def limpiar_fallos(self, correo: str) -> None:
        self._ejecutar("delete from acceso.intentos where correo = %s", (correo,))

    def limpiar_vencidos(self) -> None:
        with self.pool.connection() as con:
            con.execute("delete from acceso.sesiones where expira <= now()")
            con.execute("delete from acceso.intentos where en < now() - interval '1 day'")
