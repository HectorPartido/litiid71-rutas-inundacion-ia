

"""Modelo del terreno inundado.

El terreno es una cuadrícula (np.ndarray 2D de enteros) donde cada celda
guarda su nivel de inundación: LIBRE, LEVE, MEDIA o BLOQUEADA.

Las posiciones son tuplas (fila, columna).
"""

import numpy as np

from src.modelo import Posicion, LIBRE, BLOQUEADA, RIESGO_POR_NIVEL


# Orden fijo de exploración: arriba, abajo, izquierda, derecha.
# Mantenerlo fijo hace que BFS y DFS den siempre el mismo resultado.
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def crear_terreno(filas: int, columnas: int, nivel: int = LIBRE) -> np.ndarray:
    """Crea un terreno de filas x columnas con todas las celdas en el mismo nivel."""
    if filas <= 0 or columnas <= 0:
        raise ValueError("El terreno debe tener al menos una fila y una columna")

    return np.full((filas, columnas), nivel, dtype=int)


def dentro_de_limites(terreno: np.ndarray, pos: Posicion) -> bool:
    """Indica si la posición existe dentro de la cuadrícula."""
    fila, columna = pos
    filas, columnas = terreno.shape

    return 0 <= fila < filas and 0 <= columna < columnas


def es_transitable(terreno: np.ndarray, pos: Posicion) -> bool:
    """Una celda es transitable si existe y no está bloqueada por inundación."""
    return dentro_de_limites(terreno, pos) and terreno[pos] != BLOQUEADA


def colocar_zona(
    terreno: np.ndarray,
    esquina1: Posicion,
    esquina2: Posicion,
    nivel: int
) -> np.ndarray:
    """Devuelve una copia del terreno con un rectángulo cambiado al nivel indicado.

    esquina1 y esquina2 son esquinas opuestas del rectángulo (incluidas).
    No modifica el terreno original, para poder comparar antes y después.
    """
    nuevo = terreno.copy()

    f1, f2 = sorted((esquina1[0], esquina2[0]))
    c1, c2 = sorted((esquina1[1], esquina2[1]))

    nuevo[f1:f2 + 1, c1:c2 + 1] = nivel

    return nuevo
