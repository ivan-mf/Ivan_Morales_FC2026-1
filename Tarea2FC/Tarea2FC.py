#!/usr/bin/env Python3



import numpy as np
import matplotlib.pyplot as plt
import math as math
from math import sqrt
import random
import bisect
import time



#EJERCICIO 1 
print("   Ejercicio 1")
# Capacidad máxima de la memoria RAM: 16 GB = 16*1024^3 bytes
ram_max = 16 * (1024**3)

# Grilla inicial
n0 = 2**2
m0 = 2**3

# Peso inicial de la grilla (cada float ocupa 8 bytes)
peso_inicial = n0 * m0 * 8


# a) Crecimiento sin acumular
def crecer_sin_acumular(peso):
    '''
    Duplica el peso de la grilla en cada paso sin acumular grillas previas.

    Args:
    peso (int): Peso inicial de la grilla en bytes.

    Returns:
    int: Peso en bytes de la última grilla válida antes de exceder ram_max.

    Raises:
    ValueError: Si el peso inicial es menor o igual a 0.
    '''
    if peso <= 0:
        raise ValueError("El peso inicial debe ser mayor que 0.")

    pasos = 0
    peso_actual = peso
    while True:
        peso_nuevo = peso_actual * 2
        if peso_nuevo > ram_max:
            print(f"Número de pasos: {pasos}")
            return peso_actual
        peso_actual = peso_nuevo
        pasos += 1



print(f"la grilla más grande a la que se llegó fue de {crecer_sin_acumular(peso_inicial)} bytes")

## b) Crecimiento acumulando
#def crecer_acumulando(peso):
#    '''
#    Duplica el peso de la grilla en cada paso y suma la grilla anterior.
#
#    Args:
#    peso (int): Peso inicial de la grilla en bytes.
#
#    Returns:
#    int: Peso acumulado en bytes de la última grilla más la grilla anterior.
#
#    Raises:
#    ValueError: Si el peso inicial es menor o igual a 0.
#    '''
#    if peso <= 0:
#        raise ValueError("El peso inicial debe ser mayor que 0.")
#
#    pasos = 0
#    peso1 = peso 
#    peso0 = 0
#    while True:
#        peso2 = peso1 * 2
#        peso_actual = peso2 + peso0
#        if peso_actual > ram_max:
#            if peso_z
#            print(f"Número de pasos: {pasos}")
#            return peso2
#
#
#
#        pasos += 1
#
#print(f"la grilla más grande a la que se llegó fue de {crecer_acumulando(peso_inicial)} bytes")
#

# c) Crecimiento con gasto extra
# gasto extra = 10% de ram_max + 20 GB en bytes
gastoextra = int(0.10 * ram_max) + 20 * (1024**3)

# Corrección: si el gasto extra supera ram_max, se ajusta al máximo permitido
if gastoextra >= ram_max:
    gastoextra = int(0.9 * ram_max)


def crecer_con_gastoextra(peso, gastoextra=gastoextra):
    '''
    Duplica el peso de la grilla en cada paso considerando un gasto fijo del sistema.

    Args:
    peso (int): Peso inicial de la grilla en bytes.
    gastoextra (int): Memoria en bytes ya ocupada por sistema y librerías.

    Returns:
    int: Peso en bytes de la última grilla válida antes de exceder ram_max.

    Raises:
    ValueError: Si el peso inicial es menor o igual a 0.
    '''
    if peso <= 0:
        raise ValueError("El peso inicial debe ser mayor que 0.")

    pasos = 0
    peso_actual = peso
    while True:
        peso_nuevo = peso_actual * 2
        if peso_nuevo + gastoextra > ram_max:
            print(f"Número de pasos: {pasos}")
            return peso_actual
        peso_actual = peso_nuevo
        pasos += 1


print(f"la grilla más grande a la que se llegó fue de {crecer_con_gastoextra(peso_inicial)} bytes\n")





#EJERCICIO 2

print("   Ejercicio 2")

# a) regla de Horner
def horner(coeficientes, x):
    '''
    Evalúa un polinomio usando la regla de Horner.
    
    Args:
    coeficientes (list): Coeficientes del polinomio [a_n, ..., a_1, a_0].
    x (float): Valor en el que se evalúa el polinomio.
    
    Returns:
    float: Resultado de la evaluación del polinomio en "valor".
    
    Raises:
    TypeError: Si los coeficientes no están en una lista o si valor no es numérico.
    '''

    #Primero a_ni luego a_n-1 + a_n * x  luego a_n-2 * x(a_n * x + a_n-1), etc.
    resultado = 0.0
    for a in coeficientes:
        resultado = a + resultado * x
    return resultado
