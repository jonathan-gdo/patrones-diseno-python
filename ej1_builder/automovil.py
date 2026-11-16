"""Ejercicio 1 - Patrón Builder (creacional).

Producto inmutable (Automovil) construido paso a paso por AutomovilBuilder.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Automovil:
    """Producto inmutable: no se puede modificar tras su construcción."""

    modelo: str
    motor: str
    color: str
    llantas: str
    sonido: str | None = None
    interiores: str | None = None
    techo_solar: bool = False
    gps: bool = False

    def __str__(self) -> str:
        extras = [
            f"sonido={self.sonido}" if self.sonido else None,
            f"interiores={self.interiores}" if self.interiores else None,
            "techo solar" if self.techo_solar else None,
            "GPS" if self.gps else None,
        ]
        extras_txt = ", ".join(e for e in extras if e) or "sin extras"
        return (f"{self.modelo} | motor={self.motor} | color={self.color} | "
                f"llantas={self.llantas} | {extras_txt}")


class AutomovilBuilder:
    """Constructor fluido. Los atributos obligatorios se validan en build()."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> "AutomovilBuilder":
        self._modelo = None
        self._motor = None
        self._color = None
        self._llantas = None
        self._sonido = None
        self._interiores = None
        self._techo_solar = False
        self._gps = False
        return self

    def modelo(self, valor: str) -> "AutomovilBuilder":
        self._modelo = valor
        return self

    def motor(self, valor: str) -> "AutomovilBuilder":
        self._motor = valor
        return self

    def color(self, valor: str) -> "AutomovilBuilder":
        self._color = valor
        return self

    def llantas(self, valor: str) -> "AutomovilBuilder":
        self._llantas = valor
        return self

    def sonido(self, valor: str) -> "AutomovilBuilder":
        self._sonido = valor
        return self

    def interiores(self, valor: str) -> "AutomovilBuilder":
        self._interiores = valor
        return self

    def con_techo_solar(self) -> "AutomovilBuilder":
        self._techo_solar = True
        return self

    def con_gps(self) -> "AutomovilBuilder":
        self._gps = True
        return self

    def build(self) -> Automovil:
        faltantes = [n for n, v in (("modelo", self._modelo), ("motor", self._motor),
                                    ("color", self._color), ("llantas", self._llantas))
                     if v is None]
        if faltantes:
            raise ValueError(f"Faltan atributos obligatorios: {', '.join(faltantes)}")
        auto = Automovil(self._modelo, self._motor, self._color, self._llantas,
                         self._sonido, self._interiores, self._techo_solar, self._gps)
        self.reset()
        return auto


class DirectorAutomovil:
    """Opcional: encapsula configuraciones predefinidas reutilizables."""

    def __init__(self, builder: AutomovilBuilder) -> None:
        self._builder = builder

    def basico(self) -> Automovil:
        return (self._builder.modelo("Urbano").motor("1.2L gasolina")
                .color("Blanco").llantas("15\" acero").build())

    def deportivo_full(self) -> Automovil:
        return (self._builder.modelo("Sport").motor("V6 turbo").color("Rojo")
                .llantas("19\" aleación").sonido("Premium 12 parlantes")
                .interiores("Cuero").con_techo_solar().con_gps().build())
