#!/usr/bin/env Python3 

#EJERCICIO 1:

#a) Conviene usar Unidades astronómicas (1.49x10^11m), pues las distnacias son del orden de solo un orden de magnitud mayor, como se vio en clase, el error entre el valor real y el que reproduce la computadora se minimizará mientras menos órdenes de magnitud se tengan que cruzar. 

#b)

def distancia_m_UA(metros: float) -> float:
    '''
    Convierte una distancia en metros a Unidades Astronómicas (UA).
    
    Args:
    metros (float): distancia en metros
    
    Returns:
    float: distancia en UA
    '''
    UA = metros / 1.496e11
    return UA


def velocidad_ms_UAa(vel_m_s: float) -> float:
    '''
    Convierte una velocidad en m/s a UA/año.
    
    Args:
    vel_m_s (float): velocidad en metros por segundo
    
    Returns:
    float: velocidad en UA por año
    '''
    segundos_por_anio = 365.25 * 24 * 3600
    UA_por_anio = (vel_m_s * segundos_por_anio) / 1.496e11
    return UA_por_anio


if __name__ == "__main__":
    distancia_metros = float(input("Escribe una distancia en metros: "))
    distancia_UA = distancia_m_UA(distancia_metros)
    print("La distancia equivale a", distancia_UA, "UA")

    velocidad_m_s = float(input("Escribe una velocidad en m/s: "))
    velocidad_UA_anio = velocidad_ms_UAa(velocidad_m_s)
    print("La velocidad equivale a", velocidad_UA_anio, "UA/año")

    print("\n--- Cometa Halley ---")
    distancia_halley_m = 5.28e12     # metros
    velocidad_halley_m_s = 9.12e2    # m/s

    distancia_halley_UA = distancia_m_UA(distancia_halley_m)
    velocidad_halley_UA_anio = velocidad_ms_UAa(velocidad_halley_m_s)

    print("Distancia de afelio:", distancia_halley_UA, "UA")
    print("Velocidad en afelio:", velocidad_halley_UA_anio, "UA/año")

#c)

# Como se vio en clase, en la aritmética de punto flotante cada operación introduce un pequeño error, del orden del "epsilon de máquina" (como ~10^-16). Queremos estimar cuánto error podría acumularse en el cálculo del periodo del cometa Halley.

años = 76
segundos_por_año = 365.25 * 24 * 3600   # ≈ 3.156 × 10^7 s
periodo_segundos = años * segundos_por_año
# periodo_segundos ≈ 2.4 × 10^9 s

# Supongamos que el programa avanza en intervalos de Δt = 1 s.
dt = 1
num_pasos = periodo_segundos / dt
# num_pasos ≈ 2.4 × 10^9 pasos

# En cada paso de un integrador sencillo (ej. método de Euler) hay:
# - 2 multiplicaciones
# - 2 sumas/restas
# ≈ 4 operaciones de punto flotante por paso.
ops_por_paso = 4

total_ops = num_pasos * ops_por_paso
# total_ops ≈ 9.6 × 10^9 operaciones

# Si cada operación introduce un error relativo de orden epsilon ≈ 10^-16:
epsilon = 1e-16
error_relativo = total_ops * epsilon
# error_relativo ≈ 10^-6




#EJERCICO 2:

# PRIMOS ANTERIORES
import sys
sys.path.append("/Users/ivanmorales/Desktop/F_Comp")

from MisFunciones import isprime

def nprimes(num: int) -> list:
    try:
        
        PP=[]
        """
        Devuelve la lista de todos los primos anteriores al número num 
        
        Args:
        n (int): Número entero positivo para buscar sus primos anteriores.
        
        Returns:
        list: Lista de primos anteriores.
        
        Raises:
        TypeError: Si la entrada no es un entero.
        ValueError: Si la entrada es menor o igual a cero.
        """
        for i in range(1, num+1):
            if isprime(i):
                PP.append(i)
        return PP
    except TypeError as e: 
        print("Error de tipo", e)

if __name__ == "__main__":
    PrimosPrevios =  nprimes(int(input("Escribe un número entero para encontrar sus primos previos: ")))
    print(PrimosPrevios)
       

