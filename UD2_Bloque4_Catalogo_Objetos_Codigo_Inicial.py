"""
UD2 - Bloque 4
Tarea individual: primeros pasos del catálogo orientado a objetos

Objetivos:
1. Crear las dataclasses Libro y Socio.
2. Listar libros utilizando class_row.
3. Buscar un libro por su identificador.

Base de datos: biblioteca
"""

import os
from dataclasses import dataclass
from decimal import Decimal

import psycopg
from psycopg.rows import class_row


# ==========================================================
# ACTIVIDAD 1. CREAR LAS DATACLASSES
# ==========================================================

# TODO 1:
# Añade el decorador adecuado y declara la clase Libro.
# Debe contener exactamente estos campos:
#   id_libro: int
#   titulo: str
#   autor: str
#   precio: Decimal


class Libro:
    pass


# TODO 2:
# Añade el decorador adecuado y declara la clase Socio.
# Debe contener exactamente estos campos:
#   id_socio: int
#   nombre: str
#   apellidos: str
#   telefono: str | None
#   activo: bool


class Socio:
    pass


# ==========================================================
# CONFIGURACIÓN DE LA CONEXIÓN
# ==========================================================


def obtener_configuracion():
    """Recupera la configuración desde variables de entorno."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "connect_timeout": 5,
    }


# ==========================================================
# ACTIVIDAD 2. LISTAR LIBROS CON class_row
# ==========================================================


def listar_libros(conexion) -> list[Libro]:
    """
    Recupera los libros ordenados por título.

    Debe devolver una lista de objetos Libro, no tuplas
    ni diccionarios.
    """

    # TODO 3:
    # 1. Crea un cursor con row_factory=class_row(Libro).
    # 2. Ejecuta la consulta indicada más abajo.
    # 3. Devuelve todos los resultados con fetchall().
    #
    # Consulta que debes utilizar:
    #
    # SELECT
    #     l.id_libro,
    #     l.titulo,
    #     CONCAT(a.nombre, ' ', a.apellidos) AS autor,
    #     l.precio
    # FROM libros AS l
    # JOIN autores AS a
    #     ON a.id_autor = l.id_autor
    # ORDER BY l.titulo

    pass


# ==========================================================
# ACTIVIDAD 3. BUSCAR UN LIBRO POR ID
# ==========================================================


def buscar_libro_por_id(
    conexion,
    id_libro: int,
) -> Libro | None:
    """
    Busca un libro mediante su identificador.

    Devuelve:
    - Un objeto Libro si existe.
    - None si no existe.
    """

    # TODO 4:
    # 1. Crea un cursor con row_factory=class_row(Libro).
    # 2. Ejecuta la consulta parametrizada indicada abajo.
    # 3. Recupera una única fila mediante fetchone().
    # 4. Devuelve directamente el resultado.
    #
    # Consulta que debes utilizar:
    #
    # SELECT
    #     l.id_libro,
    #     l.titulo,
    #     CONCAT(a.nombre, ' ', a.apellidos) AS autor,
    #     l.precio
    # FROM libros AS l
    # JOIN autores AS a
    #     ON a.id_autor = l.id_autor
    # WHERE l.id_libro = %s

    pass


# ==========================================================
# FUNCIONES DE PRESENTACIÓN YA COMPLETADAS
# ==========================================================


def mostrar_libro(libro: Libro) -> None:
    """Muestra los datos de un objeto Libro."""
    print(
        f"{libro.id_libro} | "
        f"{libro.titulo} | "
        f"{libro.autor} | "
        f"{libro.precio:.2f} €"
    )


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================


def main():
    configuracion = obtener_configuracion()

    try:
        with psycopg.connect(**configuracion) as conexion:
            print("\n--- CATÁLOGO DE LIBROS ---")

            libros = listar_libros(conexion)

            if not libros:
                print("No hay libros registrados.")
            else:
                for libro in libros:
                    mostrar_libro(libro)

            print("\n--- BÚSQUEDA POR IDENTIFICADOR ---")

            # Puedes cambiar este identificador para realizar pruebas.
            id_buscado = 1

            libro_encontrado = buscar_libro_por_id(
                conexion,
                id_buscado,
            )

            if libro_encontrado is None:
                print(
                    "No existe ningún libro con el "
                    f"identificador {id_buscado}."
                )
            else:
                print("Libro encontrado:")
                mostrar_libro(libro_encontrado)

            print("\n--- COMPROBACIÓN DE None ---")

            libro_inexistente = buscar_libro_por_id(
                conexion,
                999999,
            )

            if libro_inexistente is None:
                print(
                    "La búsqueda de un identificador inexistente "
                    "ha devuelto None correctamente."
                )

    except KeyError as error:
        print(
            "Falta una variable de entorno:",
            error,
        )

    except ValueError:
        print(
            "DB_PORT debe contener un número entero."
        )

    except psycopg.OperationalError as error:
        print(
            "No se pudo establecer la conexión "
            "con PostgreSQL."
        )
        print(error)

    except psycopg.Error as error:
        print("Se produjo un error de base de datos.")
        print(error)


if __name__ == "__main__":
    main()
