"""Búsqueda informada: Greedy Best-First y A*.

Siguen el mismo contrato y los mismos criterios de métricas que
src/busqueda_no_informada.py para que la comparación sea justa:
- nodos_generados: nodos agregados a la frontera (incluye el inicio).
- nodos_expandidos: nodos sacados de la frontera y cuyos vecinos se revisaron.
- La prueba de meta se hace al sacar el nodo de la frontera.
"""
import heapq
import time

from src.modelo import Posicion, Resultado
from src.terreno import es_transitable, vecinos, costo_paso
from src.busqueda_comun import construir_resultado


def heuristica_manhattan(pos: Posicion, refugios: list[Posicion]) -> int:
    """Distancia Manhattan al refugio más cercano.

    Es admisible (nunca sobreestima el costo real) porque:
    - sin diagonales, se necesitan al menos |Δfila| + |Δcolumna| pasos, y
    - cada paso cuesta como mínimo 1 (cuando el riesgo es 0).
    También es consistente, así que A* con conjunto de cerrados da la ruta óptima.
    """
    return min(abs(pos[0] - r[0]) + abs(pos[1] - r[1]) for r in refugios)