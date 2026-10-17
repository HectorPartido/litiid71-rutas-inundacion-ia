"""Búsqueda no informada: BFS, DFS y UCS.

Todas siguen el contrato de src/modelo.py:
    algoritmo(terreno, inicio, refugios, lam=1.0) -> Resultado

Criterios comunes para que las métricas sean comparables:
- nodos_generados: nodos agregados a la frontera (incluye el inicio).
- nodos_expandidos: nodos sacados de la frontera y cuyos vecinos se revisaron.
- La prueba de meta se hace al sacar el nodo de la frontera.
"""
import heapq
import time
from collections import deque

from src.modelo import Posicion, Resultado
from src.terreno import es_transitable, vecinos, costo_paso
from src.busqueda_comun import construir_resultado


def bfs(terreno, inicio: Posicion, refugios: list[Posicion],
        lam: float = 1.0) -> Resultado:
    """Búsqueda en anchura: encuentra la ruta con MENOS PASOS.

    Ignora el riesgo al decidir; lam solo se usa para reportar
    el costo real de la ruta que encontró.
    """
    t0 = time.perf_counter()
    metas = set(refugios)

    if not es_transitable(terreno, inicio):
        return construir_resultado("BFS", terreno, lam, {}, None, 0, 0, 0,
                                   (time.perf_counter() - t0) * 1000)

    frontera = deque([inicio])
    padres = {inicio: None}  # también funciona como conjunto de visitados
    generados, expandidos, frontera_max = 1, 0, 1

    while frontera:
        actual = frontera.popleft()

        if actual in metas:
            return construir_resultado("BFS", terreno, lam, padres, actual,
                                       expandidos, generados, frontera_max,
                                       (time.perf_counter() - t0) * 1000)

        expandidos += 1
        for vecino in vecinos(terreno, actual):
            if vecino not in padres:
                padres[vecino] = actual
                frontera.append(vecino)
                generados += 1
        frontera_max = max(frontera_max, len(frontera))

    return construir_resultado("BFS", terreno, lam, padres, None, expandidos,
                               generados, frontera_max,
                               (time.perf_counter() - t0) * 1000)

                               

def dfs(terreno, inicio: Posicion, refugios: list[Posicion],
        lam: float = 1.0) -> Resultado:
    """Búsqueda en profundidad: encuentra UNA ruta, sin garantía de ser buena.

    Sirve como contraste: muestra la diferencia entre encontrar una ruta
    y encontrar una ruta conveniente.
    """
    t0 = time.perf_counter()
    metas = set(refugios)

    if not es_transitable(terreno, inicio):
        return construir_resultado("DFS", terreno, lam, {}, None, 0, 0, 0,
                                   (time.perf_counter() - t0) * 1000)

    pila = [inicio]
    padres = {inicio: None}
    visitados = set()
    generados, expandidos, frontera_max = 1, 0, 1

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)

        if actual in metas:
            return construir_resultado("DFS", terreno, lam, padres, actual,
                                       expandidos, generados, frontera_max,
                                       (time.perf_counter() - t0) * 1000)

        expandidos += 1
        # Se apilan al revés para explorar en el orden de MOVIMIENTOS.
        for vecino in reversed(vecinos(terreno, actual)):
            if vecino not in visitados:
                padres[vecino] = actual
                pila.append(vecino)
                generados += 1
        frontera_max = max(frontera_max, len(pila))

    return construir_resultado("DFS", terreno, lam, padres, None, expandidos,
                               generados, frontera_max,
                               (time.perf_counter() - t0) * 1000)



def ucs(terreno, inicio: Posicion, refugios: list[Posicion],
        lam: float = 1.0) -> Resultado:
    """Búsqueda de costo uniforme: encuentra la ruta de MENOR COSTO.

    El costo de cada paso es 1 + lam * riesgo, así que el riesgo
    sí influye en la decisión.
    """
    t0 = time.perf_counter()
    metas = set(refugios)

    if not es_transitable(terreno, inicio):
        return construir_resultado("UCS", terreno, lam, {}, None, 0, 0, 0,
                                   (time.perf_counter() - t0) * 1000)

    contador = 0  # desempate estable cuando dos nodos tienen el mismo costo
    frontera = [(0.0, contador, inicio)]
    mejor_costo = {inicio: 0.0}
    padres = {inicio: None}
    cerrados = set()
    generados, expandidos, frontera_max = 1, 0, 1

    while frontera:
        g, _, actual = heapq.heappop(frontera)
        if actual in cerrados:
            continue  # entrada vieja: ya se expandió con un costo menor
        cerrados.add(actual)

        if actual in metas:
            return construir_resultado("UCS", terreno, lam, padres, actual,
                                       expandidos, generados, frontera_max,
                                       (time.perf_counter() - t0) * 1000)

        expandidos += 1
        for vecino in vecinos(terreno, actual):
            nuevo_g = g + costo_paso(terreno, vecino, lam)
            if vecino not in cerrados and nuevo_g < mejor_costo.get(vecino, float("inf")):
                mejor_costo[vecino] = nuevo_g
                padres[vecino] = actual
                contador += 1
                heapq.heappush(frontera, (nuevo_g, contador, vecino))
                generados += 1
        frontera_max = max(frontera_max, len(frontera))

    return construir_resultado("UCS", terreno, lam, padres, None, expandidos,
                               generados, frontera_max,
                               (time.perf_counter() - t0) * 1000)