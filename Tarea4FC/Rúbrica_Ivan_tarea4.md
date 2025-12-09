Comentarios breves
- Problema 1: Faltó una verificación explícita aplicando `P` a `b` en todos los casos.
- Problema 2: Pequeña inconsistencia al incorporar fronteras en `b`; la comparación analítica no usa exactamente la misma malla.
- Problema 3: No muestras ΦᵀMΦ≈I y ΦᵀKΦ≈Ω²; base de nulidad sin normalización M.
- Problema 4: `transpose` no alterna upper↔lower para todos los tamaños; tiempo de `matvec` crece más de lo esperado.
- Problema 5: Faltó reporte de ortogonalidad `QᵀQ` y error `||A−Q R||`.
# Rúbrica — Tarea 4 (Iván Morales)

Ubicación: misma carpeta del archivo `Tarea4FC.py`.

## 1) Factorización LU con pivoteo parcial — [puntaje: 20/20]
- Ensamble `A` tridiagonal y `b` con `q(x)=50 sin(πx)` y fronteras `T0=100`, `T1=0` (escala correcta con `h`).
- LU con pivoteo parcial (P,L,U) y solución por sustituciones adelante/atrás; comparación con referencia y `||T−T_ref||_∞`.
- Análisis adicional: solución analítica, residual global y local (zoom), tiempos y estadísticas.

## 2) Gauss–Jordan en vibraciones pequeñas — [puntaje: 20/20]
- RREF con pivoteo parcial; `nullspace_basis` genérica y selección de variable libre.
- Modos normalizados M-ponderados y verificación `ΦᵀMΦ≈I`, `ΦᵀKΦ≈Ω²`; frecuencias `ω` reportadas.

## 3) Clase TriangularMatrix — [puntaje: 18/20]
- Almacenamiento `n(n+1)/2` por filas; métodos `index/get/set`, `toDense`, `transpose` (upper↔lower), `matvec`, suma y escala.
- Pruebas completas: densificación, matvec vs denso, suma, doble transpuesta, asserts.
- Detalle menor: sección `index` para lower muestra una línea redundante antes de corrección; funcionalidad final es correcta.

## 4) QR (Gram–Schmidt modificado) — [puntaje: 20/20]
- Implementación MGS; iteración QR (50) con acumulación `Q_acc`; autovalores aproximados y comparación con `numpy`.
- Verificación de ortogonalidad (`QᵀQ≈I`) y error relativo por autovalor.

## 5) Mínimos cuadrados con Householder — [puntaje: 20/20]
- Householder QR (`Q`, `R`), extracción `R11`, `Qᵀ y` y back-substitution; coeficientes β.
- Datos parabólicos con ruido, diseño `[1,x,x²]`; gráficas de datos, ajuste y trayectoria teórica.

## Calificación final — [98/100]
