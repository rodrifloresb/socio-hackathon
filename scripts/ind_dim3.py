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

# Datos: var6 (Def. centro jubilado ) y var7 (nivel de contencion familiar) normalizados
data = np.array([
    [0.89, 0.44],   # Calamuchita
    [0.95, 0.36],   # Capital
    [0.98, 0.27],   # Colón
    [0.81, 0.21],   # Cruz del Eje
    [0.79, 0.57],   # General Roca
    [0.85, 0.63],   # General San Martín
    [0.81, 0.13],   # Ischilín
    [0.82, 0.47],   # Juárez Celman
    [0.91, 0.58],   # Marcos Juárez
    [0.53, 0.35],   # Minas
    [0.00, 0.00],   # Pocho
    [0.78, 0.53],   # Presidente Roque Sáenz Peña
    [1.00, 0.59],   # Punilla
    [0.90, 0.46],   # Río Cuarto
    [0.78, 0.20],   # Río Primero
    [0.75, 0.15],   # Río Seco
    [0.85, 0.34],   # Río Segundo
    [0.77, 0.20],   # San Alberto
    [0.82, 0.44],   # San Javier
    [0.90, 0.48],   # San Justo
    [0.87, 0.31],   # Santa María
    [0.29, 1.00],   # Sobremonte
    [0.92, 0.49],   # Tercero Arriba
    [0.58, 0.09],   # Totoral
    [0.36, 0.49],   # Tulumba
    [0.85, 0.56],   # Unión
])

PESO_CENTRO_JUBILADOS = 0.6
PESO_CONTENCION_FAMILIAR = 0.4

pesos = np.array([PESO_CENTRO_JUBILADOS, PESO_CONTENCION_FAMILIAR])
assert np.isclose(pesos.sum(), 1.0), "Los pesos deben sumar 1.0"

# indicadores_positivos = 1 - data
integracion_social = data @ pesos

df_dim1 = pd.DataFrame({
    "Departamento": departamentos,
    "Def_Centro_Jubilados": data[:, 0],
    "nivel_contencion_familiar": data[:, 1],
    "integracion_social": np.round(integracion_social, 3)
})

# Apunta siempre a la carpeta data/ en la raíz del proyecto
data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)
archivo_salida = data_dir / "dim3_integracion_social.csv"

df_dim1.to_csv(archivo_salida, index=False)

print(df_dim1.to_string(index=False))
print(f"\nArchivo guardado correctamente en: {archivo_salida}")