print("a) función horner ya fue implementada")

# Polinomio dado: y(t) = 4.905 t^4 + 19.62 t^3 + 35.355 t^2 - 0.981 t
miscoef = [-4.905, -19.62, -35.355, 0.981, 0.0]

# b) Calcular la altura en tiempos específicos
ts = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
alturas = [horner(miscoef, i) for i in ts]
print("b) Altura en tiempos específicos:")
for t, y in zip(ts, alturas):
    print(f" t = {t:.1f} s -> y = {y:.4f} m")

# c) Encontrar el tiempo de altura máxima sabemos que 
a4, a3, a2, a1, a0 = miscoef
derivadas = [4*a4, 3*a3, 2*a2, a1]
raices = np.roots(derivadas)
raices_reales = [r.real for r in raices if abs(r.imag) < 1e-8 and r.real >= 0]

tiempo_max = max(raices_reales, key=lambda r: horner(miscoef, r))
altura_max = horner(miscoef, tiempo_max)

print(f"\nc) Tiempo en que alcanza la altura máxima: t = {tiempo_max:.4f} s")
print(f"Altura máxima alcanzada: y = {altura_max:.4f} m")

# d) Tiempo de vuelo total
raices_y = np.roots(miscoef)
raices_reales_y = [r.real for r in raices_y if abs(r.imag) < 1e-8 and r.real > 1e-8]
tiempo_vuelo = max(raices_reales_y)

print(f"\n Tiempo total de vuelo: {tiempo_vuelo:.4f} s")

# e) Gráfica de la trayectoria
velocidad_inicial = 50.0
vx = velocidad_inicial / sqrt(2)

t_graf = np.linspace(0, tiempo_vuelo, 400)
x_graf = vx * t_graf
y_graf = [horner(miscoef, t) for t in t_graf]

plt.figure(figsize=(8,5))
plt.plot(x_graf, y_graf, label="Trayectoria")
plt.scatter([vx*tiempo_max], [altura_max], color="red", label="Altura máxima")
plt.title("Trayectoria del proyectil")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.legend()
plt.grid(True)
plt.show()
print("e) Trayectoria graficada\n")


#Ejercicio 3
print(".  Ejercicio 3")

# Agregar la ruta al archivo MisFunciones.py, aunque aún tnego dudas de mejores formas de hacerlo. 
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#from MisFunciones import epsilon_maquina
def epsilon_maquina():
    """
    Calcula el épsilon usando el método básico de división sucesiva.

    Returns:
        float: El valor del épsilon de máquina
    """
    epsilon = 1.0
    while True:
        epsilon = 0.5 * epsilon
        if 1.0 + epsilon == 1.0:
            break
    return 2.0 * epsilon


def sin_taylor(x: float, tol: float = None) -> float:
    """
    Calcula sin(x) usando la serie de Taylor.

    Args:
        x (float): Valor para calcular sin(x).
        tol (float, opcional): Tolerancia. Por defecto usa épsilon de máquina.

    Returns:
        float: Aproximación de sin(x).

    Raises:
        TypeError: Si x o tol no son numéricos.
        ValueError: Si la tolerancia es no positiva.
    """
    try:
        if not isinstance(x, float):
            raise TypeError(f"x debe ser float, se recibió: {type(x).__name__}")
        if tol is not None and not isinstance(tol, float):
            raise TypeError(f"tol debe ser float o None, se recibió: {type(tol).__name__}")

        if tol is None:
            tol = epsilon_maquina()
        elif tol <= 0:
            raise ValueError(f"tol debe ser positiva, se recibió: {tol}")

        resultado = 0.0
        termino = x
        n = 1
        signo = 1

        while abs(termino) > tol:
            resultado += termino
            n += 2
            signo *= -1
            termino = signo * (x**n) / math.factorial(n)

        return resultado

    except (TypeError, ValueError) as e:
        print("Error en sin_taylor:", e)
        return None
    finally:
        print(f"Se intentó calcular sin({x}) con tolerancia {tol}.")


