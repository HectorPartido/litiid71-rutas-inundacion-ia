"""Contrato común del proyecto.

Todos los algoritmos de búsqueda deben tener esta firma:

    def nombre_algoritmo(terreno, inicio, refugios, lam=1.0) -> Resultado

- terreno: np.ndarray 2D de enteros con el nivel de inundación de cada celda.
- inicio: Posicion (fila, columna).
- refugios: list[Posicion]; llegar a cualquiera cuenta como éxito.
- lam: peso del riesgo en el costo.

Reglas del modelo:
- Movimiento en 4 direcciones (arriba, abajo, izquierda, derecha), sin diagonales.
- Una celda con nivel BLOQUEADA nunca se puede pisar.
- Costo de entrar a una celda = 1 + lam * RIESGO_POR_NIVEL[nivel].
"""
from dataclasses import dataclass, field

Posicion = tuple[int, int]  # (fila, columna)

# Niveles de inundación
LIBRE, LEVE, MEDIA, BLOQUEADA = 0, 1, 2, 3

# Riesgo por nivel; BLOQUEADA no aparece porque no es transitable
RIESGO_POR_NIVEL = {LIBRE: 0, LEVE: 1, MEDIA: 3}


@dataclass
class Resultado:
    algoritmo: str
    encontrada: bool
    ruta: list[Posicion] = field(default_factory=list)
    costo: float = 0.0
    pasos: int = 0
    riesgo_acumulado: float = 0.0
    nodos_expandidos: int = 0
    nodos_generados: int = 0
    frontera_max: int = 0
    tiempo_ms: float = 0.0