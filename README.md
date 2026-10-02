# Indian Pines: de HSI a MSI y características espaciales

**Camilo Acevedo-Correa**

Tutorial en Python para reducir un cubo hiperespectral mediante promedios por intervalos de longitud de onda y extraer características de entropía local y morfología matemática.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/camiloace/indian-pines-hsi-to-msi/blob/main/preprocessing_indian_pines.ipynb)

## Qué produce

| Entrada | Bandas agregadas | MSI + entropía + morfología |
|---|---:|---:|
| Indian Pines corregido, 145×145×200, con mapeo estándar | 8 | 24 |
| Cubo completo de 220 canales, con su calibración alineada | 9 | 27 |

**Por qué cambia el resultado original:** el notebook inicial conservaba 201 longitudes de onda para 200 bandas. Además, B9 (1360–1390 nm) depende de los canales originales 104, 105 y 106, eliminados en la convención estándar de 200 bandas. La versión revisada omite explícitamente ese intervalo o genera un error si se exige cubrirlo. No rellena una banda inexistente. El flujo de 220 canales permite nueve intervalos, pero la región de absorción puede tener baja calidad.

El mapeo de 200 canales se considera un **supuesto que debe comprobarse contra la procedencia del archivo**: se excluyen 104–108, 150–163 y 220, numerados desde 1. Si su copia fue modificada, proporcione su lista de canales originales. El tamaño del cubo no basta para verificar el mapeo.

## Uso en Google Colab

1. Abrir el enlace de Colab.
2. Ejecutar la celda de preparación: clona este repositorio e instala las dependencias.
3. Cargar `Indian_pines_corrected.mat` cuando el notebook lo solicite.
4. Revisar el mapeo y ejecutar las celdas restantes en orden.
5. Descargar los resultados desde `indian-pines-hsi-to-msi/results/` en el panel de archivos.

No es necesario montar Google Drive. Para otra variante del dataset, modificar `MAT_PATH`, `MAT_KEY` y `channel_ids`.

## Uso local

Se recomienda Python 3.12. Desde una terminal:

```bash
git clone https://github.com/camiloace/indian-pines-hsi-to-msi.git
cd indian-pines-hsi-to-msi
python -m venv .venv
```

Activar el entorno en Windows PowerShell con `.venv\Scripts\Activate.ps1`, o en Linux/macOS con `source .venv/bin/activate`. Después:

```bash
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyterlab
```

Colocar el MAT en `data/` y abrir `preprocessing_indian_pines.ipynb` desde la raíz del repositorio. Las versiones exactas usadas en la verificación se registran en `requirements-tested.txt`.

## Archivos

- `preprocessing_indian_pines.ipynb`: tutorial revisado.
- `hsi_processing.py`: funciones de selección y procesamiento.
- `notebook-original-sin-salidas.ipynb`: código original como referencia histórica; conserva sus errores y requiere dependencias adicionales como `spectral`. Usar el tutorial revisado para ejecutar el flujo.
- `data/wavelenght.csv`: tabla original de 220 canales; se conserva el nombre de archivo del autor.
- `tests/test_processing.py`: pruebas de alineación, intervalos vacíos y entradas constantes.
- `REVISION.md`: registro de cambios y límites de la verificación.

## Método

Se promedian uniformemente los canales incluidos en cada intervalo del notebook original (nm): 433–453, 450–515, 525–600, 630–680, 845–885, 1560–1660, 2100–2300, 500–680 y 1360–1390. Algunos intervalos se superponen.

La entropía se calcula sobre intensidades normalizadas globalmente y cuantizadas a 8 bits, con disco de radio 4. Cada mapa se escala por su máximo. La morfología procesa cada banda con dos erosiones, apertura, dos dilataciones y cierre/apertura por área; usa una huella de 5×5 y umbral de 1000 píxeles.

El promedio por intervalo **aproxima** una MSI: no simula la respuesta espectral completa ni las resoluciones espaciales de Landsat 8. La salida final contiene características, no nuevas bandas espectrales físicas. No se demuestra una mejora de clasificación; para evaluarla se requiere un experimento separado. Evitar que los vecindarios espaciales de entrenamiento y prueba se solapen y ajustar cualquier escalado usando solo entrenamiento.

## Resultados

El notebook escribe `results/IP_MSI_8.mat` y `results/IP_FEATURES_24.mat` para la configuración estándar de 200 canales, o los equivalentes de 9 y 27 canales para 220. También guarda `processing_metadata.json` y `preview.png`. El JSON documenta índices, longitudes de onda y parámetros. Repetir una ejecución reemplaza los resultados de esa configuración.

## Datos, atribución y licencia

El cubo MAT no se redistribuye aquí. Obtenerlo de la [colección de escenas de EHU](https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes#Indian_Pines). Durante la preparación, esa página devolvió HTTP 403; se utilizó la copia local del autor para las pruebas.

La publicación original de [Baumgardner, Biehl y Landgrebe (2015), Purdue PURR](https://doi.org/10.4231/R7RX991C) incluye la calibración de 220 canales y está marcada CC0. El CSV fue comparado, fila por fila, con el documento de calibración asociado a la copia local. Esto verifica los valores de calibración, pero no demuestra el historial de procesamiento del MAT.

La licencia del código está pendiente de elección por el autor; todavía no se ha añadido una licencia MIT. Las referencias conservan sus propias condiciones de uso.

## Referencias

1. [Landsat 8 — NASA](https://science.nasa.gov/mission/landsat-8/).
2. [Hyperspectral Remote Sensing Scenes — EHU](https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes#Indian_Pines).
3. [Image Processing with Python: Working with Entropy](https://towardsdatascience.com/image-processing-with-python-working-with-entropy-b05e9c84fc36).
4. [Morphological Operations — j-manansala](https://github.com/j-manansala/morphological/blob/main/Morphological%20Operations.ipynb).
5. [Dataset y calibración original — Purdue PURR](https://doi.org/10.4231/R7RX991C).

## Pruebas

```bash
python -m unittest discover -s tests -v
```


