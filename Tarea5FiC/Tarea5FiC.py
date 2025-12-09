#!/usr/bin/env python3

import numpy as np


#EJERCICIO 1-------------------------------------------------------------------

# Método de Newton multidimensional

def newton_multidimensional(F, JF, y0, tol=1e-10, kmax=50):
    """
    Implementa el método de Newton para sistemas no lineales en R^2.

    Parámetros:
        F   : función que recibe y = (x, y) y devuelve un vector F(y)
        JF  : función que devuelve la matriz jacobiana J_F(y)
        y0  : vector inicial
        tol : tolerancia ||F(y)|| < tol
        kmax: máximo número de iteraciones

    Regresa:
        y    : aproximación final
        k    : número de iteraciones realizadas
        resid: residuo final ||F(y)||
    """

    y = np.array(y0, dtype=float)

    for k in range(kmax):
        Fy = F(y)
        resid = np.linalg.norm(Fy)

        if resid < tol:
            return y, k, resid

        JFy = JF(y)

        # Resolver JF(y_k) Δy = -F(y_k)
        delta_y = np.linalg.solve(JFy, -Fy)

        # Actualizar
        y = y + delta_y

    # Si no se alcanzó la tolerancia
    Fy = F(y)
    resid = np.linalg.norm(Fy)
    return y, kmax, resid



# Sistema de prueba


def F_test(y):
    x, yy = y
    return np.array([
        x**2 + yy**2 - 1,
        yy - x
    ], dtype=float)

def JF_test(y):
    x, yy = y
    return np.array([
        [2*x, 2*yy],
        [-1, 1]
    ], dtype=float)


# Ejecución del método

if __name__ == "__main__":
    # Punto inicial sugerido: (1/sqrt(2), 1/sqrt(2))
    y0 = (0.7, 0.7)

    y_star, iterations, resid = newton_multidimensional(F_test, JF_test, y0)


    print("   Método de Newton multidimensional")

    print(f"Solución aproximada (x*, y*): {y_star}")
    print(f"Número de iteraciones: {iterations}")
    print(f"Residuo final ||F(y*)||: {resid:.5e}")

#EJERCICIO 2 ---------------------------------------------------------------
import numpy as np


# MÉTODO DE NEWTON MULTIDIMENSIONAL


def newton_multidimensional(G, JG, z0, tol=1e-12, kmax=20):
    z = z0.copy()
    for k in range(kmax):
        Gz = G(z)
        if np.linalg.norm(Gz) < tol:
            return z
        JGz = JG(z)
        delta = np.linalg.solve(JGz, -Gz)
        z = z + delta
    return z



# EULER IMPLÍCITO PARA SISTEMAS EN R2


def euler_implicito_R2(f, Jf, y0, t0, h, N):
    y = y0.copy()
    t = t0
    ts = [t]
    ys = [y.copy()]

    I = np.eye(2)

    for n in range(N):
        tnew = t + h

        # Definición de G(z) y su jacobiano
        def G(z):
            return z - y - h * f(tnew, z)

        def JG(z):
            return I - h * Jf(tnew, z)

        # Newton
        z0 = y.copy()  # aproximación inicial
        y = newton_multidimensional(G, JG, z0)

        t = tnew
        ts.append(t)
        ys.append(y.copy())

    return np.array(ts), np.array(ys)



# APLICACIÓN AL OSCILADOR ARMÓNICO


def f_osc(t, y):
    x, v = y
    return np.array([v, -x])

def Jf_osc(t, y):
    return np.array([[0, 1],
                     [-1, 0]])

# Parámetros
t0 = 0
y0 = np.array([1.0, 0.0])
h = 0.1
T = 10
N = int((T - t0) / h)

ts, ys = euler_implicito_R2(f_osc, Jf_osc, y0, t0, h, N)

# Soluciones exactas
x_exact = np.cos(ts)
v_exact = -np.sin(ts)

# Errores
err_x = np.abs(ys[:,0] - x_exact)
err_v = np.abs(ys[:,1] - v_exact)

# Mostrar algunos valores
print("t       x_num      x_exac     v_num      v_exact")
for i in range(0, len(ts), 10):
    print(f"{ts[i]:.2f}   {ys[i,0]:.6f}   {x_exact[i]:.6f}   {ys[i,1]:.6f}   {v_exact[i]:.6f}")

print("\nErrores máximos:")
print("max |x - cos t| =", np.max(err_x))
print("max |v + sin t| =", np.max(err_v))

#EJERCICIO 3---------------------------------------------------------------------

import numpy as np


# EULER IMPLÍCITO PARA SISTEMAS EN R4


def euler_implicito_R4(f, Jf, y0, t0, h, N):
    y = y0.copy()
    t = t0
    ts = [t]
    ys = [y.copy()]

    I = np.eye(4)

    for n in range(N):
        tnew = t + h

        def G(z):
            return z - y - h * f(z)

        def JG(z):
            return I - h * Jf(z)

        z0 = y.copy()
        y = newton_multidimensional(G, JG, z0)

        t = tnew
        ts.append(t)
        ys.append(y.copy())

    return np.array(ts), np.array(ys)



# PROBLEMA DE KEPLER


def f_kepler(y):
    x, y_, vx, vy = y
    r = np.sqrt(x*x + y_*y_)
    return np.array([vx,
                     vy,
                     -x/r**3,
                     -y_/r**3])

def Jf_kepler(y):
    x, y_, vx, vy = y
    r = np.sqrt(x*x + y_*y_)

    # Derivadas parciales analíticas
    dVx_dx = -1/r**3 + 3*x*x/r**5
    dVx_dy = 3*x*y_/r**5
    dVy_dx = 3*x*y_/r**5
    dVy_dy = -1/r**3 + 3*y_*y_/r**5

    return np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [dVx_dx, dVx_dy, 0, 0],
        [dVy_dx, dVy_dy, 0, 0]
    ])

# Parámetros
t0 = 0
y0 = np.array([1.0, 0.0, 0.0, 1.0])

h = 0.01
T = 20 * np.pi    # ~10 vueltas
N = int((T - t0) / h)

ts, ys = euler_implicito_R4(f_kepler, Jf_kepler, y0, t0, h, N)


# ENERGÍA Y MOMENTO ANGULAR


def energia(y):
    x, y_, vx, vy = y
    r = np.sqrt(x*x + y_*y_)
    return 0.5*(vx*vx + vy*vy) - 1/r

def Lz(y):
    x, y_, vx, vy = y
    return x*vy - y_*vx

E = np.array([energia(y) for y in ys])
L = np.array([Lz(y) for y in ys])

E0 = E[0]
L0 = L[0]

err_E = np.max(np.abs(E - E0)/np.abs(E0))
err_L = np.max(np.abs(L - L0)/np.abs(L0))

print("Variación relativa máxima de energía:", err_E)
print("Variación relativa máxima de momento angular:", err_L)
