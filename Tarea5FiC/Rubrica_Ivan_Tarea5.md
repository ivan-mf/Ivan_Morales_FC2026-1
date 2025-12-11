# Rúbrica — Iván Morales — Tarea 5

Evaluación según `Rubrica_Tarea5.md`.

## 1) Newton multidimensional (R²) — 27/30
- Implementas Newton genérico con jacobiano analítico, tolerancia y `np.linalg.solve`; pruebas en el sistema de círculo–recta con `y0=(0.7,0.7)` y reportas residuo e iteraciones.
- Falta manejo de jacobiano singular o aviso de fallo, y no guardas trazas de iteraciones/residuos más allá del print final.

## 2) Euler implícito (oscilador) — 26/30
- Reusas Newton para G=z−y−h f(t+h,z), J_G=I−h Jf(t+h,z) con I 2×2; integra hasta T=10 con h=0.1.
- Comparas contra la solución exacta y reportas errores máximos de x y v; faltan gráficas y control de no convergencia de Newton (tol 1e-12, kmax=20 sin devolución de estado).

## 3) Kepler (E y L_z) — 18/40
- Planteas Euler implícito en R4 con G=z−y−h f(z), J_G=I−h Jf(z) y calculas E y L en cada paso (h=0.01, ~10 vueltas).
- El código no corre: `f_kepler` tiene un typo en la definición (`def f_kepler(y):i`) y no se importa `matplotlib.pyplot` antes de graficar, por lo que las gráficas y métricas no se generan. Además repites la integración dos veces y no reportas variaciones si el código falla.
- Necesario: corregir la firma de `f_kepler`, importar `matplotlib.pyplot as plt`, y ejecutar para obtener variación relativa máxima de E y L y las gráficas de órbita/E/L.

## Calificación final
- Total: **71/100**.

## Sugerencias
- Newton: añade detección de jacobiano singular y devuelve iteraciones/residuo para monitoreo. 
- Oscilador: registra iteraciones de Newton por paso y añade una gráfica x–v o x(t)/v(t) para evidenciar estabilidad.
- Kepler: corrige el typo y las importaciones, elimina la ejecución duplicada, y muestra los valores numéricos de variación relativa de E y L junto con las gráficas solicitadas.
