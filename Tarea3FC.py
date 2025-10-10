#!/usr/bin/env Python3


#      ---------------------------TAREA 3----------------------------------

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

EPSILON = sys.float_info.epsilon

def biseccion(f, a, b, max_iter=1000, TOL=EPSILON):
    history = []
    try:
        if f(a) * f(b) > 0:
            raise ValueError("No se puede asegurar que la función tenga una raíz en [a,b]")

        if f(a) == 0:
            return a, 0, [a]
        if f(b) == 0:
            return b, 0, [b]

        counter = 0
        while abs(b - a) > TOL and counter < max_iter:
            m = a + 0.5 * (b - a)
            history.append(m)
            if f(a) * f(m) < 0:
                b = m
            else:
                a = m
            counter += 1

        return m, counter, history

    except Exception as e:
        print(f"[Error en Bisección] {e}")
        return None, 0, []


def newton(f, df, x0, max_iter=1000, TOL=EPSILON):
    """
    Newton con criterio relativo escalado usando EPSILON como base.
    Devuelve última aproximación + historial aunque no converja.
    """
    history = []
    x = x0
    try:
        for i in range(max_iter):
            fx = f(x)
            dfx = df(x)
            if dfx == 0:
                raise ZeroDivisionError("Derivada nula: no se puede continuar")

            x_new = x - fx / dfx
            history.append(x_new)

            # criterio relativo escalado (usa EPSILON)
            if abs(x_new - x) < TOL * max(1.0, abs(x_new)):
                return x_new, i + 1, history

            x = x_new

        # no convergió: devolvemos la última aproximación y el número de iteraciones
        print("Warning: Newton-Raphson no llegó a EPSILON; devolviendo última aproximación.")
        return x, max_iter, history

    except Exception as e:
        print(f"[Error en Newton-Raphson] {e}")
        return None, 0, []


def secante(f, x0, x1, max_iter=1000, TOL=EPSILON):
    """
    Secante con criterio relativo escalado.
    Devuelve última aproximación + historial aunque no converja.
    """
    history = []
    try:
        for i in range(max_iter):
            f0, f1 = f(x0), f(x1)
            denom = (f1 - f0)
            if denom == 0:
                raise ZeroDivisionError("Diferencia nula: no se puede continuar")

            x2 = x1 - f1 * (x1 - x0) / denom
            history.append(x2)

            if abs(x2 - x1) < TOL * max(1.0, abs(x2)):
                return x2, i + 1, history

            x0, x1 = x1, x2

        print("Warning: Secante no llegó a EPSILON; devolviendo última aproximación.")
        return x1, max_iter, history

    except Exception as e:
        print(f"[Error en Secante] {e}")
        return None, 0, []


    #         ------------------------------ EJERCICIO 1 -----------------------------
print("\n=== Ejercicio 1 ===")

def f1(omega):
    """f(ω) = cos(ω) cosh(ω) + 1"""
    return math.cos(omega) * math.cosh(omega) + 1.0

print("Inciso 1.a) Bisección para f(ω)=cos(ω)cosh(ω)+1 (TOL=1e-5)")

a_scan = 0.0
b_scan = 0.0
found = False
xs = np.linspace(0.0, 10.0, 10001)
for i in range(len(xs)-1):
    if f1(xs[i]) * f1(xs[i+1]) <= 0 and xs[i+1] > 0:
        a_scan = xs[i]
        b_scan = xs[i+1]
        found = True
        break

if not found:
    print("No se encontró un intervalo de cambio de signo en [0,10].")
    root1, it1, hist1 = None, 0, []
else:
    root1, it1, hist1 = biseccion(f1, a_scan, b_scan, TOL=1e-5)
    print(f"Intervalo inicial seleccionado: [{a_scan:.6g}, {b_scan:.6g}]")
    print(f"Raíz aproximada (menor raíz positiva): {root1:.8f}, Iteraciones: {it1}")

print("Inciso 1.b) Gráfica de f(ω) en [0,4] y marca de intervalo y raíz")
w = np.linspace(0, 4, 1001)
fw = [f1(wi) for wi in w]

plt.figure(figsize=(8,5))
plt.axhline(0, linestyle='--')
plt.plot(w, fw)
if found:
    plt.plot([a_scan, b_scan], [f1(a_scan), f1(b_scan)], marker='o', linestyle='None', markersize=6)
    plt.plot(root1, f1(root1), marker='x', markersize=8)