def cos_taylor(x: float, tol: float = None) -> float:
    """
    Calcula cos(x) usando la serie de Taylor.

    Args:
        x (float): Valor para calcular cos(x).
        tol (float, opcional): Tolerancia. Por defecto usa épsilon de máquina.

    Returns:
        float: Aproximación de cos(x).

    Raises:
        TypeError: Si x o tol no son numéricos.
        ValueError: Si la tolerancia es no positiva.
    """
    try:
        if not isinstance(x, float):
            raise TypeError(f"x debe ser float, se recibió: {type(x).__name__}")
        if tol is not None and not isinstance(tol, float):
            raise TypeError(f"tol debe ser float o None, se recibió: {type(tol).__name__}")

        if tol is None:
            tol = epsilon_maquina()
        elif tol <= 0:
            raise ValueError(f"tol debe ser positiva, se recibió: {tol}")

        resultado = 0.0
        termino = 1.0
        n = 0
        signo = 1

        while abs(termino) > tol:
            resultado += termino
            n += 2
            signo *= -1
            termino = signo * (x**n) / math.factorial(n)

        return resultado

    except (TypeError, ValueError) as e:
        print("Error en cos_taylor:", e)
        return None
    finally:
        print(f"Se intentó calcular cos({x}) con tolerancia {tol}.")


def tan_taylor(x: float, tol: float = None) -> float:
    """
    Calcula tan(x) como sin(x)/cos(x).

    Args:
        x (float): Valor para calcular tan(x).
        tol (float, opcional): Tolerancia. Por defecto usa épsilon de máquina.

    Returns:
        float: Aproximación de tan(x).

    Raises:
        TypeError: Si x o tol no son numéricos.
        ValueError: Si la tolerancia es no positiva.
        ZeroDivisionError: Si cos(x) ≈ 0.
    """
    try:
        if not isinstance(x, float):
            raise TypeError(f"x debe ser float, se recibió: {type(x).__name__}")
        if tol is not None and not isinstance(tol, float):
            raise TypeError(f"tol debe ser float o None, se recibió: {type(tol).__name__}")

        if tol is None:
            tol = epsilon_maquina()
        elif tol <= 0:
            raise ValueError(f"tol debe ser positiva, se recibió: {tol}")

        cos_x = cos_taylor(x, tol)
        if abs(cos_x) < tol:
            raise ZeroDivisionError("Tangente indefinida, cos(x) ≈ 0.")

        return sin_taylor(x, tol) / cos_x

    except (TypeError, ValueError, ZeroDivisionError) as e:
        print("Error en tan_taylor:", e)
        return None
    finally:
        print(f"Se intentó calcular tan({x}) con tolerancia {tol}.")


def log_taylor(x: float, tol: float = None) -> float:
    """
    Calcula ln(x) usando la serie de Taylor alrededor de 1.

    Usa la expansión: ln(x) = 2 * [ (y + y^3/3 + y^5/5 + ... ) ] con y = (x-1)/(x+1).

    Args:
        x (float): Valor positivo para calcular ln(x).
        tol (float, opcional): Tolerancia. Por defecto usa épsilon de máquina.

    Returns:
        float: Aproximación de ln(x).

    Raises:
        TypeError: Si x o tol no son numéricos.
        ValueError: Si x <= 0 o tol no es positiva.
    """
    try:
        if not isinstance(x, float):
            raise TypeError(f"x debe ser float, se recibió: {type(x).__name__}")
        if tol is not None and not isinstance(tol, float):
            raise TypeError(f"tol debe ser float o None, se recibió: {type(tol).__name__}")

        if tol is None:
            tol = epsilon_maquina()
        elif tol <= 0:
            raise ValueError(f"tol debe ser positiva, se recibió: {tol}")
        if x <= 0:
            raise ValueError("El argumento de log debe ser positivo.")

        y = (x - 1) / (x + 1)
        termino = y
        resultado = 0.0
        n = 1

        while abs(termino) > tol:
            resultado += termino / n
            n += 2
            termino = (y**n)

        return 2 * resultado

    except (TypeError, ValueError) as e:
        print("Error en log_taylor:", e)
        return None
    finally:
        print(f"Se intentó calcular ln({x}) con tolerancia {tol}.")


if __name__ == "__main__":
    print("\nPruebas de funciones con series de Taylor:\n")

    print("sin_taylor(pi/6) ≈", sin_taylor(float(math.pi/6)))
    print("cos_taylor(pi/6) ≈", cos_taylor(float(math.pi/6)))
    print("tan_taylor(pi/6) ≈", tan_taylor(float(math.pi/6)))
    print("log_taylor(e) ≈", log_taylor(float(math.e)))
print("\n")
#EJERCICIO 4: 

print("   EJERCICIO4:")


def norma_sencilla(x: np.ndarray) -> float:
    """
    Implementación sencilla de la norma euclidiana.
    Puede producir overflow o underflow para vectores extremos.
    """
    return np.sqrt(np.sum(x**2))