# PRIMOS GEMELOS ANTERIORES
def twinprimes(num: int) -> list:
    try: 
        PG=[]
        """
        Devuelve la lista de todas las  tuplas de primos pares anteriores al número num.
        
        Args:
        n (int): Número entero positivo.
        
        Returns:
        list: Lista de todas las  tuplas de primos pares anteriores al número num.
        
        Raises:
        TypeError: Si la entrada no es un entero.
        ValueError: Si la entrada es menor o igual a cero.
        """
        for i in range(1,num-1):
            if isprime(i) == True and isprime(i+2) == True:
                PG.append((i, i+2))
        return PG
    except TypeError as e: 
        print("Error de tipo", e)
if __name__ == "__main__": 
    PrimosGemelos = twinprimes(int(input("Escribe un número entero para encontrar sus primos gemelos previos: ")))
    print(PrimosGemelos)


# DESCOMPOSICIÓN EN FACTORES PRIMOS
def descomposition(num: int) -> str:
    """
    Devuelve la descomposición en factores primos de un entero positivo con sus potencias.
    
    Args:
    n (int): Número entero positivo a descomponer.
    
    Returns:
    str: Cadena con la descomposición en factores primos, por ejemplo "2^2 ∗ 3^1 ∗ 5^1".
    
    Raises:
    TypeError: Si la entrada no es un entero.
    ValueError: Si la entrada es menor o igual a cero.
    """
    factores = []
    i = 2
    while i * i <= num:
        if num % i == 0 and isprime(i):
            k=1
            while num % (i ** k) == 0:
                k += 1
            factores.append((i,k-1))
        i += 1

    f=[]
    for l in factores:
        f.append(str(l[0])+"*"+str(l[1]))

    return f 
if __name__ == "__main__":
    num = int(input("Escribe un número entero positivo para descomponer: "))
    print(descomposition(num))





#EJERCICIO 3:

def nameFile(nombre, *args, **kwargs):
    """
    Genera un nombre de archivo en el formato: "Nombre-Parametro1-Parametro2-...-ParametroN.dat"

    - Los números se convierten a cadenas reemplazando '.' por '_'.
    - Puede recibir una lista de condiciones, argumentos posicionales
      adicionales (*args) y argumentos nombrados (**kwargs).
    """
    lista = [nombre] 
    for i in args:
        lista.append(str(i).replace('.', '_') if isinstance(i, (int, float)) else str(i))

    for k, v in kwargs.items():
        val = str(v).replace('.', '_') if isinstance(v, (int, float)) else str(v)
        lista.append(f"{k}-{val}")

    return "-".join(lista) + ".dat"


#EJERCICIO 5: 
def media(lista: list) -> float:
    suma = 0
    for i in lista:
        suma += i
    med = suma/len(lista)
    return med

print(media([2.5,3.5]))

def media_y_desv(x: list[float]) -> dict[str, float]:
    '''
    Calcula la media y la desviación estándar de una secuencia de números
    usando tanto la fórmula de dos pasos como la de un paso.
    
    Args:
    x (list[float]): Secuencia de valores numéricos.
    
    Returns:
    dict[str, float]: Diccionario con las llaves:
        - "media": valor de la media aritmética.
        - "sigma_dos_pasos": desviación estándar usando la fórmula de dos pasos.
        - "sigma_un_paso": desviación estándar usando la fórmula de un paso.
    
    Raises:
    ValueError: Si la secuencia tiene menos de dos elementos.
    TypeError: Si algún elemento de la secuencia no es numérico.
    '''
    # Media 
    suma = 0
    for i in x:
        suma += i
    med = suma/len(x)

    # Fórmula de dos pasos
    suma_cuadrados: float = 0.0
    for j in x:
        suma_cuadrados += (j - med) ** 2
    sigma_dos_pasos: float = (suma_cuadrados / (len(x) - 1))**0.5

    # Fórmula de un paso
    suma_x2: float = 0.0
    for k in x:
        suma_x2 += k ** 2
    sigma_un_paso: float = ((suma_x2 - len(x) * med ** 2) / (len(x) - 1))**0.5

    return {
        "media": med,
        "sigma_dos_pasos": sigma_dos_pasos,
        "sigma_un_paso": sigma_un_paso,
    }

print(media_y_desv(x=[3.0,3.0,3.0,5.0,6]))




