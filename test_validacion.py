from src.modelo import *
from src.terreno import crear_terreno, colocar_zona
from src.validacion import validar_resultado

t = crear_terreno(3, 4)
t = colocar_zona(t, (1,1), (1,1), MEDIA)
t = colocar_zona(t, (0,2), (1,2), BLOQUEADA)
print(t)
ini, ref = (0,0), [(0,3)]
buena = [(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(1,3),(0,3)]
casos = {
    'ruta correcta': Resultado('manual', True, buena, 7.0, 7, 0.0),
    'pisa bloqueada': Resultado('manual', True, [(0,0),(0,1),(0,2),(0,3)], 3.0, 3, 0.0),
    'salto diagonal': Resultado('manual', True, [(0,0),(1,1),(2,2),(2,3),(1,3),(0,3)], 8.0, 5, 3.0),
    'costo mal reportado': Resultado('manual', True, buena, 5.0, 7, 0.0),
    'no termina en refugio': Resultado('manual', True, [(0,0),(1,0)], 1.0, 1, 0.0),
    'dice sin ruta pero existe': Resultado('manual', False),
}
for nombre, r in casos.items():
    ok, errores = validar_resultado(t, ini, ref, r, lam=1.0)
    print(nombre + ':', 'VALIDA' if ok else 'INVALIDA', errores)

t2 = colocar_zona(t, (0,2), (2,2), BLOQUEADA)
ok, errores = validar_resultado(t2, ini, ref, Resultado('manual', False), lam=1.0)
print('sin ruta real:', 'VALIDA' if ok else 'INVALIDA', errores)