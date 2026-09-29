"""Agregación espectral y características espaciales para Indian Pines."""
import numpy as np
import pandas as pd
from skimage.filters.rank import entropy
from skimage.morphology import disk, erosion, dilation, opening, area_opening, area_closing

# Intervalos del notebook de Camilo Acevedo-Correa, en nm.
RANGES = [(433,453), (450,515), (525,600), (630,680), (845,885),
          (1560,1660), (2100,2300), (500,680), (1360,1390)]
NAMES = ['B1','B2','B3','B4','B5','B6','B7','B8','B9']

def wavelengths(csv_path, channels):
    """Alinear por identificadores de canal originales (numeración desde 1)."""
    table = pd.read_csv(csv_path, sep=';')
    required = {'data_channel', 'center_wavelength'}
    if not required.issubset(table.columns):
        raise ValueError(f'El CSV debe contener {required}')
    if table.data_channel.duplicated().any():
        raise ValueError('Hay canales duplicados en el CSV')
    ids = np.asarray(channels)
    if ids.ndim != 1 or len(np.unique(ids)) != len(ids):
        raise ValueError('Los canales deben formar una lista unidimensional sin duplicados')
    result = table.set_index('data_channel').loc[ids, 'center_wavelength'].to_numpy(float)
    # Conservar el orden del cubo: la calibración puede solaparse entre detectores.
    if not np.isfinite(result).all() or np.any(result <= 0):
        raise ValueError('Las longitudes de onda deben ser finitas y positivas')
    return result

def standard_channels(n_bands):
    """Convención estándar; el usuario debe comprobar la procedencia del MAT."""
    if n_bands == 220:
        return np.arange(1, 221)
    if n_bands == 200:
        removed = set(range(104,109)) | set(range(150,164)) | {220}
        return np.array([c for c in range(1,221) if c not in removed])
    raise ValueError('Proporcione un mapeo explícito para cubos distintos de 200/220 bandas')

def validate_cube(cube):
    cube = np.asarray(cube, dtype=np.float64)
    if cube.ndim != 3 or 0 in cube.shape or not np.isfinite(cube).all():
        raise ValueError('Se requiere un cubo H×W×C no vacío, con valores finitos')
    return cube

def aggregate_bands(cube, wave, missing='error'):
    """Media uniforme por intervalo; missing='skip' omite intervalos sin muestras."""
    cube = validate_cube(cube)
    wave = np.asarray(wave, dtype=float)
    if wave.shape != (cube.shape[2],) or not np.isfinite(wave).all():
        raise ValueError('Se necesita una longitud de onda finita por canal del cubo')
    if missing not in ('error', 'skip'):
        raise ValueError('missing debe ser error o skip')
    bands, records = [], []
    for name, (lo, hi) in zip(NAMES, RANGES):
        idx = np.flatnonzero((wave >= lo) & (wave <= hi))
        records.append(dict(band=name, lower_nm=lo, upper_nm=hi,
                            count=len(idx), cube_indices=idx.tolist(),
                            wavelengths_nm=wave[idx].tolist(), included=bool(len(idx))))
        if not len(idx):
            if missing == 'error':
                raise ValueError(f'{name}: no hay canales en {lo}–{hi} nm. Use el cubo completo o missing="skip".')
            continue
        bands.append(cube[:,:,idx].mean(axis=2))
    if not bands:
        raise ValueError('Ningún intervalo contiene canales')
    return np.stack(bands, axis=2), records

def normalize_image(image):
    image = np.asarray(image, dtype=np.float64)
    if image.size == 0 or not np.isfinite(image).all():
        raise ValueError('Entrada vacía o no finita')
    span = np.ptp(image)
    return np.zeros_like(image) if span == 0 else (image-image.min()) / span

def spatial_features(msi, radius=4, footprint_size=5, iterations=2, area_threshold=1000):
    """Normalización global, cuantización a 8 bits, entropía y morfología por banda."""
    msi = validate_cube(msi)
    if any(not isinstance(v, (int, np.integer)) for v in (radius, footprint_size, iterations, area_threshold)):
        raise ValueError('Los parámetros espaciales deben ser enteros')
    if radius < 1 or footprint_size < 1 or iterations < 0 or area_threshold < 1:
        raise ValueError('Parámetros espaciales fuera de rango')
    quantized = np.rint(normalize_image(msi)*255).astype(np.uint8)
    footprint = np.ones((footprint_size, footprint_size), dtype=bool)
    entropic, morph = [], []
    for k in range(msi.shape[2]):
        e = entropy(quantized[:,:,k], disk(radius))
        entropic.append(e / e.max() if e.max() else np.zeros_like(e))
        x = msi[:,:,k].copy()
        for _ in range(iterations):
            x = erosion(x, footprint=footprint)
        x = opening(x, footprint=footprint)
        for _ in range(iterations):
            x = dilation(x, footprint=footprint)
        morph.append(area_opening(area_closing(x, area_threshold=area_threshold), area_threshold=area_threshold))
    return np.stack(entropic, axis=2), np.stack(morph, axis=2)
