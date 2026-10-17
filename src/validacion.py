
import math
from collections import deque

from src.modelo import Posicion, Resultado, BLOQUEADA, RIESGO_POR_NIVEL


def _dentro(terreno, pos: Posicion) -> bool:
    filas, columnas = terreno.shape
    return 0 <= pos[0] < filas and 0 <= pos[1] < columnas


def _adyacentes(a: Posicion, b: Posicion) -> bool:
    """Dos celdas son adyacentes si están a distancia Manhattan 1 (sin diagonales)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def revisar_estructura(terreno, inicio: Posicion, refugios: list[Posicion],
                       ruta: list[Posicion]) -> list[str]:
    """Revisa que la ruta sea físicamente posible. Devuelve la lista de errores."""
    errores = []
    if not ruta:
        return ["La ruta está vacía"]

    if ruta[0] != inicio:
        errores.append(f"La ruta empieza en {ruta[0]}, no en el inicio {inicio}")
    if ruta[-1] not in set(refugios):
        errores.append(f"La ruta termina en {ruta[-1]}, que no es un refugio")

    for i, celda in enumerate(ruta):
        if not _dentro(terreno, celda):
            errores.append(f"Paso {i}: la celda {celda} está fuera del terreno")
        elif terreno[celda] == BLOQUEADA:
            errores.append(f"Paso {i}: la celda {celda} está bloqueada por inundación")

    for i in range(1, len(ruta)):
        if not _adyacentes(ruta[i - 1], ruta[i]):
            errores.append(f"Paso {i}: salto no permitido de {ruta[i - 1]} a {ruta[i]}")

    if len(set(ruta)) != len(ruta):
        errores.append("La ruta pasa más de una vez por la misma celda")
    return errores


def revisar_metricas(terreno, resultado: Resultado, lam: float) -> list[str]:
    """Recalcula pasos, riesgo y costo, y los compara con lo que reportó el algoritmo."""
    ruta = resultado.ruta
    pasos = len(ruta) - 1
    riesgo_total = sum(RIESGO_POR_NIVEL[int(terreno[c])] for c in ruta[1:])
    costo = pasos + lam * riesgo_total

    errores = []
    if resultado.pasos != pasos:
        errores.append(f"Pasos reportados {resultado.pasos}, recalculados {pasos}")
    if not math.isclose(resultado.riesgo_acumulado, riesgo_total):
        errores.append(f"Riesgo reportado {resultado.riesgo_acumulado}, recalculado {riesgo_total}")
    if not math.isclose(resultado.costo, costo):
        errores.append(f"Costo reportado {resultado.costo}, recalculado {costo}")
    return errores



def hay_camino(terreno, inicio: Posicion, refugios: list[Posicion]) -> bool:
    """Exploración independiente: ¿existe algún camino del inicio a un refugio?

    Sirve para confirmar que, cuando un algoritmo dice "sin ruta",
    realmente no existe ninguna.
    """
    if not _dentro(terreno, inicio) or terreno[inicio] == BLOQUEADA:
        return False
    metas = set(refugios)
    visitados = {inicio}
    cola = deque([inicio])
    while cola:
        actual = cola.popleft()
        if actual in metas:
            return True
        for df, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            sig = (actual[0] + df, actual[1] + dc)
            if _dentro(terreno, sig) and terreno[sig] != BLOQUEADA and sig not in visitados:
                visitados.add(sig)
                cola.append(sig)
    return False