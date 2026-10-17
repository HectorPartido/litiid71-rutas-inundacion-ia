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


def greedy(terreno, inicio: Posicion, refugios: list[Posicion],
           lam: float = 1.0) -> Resultado:
    """Greedy Best-First: siempre avanza hacia la celda que PARECE más cercana al refugio.

    Solo usa la heurística, ignora el costo acumulado y el riesgo.
    Suele expandir pocos nodos, pero no garantiza la mejor ruta.
    lam solo se usa para reportar el costo real de la ruta encontrada.
    """
    t0 = time.perf_counter()
    metas = set(refugios)
    if not es_transitable(terreno, inicio) or not refugios:
        return construir_resultado("Greedy", terreno, lam, {}, None, 0, 0, 0,
                                   (time.perf_counter() - t0) * 1000)
    contador = 0
    frontera = [(heuristica_manhattan(inicio, refugios), contador, inicio)]
    padres = {inicio: None}
    cerrados = set()
    generados, expandidos, frontera_max = 1, 0, 1
    while frontera:
        _, _, actual = heapq.heappop(frontera)
        if actual in cerrados:
            continue
        cerrados.add(actual)
        if actual in metas:
            return construir_resultado("Greedy", terreno, lam, padres, actual,
                                       expandidos, generados, frontera_max,
                                       (time.perf_counter() - t0) * 1000)
        expandidos += 1
        for vecino in vecinos(terreno, actual):
            if vecino not in padres:
                padres[vecino] = actual
                contador += 1
                heapq.heappush(frontera, (heuristica_manhattan(vecino, refugios),
                                          contador, vecino))
                generados += 1
        frontera_max = max(frontera_max, len(frontera))
    return construir_resultado("Greedy", terreno, lam, padres, None, expandidos,
                               generados, frontera_max,
                               (time.perf_counter() - t0) * 1000)