import contextlib
import dataclasses
import io
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for carpeta in ("ej1_builder", "ej2_bridge", "ej3_mediator"):
    sys.path.insert(0, str(RAIZ / carpeta))

from automovil import AutomovilBuilder, DirectorAutomovil  # noqa: E402
from notificaciones import (Alerta, Mensaje, PlataformaMovil,  # noqa: E402
                            PlataformaWeb)
from chat import SalaChat, Usuario  # noqa: E402


class TestBuilder(unittest.TestCase):
    def test_opcionales_y_inmutabilidad(self):
        a = AutomovilBuilder().modelo("X").motor("m").color("c").llantas("l").con_gps().build()
        self.assertTrue(a.gps)
        self.assertIsNone(a.sonido)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            a.color = "otro"

    def test_obligatorios(self):
        with self.assertRaises(ValueError):
            AutomovilBuilder().modelo("X").build()

    def test_director_y_reset(self):
        b = AutomovilBuilder()
        d = DirectorAutomovil(b)
        self.assertTrue(d.deportivo_full().techo_solar)
        self.assertFalse(d.basico().techo_solar)  # el builder se reinicia


class TestBridge(unittest.TestCase):
    def test_combinaciones_y_cambio_en_runtime(self):
        n = Alerta(PlataformaWeb())
        self.assertIn("Web", n.enviar("x"))
        n.cambiar_plataforma(PlataformaMovil())
        self.assertIn("Móvil", n.enviar("x"))
        self.assertIn("Móvil", Mensaje(PlataformaMovil()).enviar("y"))


class TestMediator(unittest.TestCase):
    def setUp(self):
        self.sala = SalaChat("t")
        self.a, self.b, self.c = Usuario("a"), Usuario("b"), Usuario("c")
        with contextlib.redirect_stdout(io.StringIO()):
            for u in (self.a, self.b, self.c):
                u.unirse(self.sala)

    def test_difusion_y_privado(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.a.enviar("hola")
            self.b.enviar("privado", "c")
        self.assertIn("a -> b: hola", self.b.bandeja)
        self.assertIn("a -> c: hola", self.c.bandeja)
        self.assertIn("b -> c: privado", self.c.bandeja)
        self.assertNotIn("b -> c: privado", self.a.bandeja)

    def test_retirar_usuario(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.sala.retirar(self.c)
            self.a.enviar("x")
        self.assertNotIn("a -> c: x", self.c.bandeja)
        with self.assertRaises(RuntimeError):
            self.c.enviar("y")


if __name__ == "__main__":
    unittest.main()
