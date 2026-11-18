from pathlib import Path
import numpy as np
import pandas as pd

departamentos = [
    "Calamuchita", "Capital", "Colón", "Cruz del Eje", "General Roca",
    "General San Martín", "Ischilín", "Juárez Celman", "Marcos Juárez",
    "Minas", "Pocho", "Presidente Roque Sáenz Peña", "Punilla",
    "Río Cuarto", "Río Primero", "Río Seco", "Río Segundo",
    "San Alberto", "San Javier", "San Justo", "Santa María",
    "Sobremonte", "Tercero Arriba", "Totoral", "Tulumba", "Unión"
]

# Datos: var1 (Def. centro salud), var2 (Def. educativo) y var3 (Déficit material) normalizados
data = np.array([
    [0.86, 0.30, 0.32],   # Calamuchita
    [1.00, 0.00, 0.02],   # Capital
    [0.94, 0.23, 0.18],   # Colón
    [0.82, 0.56, 0.37],   # Cruz del Eje
    [0.89, 0.87, 0.17],   # General Roca
    [0.96, 0.42, 0.05],   # General San Martín
    [0.75, 0.61, 0.19],   # Ischilín
    [0.94, 0.81, 0.10],   # Juárez Celman
    [0.96, 0.61, 0.14],   # Marcos Juárez
    [0.59, 0.91, 0.72],   # Minas
    [0.58, 0.94, 1.00],   # Pocho
    [0.88, 0.73, 0.13],   # Presidente Roque Sáenz Peña
    [0.96, 0.09, 0.20],   # Punilla
    [0.98, 0.53, 0.12],   # Río Cuarto
    [0.84, 0.87, 0.28],   # Río Primero
    [0.65, 0.97, 0.65],   # Río Seco
    [0.95, 0.76, 0.00],   # Río Segundo
    [0.88, 0.54, 0.39],   # San Alberto
    [0.85, 0.41, 0.46],   # San Javier
    [0.95, 0.66, 0.04],   # San Justo
    [0.89, 0.34, 0.25],   # Santa María
    [0.00, 0.93, 0.54],   # Sobremonte
    [0.94, 0.56, 0.02],   # Tercero Arriba
    [0.84, 0.76, 0.35],   # Totoral
    [0.70, 1.00, 0.61],   # Tulumba
    [0.93, 0.58, 0.18],   # Unión
])

PESO_CENTRO_SALUD = 0.35
PESO_EDUCATIVO = 0.4
PESO_DEF_MATERIAL = 0.25

pesos = np.array([PESO_CENTRO_SALUD,PESO_EDUCATIVO,PESO_DEF_MATERIAL])
assert np.isclose(pesos.sum(), 1.0), "Los pesos deben sumar 1.0"

# indicadores_positivos = 1 - data
bienestar_estructural = data @ pesos

df_dim1 = pd.DataFrame({
    "Departamento": departamentos,
    "Def_Centro_Salud": data[:, 0],
    "Def_Educativo": data[:, 1],
    "Def_Material": data[:, 2],
    "bienestar_estructural": np.round(bienestar_estructural, 3)
})

# Apunta siempre a la carpeta data/ en la raíz del proyecto
data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)
archivo_salida = data_dir / "dim2_bienestar_estructural.csv"

df_dim1.to_csv(archivo_salida, index=False)

print(df_dim1.to_string(index=False))
print(f"\nArchivo guardado correctamente en: {archivo_salida}")