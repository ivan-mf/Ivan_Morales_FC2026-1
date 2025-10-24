# Rúbrica Tarea 2 — Iván Morales

- P1: 0.4/1
  - Problemas: (b) no implementado (bloque comentado e incompleto); (c) modela “gasto extra” como 10% + 20 GB y luego lo recorta a 0.9·RAM, no coincide con el enunciado (2 GB + 10% de 16 GB → 12.4 GB disponibles). (a) sí simula el crecimiento sin acumular.
  - Evidencia: funciones `crecer_sin_acumular` y `crecer_con_gastoextra`; la versión “acumulando” está comentada; definición de `gastoextra`.

- P2: 0.3/1
  - Problemas: Coeficientes del polinomio con signos incorrectos (19.62 y 35.355 deberían ser positivos; −0.981 negativo); el Horner evalúa con esa lista errónea y las raíces (t_max y tiempo de vuelo) se calculan sobre ese polinomio mal parametrizado.
  - Evidencia: `miscoef = [-4.905, -19.62, -35.355, 0.981, 0.0]`; uso de `horner(miscoef, t)` y `np.roots(miscoef)`.

- P3: 1,0/1
  - Observación: Serie con corte por ε y manejo de errores; exige `float` explícitamente y no reduce rango angular; funciona correctamente.

- P4: 1.0/1
  - Sin conflicto relevante (ingenua vs robusta, vector problemático y medición de tiempos reportados).

- P5: 1.0/1
  - Observación: Clase `Intervalo` con `Decimal`; redondeo a enteros con `to_integral_value` (aceptado por criterio); valida a≤b y bloquea división si el divisor contiene 0; métodos nominales (`sumar/restar/...`). Pruebas: 10×0.1 y 1/3.

- P6: 1.0/1
  - Sin conflicto relevante (lineal retorna índice; binaria con `bisect_left`; experimento y gráfica en escala log-log).

Total: 4.7/6
