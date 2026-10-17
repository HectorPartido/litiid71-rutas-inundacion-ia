# litiid71-rutas-inundacion-ia

# Cuando el camino más corto no es el mejor

Práctica en equipo de **Fundamentos de Inteligencia Artificial** — Grupo LITIID71.

Prototipo que simula una zona inundada representada como cuadrícula. Un agente debe llegar desde una zona afectada hasta un refugio, sin atravesar zonas bloqueadas y considerando el riesgo de cada zona según su nivel de inundación. Se implementan y comparan varias estrategias de búsqueda para mostrar la diferencia entre **encontrar una ruta** y **encontrar una ruta conveniente**.

## Integrantes y roles

| Integrante | Usuario de GitHub | Rol |
|---|---|---|
| Hector Partido Flores | @HectorPartido | Coordinación, integración y documentación |
| Ismael Alexander Hidalgo Aguilando | @Ismael-78 | Modelo del terreno y visualización |
| Hector Martínez Sánchez | @HectorMartinez17 | Búsqueda no informada (BFS, DFS, UCS) |
| Gildardo Emmanuel González García | @Thenoob20-0 | Búsqueda informada (Greedy, A*) y comparación |
| Anthony Oziel Ramos López | @ThonyOziel | Validación de rutas y pruebas |

## Estructura del repositorio

```
├── practica_rutas.ipynb            Notebook principal (demostraciones, comparación y pruebas)
├── src/
│   ├── modelo.py                   Contrato común: niveles, riesgo, Resultado
│   ├── terreno.py                  Terreno, vecinos, costo y escenarios
│   ├── visualizacion.py            Dibujo del terreno y las rutas
│   ├── busqueda_no_informada.py    BFS, DFS, UCS
│   ├── busqueda_informada.py       Greedy Best-First, A*
│   └── validacion.py               Validador de rutas
├── docs/                           Justificaciones (PDF opcional)
├── requirements.txt
└── README.md
```

## Modelo del problema

| Nivel | Significado | Transitable | Riesgo |
|---|---|---|---|
| 0 | Seco | Sí | 0 |
| 1 | Inundación leve | Sí | 1 |
| 2 | Inundación media | Sí | 3 |
| 3 | Inundación severa | No | — |

- Movimiento en 4 direcciones (sin diagonales).
- Costo de entrar a una celda: `1 + λ · riesgo(nivel)`.
- Con `λ = 0` se busca la ruta más corta; al aumentar `λ` el algoritmo prefiere evitar zonas de riesgo.

Todos los algoritmos tienen la misma firma y devuelven un `Resultado` (ver `src/modelo.py`):

```python
nombre_algoritmo(terreno, inicio, refugios, lam=1.0) -> Resultado
```

## Cómo ejecutar

Requisitos: Python 3.10 o superior y Git.

```bash
git clone https://github.com/USUARIO/litiid71-rutas-inundacion-ia.git
cd litiid71-rutas-inundacion-ia
```

Crear y activar el entorno virtual:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias y abrir el notebook:

```bash
pip install -r requirements.txt
jupyter notebook practica_rutas.ipynb
```

Ejecutar todas las celdas en orden (**Run All**). Todos los resultados de la comparación y las pruebas se generan al ejecutar el notebook.

## Forma de trabajo

### Configuración inicial (una vez por integrante)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "correo-de-tu-cuenta@github.com"
nbstripout --install
```

El correo debe ser el de tu cuenta de GitHub para que los commits se te atribuyan. `nbstripout` limpia las salidas del notebook antes de cada commit para evitar conflictos.

### Flujo con ramas

1. Actualizar `main`: `git checkout main && git pull`
2. Crear una rama por tarea: `git checkout -b feature/nombre-de-la-tarea`
3. Hacer commits pequeños y descriptivos.
4. Subir la rama: `git push -u origin feature/nombre-de-la-tarea`
5. Abrir un Pull Request a `main` y pedir revisión a otro integrante.
6. Hacer merge solo después de la aprobación.

Nadie sube cambios directamente a `main`.

### Convención de commits

Formato: `tipo(área): descripción en presente`

| Tipo | Uso | Ejemplo |
|---|---|---|
| `feat` | Nueva funcionalidad | `feat(busqueda): implementa A* con heurística Manhattan` |
| `fix` | Corrección de un error | `fix(terreno): evita vecinos fuera de la cuadrícula` |
| `test` | Pruebas | `test: agrega prueba de refugio inaccesible` |
| `docs` | Documentación | `docs: justifica los valores de riesgo por nivel` |
| `refactor` | Reorganización sin cambiar comportamiento | `refactor(validacion): separa cálculo de costo` |
| `chore` | Configuración y mantenimiento | `chore: agrega pandas a requirements` |

Usar `git add archivo` en lugar de `git add .` para que cada commit tenga un solo propósito.

## Uso de herramientas de IA

Se documenta en la sección 8 del notebook principal.