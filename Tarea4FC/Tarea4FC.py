#!/usr/bin/env python3


import numpy as np
import matplotlib.pyplot as plt
import time

#EJERCICIO 1--------------------------------------------------------------------

def build_system(N):
    L = 1.0
    h = L / (N + 1)
    x = np.linspace(h, L - h, N)
    A = np.zeros((N, N), dtype=float)
    b = np.zeros(N, dtype=float)
    for i in range(N):
        A[i, i] = 2.0
        if i > 0: A[i, i-1] = -1.0
        if i < N-1: A[i, i+1] = -1.0
        b[i] = (h**2) * 50.0 * np.sin(np.pi * x[i])
    b[0] += 100.0
    return A, b, x

def lu_factorization_pp(A):
    A = A.astype(float)
    n = A.shape[0]
    U = A.copy()
    L = np.eye(n)
    P = np.eye(n)
    for k in range(n-1):
        pivot = k + np.argmax(np.abs(U[k:, k]))
        if pivot != k:
            U[[k,pivot],:] = U[[pivot,k],:]
            P[[k,pivot],:] = P[[pivot,k],:]
            if k>0:
                L[[k,pivot],:k] = L[[pivot,k],:k]
        for i in range(k+1, n):
            L[i,k] = U[i,k] / U[k,k]
            U[i,k:] -= L[i,k]*U[k,k:]
    return P, L, U

def lu_solve_pp(A, b):
    P,L,U = lu_factorization_pp(A)
    Pb = P @ b
    n = A.shape[0]
    y = np.zeros(n)
    for i in range(n):
        y[i] = Pb[i] - np.dot(L[i,:i], y[:i])
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i,i]
    return x

def analytic_solution(x):
    return 100.0*(1.0-x) + (50.0/(np.pi**2))*np.sin(np.pi*x)

