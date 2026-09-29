# Cambios y validación

Autor original: Camilo Acevedo-Correa.

La versión revisada alinea por identificadores de canal, procesa el argumento de la función morfológica, admite imágenes constantes, cuantiza explícitamente a 8 bits para entropía y guarda MSI y características por separado. Se conserva el notebook original sin salidas como referencia histórica.

## Validación

- Cuatro pruebas unitarias aprobadas: alineación y B9 vacía, nueve intervalos con 220 canales sintéticos, entradas constantes y dimensiones incompatibles.
- Notebook validado con nbformat; todas las celdas de código ejecutadas en orden en un proceso Python 3.12, con Matplotlib sin interfaz gráfica.
- MAT local del autor: (145,145,200), uint16.
- SHA-256 del MAT: ec2f8808710919d566f70f0d4aa885aae1ddfd42b734aba71c5e12ca65450939.
- MSI resultante: (145,145,8); características: (145,145,24), todas finitas. Se verificó la lectura del MAT guardado.
- Conteos de canales B1–B9: 2, 6, 8, 5, 4, 10, 20, 18, 0.
- El CSV coincide en sus 220 filas con el documento local de calibración asociado al dataset.
- Versiones registradas en requirements-tested.txt.

## Supuestos y límites

El mapeo estándar de 200 canales elimina 104–108, 150–163 y 220 (desde 1). Su aplicación al MAT local debe confirmarse mediante la procedencia del archivo: el tamaño y nombre no prueban ese historial. El original eliminaba 19 filas y dejaba 201 longitudes de onda. Con el mapeo estándar, B9 no tiene muestras y se omite explícitamente.

No se ejecutó una sesión remota de Colab ni se procesó un cubo real de 220 canales. La prueba de nueve intervalos usa datos sintéticos. EHU devolvió HTTP 403 durante la preparación. No se entrenó un clasificador ni se midió mejora de precisión. La licencia del código queda pendiente de elección del autor.