def norma_robusta(x: np.ndarray) -> float:
    """
    Implementación robusta de la norma euclidiana.
    Reescala por el valor absoluto máximo del vector
    para evitar overflow o underflow.
    """
    if len(x) == 0:
        return 0.0
    val_max = np.max(np.abs(x))
    if val_max == 0.0:
        return 0.0
    reescalado = x / val_max
    return val_max * np.sqrt(np.sum(reescalado**2))

if __name__ == "__main__":
    # Vector extremo para probar diferencia entre sencilla y robusta
    v = np.array([1e200, 1e-200, 3.0, -4.0, 1e199])

    val_sencillo = norma_sencilla(v)
    val_robusto = norma_robusta(v)

    print("Resultado sencilla:", val_sencillo)
    print("Resultado robusta:", val_robusto)

    print("\na) ¿Puede construir un vector que produzca resultados distintos?")
    if np.isinf(val_sencillo) and not np.isinf(val_robusto):
        print("Sí. Con el vector [1e200, 1e-200, 3, -4, 1e199],")
        print("la rutina sencilla produce 'inf' por overflow,")
        print("mientras que la robusta devuelve un valor finito:", val_robusto)
    else:
        print("En este caso no hubo diferencia significativa.")

    # Comparación de tiempos para vectores grandes
    N = 10**6
    w = np.random.randn(N) * 1e100

    t0 = time.time()
    for _ in range(100):
        norma_sencilla(w)
    t_sencilla = time.time() - t0

    t0 = time.time()
    for _ in range(100):
        norma_robusta(w)
    t_robusta = time.time() - t0

    print("\nTiempo sencilla:", f"{t_sencilla:.4f} s")
    print("Tiempo robusta:", f"{t_robusta:.4f} s")

    print("\nb) ¿Cuánto rendimiento sacrifica la rutina robusta?")
    perdida = (t_robusta - t_sencilla) / t_sencilla * 100
    print(f"La rutina robusta es aproximadamente {perdida:.2f}% más lenta,")
    print("pero a cambio evita problemas de overflow y underflow.\n")


#EJERCICIO 5:

print("   EJERCICIO 5:")

from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING

# Configuramos precisión suficiente
getcontext().prec = 50  

class Intervalo:
    '''
    Representa un intervalo cerrado [a, b] usando aritmética de intervalos.
    '''
    def __init__(x, a, b):
        '''
        Inicializa un intervalo [a, b].

        Args:
        a (float | str | int): Extremo izquierdo del intervalo.
        b (float | str | int): Extremo derecho del intervalo.

        Returns:
        Intervalo: Un nuevo objeto de tipo Intervalo.

        Raises:
        ValueError: Si a > b.
        '''
        if a > b:
            raise ValueError("El extremo izquierdo debe ser menor o igual al derecho")
        x.a = Decimal(a)
        x.b = Decimal(b)

    def __repr__(x):
        '''
        Representación en cadena del intervalo.

        Returns:
        str: Intervalo en formato "[a, b]".
        '''
        return f"[{x.a}, {x.b}]"

    def sumar(x, otro):
        '''
        Suma dos intervalos.

        Args:
        otro (Intervalo): Otro intervalo a sumar.

        Returns:
        Intervalo: Intervalo resultado de la suma.

        Raises:
        TypeError: Si el argumento no es un Intervalo.
        '''
        if not isinstance(otro, Intervalo):
            raise TypeError("El argumento debe ser de tipo Intervalo")
        izq = (x.a + otro.a).to_integral_value(rounding=ROUND_FLOOR)
        der = (x.b + otro.b).to_integral_value(rounding=ROUND_CEILING)
        return Intervalo(izq, der)

    def restar(x, otro):
        '''
        Resta dos intervalos.

        Args:
        otro (Intervalo): Intervalo a restar.

        Returns:
        Intervalo: Intervalo resultado de la resta.

        Raises:
        TypeError: Si el argumento no es un Intervalo.
        '''
        if not isinstance(otro, Intervalo):
            raise TypeError("El argumento debe ser de tipo Intervalo")
        izq = (x.a - otro.b).to_integral_value(rounding=ROUND_FLOOR)
        der = (x.b - otro.a).to_integral_value(rounding=ROUND_CEILING)
        return Intervalo(izq, der)

    def multiplicar(x, otro):
        '''
        Multiplica dos intervalos.

        Args:
        otro (Intervalo): Intervalo a multiplicar.

        Returns:
        Intervalo: Intervalo resultado de la multiplicación.

        Raises:
        TypeError: Si el argumento no es un Intervalo.
        '''
        if not isinstance(otro, Intervalo):
            raise TypeError("El argumento debe ser de tipo Intervalo")
        productos = [
            x.a * otro.a,
            x.a * otro.b,
            x.b * otro.a,
            x.b * otro.b
        ]
        izq = min(productos).to_integral_value(rounding=ROUND_FLOOR)
        der = max(productos).to_integral_value(rounding=ROUND_CEILING)
        return Intervalo(izq, der)

    def dividir(x, otro):
        '''
        Divide dos intervalos.

        Args:
        otro (Intervalo): Intervalo divisor.

        Returns:
        Intervalo: Intervalo resultado de la división.

        Raises:
        TypeError: Si el argumento no es un Intervalo.
        ZeroDivisionError: Si el divisor contiene al 0.
        '''
        if not isinstance(otro, Intervalo):
            raise TypeError("El argumento debe ser de tipo Intervalo")
        if otro.a <= 0 <= otro.b:
            raise ZeroDivisionError("El intervalo divisor contiene al 0")
        cocientes = [
            x.a / otro.a,
            x.a / otro.b,
            x.b / otro.a,
            x.b / otro.b
        ]
        izq = min(cocientes).to_integral_value(rounding=ROUND_FLOOR)
        der = max(cocientes).to_integral_value(rounding=ROUND_CEILING)
        return Intervalo(izq, der)


