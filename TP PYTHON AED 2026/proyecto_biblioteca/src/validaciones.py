"""
Funciones utilitarias para leer y validar datos ingresados por teclado.
No pertenecen a ninguna clase del dominio (Libro, Usuario, Prestamo):
son herramientas genéricas de entrada/salida.
"""


def leer_entero(mensaje, minimo=None):
    """Pide un número entero por teclado, validando que sea válido y >= mínimo si se indica."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"⚠ El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("⚠ Ingrese un número entero válido.")


def leer_texto_no_vacio(mensaje):
    """Pide un texto por teclado, validando que no esté vacío ni contenga '|'."""
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("⚠ El campo no puede estar vacío.")
            continue
        if "|" in texto:
            print("⚠ El texto no puede contener el carácter '|'.")
            continue
        return texto


def leer_dni(mensaje):
    """Pide un DNI, validando que sea numérico y de longitud razonable."""
    while True:
        dni = input(mensaje).strip()
        if not dni.isdigit():
            print("⚠ El DNI debe contener solo números.")
            continue
        if len(dni) < 6 or len(dni) > 9:
            print("⚠ El DNI debe tener entre 6 y 9 dígitos.")
            continue
        return dni
