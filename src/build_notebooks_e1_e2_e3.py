#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los 3 notebooks estadísticos reproducibles solicitados:
  1. docs/E1/pronostico_series_tiempo.ipynb
  2. docs/E2/experimento_factorial_2k.ipynb
  3. docs/E3/analisis_multivariado_pca_manova.ipynb
"""

from pathlib import Path
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BASE_DIR = Path(__file__).resolve().parent.parent


def make_nb(cells):
    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3.11"}
    nb.cells = cells
    return nb


def build_e1_forecast_nb() -> Path:
    path = BASE_DIR / "docs" / "E1" / "pronostico_series_tiempo.ipynb"
    path.parent.mkdir(parents=True, exist_ok=True)
    cells = [
        new_markdown_cell(
            """# 📈 Pronóstico de Series de Tiempo: Precio Residencial por $m^2$ en la ZMVM (E1)

**Proyecto Integrador — Trusted Data Lab (Etapa E1)**  
**Integrantes:** Juan Antonio Ortiz Hinojosa & Diego Alberto Virgen Cuéllar

---

## 🎯 Contenido del Notebook
1. **Descomposición Aditiva y Multiplicativa** de la serie histórica de 36 meses (`2023-11` a `2026-10`).
2. **Prueba de Estacionariedad Augmented Dickey-Fuller (ADF)** en nivel y primera diferencia ($\\Delta Y_t$) + **ACF y PACF**.
3. **Entrenamiento y Backtesting de 4 Modelos:** Suavizamiento Exponencial Simple (SES), Método Lineal de Holt, Holt-Winters Estacional y ARIMA/SARIMA.
4. **Comparación en Conjunto de Prueba (MAE, RMSE, MAPE)** y **Diagnóstico de Residuos Ljung-Box**.
5. **Pronóstico a 4 Trimestres (12 meses)** con intervalos de confianza al 95%."""
        ),
        new_code_cell(
            """import sys
from pathlib import Path
import json
import pandas as pd

ROOT_DIR = Path.cwd().resolve()
if not (ROOT_DIR / "src").exists():
    ROOT_DIR = ROOT_DIR.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.analytics_e3_e4 import run_time_series_forecasting_e1

res_e1 = run_time_series_forecasting_e1(horizon_months=12)
print("Serie histórica cargada:", len(res_e1["historico_df"]), "periodos mensuales.")"""
        ),
        new_markdown_cell(
            """## 1. Descomposición Aditiva/Multiplicativa, Prueba Dickey-Fuller (ADF) y ACF/PACF"""
        ),
        new_code_cell(
            """print("=== Prueba Augmented Dickey-Fuller (ADF) ===")
print(json.dumps(res_e1["adf_test"], indent=2))
print("\\nACF (primeros 8 rezagos):", res_e1["acf_values"][:8])
print("PACF (primeros 8 rezagos):", res_e1["pacf_values"][:8])

df_decomp = pd.DataFrame({
    "periodo": res_e1["descomposicion"]["periodos"],
    "observado": res_e1["descomposicion"]["observado"],
    "tendencia_aditiva": res_e1["descomposicion"]["tendencia_aditiva"],
    "estacional_aditiva": res_e1["descomposicion"]["estacional_aditiva"],
    "residuo_aditivo": res_e1["descomposicion"]["residuo_aditivo"],
    "estacional_multiplicativa": res_e1["descomposicion"]["estacional_multiplicativa"],
})
display(df_decomp.head(12))"""
        ),
        new_markdown_cell(
            """## 2. Comparación de los 4 Modelos (SES, Holt, Holt-Winters, ARIMA/SARIMA) y Prueba Ljung-Box"""
        ),
        new_code_cell(
            """df_metrics = pd.DataFrame(res_e1["metricas_comparativas_modelos"])
display(df_metrics)"""
        ),
        new_markdown_cell(
            """## 3. Pronóstico a 12 Meses (4 Trimestres) con Intervalos de Confianza al 95%"""
        ),
        new_code_cell(
            """print("=== Pronóstico Mensual (12 Meses) ===")
display(res_e1["pronostico_12_meses_df"])
print("\\n=== Resumen Trimestral (Próximos 4 Trimestres) ===")
display(res_e1["pronostico_4_trimestres_df"])"""
        ),
    ]
    with path.open("w", encoding="utf-8") as f:
        nbformat.write(make_nb(cells), f)
    return path


