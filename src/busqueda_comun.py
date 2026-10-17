"""Utilidades compartidas por todos los algoritmos de búsqueda."""
from src.modelo import Posicion, Resultado
from src.terreno import riesgo, costo_paso


def reconstruir_ruta(padres: dict[Posicion, Posicion | None],
                     meta: Posicion) -> list[Posicion]:
    """Recorre el diccionario de padres desde la meta hasta el inicio."""
    ruta = [meta]
    while padres[ruta[-1]] is not None:
        ruta.append(padres[ruta[-1]])
    ruta.reverse()
    return ruta


def resumir_ruta(terreno, ruta: list[Posicion], lam: float) -> tuple[float, int, float]:
    """Calcula (costo, pasos, riesgo_acumulado) de una ruta.

    La celda de inicio no suma costo ni riesgo: solo se cobra al entrar a una celda.
    Siempre se cumple: costo = pasos + lam * riesgo_acumulado.
    """
    celdas_recorridas = ruta[1:]
    costo = sum(costo_paso(terreno, celda, lam) for celda in celdas_recorridas)
    riesgo_total = sum(riesgo(terreno, celda) for celda in celdas_recorridas)
    return float(costo), len(celdas_recorridas), float(riesgo_total)


def construir_resultado(algoritmo: str, terreno, lam: float,
                        padres: dict[Posicion, Posicion | None],
                        meta: Posicion | None, expandidos: int, generados: int,
                        frontera_max: int, tiempo_ms: float) -> Resultado:
    """Arma el Resultado común. Si meta es None, no se encontró ruta."""
    if meta is None:
        return Resultado(algoritmo=algoritmo, encontrada=False,
                         nodos_expandidos=expandidos, nodos_generados=generados,
                         frontera_max=frontera_max, tiempo_ms=tiempo_ms)

    ruta = reconstruir_ruta(padres, meta)
    costo, pasos, riesgo_total = resumir_ruta(terreno, ruta, lam)
    return Resultado(algoritmo=algoritmo, encontrada=True, ruta=ruta,
                     costo=costo, pasos=pasos, riesgo_acumulado=riesgo_total,
                     nodos_expandidos=expandidos, nodos_generados=generados,
                     frontera_max=frontera_max, tiempo_ms=tiempo_ms)