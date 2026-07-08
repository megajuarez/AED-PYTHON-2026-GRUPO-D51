"""
Clase Biblioteca: administra usuarios, libros y préstamos.
Persiste todo en archivos .txt para que los datos no se pierdan
al cerrar el programa.
"""

import datetime

from src.libro import Libro
from src.usuario import Usuario
from src.prestamo import Prestamo
from src.validaciones import leer_entero, leer_dni, leer_texto_no_vacio


class Biblioteca:
    ARCHIVO_USUARIOS = "usuarios.txt"
    ARCHIVO_LIBROS = "libros.txt"
    ARCHIVO_PRESTAMOS = "prestamos.txt"

    def __init__(self):
        self.usuarios = []
        self.libros = []
        self.prestamos = []
        self.total_multas_cobradas = 0.0
        self.cargar_datos()

    # ---------- persistencia ----------
    def cargar_datos(self):
        """Carga usuarios, libros y préstamos desde los archivos .txt (si existen)."""
        self._cargar_usuarios()
        self._cargar_libros()
        self._cargar_prestamos()

    def _cargar_usuarios(self):
        try:
            with open(self.ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        dni, nombre = linea.split("|")
                        self.usuarios.append(Usuario(dni, nombre))
                    except ValueError:
                        print(f"⚠ Línea inválida en {self.ARCHIVO_USUARIOS}, se ignora: {linea}")
        except FileNotFoundError:
            pass  # Primera ejecución: todavía no existe el archivo.

    def _cargar_libros(self):
        try:
            with open(self.ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        id_libro, titulo, autor, copias_tot, copias_disp = linea.split("|")
                        self.libros.append(
                            Libro(int(id_libro), titulo, autor, int(copias_tot), int(copias_disp))
                        )
                    except ValueError:
                        print(f"⚠ Línea inválida en {self.ARCHIVO_LIBROS}, se ignora: {linea}")
        except FileNotFoundError:
            pass

    def _cargar_prestamos(self):
        try:
            with open(self.ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        (id_p, dni, id_libro, fecha_p, fecha_l,
                         devuelto, fecha_dev, multa) = linea.split("|")

                        usuario = self.buscar_usuario(dni)
                        libro = self.buscar_libro(int(id_libro))
                        if usuario is None or libro is None:
                            print(f"⚠ Préstamo #{id_p} referencia un usuario o libro "
                                  f"inexistente, se ignora.")
                            continue

                        prestamo = Prestamo(
                            usuario, libro,
                            id_prestamo=int(id_p),
                            fecha_prestamo=datetime.date.fromisoformat(fecha_p),
                            fecha_limite=datetime.date.fromisoformat(fecha_l),
                            devuelto=bool(int(devuelto)),
                            fecha_devolucion=(datetime.date.fromisoformat(fecha_dev)
                                               if fecha_dev else None),
                            multa=float(multa),
                        )
                        self.prestamos.append(prestamo)
                        if prestamo.multa > 0:
                            self.total_multas_cobradas += prestamo.multa
                    except (ValueError, IndexError):
                        print(f"⚠ Línea inválida en {self.ARCHIVO_PRESTAMOS}, se ignora: {linea}")
        except FileNotFoundError:
            pass

    def guardar_datos(self):
        """Vuelca el estado actual de usuarios, libros y préstamos a los archivos .txt."""
        try:
            with open(self.ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
                for usuario in self.usuarios:
                    archivo.write(usuario.a_linea() + "\n")

            with open(self.ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
                for libro in self.libros:
                    archivo.write(libro.a_linea() + "\n")

            with open(self.ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
                for prestamo in self.prestamos:
                    archivo.write(prestamo.a_linea() + "\n")
        except IOError as error:
            print(f"⚠ No se pudo guardar la información en disco: {error}")

    # ---------- búsquedas ----------
    def buscar_usuario(self, dni):
        for usuario in self.usuarios:
            if usuario.dni == dni:
                return usuario
        return None

    def buscar_libro(self, id_libro):
        for libro in self.libros:
            if libro.id == id_libro:
                return libro
        return None

    def buscar_prestamo(self, id_prestamo):
        for prestamo in self.prestamos:
            if prestamo.id == id_prestamo:
                return prestamo
        return None

    def usuario_tiene_prestamo_activo(self, dni, id_libro):
        for p in self.prestamos:
            if p.usuario.dni == dni and p.libro.id == id_libro and not p.devuelto:
                return True
        return False

    # ---------- usuarios ----------
    def registrar_usuario(self):
        print("\n--- Registro de nuevo usuario ---")
        dni = leer_dni("Ingrese DNI del usuario: ")
        if self.buscar_usuario(dni) is not None:
            print("⚠ Ya existe un usuario registrado con ese DNI.")
            return
        nombre = leer_texto_no_vacio("Ingrese nombre y apellido: ")
        self.usuarios.append(Usuario(dni, nombre))
        self.guardar_datos()
        print(f"✔ Usuario '{nombre}' registrado correctamente.")

    def listar_usuarios(self):
        print("\n--- Usuarios registrados ---")
        if not self.usuarios:
            print("No hay usuarios registrados todavía.")
            return
        for usuario in self.usuarios:
            print(usuario)

    # ---------- libros ----------
    def registrar_libro(self):
        print("\n--- Registro de nuevo libro ---")
        titulo = leer_texto_no_vacio("Título del libro: ")
        autor = leer_texto_no_vacio("Autor: ")
        copias = leer_entero("Cantidad de copias disponibles: ", minimo=1)
        nuevo_id = self.libros[-1].id + 1 if self.libros else 1
        self.libros.append(Libro(nuevo_id, titulo, autor, copias))
        self.guardar_datos()
        print(f"✔ Libro '{titulo}' registrado con ID {nuevo_id}.")

    def listar_libros(self):
        print("\n--- Catálogo de libros ---")
        if not self.libros:
            print("No hay libros cargados todavía.")
            return
        for libro in self.libros:
            print(libro)

    # ---------- préstamos ----------
    def realizar_prestamo(self):
        print("\n--- Registrar préstamo ---")
        if not self.usuarios:
            print("⚠ No hay usuarios registrados. Registre uno primero.")
            return
        if not self.libros:
            print("⚠ No hay libros cargados. Registre uno primero.")
            return

        dni = leer_dni("DNI del usuario: ")
        usuario = self.buscar_usuario(dni)
        if usuario is None:
            print("⚠ No existe un usuario con ese DNI. Debe registrarlo primero.")
            return

        self.listar_libros()
        id_libro = leer_entero("ID del libro a prestar: ", minimo=1)
        libro = self.buscar_libro(id_libro)
        if libro is None:
            print("⚠ No existe un libro con ese ID.")
            return
        if not libro.hay_stock():
            print(f"⚠ No hay copias disponibles de '{libro.titulo}' en este momento.")
            return
        if self.usuario_tiene_prestamo_activo(dni, id_libro):
            print("⚠ Este usuario ya tiene un préstamo activo de ese mismo libro.")
            return

        prestamo = Prestamo(usuario, libro)
        libro.prestar()
        self.prestamos.append(prestamo)
        self.guardar_datos()

        print(f"✔ Préstamo registrado. '{libro.titulo}' para {usuario.nombre}.")
        print(f"  Fecha límite de devolución: {prestamo.fecha_limite.strftime('%d/%m/%Y')}")

    def listar_prestamos_activos(self):
        print("\n--- Préstamos activos ---")
        activos = [p for p in self.prestamos if not p.devuelto]
        if not activos:
            print("No hay préstamos activos en este momento.")
            return
        for prestamo in activos:
            print(prestamo)

    def realizar_devolucion(self):
        print("\n--- Registrar devolución ---")
        if not self.prestamos:
            print("⚠ No hay préstamos registrados.")
            return

        self.listar_prestamos_activos()
        id_prestamo = leer_entero("Ingrese el número de préstamo a devolver: ", minimo=1)
        prestamo = self.buscar_prestamo(id_prestamo)

        if prestamo is None:
            print("⚠ No existe un préstamo con ese número.")
            return
        if prestamo.devuelto:
            print("⚠ Ese préstamo ya fue devuelto anteriormente.")
            return

        multa = prestamo.registrar_devolucion()
        prestamo.libro.devolver()
        self.guardar_datos()

        print(f"✔ Devolución registrada para '{prestamo.libro.titulo}'.")
        if multa > 0:
            dias_atraso = (prestamo.fecha_devolucion - prestamo.fecha_limite).days
            self.total_multas_cobradas += multa
            print(f"  ⚠ Devolución con {dias_atraso} día(s) de atraso.")
            print(f"  Multa a cobrar: ${multa:.2f}")
        else:
            print("  Devolución en tiempo y forma. Sin multa.")

    # ---------- estadísticas ----------
    def mostrar_estadisticas(self):
        print("\n--- Estadísticas de la biblioteca ---")
        print(f"Total de préstamos realizados: {len(self.prestamos)}")

        activos = sum(1 for p in self.prestamos if not p.devuelto)
        devueltos = len(self.prestamos) - activos
        print(f"Préstamos activos actualmente: {activos}")
        print(f"Préstamos ya devueltos: {devueltos}")
        print(f"Total recaudado en multas: ${self.total_multas_cobradas:.2f}")

        if self.prestamos:
            conteo = {}
            for p in self.prestamos:
                conteo[p.libro.id] = conteo.get(p.libro.id, 0) + 1
            id_top = max(conteo, key=conteo.get)
            libro_top = self.buscar_libro(id_top)
            print(f"Libro más solicitado: '{libro_top.titulo}' ({conteo[id_top]} préstamo/s)")
        else:
            print("Todavía no se registraron préstamos.")
