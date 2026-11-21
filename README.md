# 🏢 Observatorio del Mercado Inmobiliario y Renta Habitacional (ZMVM) — Trusted Data Lab

[![Sello TDL Certificado](https://img.shields.io/badge/Sello_TDL-Certificado_100%25-10B981?style=for-the-badge)](docs/etica-datos.md)
[![Cobertura Pytest](https://img.shields.io/badge/Coverage_Pytest->70%25-0284C7?style=for-the-badge)](tests/test_pipeline.py)
[![Costo Operativo](https://img.shields.io/badge/Costo_Operativo-$0_USD_(0_API_Keys)-7C3AED?style=for-the-badge)](tablero/app.py)

Repositorio oficial del **Proyecto Integrador ("Trusted Data Lab" — Entregas E0, E1, E2, E3 y Demo Day E4)** enfocado en el análisis econométrico, simulación *what-if*, diseño experimental factorial $2^k$, análisis multivariado (PCA y MANOVA) e integración geoespacial satelital del mercado de alquiler residencial en la Zona Metropolitana del Valle de México (ZMVM).

## 👥 Integrantes del Equipo
- **Juan Antonio Ortiz Hinojosa**
- **Diego Alberto Virgen Cuéllar**

---

## 🖥️ Ejecución del Observatorio Web Completo en Streamlit (`tablero/app.py`)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Lanzar la aplicación web con las 4 pestañas ejecutivas del Demo Day
streamlit run tablero/app.py
```

### Pestañas del Observatorio Web (`tablero/app.py`):
1. **📈 Pestaña 1 — Resumen Ejecutivo y Pronóstico (`E1`):** KPIs del mercado ZMVM, serie histórica de 36 meses y pronóstico a 4 trimestres con intervalos de confianza al 95% comparando **Exponencial Simple (SES)**, **Lineal de Holt**, **Holt-Winters** y **ARIMA/SARIMA** (con métricas MAE, RMSE, MAPE y prueba de ruido blanco de **Ljung-Box**).
2. **🛰️ Pestaña 2 — Explorador Satelital Estilo Google Earth y Mapa Multivariado PCA/MANOVA (`E2` y `E3`):** Mapa satelital híbrido interactivo (`Esri.WorldImagery` + etiquetas híbridas de calles/colonias sin API Keys, buscador de colonias y pantalla completa) + matriz de correlaciones, normalidad multivariada de Mardia, **Biplot interactivo de Componentes Principales (PCA)** con perfiles de negocio y resultados de **MANOVA** (**Lambda de Wilks** y **Traza de Pillai**).
3. **🧪 Pestaña 3 — Experimento Factorial $2^3$ y Simulador What-If (`E2`):** Diseño factorial $2^3$ aleatorizado con réplicas sobre el rendimiento del pipeline, gráficas de efectos principales e interacción, tabla ANOVA, comparativa teórico-práctica de matriz **$2^4$ completa vs $2^{4-1}$ fraccionada (Resolución IV)** y simulador interactivo de contratos a 24 meses.
4. **🏅 Pestaña 4 — Certificación Sello TDL y Puerta de Calidad en Vivo (`Calidad & Demo Day E4`):** Badge del **Sello TDL**, evaluación **ISO/IEC 25010** e **ISO/IEC 25012**, catálogo de linaje (`catalogo_linaje_oro_a_bronce.csv`) y simulador interactivo **"Simular Ingesta en Vivo"** que intercepta registros corruptos con `Pandera` hacia `cuarentena_inmobiliario.csv`.

---

## 🔗 Accesos Directos a Notebooks y Artefactos por Etapa

### 📓 Notebooks Reproducibles Ejecutados
- **E1 (Limpieza Estadística y Pandera):** [`docs/E1/limpieza.ipynb`](docs/E1/limpieza.ipynb)
- **E1 (Pronóstico de Series de Tiempo):** [`docs/E1/pronostico_series_tiempo.ipynb`](docs/E1/pronostico_series_tiempo.ipynb)
- **E2 (Geoespacial DENUE/OSM y Linaje):** [`docs/E2/geoespacial_linaje.ipynb`](docs/E2/geoespacial_linaje.ipynb)
- **E2 (Diseño Experimental Factorial $2^k$):** [`docs/E2/experimento_factorial_2k.ipynb`](docs/E2/experimento_factorial_2k.ipynb)
- **E3 (Análisis Multivariado PCA y MANOVA):** [`docs/E3/analisis_multivariado_pca_manova.ipynb`](docs/E3/analisis_multivariado_pca_manova.ipynb)

### 🗺️ Cartografía y Gobernanza
- **Mapa Interactivo Satelital Híbrido (Google Earth Style):** [`docs/E2/mapa_interactivo_zmvm.html`](docs/E2/mapa_interactivo_zmvm.html)
- **Mapa Coroplético de Alta Resolución (`PNG`):** [`docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png`](docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png)
- **Declaración de Ética, Legalidad y Privacidad:** [`docs/etica-datos.md`](docs/etica-datos.md)
- **Catálogo Maestro de Linaje (`Oro -> Bronce`):** [`data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv`](data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv)

---

## 🧪 Pruebas Automatizadas y CI/CD

```bash
# Ejecutar linter Ruff
ruff check src tests tablero

# Ejecutar suite de pruebas con verificación de cobertura (>60%)
pytest --cov=src --cov-fail-under=60 --cov-report=term-missing
```
