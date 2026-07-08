"""Clase Usuario: representa a una persona registrada en el sistema."""


class Usuario:
    def __init__(self, dni, nombre):
        self.dni = dni
        self.nombre = nombre

    def a_linea(self):
        """Convierte el usuario a una línea de texto para guardar en archivo."""
        return f"{self.dni}|{self.nombre}"

    def __str__(self):
        return f"DNI: {self.dni} | Nombre: {self.nombre}"
