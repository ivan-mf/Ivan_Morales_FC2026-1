# Rúbrica — Tarea 3 (Iván Morales) — Actualizada 2025-11-19

Total: 96/100 (P1 20/20 + P2 20/20 + P3 20/20 + P4 18/20 + P5 18/20)

Nota: Uso de ε de máquina como criterio principal es conforme al enunciado. Las siguientes son mejoras opcionales (evidencia, presentación, robustez), no correcciones obligatorias.

---

## P1 — Bisección: f(ω) = cos(ω) cosh(ω) + 1

- Evidencia (archivo: `Tarea3FC.py`):
  - Escaneo de signo en [0,10] para ubicar encuadre inicial; aplicación de `biseccion(f1, a,b, TOL=1e-5)`.
  - Gráfica f(ω) en [0,4], marca de intervalo y raíz; traza de semilog(|f(ω_n)|).
- Referencia canónica:
  - Menor raíz positiva: ω* ≈ 1.8751040687; tolerancia objetivo ≈ 1e−5.
- Observaciones:
  - Flujo correcto: exploración → encuadre → bisección → convergencia.
  - Paro por ancho aceptable; residual |f(m)| sería evidencia extra.
  - Línea horizontal de TOL/ε en la semilog agregaría claridad (opcional).
- Calificación: 20/20

Sugerencias opcionales:
 - Línea de referencia: `plt.axhline(1e-5, ls=':', color='gray', label='TOL')`.
 - Paro combinado adicional (|Δω| y |f|) como evidencia.

---

## P2 — Newton (enfriamiento de Newton)

- Evidencia:
  - Modelo T(t) = Ta + (T0−Ta)e^{−kt}; f(t) = T(t)−50; f'(t) implementada.
  - Newton con `TOL=1e-12`, t0=10; gráfica T(t) con línea T=50 y marca de t*; semilog(|f(t_n)|).
- Referencia canónica:
  - t* ≈ 12.10425515 min; convergencia típica ≈ 4 iteraciones, error ~1e−8.
- Observaciones:
  - Implementación sólida y convergencia esperada.
  - Uso de ε conforme; línea de referencia y residual final son opcionales.
- Calificación: 20/20

Sugerencias opcionales:
 - Documentar iteraciones y |f(t_final)|.
 - Línea de referencia (ε o 1e-8) en semilogy.
 - Paro combinado adicional (|Δt| y |f|).

---

## P3 — Secante (e^{x^2} ln(x^2) − x)

- Evidencia:
  - Secante con x0=0.5, x1=1.5; gráfica de f en [−2,2] (excluyendo 0) y semilog(|f|).
- Referencia canónica:
  - Raíz positiva x+ ≈ 1.1624063469; raíz negativa x− ≈ −0.8105015386.
- Observaciones:
  - Raíz positiva correcta y manejo de singularidad.
  - Raíz negativa y análisis de sensibilidad serían añadidos opcionales.
  - Línea TOL y residual final opcionales.
- Calificación: 20/20

Sugerencias opcionales:
 - Buscar raíz negativa (−0.8105...).
 - Semilogy(|f|) con línea de referencia.
 - Paro combinado y reporte de residual.

---

## P4 — Newton seguro (híbrido Newton–Bisección)

- Evidencia:
  - `newton_segura_biseccion(f, df, a, b, x0, ...)` que actualiza el encuadre por cambio de signo; usa paso de Newton dentro de [a,b] y bisección al salir; demo con f(x)=x^3−2x−5.
  - Semilog(|f(x_n)|) de la demo.
- Observaciones:
  - Estructura híbrida correcta; arranque dentro del intervalo.
  - Paro por |Δx| aceptable; residual y ancho final serían evidencia opcional.
  - Segunda función de prueba opcional para robustez.
- Calificación: 18/20

Sugerencias opcionales:
 - Añadir historial (x, |f|) y semilogy.
 - Paro combinado adicional.
 - Segunda función de prueba (x−cos x, por ejemplo).

---

## P5 — Deuterón (pozo esférico)

- Evidencia:
  - Trabajo en SI con conversiones consistentes (ħ, m_p, m_n, eV); define k, β y g(|E|) = k cot(ka) + β en función de |E| (MeV) con conversiones a Joules.
  - Barrido en |E|∈(0,V0) para detectar cambios de signo; bisección con TOL=1e−10 y comparación con secante y Newton (derivada numérica). Reporte de autovalores ligados y diferencias entre métodos.
  - Cálculo de V0_min ≈ (ħ²/2µ)(π/2a)² con unidades SI → MeV.
- Referencia canónica:
  - Con unidades MeV–fm y derivada analítica g′(E), Newton ≈ 6 iter; Bisección ≈ 42; estado fundamental típico E* ≈ −1.3805743 MeV para parámetros de referencia; V0_min ≈ 48.72 MeV.
- Observaciones:
  - Planteamiento físico coherente y detección de autovalores.
  - Migrar a MeV–fm, derivada analítica g′(E), semilog(|g|) y bisección en V0 para V0_min son mejoras opcionales.
- Calificación: 18/20

Sugerencias opcionales:
 - Migrar a MeV–fm (ħc ≈ 197.32698 MeV·fm).
 - Implementar g′(E) analítica y comparar métodos con semilog(|g|).
 - Refinar V0_min por bisección.

---

## Notas generales (opcionales)
 - Líneas de referencia y reporte de iteraciones/residual enriquecen evidencia.
 - Paros combinados (|Δx| y |f|) aportan robustez adicional si se desean.
 - Valores canónicos: ω* ≈ 1.8751041; t* ≈ 12.104255; x+ ≈ 1.1624063; x− ≈ −0.8105015; E* ≈ −1.3805743 MeV; V0_min ≈ 48.72 MeV.