plt.xlabel("ω")
plt.ylabel("f(ω)")
plt.title("f(ω)=cos(ω)cosh(ω)+1 en ω∈[0,4]")
plt.grid(True, which="both", ls="--")
plt.show()

print("Inciso 1.c) Convergencia (|f(ω_n)|) en escala semilog (bisección)")
if hist1:
    errors1 = [abs(f1(xn)) for xn in hist1]
    plt.figure(figsize=(8,5))
    plt.semilogy(range(1, len(errors1)+1), errors1, marker="o")
    plt.xlabel("Iteración n")
    plt.ylabel("|f(ω_n)| (escala semilog)")
    plt.title("Convergencia del método de bisección para f(ω)")
    plt.grid(True, which="both", ls="--")
    plt.show()
else:
    print("No hay historial de iteraciones para la bisección (hist1 vacío).")


    #    ------------------------------- EJERCICIO 2 --------------------------------
print("\n=== Ejercicio 2 ===")

Ta = 20.0
T0 = 90.0
k = 0.07  # min^-1

def T_of_t(t):
    """Modelo de Newton: T(t) = Ta + (T0 - Ta) e^{-k t}"""
    return Ta + (T0 - Ta) * math.exp(-k * t)

def f2(t):
    """Función cuyo cero buscamos: T(t) - 50"""
    return T_of_t(t) - 50.0

def df2(t):
    """Derivada de f2 respecto a t: -k (T0 - Ta) e^{-k t}"""
    return -k * (T0 - Ta) * math.exp(-k * t)

print("Inciso 2.a) Newton-Raphson para hallar t con T(t)=50 (t0=10)")
t0 = 10.0
root2, it2, hist2 = newton(f2, df2, t0, max_iter=1000, TOL=1e-12)
print(f"t* aproximado: {root2:.8f} (min), Iteraciones: {it2}")

print("Inciso 2.b) Gráfica T(t) en t∈[0,30] y línea T=50 indicando t*")
tt = np.linspace(0, 30, 301)
Tt = [T_of_t(ti) for ti in tt]

plt.figure(figsize=(8,5))
plt.plot(tt, Tt)
plt.axhline(50.0, linestyle='--')
if root2 is not None:
    plt.plot(root2, T_of_t(root2), marker='x', markersize=8)
plt.xlabel("t (min)")
plt.ylabel("T(t) (°C)")
plt.title("Enfriamiento según Newton: T(t) en [0,30]")
plt.grid(True, which="both", ls="--")
plt.show()

print("Inciso 2.c) Convergencia (|f(t_n)|) en escala semilog (Newton-Raphson)")
if hist2:
    errors2 = [abs(f2(xn)) for xn in hist2]
    plt.figure(figsize=(8,5))
    plt.semilogy(range(1, len(errors2)+1), errors2, marker="o")
    plt.xlabel("Iteración n")
    plt.ylabel("|f(t_n)| (escala semilog)")
    plt.title("Convergencia Newton-Raphson para T(t)-50=0 (Newton)")
    plt.grid(True, which="both", ls="--")
    plt.show()
else:
    print("No hay historial de iteraciones para Newton (hist2 vacío).")


# --------------------------- EJERCICIO 3  --------------------------------
print("\n=== Ejercicio 3 ===")

def f3(x):
    """f(x) = e^{x^2} ln(x^2) - x
    Nota: ln(x^2) no está definida en x=0; protegemos el caso x->0.
    """
    if x == 0:
        # valor "muy grande" para evitar usar 0 como punto válido
        return float('inf')
    return math.exp(x**2) * math.log(x**2) - x

print("Inciso 3.a) Método de la secante con x0=0.5, x1=1.5")
x0, x1 = 0.5, 1.5
root3, it3, hist3 = secante(f3, x0, x1, max_iter=1000, TOL=1e-12)
print(f"Raíz aproximada (secante): {root3}, Iteraciones: {it3}")

print("Inciso 3.a) Gráfica f(x) en [-2,2], marcar (x0,x1) y raíz")
xs = np.linspace(-2, 2, 1001)
fxs = []
for xi in xs:
    try:
        val = f3(xi)
        # Si el valor es inf o NaN lo convertimos en nan para que matplotlib no lo plotee
        if not np.isfinite(val):
            fxs.append(np.nan)
        else:
            fxs.append(val)
    except Exception:
        fxs.append(np.nan)

