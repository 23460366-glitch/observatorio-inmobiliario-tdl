#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera y ejecuta el notebook interactivo docs/E2/geoespacial_linaje.ipynb."""

from pathlib import Path
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BASE_DIR = Path(__file__).resolve().parent.parent
NB_PATH = BASE_DIR / "docs" / "E2" / "geoespacial_linaje.ipynb"
NB_PATH.parent.mkdir(parents=True, exist_ok=True)

nb = new_notebook()
nb.metadata["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
nb.metadata["language_info"] = {
    "name": "python",
    "version": "3.11",
}

cells = [
    new_markdown_cell(
        """# 🗺️ Integración de Fuente Especializada Geoespacial (DENUE INEGI + OpenStreetMap + Marco Geoestadístico) y Linaje de Datos (Bronce $\\rightarrow$ Plata $\\rightarrow$ Oro)

**Proyecto Integrador — Entrega E2 (Unidad 4 — Ponderación: 20%)**  
**Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM**  
**Integrantes del Equipo:**
- Juan Antonio Ortiz Hinojosa
- Diego Alberto Virgen Cuéllar

---

## 🎯 Alcance del Notebook (`docs/E2/geoespacial_linaje.ipynb`)
Este cuaderno ejecutable documenta y verifica los tres pilares técnicos de la **Entrega E2**:
1. **Fuente Especializada Geoespacial (`GeoPandas` + `Shapely` + `Folium`):**
   - Integración de los polígonos de AGEB/Colonias del **Marco Geoestadístico Nacional (INEGI)**, densidad de unidades económicas de servicios y comercio del **DENUE (INEGI)** y nodos de transporte masivo (Metro, Metrobús, Suburbano) e infraestructura verde de **OpenStreetMap (OSM)**.
   - Reproyección métrica oficial a **UTM Zona 14N (`EPSG:32614`)** para calcular distancias euclidianas exactas en metros al transporte masivo (`dist_transporte_masivo_m`), unidades económicas en buffers de 500 metros (`denue_unidades_buffer_500m`) y el **Índice Compuesto de Accesibilidad y Equipamiento Urbano (`0-100`)**.
2. **Visualización Cartográfica Dual:**
   - Mapa coroplético de alta resolución (`docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png`) y mapa interactivo HTML (`docs/E2/mapa_interactivo_zmvm.html`).
3. **Linaje y Trazabilidad Completa de Datos (100% Auditable):**
   - Verificación programática de que **cada uno de los 92 registros agregados en las 4 tablas de la Capa Oro** (`oro_e1`, `oro_e2`, `oro_e3` y `oro_geoespacial`) posee trazabilidad exacta hacia los registros primarios (`PROP-*`), archivos crudos en Capa Bronce, hash criptográfico SHA-256 del lote origen y timestamps UTC de ingesta."""
    ),
    new_code_cell(
        """import sys
from pathlib import Path
import json
import pandas as pd
import geopandas as gpd

PROJECT_ROOT = Path.cwd().resolve()
if (PROJECT_ROOT / "src").exists():
    ROOT_DIR = PROJECT_ROOT
else:
    ROOT_DIR = PROJECT_ROOT.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.pipeline_e2 import (
    extract_geospatial_bronze_source,
    enrich_silver_with_geopandas_and_lineage,
    update_gold_layer_with_full_lineage,
    generate_cartographic_visualizations,
)

pd.set_option("display.max_columns", 25)
pd.set_option("display.width", 130)
print("Entorno GeoPandas cargado correctamente. Versión GeoPandas:", gpd.__version__)"""
    ),
    new_markdown_cell(
        """## 1. Captura Ética en Capa Bronce de la Fuente Geoespacial (DENUE INEGI + MGN + OpenStreetMap)
Se cargan los GeoDataFrames en `EPSG:4326` de las 16 colonias representativas de las 4 sub-zonas de estudio en la ZMVM y las 14 estaciones de transporte masivo cercanas, junto con la auditoría programática de `robots.txt`."""
    ),
    new_code_cell(
        """gdf_colonias, gdf_estaciones, geo_meta = extract_geospatial_bronze_source()
print("=== Metadatos y Auditoría Ética de la Fuente Geoespacial (Capa Bronce) ===")
print(json.dumps(geo_meta, indent=2, ensure_ascii=False))
display(gdf_colonias.drop(columns=["geometry"]).head(8))"""
    ),
    new_markdown_cell(
        """## 2. Procesamiento Espacial con `GeoPandas` (`EPSG:32614` UTM 14N) y Enriquecimiento de Capa Plata
Reproyectamos las geometrías de propiedades y estaciones de transporte al sistema métrico **WGS 84 / UTM zone 14N (`EPSG:32614`)** para medir distancias reales en metros y calcular el **Índice de Accesibilidad y Equipamiento Urbano (`0-100`)**, preservando privacidad por diseño (*k-anonimato espacial a nivel polígono de colonia/AGEB*)."""
    ),
    new_code_cell(
        """gdf_silver_geo, spatial_summary = enrich_silver_with_geopandas_and_lineage(
    gdf_colonias, gdf_estaciones, geo_meta
)
print("=== Resumen del Enriquecimiento Espacial en Capa Plata ===")
print(json.dumps(spatial_summary, indent=2, ensure_ascii=False))

display(
    gdf_silver_geo[[
        "id_propiedad", "periodo_mensual", "colonia", "cve_ageb_inegi",
        "precio_m2_winsor_mxn", "dist_transporte_masivo_m", "estacion_transporte_cercana_osm",
        "denue_unidades_buffer_500m", "indice_accesibilidad_urbana_0_100",
        "linaje_fecha_captura_bronce_utc", "linaje_hash_registro_bronce"
    ]].head(8)
)"""
    ),
    new_markdown_cell(
        """## 3. Linaje y Trazabilidad Completa desde Capa Oro hasta Capa Bronce
Verificamos que cada registro de las **4 tablas de la Capa Oro** (`oro_e1_pronostico_mensual_trimestral.csv`, `oro_e2_simulacion_whatif_24m.csv`, `oro_e3_comparacion_multivariada_yield.csv` y `oro_geoespacial_colonias_denue_osm.csv`) esté vinculado en el catálogo maestro `data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv` con sus IDs de origen en Bronce, archivos fuente, hash SHA-256 y fechas de ingesta."""
    ),
    new_code_cell(
        """lineage_summary = update_gold_layer_with_full_lineage(gdf_silver_geo)
print("=== Auditoría de Trazabilidad y Linaje (Oro -> Bronce) ===")
print(json.dumps(lineage_summary, indent=2, ensure_ascii=False))

df_gold_geo = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv")
print("\\n--- Cubo Oro Geoespacial por Colonia (DENUE + OSM + Rentas + Linaje) ---")
display(df_gold_geo[[
    "colonia", "subzona_id", "cve_ageb_inegi", "precio_m2_promedio_mxn",
    "yield_bruto_promedio_pct", "dist_transporte_masivo_m", "denue_unidades_buffer_500m",
    "indice_accesibilidad_urbana_0_100", "linaje_n_registros_bronce",
    "linaje_id_bronce_primero", "linaje_fecha_captura_bronce_min_utc", "linaje_hash_lote_bronce"
]])

df_catalogo_linaje = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv")
print("\\n--- Muestra del Catálogo Maestro de Linaje (92 registros de Capa Oro auditados) ---")
display(df_catalogo_linaje.head(10))"""
    ),
    new_markdown_cell(
        """## 4. Visualización Cartográfica (`GeoPandas` + `Matplotlib` y `Folium`)
Generamos la lámina cartográfica dual de alta resolución (`docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png`) y el mapa interactivo (`docs/E2/mapa_interactivo_zmvm.html`)."""
    ),
    new_code_cell(
        """from IPython.display import Image, display as ipy_display

cart_outputs = generate_cartographic_visualizations(gdf_colonias, gdf_estaciones)
print("Artefactos cartográficos generados:", json.dumps(cart_outputs, indent=2))
ipy_display(Image(filename=str(ROOT_DIR / cart_outputs["mapa_coropletico_png"])))"""
    ),
]

nb.cells = cells
with NB_PATH.open("w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Notebook E2 creado exitosamente en: {NB_PATH}")
