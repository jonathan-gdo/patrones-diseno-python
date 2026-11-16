"""Ejercicio 3 - Patrón Mediator (comportamiento).

Los usuarios solo conocen a la sala (mediador); la sala enruta los mensajes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Mediador(ABC):
    @abstractmethod
    def enviar(self, mensaje: str, emisor: "Usuario", destino: str | None = None) -> None: ...


class Usuario:
    """Colega: no mantiene referencias a otros usuarios."""

    def __init__(self, nombre: str, sala: Mediador | None = None) -> None:
        self.nombre = nombre
        self._sala = sala
        self.bandeja: list[str] = []

    def unirse(self, sala: "SalaChat") -> None:
        sala.registrar(self)

    def enviar(self, mensaje: str, destino: str | None = None) -> None:
        if self._sala is None:
            raise RuntimeError(f"{self.nombre} no está en ninguna sala")
        self._sala.enviar(mensaje, self, destino)

    def recibir(self, mensaje: str, emisor: "Usuario") -> None:
        linea = f"{emisor.nombre} -> {self.nombre}: {mensaje}"
        self.bandeja.append(linea)
        print(linea)


class SalaChat(Mediador):
    """Mediador concreto: centraliza la lógica de comunicación."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self._usuarios: dict[str, Usuario] = {}

    def registrar(self, usuario: Usuario) -> None:
        if usuario.nombre in self._usuarios:
            raise ValueError(f"Ya existe un usuario '{usuario.nombre}' en la sala")
        self._usuarios[usuario.nombre] = usuario
        usuario._sala = self
        self._difundir(f"{usuario.nombre} se unió a {self.nombre}", usuario)

    def retirar(self, usuario: Usuario) -> None:
        if self._usuarios.pop(usuario.nombre, None) is not None:
            usuario._sala = None
            self._difundir(f"{usuario.nombre} salió de {self.nombre}", usuario)

    def enviar(self, mensaje: str, emisor: Usuario, destino: str | None = None) -> None:
        if emisor.nombre not in self._usuarios:
            raise RuntimeError("El emisor no pertenece a la sala")
        if destino is None:                      # difusión
            self._difundir(mensaje, emisor)
        elif destino in self._usuarios:          # mensaje privado
            self._usuarios[destino].recibir(mensaje, emisor)
        else:
            raise KeyError(f"Usuario '{destino}' no está en la sala")

    def _difundir(self, mensaje: str, emisor: Usuario) -> None:
        for u in self._usuarios.values():
            if u is not emisor:
                u.recibir(mensaje, emisor)
