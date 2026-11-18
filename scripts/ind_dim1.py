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

# Datos: var1 (Def. monetario) y var2 (Tasa moratoria)
data = np.array([
    [0.70, 0.19],   # Calamuchita
    [0.44, 0.13],   # Capital
    [0.61, 0.18],   # Colón
    [0.46, 0.19],   # Cruz del Eje
    [0.67, 0.18],   # General Roca
    [0.53, 0.16],   # General San Martín
    [0.70, 0.20],   # Ischilín
    [0.65, 0.15],   # Juárez Celman
    [0.58, 0.15],   # Marcos Juárez
    [0.33, 0.21],   # Minas
    [0.78, 0.21],   # Pocho
    [0.47, 0.17],   # Presidente Roque Sáenz Peña
    [0.63, 0.16],   # Punilla
    [0.61, 0.16],   # Río Cuarto
    [0.73, 0.13],   # Río Primero
    [1.00, 0.19],   # Río Seco
    [0.59, 0.17],   # Río Segundo
    [0.73, 0.18],   # San Alberto
    [0.41, 0.18],   # San Javier
    [0.59, 0.16],   # San Justo
    [0.51, 0.19],   # Santa María
    [0.10, 0.20],   # Sobremonte
    [0.53, 0.16],   # Tercero Arriba
    [0.67, 0.17],   # Totoral
    [0.00, 0.20],   # Tulumba
    [0.45, 0.16],   # Unión
])

# Ponderaciones manuales (deben sumar 1.0)
PESO_DEF_MONETARIO = 0.40
PESO_TASA_MORATORIA = 0.60

pesos = np.array([PESO_DEF_MONETARIO, PESO_TASA_MORATORIA])
assert np.isclose(pesos.sum(), 1.0), "Los pesos deben sumar 1.0"

# Invertir indicadores para que valores altos representen mayor seguridad económica
indicadores_positivos = 1 - data
seguridad_economica = indicadores_positivos @ pesos

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