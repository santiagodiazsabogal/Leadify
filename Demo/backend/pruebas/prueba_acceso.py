# -*- coding: utf-8 -*-
"""Pruebas del login y del arriendo.

Se corre desde `Demo/backend/`:

    python pruebas/prueba_acceso.py

Devuelve 0 si todo pasa y 1 si algo falla.
"""

import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import acceso  # noqa: E402
from api.almacen_acceso import AlmacenMemoria  # noqa: E402
from api.app import app  # noqa: E402

CLAVE = "una frase larga 2026"


def cliente():
    acceso.configurar_almacen(AlmacenMemoria())
    acceso.reiniciar_topes()
    return TestClient(app, base_url="https://leadify-kappa.vercel.app")


def crear(c, usuario="constructora-andes", correo="Ventas@Andes.co", clave=CLAVE):
    return c.post("/api/cuentas", json={"usuario": usuario, "correo": correo, "clave": clave})


def test_la_cuenta_nace_aprobada_y_entra_en_el_acto(c):
    r = crear(c)
    assert r.status_code == 201 and r.json() == {"correo": "ventas@andes.co"}
    r = c.post("/api/sesion", json={"correo": "ventas@andes.co", "clave": CLAVE, "recordar": True})
    assert r.status_code == 200
    assert r.json()["cuenta"]["estado"] == "aprobada"
    assert "clave_hash" not in r.json()["cuenta"]
    cookie = r.headers["set-cookie"]
    assert "leadify_sesion=" in cookie and "HttpOnly" in cookie and "Path=/api" in cookie
    assert c.get("/api/sesion").json()["cuenta"]["usuario"] == "constructora-andes"


def test_salir_borra_la_sesion(c):
    crear(c)
    c.post("/api/sesion", json={"correo": "ventas@andes.co", "clave": CLAVE})
    assert c.delete("/api/sesion").status_code == 204
    assert c.get("/api/sesion").status_code == 401


def test_no_se_repiten_correo_ni_usuario(c):
    crear(c)
    assert crear(c, usuario="otra").json()["detail"]["codigo"] == "correo_ocupado"
    assert crear(c, correo="b@andes.co").json()["detail"]["codigo"] == "usuario_ocupado"


def test_datos_invalidos_traen_cada_campo(c):
    r = crear(c, usuario="a b", correo="x", clave="corta")
    assert r.status_code == 422
    assert set(r.json()["detail"]["campos"]) == {"usuario", "correo", "clave"}


def test_credenciales_malas_y_tope_de_intentos(c):
    crear(c)
    malo = {"correo": "ventas@andes.co", "clave": "mala clave 12345"}
    assert c.post("/api/sesion", json={"correo": "nadie@x.co", "clave": CLAVE}).json()["detail"]["codigo"] == "credenciales"
    for _ in range(5):
        assert c.post("/api/sesion", json=malo).status_code == 401
    r = c.post("/api/sesion", json={"correo": "ventas@andes.co", "clave": CLAVE})
    assert r.status_code == 429


def test_origen_ajeno_rechazado(c):
    r = c.post("/api/cuentas", headers={"origin": "https://malo.com"},
               json={"usuario": "andes", "correo": "a@andes.co", "clave": CLAVE})
    assert r.status_code == 403


def test_sin_base_responde_no_disponible():
    acceso.configurar_almacen(None)
    r = TestClient(app).get("/api/sesion")
    assert r.status_code == 503 and r.json()["detail"]["codigo"] == "no_disponible"


def test_arriendo_devuelve_inmuebles(c):
    r = c.get("/api/arriendo", params={"tipo_inmueble": "vivienda", "zona": ["11"]})
    assert r.status_code == 200 and r.json()["total"] > 0
    assert c.get("/api/arriendo", params={"tipo_inmueble": "castillo"}).status_code == 400


def test_llamada_de_arriendo_conserva_los_19_campos_de_dapta(c):
    import api.app as modulo

    modulo.DAPTA_FLOW_WEBHOOK_URL = None
    base = {"nombre": "Ana", "telefono": "3001234567", "afiliado": True, "rango_ingreso": "2-4",
            "personas_a_cargo": 2, "entorno_deseado": "Tranquilo",
            "apartamento": {"nombre_proyecto": "Apto", "localidad": "Suba", "tipo_vivienda": "VIS",
                            "precio_desde_cop": 250_000_000, "cuota_mensual_estimada_cop": 1_500_000,
                            "aplica_subsidio_caja": True}}
    compra = c.post("/api/llamar", json={**base, "edad": 34}).json()["payload_enviado"]
    arriendo = c.post("/api/llamar", json={**base, "tipo_operacion": "arriendo", "tipo_inmueble": "vivienda",
                                           "apartamento": {**base["apartamento"], "precio_desde_cop": 2_500_000}}
                      ).json()["payload_enviado"]
    assert set(compra) == set(arriendo) and len(compra) == 19
    assert compra["edad"] == 34 and compra["valor_estimado_vivienda"] == 250_000_000 and compra["subsidio_estimado"] > 0
    assert arriendo["edad"] == "No informada"
    assert arriendo["cuota_estimada_mensual"] == 2_500_000 and arriendo["valor_estimado_vivienda"] == 0
    assert arriendo["subsidio_estimado"] == 0


if __name__ == "__main__":
    fallos = 0
    for nombre, prueba in list(globals().items()):
        if not nombre.startswith("test_"):
            continue
        try:
            prueba(cliente()) if prueba.__code__.co_argcount else prueba()
            print(f"ok    {nombre}")
        except Exception as exc:
            fallos += 1
            print(f"FALLA {nombre}: {type(exc).__name__} {exc}")
    acceso.configurar_almacen(None)
    sys.exit(1 if fallos else 0)