plt.figure(figsize=(8,5))
plt.axhline(0, linestyle='--')
plt.plot(xs, fxs)
plt.plot([x0, x1], [f3(x0), f3(x1)], marker='o', linestyle='None', label="Puntos iniciales")
if root3 is not None and abs(root3) < 1e6:
    plt.plot(root3, f3(root3), marker='x', markersize=8, label="Raíz aproximada")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("f(x)=e^{x^2} ln(x^2) - x en [-2,2]")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

print("Inciso 3.b) Convergencia (|f(x_n)|) en escala semilog (Secante)")
if hist3:
    errors3 = []
    for xn in hist3:
        fxn = f3(xn)
        if not np.isfinite(fxn):
            errors3.append(np.nan)
        else:
            errors3.append(abs(fxn))
    plt.figure(figsize=(8,5))
    plt.semilogy(range(1, len(errors3)+1), errors3, marker="o")
    plt.xlabel("Iteración n")
    plt.ylabel("|f(x_n)| (escala semilog)")
    plt.title("Convergencia del método de la secante para f(x)")
    plt.grid(True, which="both", ls="--")
    plt.show()
else:
    print("No hay historial de iteraciones para la secante (hist3 vacío).")

print("\nFin del script. Los resultados numéricos aparecen impresos arriba y las gráficas fueron mostradas.")


#        --------------------------- EJERCICIO 4 -----------------------------------
def newton_segura_biseccion(f, df, a, b, x0, max_iter=1000, TOL=EPSILON):
    """
    Versión segura de Newton: empieza con [a,b] que encierra raíz, intenta Newton y
    si sale del intervalo hace bisección. Retorna (raíz, iter, historial).
    """
    history = []
    try:
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            raise ValueError("El intervalo [a,b] no encierra una raíz.")
        x = x0
        for i in range(max_iter):
            fx = f(x)
            dfx = df(x)
            if dfx == 0:
                m = a + 0.5 * (b - a)
                x = m
                history.append(x)
            else:
                x_new = x - fx / dfx
                if (x_new < a) or (x_new > b) or not np.isfinite(x_new):
                    m = a + 0.5 * (b - a)
                    x = m
                    history.append(x)
                else:
                    x = x_new
                    history.append(x)
            if f(a) * f(x) < 0:
                b = x
            else:
                a = x
            if len(history) >= 2 and abs(history[-1] - history[-2]) < TOL * max(1.0, abs(history[-1])):
                return history[-1], i + 1, history
        print("Warning: newton_segura_biseccion no llegó a EPSILON; devolviendo última aproximación.")
        return history[-1] if history else None, max_iter, history
    except Exception as e:
        print(f"[Error en newton_segura_biseccion] {e}")
        return None, 0, []

print("\n=== Ejercicio 4 ===")
print("Implementación de versión segura de Newton (newton_segura_biseccion).")

def f4_demo(x):
    return x**3 - 2*x - 5

def df4_demo(x):
    return 3*x**2 - 2

a_demo, b_demo = -10, 10
found_demo = False
xs_demo = np.linspace(a_demo, b_demo, 10001)
for i in range(len(xs_demo)-1):
    if f4_demo(xs_demo[i]) * f4_demo(xs_demo[i+1]) <= 0:
        a_demo, b_demo = xs_demo[i], xs_demo[i+1]
        found_demo = True
        break

if not found_demo:
    print("No se encontró intervalo para el demo de ejercicio 4.")
else:
    x0_demo = (a_demo + b_demo)/2.0
    root4, it4, hist4 = newton_segura_biseccion(f4_demo, df4_demo, a_demo, b_demo, x0_demo, max_iter=200, TOL=1e-12)
    print(f"Demo ejercicio 4: raíz aproximada: {root4}, iteraciones: {it4}")
    if hist4:
        errors4 = [abs(f4_demo(xn)) for xn in hist4]
        plt.figure(figsize=(8,5))
        plt.semilogy(range(1, len(errors4)+1), errors4, marker='o')
        plt.xlabel("Iteración n")
        plt.ylabel("|f(x_n)| (escala semilog)")
        plt.title("Convergencia newton_segura_biseccion (demo)")
        plt.grid(True, which="both", ls="--")
        plt.show()

#                ------------------ Ejercicio 5 ------------------------------------
from scipy.constants import hbar, m_p, m_n, eV

print("\n=== Ejercicio 5 ===")
print("Resolución de la ecuación trascendental k cot(ka) = -β para estados ligados (E<0).")

V0_MeV = 60.0
a_fm = 1.45
a = a_fm * 1e-15

