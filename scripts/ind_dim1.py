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

# Datos: var1 (Def. monetario) y var2 (Tasa moratoria) normalizados
data = np.array([
    [0.70, 0.73],   # Calamuchita
    [0.44, 0.02],   # Capital
    [0.61, 0.66],   # Colón
    [0.46, 0.81],   # Cruz del Eje
    [0.67, 0.58],   # General Roca
    [0.53, 0.33],   # General San Martín
    [0.70, 0.85],   # Ischilín
    [0.65, 0.19],   # Juárez Celman
    [0.58, 0.30],   # Marcos Juárez
    [0.33, 1.00],   # Minas
    [0.78, 0.99],   # Pocho
    [0.47, 0.49],   # Presidente Roque Sáenz Peña
    [0.63, 0.42],   # Punilla
    [0.61, 0.39],   # Río Cuarto
    [0.73, 0.00],   # Río Primero
    [1.00, 0.72],   # Río Seco
    [0.59, 0.44],   # Río Segundo
    [0.73, 0.61],   # San Alberto
    [0.41, 0.70],   # San Javier
    [0.59, 0.31],   # San Justo
    [0.51, 0.76],   # Santa María
    [0.10, 0.91],   # Sobremonte
    [0.53, 0.41],   # Tercero Arriba
    [0.67, 0.57],   # Totoral
    [0.00, 0.84],   # Tulumba
    [0.45, 0.42],   # Unión
])

# Ponderaciones manuales (deben sumar 1.0)
PESO_DEF_MONETARIO = 0.40
PESO_TASA_MORATORIA = 0.60

pesos = np.array([PESO_DEF_MONETARIO, PESO_TASA_MORATORIA])
assert np.isclose(pesos.sum(), 1.0), "Los pesos deben sumar 1.0"

# Invertir indicadores para que valores altos representen mayor seguridad económica
# indicadores_positivos = 1 - data
seguridad_economica = data @ pesos

df_dim1 = pd.DataFrame({
    "Departamento": departamentos,
    "Def_monetario": data[:, 0],
    "Tasa_moratoria": data[:, 1],
    "seguridad_economica": np.round(seguridad_economica, 4)
})

# Apunta siempre a la carpeta data/ en la raíz del proyecto
data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)
archivo_salida = data_dir / "dim1_seguridad_economica.csv"

df_dim1.to_csv(archivo_salida, index=False)

print(df_dim1.to_string(index=False))
print(f"\nArchivo guardado correctamente en: {archivo_salida}")