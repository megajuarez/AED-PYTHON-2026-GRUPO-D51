"""
Sistema de Gestión de Biblioteca
Algoritmos y Estructuras de Datos - ISI 
Punto de entrada del programa. Las Funciones estan definidas dentro
de la carpeta src/ (clases Libro, Usuario, Prestamo y Biblioteca).
"""

from src.biblioteca import Biblioteca
from src.validaciones import leer_entero


def mostrar_menu():
    print("\n" + "=" * 45)
    print("      SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print("=" * 45)
    print("1. Registrar usuario")
    print("2. Listar usuarios")
    print("3. Registrar libro")
    print("4. Listar catálogo de libros")
    print("5. Realizar préstamo")
    print("6. Listar préstamos activos")
    print("7. Registrar devolución")
    print("8. Ver estadísticas")
    print("0. Salir")
    print("=" * 45)


def main():
    biblioteca = Biblioteca()

    acciones = {
        1: biblioteca.registrar_usuario,
        2: biblioteca.listar_usuarios,
        3: biblioteca.registrar_libro,
        4: biblioteca.listar_libros,
        5: biblioteca.realizar_prestamo,
        6: biblioteca.listar_prestamos_activos,
        7: biblioteca.realizar_devolucion,
        8: biblioteca.mostrar_estadisticas,
    }

    print("Bienvenido/a al Sistema de Gestión de Biblioteca")

    while True:
        mostrar_menu()
        opcion = leer_entero("Seleccione una opción: ")

        if opcion == 0:
            print("\nGracias por usar el sistema. ¡Hasta luego!")
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            print("⚠ Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
