from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Datos: (Departamento, DIM1, DIM2, DIM3, INDICE_VUL)
datos = [
    ("Calamuchita",                 0.76, 0.50, 0.72, 0.660),
    ("Capital",                     0.19, 0.36, 0.64, 0.337),
    ("Colón",                       0.68, 0.47, 0.63, 0.592),
    ("Cruz del Eje",                0.71, 0.60, 0.55, 0.641),
    ("General Roca",                0.65, 0.70, 0.76, 0.690),
    ("General San Martín",          0.43, 0.52, 0.79, 0.532),
    ("Ischilín",                    0.84, 0.55, 0.53, 0.676),
    ("Juárez Celman",               0.38, 0.68, 0.71, 0.552),
    ("Marcos Juárez",               0.43, 0.62, 0.82, 0.572),
    ("Minas",                       0.73, 0.75, 0.52, 0.695),
    ("Pocho",                       0.91, 0.83, 0.09, 0.718),
    ("Presidente Roque Sáenz Peña", 0.51, 0.63, 0.74, 0.597),
    ("Punilla",                     0.52, 0.42, 0.78, 0.540),
    ("Río Cuarto",                  0.50, 0.59, 0.75, 0.580),
    ("Río Primero",                 0.29, 0.71, 0.54, 0.488),
    ("Río Seco",                    0.87, 0.78, 0.55, 0.773),
    ("Río Segundo",                 0.53, 0.64, 0.69, 0.598),
    ("San Alberto",                 0.69, 0.62, 0.51, 0.631),
    ("San Javier",                  0.62, 0.58, 0.63, 0.607),
    ("San Justo",                   0.44, 0.61, 0.77, 0.564),
    ("Santa María",                 0.70, 0.51, 0.61, 0.615),
    ("Sobremonte",                  0.64, 0.51, 0.58, 0.579),
    ("Tercero Arriba",              0.48, 0.56, 0.80, 0.571),
    ("Totoral",                     0.64, 0.69, 0.35, 0.599),
    ("Tulumba",                     0.55, 0.80, 0.42, 0.611),
    ("Unión",                       0.46, 0.60, 0.79, 0.576),
]

df = pd.DataFrame(datos, columns=["Departamento", "DIM1", "DIM2", "DIM3", "INDICE_VUL"])

# 2. Aportes ponderados: 0.45 * DIM1 + 0.35 * DIM2 + 0.20 * DIM3
df["c1_raw"] = 0.45 * df["DIM1"]
df["c2_raw"] = 0.35 * df["DIM2"]
df["c3_raw"] = 0.20 * df["DIM3"]

# Ajuste proporcional mínimo (<0.004) por redondeo a 2 decimales de DIM1-3
factor = df["INDICE_VUL"] / (df["c1_raw"] + df["c2_raw"] + df["c3_raw"])
df["c1"] = df["c1_raw"] * factor
df["c2"] = df["c2_raw"] * factor
df["c3"] = df["c3_raw"] * factor

# Ordenar ascendente para que el más vulnerable quede arriba en barh
df = df.sort_values("INDICE_VUL", ascending=True).reset_index(drop=True)
promedio = df["INDICE_VUL"].mean()  # 0.585846

# 3. Configurar figura
fig, ax = plt.subplots(figsize=(12, 10.5), dpi=150)
fig.patch.set_facecolor("white")
ax.set_facecolor("#F8FAFC")

y = np.arange(len(df))
alto = 0.68

col_dim1 = "#1B2A4A"  # Azul marino (45%)
col_dim2 = "#E67512"  # Naranja (35%)
col_dim3 = "#489ACA"  # Celeste (20%)

b1 = ax.barh(
    y, df["c1"], height=alto, color=col_dim1, edgecolor="white", linewidth=0.8,
    label="DIM 1 (45%): Económica / Previsional"
)
b2 = ax.barh(
    y, df["c2"], left=df["c1"], height=alto, color=col_dim2, edgecolor="white", linewidth=0.8,
    label="DIM 2 (35%): Salud, Educación y Vivienda"
)
b3 = ax.barh(
    y, df["c3"], left=df["c1"] + df["c2"], height=alto, color=col_dim3, edgecolor="white", linewidth=0.8,
    label="DIM 3 (20%): Redes y Contención Social"
)

# 4. Etiquetas internas por segmento y valor total al final de la barra
for i, row in df.iterrows():
    # Segmento 1
    if row["c1"] >= 0.055:
        ax.text(
            row["c1"] / 2, i, f"{row['c1_raw']:.2f}",
            ha="center", va="center", color="white", fontsize=7.5, fontweight="bold"
        )
    # Segmento 2
    if row["c2"] >= 0.055:
        ax.text(
            row["c1"] + row["c2"] / 2, i, f"{row['c2_raw']:.2f}",
            ha="center", va="center", color="white", fontsize=7.5, fontweight="bold"
        )
    # Segmento 3 (omite textos en segmentos muy angostos como Pocho = 0.018)
    if row["c3"] >= 0.055:
        ax.text(
            row["c1"] + row["c2"] + row["c3"] / 2, i, f"{row['c3_raw']:.2f}",
            ha="center", va="center", color="white", fontsize=7.5, fontweight="bold"
        )

    # Total INDICE VUL a la derecha de la barra
    ax.text(
        row["INDICE_VUL"] + 0.008, i, f"{row['INDICE_VUL']:.3f}",
        ha="left", va="center", color="#1A1A1A", fontsize=8.3, fontweight="bold"
    )

# 5. Línea de promedio provincial
ax.axvline(promedio, color="#242424", linestyle="--", linewidth=1.6, zorder=4)
ax.text(
    promedio + 0.006, 0.35, f"Promedio provincial: {promedio:.3f}",
    color="#242424", fontsize=8.5, fontweight="bold", va="bottom",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#242424", alpha=0.92)
)

# 6. Títulos, ejes y leyenda
fig.text(
    0.5, 0.965,
    "COMPOSICIÓN DEL ÍNDICE DE VULNERABILIDAD POR DIMENSIÓN — CÓRDOBA",
    ha="center", va="center",
    fontsize=12.5, fontweight="bold", color="white",
    bbox=dict(boxstyle="square,pad=0.6", facecolor="#1B2A4A", edgecolor="none")
)

ax.set_yticks(y)
ax.set_yticklabels(df["Departamento"], fontsize=8.8, fontweight="bold", color="#1A1A1A")
ax.set_xlim(0, 0.86)
ax.set_xlabel("Aporte ponderado al Índice de Vulnerabilidad (0,45·DIM1 + 0,35·DIM2 + 0,20·DIM3)", fontsize=9, color="#333333")

ax.grid(axis="x", linestyle=":", linewidth=0.7, color="#CBD5E1", zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#94A3B8")
ax.spines["bottom"].set_color("#94A3B8")

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.045),
    ncol=3,
    frameon=True,
    facecolor="white",
    edgecolor="#CBD5E1",
    fontsize=8.5
)

# 7. Guardar en graph/
root_dir = Path(__file__).resolve().parent.parent
out_dir = root_dir / "graph"
out_dir.mkdir(parents=True, exist_ok=True)
salida = out_dir / "barras_apiladas_vulnerabilidad.png"

plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig(salida, dpi=300)
plt.close(fig)
print(f"Gráfico guardado en: {salida}")