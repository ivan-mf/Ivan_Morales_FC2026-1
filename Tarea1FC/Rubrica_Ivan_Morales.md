# Rúbrica: Ivan_Morales_FC2026-1 - Tarea 1

Referencia: ejercicios 1,2,3,5 del enunciado (Problema 4 descartado). Total = 4.0 puntos (P1, P2, P3, P5).

Resumen de comprobaciones

- Archivo revisado: `Tarea1FC/Tarea1FC.py` (script)
- Evaluación por problema:
  - Problema 1 (Unidad y conversión): 1.0 / 1.0
  - Problema 2 (Primos y factorización): 0.5 / 1.0
  - Problema 3 (nameFile): 0.9 / 1.0
  - Problema 5 (Media y desviación): 0.8 / 1.0

Total: 3.2 / 4.0

Evidencia y comentarios

Problema 1:
- `distancia_m_UA(metros: float)` y `velocidad_ms_UAa(vel_m_s: float)` están definidas y devuelven valores correctos; hay docstrings y ejemplos en el bloque `if __name__ == "__main__":`.

Problema 2:
- Se importa `isprime` desde `MisFunciones` mediante una ruta absoluta: `sys.path.append("/Users/ivanmorales/Desktop/F_Comp")` — esto no es portátil.
- `nprimes` usa `for i in range(1, num+1):` lo que incluye a 1 (no primo).
- `twinprimes` itera `for i in range(1,num-1):` (comienza en 1 y el límite podría ser confuso).
- `descomposition` detecta factores pero no reduce `num` al extraer potencias; además devuelve una lista de strings `['2*2', ...]` en vez de una cadena formateada como indica la docstring.

Problema 3:
- `nameFile(nombre, *args, **kwargs)` construye nombres y reemplaza `.` por `_` en números; acepta `args` y `kwargs` y devuelve `"... .dat"`.
- Pequeña limitación: la función trata cada `arg` como iterable en el bucle de procesamiento, por lo que no maneja correctamente args posicionales simples (p.ej. `nameFile('X', 1.2, 2.3)`).

Problema 5:
- `media(lista)` y `media_y_desv(x)` calculan correctamente media y desviaciones.
- Problema: hay `print(...)` a nivel de módulo (`print(media([2.5,3.5]))` y `print(media_y_desv(...))`) que se ejecutan al importar el módulo.
- Falta validación de tamaño: las fórmulas usan división por `(len(x)-1)` sin comprobar que `len(x) >= 2`.

Recomendaciones (priorizadas)
1. Mover los `print(...)` a un bloque `if __name__ == '__main__':` para evitar salida al importar el módulo (mejora reusabilidad). [P5]
2. Corregir los rangos en `nprimes` y `twinprimes` para empezar en 2 y usar límites claros (p.ej. `range(2, num+1)`); además evitar incluir 1 como primo. [P2]
3. Reescribir `descomposition` para que reduzca `num` conforme extrae factores (usar `num //= p`) y devolver la descomposición en el formato indicado (p.ej. `"2^2 * 3^1"`). [P2]
4. Eliminar `sys.path.append(...)` y documentar la dependencia `MisFunciones`; preferir un try/except en el import que falle con mensaje claro si falta la dependencia. [P2]
5. Añadir validaciones en `media` y `media_y_desv` para lanzar `ValueError` en caso de listas demasiado cortas (`len(x) < 2`). [P5]

Recomendaciones de pruebas y estilo
- Evitar rutas absolutas en el repositorio y usar imports relativos o documentados.

Archivos modificados:
- Ninguno (solo se creó/actualizó esta rúbrica).