m_reducido = 2.0 * m_p * m_n / (m_p + m_n)

MeV_a_J = 1e6 * eV
J_a_MeV = 1.0 / MeV_a_J

def k_and_beta(Ebind_MeV, V0_MeV_local=V0_MeV):
    """
    Dado Ebind (positivo = |E| en MeV) devuelve (k, beta) en SI.
    """
    Ebind_J = Ebind_MeV * MeV_a_J
    V0_J = V0_MeV_local * MeV_a_J
    if Ebind_J >= V0_J:
        return (np.nan, np.nan)
    k = math.sqrt(m_reducido * (V0_J - Ebind_J)) / hbar
    beta = math.sqrt(m_reducido * Ebind_J) / hbar
    return (k, beta)

def transcendental_g(Ebind_MeV, V0_MeV_local=V0_MeV, a_local=a):
    """
    Evalúa g(E) = k cot(k a) + beta.
    """
    try:
        k, beta = k_and_beta(Ebind_MeV, V0_MeV_local)
        if (not np.isfinite(k)) or (not np.isfinite(beta)):
            return np.nan
        ka = k * a_local
        s = math.sin(ka)
        c = math.cos(ka)
        if abs(s) < 1e-14:
            return np.sign(c) * 1e20
        cotka = c / s
        return k * cotka + beta
    except Exception:
        return np.nan

Egrid = np.linspace(1e-6, V0_MeV - 1e-6, 2000)
gvals = np.array([transcendental_g(E) for E in Egrid])

plt.figure(figsize=(8,5))
plt.plot(Egrid, gvals)
plt.axhline(0, linestyle='--')
plt.xlabel("|E| (MeV)")
plt.ylabel("g(|E|) = k cot(ka) + β")
plt.title("Ecuación trascendental k cot(ka) = -β (V0=60 MeV, a=1.45 fm)")
plt.grid(True, which="both", ls="--")
plt.show()

intervals = []
for i in range(len(Egrid)-1):
    g1, g2 = gvals[i], gvals[i+1]
    if np.isfinite(g1) and np.isfinite(g2) and g1 * g2 < 0:
        intervals.append((Egrid[i], Egrid[i+1]))

print(f"Intervalos detectados donde g cambia de signo (posibles autovalores): {intervals}")

roots_found = []
for (ea, eb) in intervals:
    rootE, itE, histE = biseccion(lambda E: transcendental_g(E, V0_MeV, a), ea, eb, TOL=1e-10, max_iter=200)
    if rootE is not None:
        roots_found.append((rootE, itE, histE))

if roots_found:
    for i, (r, iters, hist) in enumerate(roots_found, start=1):
        print(f"Autovalor {i}: E_bind ≈ {r:.6f} MeV (E = -{r:.6f} MeV), iteraciones bisección: {iters}")
else:
    print("No se encontraron autovalores ligados con la búsqueda en el intervalo.")

if intervals:
    ea, eb = intervals[0]
    if roots_found:
        bisection_root = roots_found[0][0]
    else:
        bisection_root = None

    sec_root, sec_it, sec_hist = secante(lambda E: transcendental_g(E, V0_MeV, a), ea, eb, max_iter=500, TOL=1e-12)
    print(f"Secante: Ebind ≈ {sec_root} MeV, iteraciones: {sec_it}")

    def g_numeric(E):
        return transcendental_g(E, V0_MeV, a)
    def dg_numeric(E, h=1e-6):
        return (g_numeric(E + h) - g_numeric(E - h)) / (2*h)

    x0_newton = 0.5*(ea + eb)
    newt_root, newt_it, newt_hist = newton(lambda E: g_numeric(E), lambda E: dg_numeric(E), x0_newton, max_iter=500, TOL=1e-12)
    print(f"Newton (numérico): Ebind ≈ {newt_root} MeV, iteraciones: {newt_it}")

    if bisection_root is not None:
        if sec_root is not None:
            print(f"Diferencia secante vs bisección: {abs(sec_root - bisection_root):.3e} MeV")
        if newt_root is not None:
            print(f"Diferencia Newton vs bisección: {abs(newt_root - bisection_root):.3e} MeV")

k_crit = math.pi / (2.0 * a)
V0min_J = (hbar**2 * k_crit**2) / m_reducido
V0min_MeV = V0min_J * J_a_MeV
print(f"Valor mínimo teórico de V0 para que exista un estado ligado (approx): {V0min_MeV:.6f} MeV")

