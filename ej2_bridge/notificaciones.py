"""Ejercicio 2 - Patrón Bridge (estructural).

Dos jerarquías independientes:
  * Abstracción: tipos de notificación (Mensaje, Alerta, Advertencia, Confirmacion)
  * Implementación: plataformas de visualización (Escritorio, Movil, Web)
La abstracción delega en la plataforma, evitando N x M subclases.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------- Implementador ----------
class Plataforma(ABC):
    @abstractmethod
    def mostrar(self, titulo: str, contenido: str, estilo: str) -> str: ...


class PlataformaEscritorio(Plataforma):
    def mostrar(self, titulo, contenido, estilo):
        return f"[Escritorio/ventana emergente {estilo}] {titulo}: {contenido}"


class PlataformaMovil(Plataforma):
    def mostrar(self, titulo, contenido, estilo):
        return f"[Móvil/push {estilo}] {titulo} - {contenido}"


class PlataformaWeb(Plataforma):
    def mostrar(self, titulo, contenido, estilo):
        return f"[Web/toast {estilo}] <b>{titulo}</b> {contenido}"


# ---------- Abstracción ----------
class Notificacion(ABC):
    estilo = "info"
    prefijo = ""

    def __init__(self, plataforma: Plataforma) -> None:
        self._plataforma = plataforma

    @property
    def plataforma(self) -> Plataforma:
        return self._plataforma

    def cambiar_plataforma(self, plataforma: Plataforma) -> None:
        """Flexibilidad en tiempo de ejecución."""
        self._plataforma = plataforma

    def enviar(self, contenido: str) -> str:
        return self._plataforma.mostrar(self.prefijo, contenido, self.estilo)


class Mensaje(Notificacion):
    estilo, prefijo = "info", "Mensaje"


class Alerta(Notificacion):
    estilo, prefijo = "error", "ALERTA"


class Advertencia(Notificacion):
    estilo, prefijo = "warning", "Advertencia"


class Confirmacion(Notificacion):
    estilo, prefijo = "success", "Confirmación"
