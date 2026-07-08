"""Clase Prestamo: representa el préstamo de un libro a un usuario."""

import datetime

DIAS_PLAZO_PRESTAMO = 7
MULTA_POR_DIA_ATRASO = 100 # pesos por día de atraso


class Prestamo:
    contador_ids = 0  # atributo de clase: lleva el máximo ID usado

    def __init__(self, usuario, libro, id_prestamo=None, fecha_prestamo=None,
                 fecha_limite=None, devuelto=False, fecha_devolucion=None, multa=0.0):
        if id_prestamo is None:
            # Alta nueva: genero un ID incremental
            Prestamo.contador_ids += 1
            self.id = Prestamo.contador_ids
        else:
            # Dato cargado desde archivo: respeto el ID guardado
            self.id = id_prestamo
            if id_prestamo > Prestamo.contador_ids:
                Prestamo.contador_ids = id_prestamo

        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.date.today()
        self.fecha_limite = fecha_limite if fecha_limite else (
            self.fecha_prestamo + datetime.timedelta(days=DIAS_PLAZO_PRESTAMO))
        self.devuelto = devuelto
        self.fecha_devolucion = fecha_devolucion
        self.multa = multa

    def registrar_devolucion(self):
        """Marca el préstamo como devuelto y calcula la multa si hay atraso."""
        self.fecha_devolucion = datetime.date.today()
        self.devuelto = True
        dias_atraso = (self.fecha_devolucion - self.fecha_limite).days
        self.multa = dias_atraso * MULTA_POR_DIA_ATRASO if dias_atraso > 0 else 0.0
        return self.multa

    def a_linea(self):
        """Convierte el préstamo a una línea de texto para guardar en archivo."""
        fecha_dev = self.fecha_devolucion.isoformat() if self.fecha_devolucion else ""
        return (f"{self.id}|{self.usuario.dni}|{self.libro.id}|"
                f"{self.fecha_prestamo.isoformat()}|{self.fecha_limite.isoformat()}|"
                f"{int(self.devuelto)}|{fecha_dev}|{self.multa}")

    def __str__(self):
        return (f"Préstamo #{self.id} | Libro: '{self.libro.titulo}' "
                f"| Usuario: {self.usuario.nombre} "
                f"| Límite: {self.fecha_limite.strftime('%d/%m/%Y')}")
