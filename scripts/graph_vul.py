from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

departamentos = [
    "Calamuchita", "Capital", "Colón", "Cruz del Eje", "General Roca",
    "General San Martín", "Ischilín", "Juárez Celman", "Marcos Juárez",
    "Minas", "Pocho", "Presidente Roque Sáenz Peña", "Punilla",
    "Río Cuarto", "Río Primero", "Río Seco", "Río Segundo",
    "San Alberto", "San Javier", "San Justo", "Santa María",
    "Sobremonte", "Tercero Arriba", "Totoral", "Tulumba", "Unión"
]

# Índice de vulnerabilidad
data = np.array([
    [0.660],   # Calamuchita
    [0.337],   # Capital
    [0.592],   # Colón
    [0.641],   # Cruz del Eje
    [0.690],   # General Roca
    [0.532],   # General San Martín
    [0.676],   # Ischilín
    [0.552],   # Juárez Celman
    [0.572],   # Marcos Juárez
    [0.695],   # Minas
    [0.718],   # Pocho
    [0.597],   # Presidente Roque Sáenz Peña
    [0.540],   # Punilla
    [0.580],   # Río Cuarto
    [0.488],   # Río Primero
    [0.773],   # Río Seco
    [0.598],   # Río Segundo
    [0.631],   # San Alberto
    [0.607],   # San Javier
    [0.564],   # San Justo
    [0.615],   # Santa María
    [0.579],   # Sobremonte
    [0.571],   # Tercero Arriba
    [0.599],   # Totoral
    [0.611],   # Tulumba
    [0.576],   # Unión
])

promedio = np.mean(data)  # 0.585846

# --- Grafico ---

# 1. Crear DataFrame y ordenar de menor a mayor (para que el más vulnerable quede arriba)
df = pd.DataFrame({
    "Departamento": departamentos,
    "INDICE_VUL": data.flatten()
})
df_ordenado = df.sort_values(by="INDICE_VUL", ascending=True).reset_index(drop=True)

# 2. Asignar colores según umbrales de vulnerabilidad
colores = [
    "#AD1D0D" if v >= 0.65 else ("#E67512" if v > promedio else "#489ACA")
    for v in df_ordenado["INDICE_VUL"]
]

# 3. Construir el gráfico de barras horizontales
fig, ax = plt.subplots(figsize=(10, 8.5), dpi=150)
barras = ax.barh(
    df_ordenado["Departamento"],
    df_ordenado["INDICE_VUL"],
    color=colores,
    height=0.68
)

# Línea vertical con el promedio departamental
ax.axvline(promedio, color="#1D1D1D", linestyle="--", linewidth=1.3, zorder=2)

# Etiquetas numéricas al final de cada barra
for barra in barras:
    valor = barra.get_width()
    ax.text(
        valor + 0.008,
        barra.get_y() + barra.get_height() / 2,
        f"{valor:.3f}",
        va="center",
        ha="left",
        fontsize=8.5,
        color="#222222",
        fontweight="normal",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=0.8),
        zorder=3
    )
# 4. Formato de ejes, grilla y leyenda
ax.set_xlim(0, 0.85)
ax.set_xlabel(
    "Índice de Vulnerabilidad en la Vejez (0 = menor vulnerabilidad, 1 = mayor vulnerabilidad)",
    fontsize=10,
    fontweight="bold",
    color="#222222"
)
ax.set_title(
    "Vulnerabilidad en la Vejez por Departamento — Provincia de Córdoba",
    fontsize=12.5,
    fontweight="bold",
    pad=14,
    color="#1B2A4A"
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#CCCCCC")
ax.spines["bottom"].set_color("#CCCCCC")
ax.grid(axis="x", linestyle=":", alpha=0.5, color="#AAAAAA")
ax.set_axisbelow(True)

leyenda = [
    Patch(facecolor="#AD1D0D", label="Vulnerabilidad Alta (≥ 0,650)"),
    Patch(facecolor="#E67512", label=f"Sobre el promedio (> {promedio:.3f})"),
    Patch(facecolor="#489ACA", label=f"Bajo el promedio (< {promedio:.3f})"),
    plt.Line2D([0], [0], color="#1A1A1A", linestyle="--", linewidth=1.3, label=f"Promedio Departamental ({promedio:.3f})")
]
ax.legend(
    handles=leyenda,
    loc="lower right",
    frameon=True,
    facecolor="white",
    edgecolor="#DDDDDD",
    fontsize=8.5
)

out_dir = Path(__file__).resolve().parent.parent / "graph"
out_dir.mkdir(parents=True, exist_ok=True)
salida = out_dir / "grafico_indice_vul.png"

plt.tight_layout()
plt.savefig(salida, dpi=300)
plt.close(fig)
print(f"Gráfico guardado correctamente en: {salida.resolve()}")