if __name__ == "__main__":
    N = 100  # elige 50,100,500 o haz un loop si quieres
    A,b,x = build_system(N)
    print("||b||_inf =", np.max(np.abs(b)))
    print("b[0:6] =", b[:6])

    t0 = time.time()
    Tnum = lu_solve_pp(A, b)
    t1 = time.time()
    Tref = np.linalg.solve(A, b)
    print("Tiempo LU:", t1-t0)
    print("||Tnum - Tref||_inf =", np.max(np.abs(Tnum - Tref)))

    # Valores en x~0.5: índice interior correspondiente
    x_full = np.linspace(0.0, 1.0, N+2)
    T_full = np.concatenate(([100.0], Tnum, [0.0]))
    Tfull_analytic = analytic_solution(x_full)
    mid_idx = np.argmin(np.abs(x_full - 0.5))
    print(f"x_mid ~ {x_full[mid_idx]:.6f}")
    print("Tnum(mid) =", T_full[mid_idx])
    print("Tanalytic(mid) =", Tfull_analytic[mid_idx])
    print("Tnum - Tanalytic at mid =", T_full[mid_idx] - Tfull_analytic[mid_idx])

    # Estadísticas del residual
    residual = T_full - Tfull_analytic
    print("Residual max abs =", np.max(np.abs(residual)))
    print("Residual L2 norm =", np.linalg.norm(residual))

    # Gráficas
    plt.figure(figsize=(8,4))
    plt.plot(x_full, T_full, '-o', markevery=max(1,(N+2)//12), label="Num (LU)", linewidth=1.4)
    x_dense = np.linspace(0,1,1001)
    plt.plot(x_dense, analytic_solution(x_dense), 'k--', label="Analítica", linewidth=2)
    plt.xlabel("x"); plt.ylabel("T(x)")
    plt.title("Comparación global")
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.show()

    # Zoom en el centro
    plt.figure(figsize=(8,3))
    plt.plot(x_full, T_full, '-o', markevery=max(1,(N+2)//12), label="Num (LU)")
    plt.plot(x_dense, analytic_solution(x_dense), 'k--', label="Analítica", linewidth=2)
    plt.xlim(0.35, 0.65)
    # ajustar límites verticales centrados en el valor medio
    vmid = analytic_solution(0.5)
    plt.ylim(vmid - 7, vmid + 7)
    plt.xlabel("x"); plt.ylabel("T(x)"); plt.title("Zoom centro (ver bump ~5°C)"); plt.legend(); plt.grid(True)
    plt.tight_layout(); plt.show()

    # Residual
    plt.figure(figsize=(8,2.5))
    plt.plot(x_full, residual, '-o', markevery=max(1,(N+2)//12))
    plt.axhline(0, color='k', lw=0.7)
    plt.xlabel("x"); plt.ylabel("Tnum - Tanalytic"); plt.title("Residual"); plt.grid(True); plt.tight_layout(); plt.show()



#EJERCICIO 2--------------------------------------------------------------------------------------

import numpy as np

def rref(A, tol=1e-12):
    """
    Reduce matrix A to RREF (reduced row echelon form) with pivoteo parcial.
    Devuelve la matriz transformada (no modifica A original).
    """
    A = A.copy().astype(float)
    m, n = A.shape
    row = 0
    for col in range(n):
        # encontrar pivote máximo en valor absoluto en columna col, desde row..m-1
        sel = row + np.argmax(np.abs(A[row:, col]))
        if abs(A[sel, col]) < tol:
            continue
        # intercambiar filas
        if sel != row:
            A[[row, sel]] = A[[sel, row]]
        # normalizar fila pivot
        A[row, :] = A[row, :] / A[row, col]
        # eliminar en todas las demás filas
        for r in range(m):
            if r != row:
                A[r, :] = A[r, :] - A[r, col] * A[row, :]
        row += 1
        if row == m:
            break
    return A

def nullspace_basis(A, tol=1e-12):
    """
    Encuentra un vector no trivial en el nullspace (si existe) usando RREF.
    Para matrices m x n, devuelve una base (lista) de vectores de longitud n.
    Aquí si hay grados de libertad, asignamos 1 a una variable libre y resolvemos las dependientes.
    """
    m, n = A.shape
    R = rref(A, tol=tol)
    pivots = []
    pivot_row_for_col = {}
    for i in range(m):
        # encontrar primer 1 en la fila (si existe)
        nz = np.where(np.abs(R[i, :]) > tol)[0]
        if nz.size == 0:
            continue
        first = nz[0]
        if abs(R[i, first] - 1.0) < 1e-8:
            pivots.append(first)
            pivot_row_for_col[first] = i

    free_cols = [j for j in range(n) if j not in pivots]
    basis = []
    if len(free_cols) == 0:
        # espacio nulo trivial {0}
        return np.array(basis)

    # construir un vector por cada variable libre (asignarla a 1)
    for free in free_cols:
        v = np.zeros(n, dtype=float)
        v[free] = 1.0
        # resolver variables dependientes: para cada pivot column j, row = pivot_row_for_col[j]
        for j in pivots:
            row = pivot_row_for_col[j]
            # v[j] = - sum_{k>j} R[row,k] * v[k]  (pero R is RREF)
            # más robusto: v[j] = - sum_{k in free_cols and k!=free} R[row,k]*v[k] - R[row,free]*1
            v[j] = -np.dot(R[row, :], v)
            if abs(v[j]) < 1e-14:
                v[j] = 0.0
        basis.append(v)
    return np.array(basis).T  # columnas = vectores de la base

# Datos del sistema
m1, m2 = 1.0, 2.0
k1, k2, kc = 3.0, 4.0, 1.0
M = np.array([[m1, 0.0], [0.0, m2]])
K = np.array([[k1 + kc, -kc], [-kc, k2 + kc]])

# construir polinomio característico en variable lambda = omega^2:
# det(K - lambda M) = 0
# en 2x2: det = (K11 - lambda M11)(K22 - lambda M22) - (K12 - lambda M12)^2
a = M[0,0]*M[1,1]
b = - (K[0,0]*M[1,1] + K[1,1]*M[0,0])  # coeficiente lambda
c = np.linalg.det(K)
# Raíces lambda = omega^2:
omega2 = np.roots([a, b, c])
print("omega^2 (soluciones del determinante) =", omega2)

# Para cada omega2, hallamos nullspace de (K - omega2 M)
modes = []
for idx, w2 in enumerate(omega2):
    A = K - w2 * M
    ns = nullspace_basis(A)
    if ns.size == 0:
        raise RuntimeError("No se encontró espacio nulo no trivial (revisar precisión numérica).")
    # si ns tiene varias columnas, tomamos la primera base vector
    v = ns[:, 0]
    # normalizar con producto M-ponderado: v^T M v = 1
    norm = np.sqrt(np.abs(v.T @ M @ v))
    if norm == 0:
        raise RuntimeError("Vector nulo en normalización.")
    v = v / norm
    modes.append(v)
    print(f"Modo {idx+1} (normalizado M-ponderado):", v)

Phi = np.column_stack(modes)
print("\nVerificación Φ^T M Φ =\n", Phi.T @ M @ Phi)
print("\nVerificación Φ^T K Φ =\n", Phi.T @ K @ Phi)
print("\nFrecuencias ω (sqrt(omega^2)):", np.sqrt(omega2))

#EJERCICIO 3-----------------------------------------------------------------------------


class TriangularMatrix:
    def __init__(self, n, kind="upper"):
        """
        kind: "upper" o "lower"
        Almacenamiento: por filas del triángulo.
        Para 'upper': para cada fila i (0..n-1) guardamos columnas j=i..n-1
        Para 'lower': para cada fila i (0..n-1) guardamos columnas j=0..i
        """
        if kind not in ("upper", "lower"):
            raise ValueError("kind debe ser 'upper' o 'lower'")
        self.n = int(n)
        self.kind = kind
        self.store = np.zeros(self.n * (self.n + 1) // 2, dtype=float)

    def index(self, i, j):
        """
        Devuelve índice en store para (i,j) o None si (i,j) está fuera del triángulo.
        Fórmulas basadas en almacenamiento por filas.
        """
        n = self.n
        i = int(i); j = int(j)
        if not (0 <= i < n and 0 <= j < n):
            raise IndexError("índices fuera de rango")
        if self.kind == "upper":
            if j < i:
                return None
            # número de elementos almacenados en filas previas: sum_{r=0}^{i-1} (n - r) = i*n - i*(i-1)/2
            start = i * n - (i * (i - 1)) // 2
            return start + (j - i)
        else:  # lower
            if j > i:
                return None
            # número de elementos en filas previas: sum_{r=0}^{i-1} (r+1) = i*(i+1)/2
            start = (i * (i + 1)) // 2 - (i + 1)
            start = (i * (i)) // 2
            return start + j

    def get(self, i, j):
        idx = self.index(i, j)
        return 0.0 if idx is None else self.store[idx]

    def set(self, i, j, val):
        idx = self.index(i, j)
        if idx is None:
            raise ValueError("No se puede escribir fuera de la parte triangular almacenada.")
        self.store[idx] = float(val)

    def toDense(self):
        A = np.zeros((self.n, self.n), dtype=float)
        if self.kind == "upper":
            pos = 0
            for i in range(self.n):
                for j in range(i, self.n):
                    A[i, j] = self.store[pos]
                    pos += 1
        else:
            pos = 0
            for i in range(self.n):
                for j in range(0, i + 1):
                    A[i, j] = self.store[pos]
                    pos += 1
        return A

    def transpose(self):
        """
        Devuelve una nueva TriangularMatrix que es la transpuesta.
        upper <-> lower
        Construcción: leer el denso (pero sin almacenar densamente en self),
        y llenar el nuevo store de la forma opuesta.
        """
        A = self.toDense()
        B = TriangularMatrix(self.n, "lower" if self.kind == "upper" else "upper")
        # rellenar B a partir de A^T (que es A.T)
        for i in range(self.n):
            for j in range(self.n):
                idx = B.index(i, j)
                if idx is not None:
                    B.store[idx] = A.T[i, j]
        return B

    def matvec(self, x):
        """
        Producto A @ x, recorrido optimizado sobre elementos almacenados.
        """
        x = np.asarray(x, dtype=float)
        if x.shape[0] != self.n:
            raise ValueError("Dimensión incompatible para matvec")
        y = np.zeros(self.n, dtype=float)
        if self.kind == "upper":
            pos = 0
            for i in range(self.n):
                # j from i..n-1
                for j in range(i, self.n):
                    a = self.store[pos]
                    y[i] += a * x[j]
                    pos += 1
        else:
            pos = 0
            for i in range(self.n):
                # j from 0..i
                for j in range(0, i + 1):
                    a = self.store[pos]
                    y[i] += a * x[j]
                    pos += 1
        return y

    def __add__(self, other):
        """
        Suma. Si other es TriangularMatrix del mismo kind y tamaño -> devolver TriangularMatrix.
        Si other no es TriangularMatrix (por ejemplo dense numpy array) -> convertir self a denso y sumar -> devolver denso numpy array.
        Complejidad O(n^2).
        """
        if isinstance(other, TriangularMatrix):
            if self.n != other.n:
                raise ValueError("Dimensiones incompatibles en suma")
            if self.kind != other.kind:
                # convertir a densos y sumar (devuelve matriz densa)
                return self.toDense() + other.toDense()
            C = TriangularMatrix(self.n, self.kind)
            C.store = self.store + other.store
            return C
        else:
            # asumimos other es array-like denso
            return self.toDense() + np.asarray(other)

    def scale(self, alpha):
        """Multiplicación por escalar in-place."""
        self.store *= alpha

    def equals(self, other, tol=1e-12):
        """Comparación por igualdad numérica con tolerancia."""
        if isinstance(other, TriangularMatrix):
            return (self.n == other.n) and (self.kind == other.kind) and np.allclose(self.store, other.store, atol=tol, rtol=0)
        else:
            return np.allclose(self.toDense(), np.asarray(other), atol=tol, rtol=0)

#  Pruebas
def _test_triangular():
    print("Pruebas básicas TriangularMatrix...")
    A = TriangularMatrix(4, "upper")
    # poblar A upper con valores simples
    for i in range(4):
        for j in range(i, 4):
            A.set(i, j, i*10 + j)
    print("A (densa):\n", A.toDense())

    B = A.transpose()
    print("A^T (densa):\n", B.toDense())

    x = np.array([1.0, 2.0, 3.0, 4.0])
    y1 = A.matvec(x)
    y2 = A.toDense() @ x
    print("A @ x (optimizado) =", y1)
    print("A @ x (denso)      =", y2)
    assert np.allclose(y1, y2)

    # suma upper+upper
    C = A + A
    assert isinstance(C, TriangularMatrix)
    print("Suma A + A (store):", C.store[:10])

    # transpuesta dos veces regresa original
    A_tt = A.transpose().transpose()
    assert A.equals(A_tt)
    print("Pruebas TriangularMatrix completadas con éxito.")

#EJERCICIO 4 --------------------------------------------------------------------------------------------------

def qr_decomposition_mgs(A, tol=1e-15):
    """
    Gram-Schmidt modificado (MGS).
    Entrada A (m x n), devuelve Q (m x n) con columnas ortonormales y R (n x n) triangular superior.
    """
    A = A.astype(float).copy()
    m, n = A.shape
    Q = np.zeros((m, n), dtype=float)
    R = np.zeros((n, n), dtype=float)
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], v)
            v = v - R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        if R[j, j] < tol:
            # columna casi dependiente: setear q_j a vector cero para mantener forma
            Q[:, j] = 0.0
            R[j, j] = 0.0
        else:
            Q[:, j] = v / R[j, j]
    return Q, R

# Matriz del ejercicio (discreto Laplaciano 3x3)
A0 = np.array([[2.0, -1.0, 0.0],
               [-1.0, 2.0, -1.0],
               [0.0, -1.0, 2.0]], dtype=float)

# Iteración QR sin desplazamiento
Ak = A0.copy()
Q_acc = np.eye(3)
iters = 50
for k in range(iters):
    Qk, Rk = qr_decomposition_mgs(Ak)
    Ak = Rk @ Qk
    Q_acc = Q_acc @ Qk

# Autovalores aproximados (diagonal de Ak) y revisión
eigvals_approx = np.sort(np.real(np.diag(Ak)))
eigvals_ref, eigvecs_ref = np.linalg.eig(A0)
eigvals_ref = np.sort(np.real(eigvals_ref))

print("Autovalores aproximados (diagonal de Ak):", eigvals_approx)
print("Autovalores exactos (numpy.linalg.eig):  ", eigvals_ref)
rel_error = np.abs(eigvals_approx - eigvals_ref) / np.abs(eigvals_ref)
print("Error relativo por autovalor:", rel_error)

# Verificar ortogonalidad de Q_acc
orthogonality = Q_acc.T @ Q_acc
print("Q_acc^T Q_acc (debe ser ≈ I):\n", orthogonality)
print("Desviación de la ortogonalidad (norma Frobenius de Q^TQ - I):", np.linalg.norm(orthogonality - np.eye(3)))






#EJERCICIO 5 ----------------------------------------------------------------------------------------------------


def householder_qr(A):
    """
    Factorización QR mediante reflexiones de Householder.
    Devuelve Q (m x m), R (m x n) tal que A = Q @ R (R con forma m x n, pero la parte útil es n x n).
    """
    A = A.astype(float).copy()
    m, n = A.shape
    Q = np.eye(m, dtype=float)
    R = A.copy()
    for k in range(n):
        x = R[k:, k]
        norm_x = np.linalg.norm(x)
        if norm_x == 0:
            continue
        # construir vector v para reflexión
        e1 = np.zeros_like(x)
        e1[0] = 1.0
        v = x + np.sign(x[0]) * norm_x * e1
        v_norm = np.linalg.norm(v)
        if v_norm == 0:
            continue
        v = v / v_norm
        # construir Hk = I - 2 v v^T en bloque
        Hk = np.eye(m)
        Hk_k = np.eye(len(x)) - 2.0 * np.outer(v, v)
        Hk[k:, k:] = Hk_k
        # aplicar Hk a R y acumular en Q
        R = Hk @ R
        Q = Q @ Hk
    return Q, R

def back_substitution_upper(R, b, tol=1e-14):
    """
    Resuelve Rx = b para R triangular superior (R es n x n).
    """
    n = b.size
    x = np.zeros_like(b, dtype=float)
    for i in range(n-1, -1, -1):
        if abs(R[i, i]) < tol:
            raise np.linalg.LinAlgError("Pivote casi cero en back substitution.")
        x[i] = (b[i] - np.dot(R[i, i+1:], x[i+1:])) / R[i, i]
    return x

# Generar datos simulados
g = 9.81
v0 = 20.0
theta = np.pi / 4.0
# Elegir x en el dominio razonable (alcance máximo A = v0^2 * sin(2 theta) / g)
x_max = (v0**2) * np.sin(2*theta) / g
m_points = 50
x_data = np.linspace(0.0, x_max, m_points)
# Trayectoria "teórica" como en el enunciado 
y_true = v0 * x_data * np.sin(theta) - 0.5 * g * x_data**2 / (v0**2)  # nota: mantuve la forma dada en el enunciado
np.random.seed(0)
y_noisy = y_true + np.random.normal(0.0, 0.5, size=m_points)

# Matriz de diseño para polinomio cuadrático: A m x 3
A_design = np.column_stack([np.ones_like(x_data), x_data, x_data**2])
m, n = A_design.shape

# Householder QR
Q_full, R_full = householder_qr(A_design)
# R_full es m x n; la porción útil para resolver es R11 = R_full[:n, :n]
R11 = R_full[:n, :n]
# calcular Q^T y y resolver
Qt_y = Q_full.T @ y_noisy
y_hat = Qt_y[:n]
beta = back_substitution_upper(R11, y_hat)

print("Coeficientes β estimados (ajuste cuadrático):", beta)

# Graficar datos y ajuste
x_plot = np.linspace(0.0, x_max, 300)
y_fit = beta[0] + beta[1] * x_plot + beta[2] * x_plot**2

plt.figure(figsize=(8,5))
plt.scatter(x_data, y_noisy, label="Datos con ruido", s=20)
plt.plot(x_plot, y_fit, label="Ajuste (Householder QR)", linewidth=2)
plt.plot(x_plot, v0 * x_plot * np.sin(theta) - 0.5 * g * x_plot**2 / (v0**2), '--', label="Trayectoria teórica (sin ruido)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.legend()
plt.title("Ajuste por mínimos cuadrados usando Householder QR")
plt.grid(True)
plt.tight_layout()
plt.show()