def build_e2_factorial_nb() -> Path:
    path = BASE_DIR / "docs" / "E2" / "experimento_factorial_2k.ipynb"
    path.parent.mkdir(parents=True, exist_ok=True)
    cells = [
        new_markdown_cell(
            """# 🧪 Diseño Experimental Factorial $2^3$ y Comparativa $2^4$ vs $2^{4-1}$ Fraccionado (E2)

**Proyecto Integrador — Trusted Data Lab (Etapa E2)**  
**Integrantes:** Juan Antonio Ortiz Hinojosa & Diego Alberto Virgen Cuéllar

---

## 🎯 Contenido del Notebook
1. **Diseño Factorial $2^3$ Aleatorizado con $r=3$ Réplicas ($N=24$ corridas)** sobre el rendimiento del pipeline:
   - Factor A: Tamaño de Lote (`-1`: 250 regs, `+1`: 1,500 regs)
   - Factor B: Estrategia de Validación (`-1`: Iteración Fila-a-Fila, `+1`: Vectorizado Pandera)
   - Factor C: Formato de Salida (`-1`: JSON Texto, `+1`: CSV Columnar)
2. **Tabla ANOVA con Efectos Principales e Interacciones** ($A, B, C, AB, AC, BC, ABC$).
3. **Validación de Supuestos** (Normalidad de Shapiro-Wilk y Homocedasticidad de Levene) y **Corrida de Confirmación**.
4. **Comparación Teórico-Práctica de Matriz $2^4$ Completa vs $2^{4-1}$ Fraccionada (Resolución IV, Generador $I=ABCD$)**."""
        ),
        new_code_cell(
            """import sys
from pathlib import Path
import json
import pandas as pd

ROOT_DIR = Path.cwd().resolve()
if not (ROOT_DIR / "src").exists():
    ROOT_DIR = ROOT_DIR.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.analytics_e3_e4 import run_factorial_experiment_2k

res_e2 = run_factorial_experiment_2k()
display(res_e2["experimento_2_3_df"].head(12))"""
        ),
        new_markdown_cell(
            """## 1. Tabla ANOVA Multifactorial ($2^3$), Supuestos y Corrida de Confirmación"""
        ),
        new_code_cell(
            """display(res_e2["anova_tabla_df"])
print("\\n=== Validación de Supuestos del ANOVA ===")
print(json.dumps(res_e2["supuestos_anova"], indent=2))
print("\\n=== Corrida de Confirmación ===")
print(json.dumps(res_e2["corrida_confirmacion"], indent=2))"""
        ),
        new_markdown_cell(
            """## 2. Comparativa Diseño $2^4$ Completo (16 corridas base) vs Fracción $2^{4-1}$ ($I=ABCD$, 8 corridas base)"""
        ),
        new_code_cell(
            """comp = res_e2["comparativa_2_4_vs_2_4_1"]
print("Generador:", comp["generador_fraccion"])
print("Resolución:", comp["resolucion"])
print("Ahorro Experimental (%):", comp["ahorro_experimental_pct"])
print("Estructura de Alias:", comp["estructura_alias_principales"])
display(comp["matriz_fraccionada_2_4_1_df"])"""
        ),
    ]
    with path.open("w", encoding="utf-8") as f:
        nbformat.write(make_nb(cells), f)
    return path


def build_e3_multivariate_nb() -> Path:
    path = BASE_DIR / "docs" / "E3" / "analisis_multivariado_pca_manova.ipynb"
    path.parent.mkdir(parents=True, exist_ok=True)
    cells = [
        new_markdown_cell(
            """# 🧬 Análisis Multivariado: Normalidad de Mardia, Distancias de Mahalanobis, PCA Biplot y MANOVA (E3)

**Proyecto Integrador — Trusted Data Lab (Etapa E3)**  
**Integrantes:** Juan Antonio Ortiz Hinojosa & Diego Alberto Virgen Cuéllar

---

## 🎯 Contenido del Notebook
1. **Matriz de Correlaciones Multivariadas** y **Prueba de Normalidad Multivariada** (Asimetría y Curtosis de Mardia + Q-Q Cuantiles $\\chi^2$ de Distancias de Mahalanobis $D^2$).
2. **Análisis de Componentes Principales (PCA):** Autovalores, porcentaje de varianza explicada, matriz de cargas (*loadings*) y scores de las 16 colonias con clasificación de perfiles de negocio.
3. **MANOVA (Análisis de Varianza Multivariado):** Estadísticos **Lambda de Wilks**, **Traza de Pillai**, **Hotelling-Lawley** y **Raíz Mayor de Roy** evaluando diferencias conjuntas por Sub-zona y Tipología."""
        ),
        new_code_cell(
            """import sys
from pathlib import Path
import json
import pandas as pd

ROOT_DIR = Path.cwd().resolve()
if not (ROOT_DIR / "src").exists():
    ROOT_DIR = ROOT_DIR.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.analytics_e3_e4 import run_multivariate_pca_manova_e3

res_e3 = run_multivariate_pca_manova_e3()
print("=== Matriz de Correlación de Pearson ===")
display(res_e3["correlacion_df"])"""
        ),
        new_markdown_cell(
            """## 1. Normalidad Multivariada (Mardia) y Distancias Cuadradas de Mahalanobis ($D^2$ vs $\\chi^2_p$)"""
        ),
        new_code_cell(
            """print(json.dumps(res_e3["normalidad_multivariada"], indent=2))"""
        ),
        new_markdown_cell(
            """## 2. Componentes Principales (PCA): Varianza Explicada, Loadings y Perfiles de Negocio"""
        ),
        new_code_cell(
            """pca_info = res_e3["pca"]
print("Autovalores:", pca_info["eigenvalues"])
print("Varianza explicada (%):", pca_info["varianza_explicada_pct"])
print("Varianza acumulada 2 PCs (%):", pca_info["varianza_acumulada_2pc_pct"])
print("\\n=== Cargas Factoriales (Loadings) ===")
display(pca_info["loadings_df"])
print("\\n=== Coordenadas PCA y Perfil de Negocio por Colonia ===")
display(pca_info["scores_colonias_df"])"""
        ),
        new_markdown_cell(
            """## 3. MANOVA: Lambda de Wilks y Traza de Pillai por Sub-zona y Tipología"""
        ),
        new_code_cell(
            """display(res_e3["manova_tabla_df"])"""
        ),
    ]
    with path.open("w", encoding="utf-8") as f:
        nbformat.write(make_nb(cells), f)
    return path


if __name__ == "__main__":
    p1 = build_e1_forecast_nb()
    p2 = build_e2_factorial_nb()
    p3 = build_e3_multivariate_nb()
    print("Notebooks generados:", p1, p2, p3)