print("Inciso (a) y (b): Clase Intervalo implementada con suma, resta, multiplicación y división.")

print("\nInciso (d): Pruebas con errores de redondeo")

# Sumar 10 veces el número 0.1
x = Intervalo("0.1", "0.1")
suma = Intervalo("0", "0")
for _ in range(10):
    suma = suma.sumar(x)
print("Suma de 10 veces 0.1 =", suma)

# Cociente 1/3
uno = Intervalo("1", "1")
tres = Intervalo("3", "3")
cociente = uno.dividir(tres)
print("Cociente 1/3 =", cociente)
print("\n")



#EJERCICIO 6

def busqueda_lineal(lista, x):
    """Recorre la lista elemento por elemento"""
    for i in range(len(lista)):
        if lista[i] == x:
            return i
    return -1

def busqueda_binaria(lista, x):
    """Usa bisect para implementar búsqueda binaria"""
    i = bisect.bisect_left(lista, x)
    if i != len(lista) and lista[i] == x:
        return i
    return -1

print("Inciso (a): Búsqueda lineal")
print("1) En el peor caso, la búsqueda lineal recorre todos los elementos, es decir, realiza n comparaciones.")
print("2) Complejidad:")
print("   - O(n): cota superior, pues nunca realiza más de n comparaciones")
print("   - Ω(1): cota inferior, si encuentra el número en la primera posición")
print("   - Θ(n): cota ajustada, porque en promedio y en el peor caso recorre n elementos")

print("\nInciso (b): Búsqueda binaria")
print("1) En el peor caso, divide la lista a la mitad en cada paso, realizando log₂(n) comparaciones.")
print("2) Complejidad:")
print("   - O(log n): cota superior")
print("   - Ω(1): cota inferior, si encuentra el número en el primer intento")
print("   - Θ(log n): cota ajustada")

print("\nInciso (c)")

tamaños = [10**3, 10**4, 10**5, 10**6]
ts_lineal = []
ts_binaria = []

for n in tamaños:
    lista = list(range(n))  
    x = -1  
    
    t0 = time.time()
    busqueda_lineal(lista, x)
    tf = time.time()
    ts_lineal.append(tf - t0)
    
    t0 = time.time()
    busqueda_binaria(lista, x)
    tf = time.time()
    ts_binaria.append(tf - t0)

plt.plot(tamaños, ts_lineal, marker='o', label="Búsqueda lineal")
plt.plot(tamaños, ts_binaria, marker='o', label="Búsqueda binaria")
plt.xlabel("Tamaño de la lista (n)")
plt.ylabel("Tiempo (s)")
plt.title("Comparación de tiempos de búsqueda")
plt.legend()
plt.xscale("log")  
plt.yscale("log")
plt.grid(True)
plt.show()

print("\nInciso (d)")
print("1) Sí, los tiempos medidos coinciden con las complejidades teóricas: ")
print("   - La búsqueda lineal crece proporcional a n.")
print("   - La búsqueda binaria crece proporcional a log n, mucho más lentamente.")
print("2) La búsqueda binaria muestra un crecimiento mucho más lento porque reduce el espacio de búsqueda a la mitad en cada paso,")
print("   mientras que la búsqueda lineal revisa todos los elementos en el peor caso.")