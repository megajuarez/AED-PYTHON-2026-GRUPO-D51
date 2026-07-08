"""Clase Libro: representa un libro del catálogo, con control de stock."""


class Libro:
    def __init__(self, id_libro, titulo, autor, copias_totales, copias_disponibles=None):
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.copias_totales = copias_totales
        # Si no se indica copias_disponibles (alta nueva), arranca igual al total.
        # Si se indica (dato cargado desde archivo), respeta ese valor.
        self.copias_disponibles = copias_totales if copias_disponibles is None else copias_disponibles

    def hay_stock(self):
        return self.copias_disponibles > 0

    def prestar(self):
        self.copias_disponibles -= 1

    def devolver(self):
        self.copias_disponibles += 1

    def a_linea(self):
        """Convierte el libro a una línea de texto para guardar en archivo."""
        return f"{self.id}|{self.titulo}|{self.autor}|{self.copias_totales}|{self.copias_disponibles}"

    def __str__(self):
        return (f"ID: {self.id} | '{self.titulo}' - {self.autor} "
                f"| Disponibles: {self.copias_disponibles}/{self.copias_totales}")
