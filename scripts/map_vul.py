from pathlib import Path
import urllib.request
import unicodedata
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Patch

# 1. Datos de departamentos e INDICE VUL
departamentos = [
    "Calamuchita", "Capital", "Colón", "Cruz del Eje", "General Roca",
    "General San Martín", "Ischilín", "Juárez Celman", "Marcos Juárez",
    "Minas", "Pocho", "Presidente Roque Sáenz Peña", "Punilla",
    "Río Cuarto", "Río Primero", "Río Seco", "Río Segundo",
    "San Alberto", "San Javier", "San Justo", "Santa María",
    "Sobremonte", "Tercero Arriba", "Totoral", "Tulumba", "Unión"
]

data = np.array([
    [0.640], [0.351], [0.589], [0.627], [0.663], [0.517], [0.665], [0.542],
    [0.555], [0.688], [0.698], [0.574], [0.541], [0.564], [0.489], [0.749],
    [0.576], [0.622], [0.596], [0.548], [0.604], [0.555], [0.549], [0.591],
    [0.588], [0.551]
])

promedio = np.mean(data)  # 0.585846

df_vul = pd.DataFrame({
    "Departamento": departamentos,
    "INDICE_VUL": data.flatten()
})

# 2. Cargar (o descargar si falta) el GeoJSON de polígonos de Córdoba
root_dir = Path(__file__).resolve().parent.parent
geojson_path = root_dir / "data" / "departamentos_cordoba.geojson"

if not geojson_path.exists():
    geojson_path.parent.mkdir(parents=True, exist_ok=True)
    url_geojson = "https://raw.githubusercontent.com/mgaitan/departamentos_argentina/master/departamentos-cordoba.json"
    print(f"Descargando polígonos de Córdoba en {geojson_path}...")
    urllib.request.urlretrieve(url_geojson, geojson_path)

gdf = gpd.read_file(geojson_path)

col_nombre = next(
    (c for c in ["departamento", "nombre", "NAM", "DEPARTAMENTO", "NOMBRE"] if c in gdf.columns),
    None
)
if col_nombre is None:
    raise KeyError(f"No se encontró columna de departamento. Columnas disponibles: {list(gdf.columns)}")

def normalizar(texto: str) -> str:
    s = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("utf-8")
    return " ".join(s.upper().strip().split())

gdf["key"] = gdf[col_nombre].apply(normalizar)
df_vul["key"] = df_vul["Departamento"].apply(normalizar)
mapa = gdf.merge(df_vul, on="key", how="inner")

# 3. Asignar exactamente los mismos 3 colores del gráfico de barras
mapa["color"] = [
    "#AD1D0D" if v >= 0.65 else ("#E67512" if v > promedio else "#489ACA")
    for v in mapa["INDICE_VUL"]
]

# 4. Configurar lienzo cartográfico
fig, ax = plt.subplots(figsize=(10, 12.5), dpi=150)
fig.patch.set_facecolor("white")
ax.set_facecolor("#F4F7FA")

mapa.plot(
    color=mapa["color"],
    edgecolor="white",
    linewidth=1.4,
    zorder=2,
    ax=ax
)

mapa.dissolve().boundary.plot(
    color="#1B2A4A",
    linewidth=1.8,
    zorder=3,
    ax=ax
)

# 5. Etiquetas centradas dentro de cada departamento
nombres_cortos = {
    "PRESIDENTE ROQUE SÁENZ PEÑA": "PTE. ROQUE\nSÁENZ PEÑA",
    "GENERAL SAN MARTÍN": "GRAL. SAN\nMARTÍN",
    "TERCERO ARRIBA": "TERCERO\nARRIBA",
    "JUÁREZ CELMAN": "JUÁREZ\nCELMAN",
    "MARCOS JUÁREZ": "MARCOS\nJUÁREZ",
    "GENERAL ROCA": "GRAL. ROCA"
}

for _, row in mapa.iterrows():
    pt = row.geometry.representative_point()
    nombre = row["Departamento"].upper()
    etiqueta_dept = nombres_cortos.get(nombre, nombre)
    texto = f"{etiqueta_dept}\n{row['INDICE_VUL']:.3f}"
    tamaño = 6.2 if nombre == "CAPITAL" else 6.8

    ax.text(
        pt.x,
        pt.y,
        texto,
        ha="center",
        va="center",
        fontsize=tamaño,
        fontweight="bold",
        color="#1A1A1A",
        zorder=4,
        path_effects=[pe.withStroke(linewidth=2.3, foreground="white")]
    )

# 6. Título superior, flecha Norte y leyenda coherente con los 3 colores
fig.text(
    0.5, 0.965,
    "MAPA DE VULNERABILIDAD EN LA VEJEZ — PROVINCIA DE CÓRDOBA",
    ha="center", va="center",
    fontsize=13, fontweight="bold", color="white",
    bbox=dict(boxstyle="square,pad=0.65", facecolor="#1B2A4A", edgecolor="none")
)

ax.annotate(
    "N",
    xy=(0.06, 0.94), xytext=(0.06, 0.88),
    xycoords="axes fraction",
    ha="center", va="center",
    fontsize=11, fontweight="bold", color="#1B2A4A",
    arrowprops=dict(arrowstyle="-|>", color="#1B2A4A", lw=2)
)

handles = [
    Patch(facecolor="#AD1D0D", edgecolor="#444444", linewidth=0.8, label="Vulnerabilidad Alta (≥ 0,650)"),
    Patch(facecolor="#E67512", edgecolor="#444444", linewidth=0.8, label=f"Sobre el promedio (> {promedio:.3f})"),
    Patch(facecolor="#489ACA", edgecolor="#444444", linewidth=0.8, label=f"Bajo el promedio (< {promedio:.3f})")
]
leyenda = ax.legend(
    handles=handles,
    title="ÍNDICE DE VULNERABILIDAD\n(0 = menor, 1 = mayor)",
    loc="lower left",
    bbox_to_anchor=(0.02, 0.02),
    frameon=True,
    facecolor="white",
    edgecolor="#CCCCCC",
    framealpha=0.96,
    fontsize=8.5,
    title_fontsize=9,
    borderpad=0.9,
    labelspacing=0.65
)
leyenda.get_title().set_fontweight("bold")
leyenda.get_title().set_color("#1B2A4A")

ax.grid(True, linestyle=":", linewidth=0.6, color="#B0C4D8", zorder=1)
ax.tick_params(labelsize=8, colors="#444444")
ax.set_xlabel("Longitud (°O)", fontsize=8.5, color="#444444")
ax.set_ylabel("Latitud (°S)", fontsize=8.5, color="#444444")

# 7. Guardar en graph/
out_dir = root_dir / "graph"
out_dir.mkdir(parents=True, exist_ok=True)
salida = out_dir / "mapa_vulnerabilidad_cordoba.png"

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig(salida, dpi=300)
plt.close(fig)
print(f"Mapa guardado en: {salida}")