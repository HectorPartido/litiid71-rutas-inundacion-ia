"""Escenarios de prueba reutilizables.

Cada función devuelve (terreno, inicio, refugios). Las pruebas modifican
copias de estos escenarios con colocar_zona, así el original no cambia.
"""
from src.modelo import LEVE, MEDIA, BLOQUEADA
from src.terreno import crear_terreno, colocar_zona


def escenario_atajo_inundado():
    """El camino recto cruza una zona inundada; rodearla es más largo pero más seguro.

    Es el escenario principal: la ruta más corta NO es la más conveniente.
    """
    t = crear_terreno(10, 12)
    t = colocar_zona(t, (2, 3), (7, 8), LEVE)        # orilla de la inundación
    t = colocar_zona(t, (3, 4), (6, 7), MEDIA)       # centro más profundo
    t = colocar_zona(t, (8, 2), (9, 9), BLOQUEADA)   # el sur está cerrado
    t = colocar_zona(t, (0, 10), (3, 10), BLOQUEADA) # muro cerca del refugio
    inicio = (5, 0)
    refugios = [(5, 11)]
    return t, inicio, refugios


def escenario_dos_refugios():
    """Hay un refugio cercano detrás de agua y otro más lejano por terreno seco.

    Sirve para ver qué refugio elige cada algoritmo según el peso del riesgo.
    La franja inundada solo tiene un paso seco en la fila 0.
    """
    t = crear_terreno(9, 12)
    t = colocar_zona(t, (1, 4), (8, 6), MEDIA)       # franja inundada al centro
    inicio = (6, 2)
    refugios = [(6, 9), (0, 11)]                     # cercano con agua / lejano seco
    return t, inicio, refugios