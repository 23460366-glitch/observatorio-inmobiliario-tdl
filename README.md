# 🏢 Observatorio del Mercado Inmobiliario y Renta Habitacional (ZMVM) — Trusted Data Lab

[![Sello TDL Certificado](https://img.shields.io/badge/Sello_TDL-Certificado_100%25-10B981?style=for-the-badge)](docs/calidad-sello-E3.md)
[![Cobertura Pytest](https://img.shields.io/badge/Coverage_Pytest-89.54%25-0284C7?style=for-the-badge)](tests/test_pipeline.py)
[![Costo Operativo](https://img.shields.io/badge/Costo_Operativo-$0_USD_(0_API_Keys)-7C3AED?style=for-the-badge)](tablero/app.py)

Repositorio oficial del **Proyecto Integrador ("Trusted Data Lab" — Entregas E0, E1, E2, E3 y Demo Day E4)** enfocado en el análisis econométrico, simulación *what-if*, diseño experimental factorial $2^k$, análisis multivariado (PCA y MANOVA), aseguramiento de calidad normativo (IEEE 730, ISO/IEC 25010, ISO/IEC 25012, MoProSoft, CMMI, PSP) e integración geoespacial satelital del mercado de alquiler residencial en la Zona Metropolitana del Valle de México (ZMVM).

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

---

## 🔗 Índice Maestro de Entregables por Materia y Etapa

### 🛡️ Documentación Normativa de Calidad (SQA, ISO, Auditoría, Procesos y Sello TDL)
1. **Plan SQA (Estándar IEEE 730 — `E1`):** [`docs/plan-sqa.md`](docs/plan-sqa.md)
2. **Evaluación Normativa ISO 9001, ISO 9126, ISO/IEC 25010 e ISO/IEC 25012 (`E2`):** [`docs/evaluacion-iso-E2.md`](docs/evaluacion-iso-E2.md)
3. **Reporte de Auditoría Cruzada entre Equipos (`E2`):** [`docs/auditoria-cruzada-E2.md`](docs/auditoria-cruzada-E2.md)
4. **Modelos de Procesos (MoProSoft/SPICE/CMMI), Retrospectiva PSP, DataOps y Checklist Sello TDL (`E3`):** [`docs/calidad-sello-E3.md`](docs/calidad-sello-E3.md)
5. **Declaración de Ética, Legalidad y Privacidad (`E2`):** [`docs/etica-datos.md`](docs/etica-datos.md)
6. **Datasheet Oficial del Dataset Abierto en Capa Oro (`E3`):** [`data/gold/inmobiliario/DATASHEET.md`](data/gold/inmobiliario/DATASHEET.md)

### 📋 Fichas Técnicas de Entrega y Relatorías
- **Entrega E0 (`tag: e0`):** [`docs/E0/propuesta.md`](docs/E0/propuesta.md) | [`docs/E0/ENTREGA.md`](docs/E0/ENTREGA.md)
- **Entrega E1 (`tag: e1`):** [`docs/E1/ENTREGA.md`](docs/E1/ENTREGA.md) | [`docs/relatoria-E1.md`](docs/relatoria-E1.md)
- **Entrega E2 (`tag: e2`):** [`docs/E2/ENTREGA.md`](docs/E2/ENTREGA.md) | [`docs/relatoria-E2.md`](docs/relatoria-E2.md)
- **Entrega E3 y Demo Day (`tag: e3`):** [`docs/E3/ENTREGA.md`](docs/E3/ENTREGA.md)

### 📓 Notebooks Reproducibles Ejecutados
- **E1 (Limpieza Estadística y Pandera):** [`docs/E1/limpieza.ipynb`](docs/E1/limpieza.ipynb)
- **E1 (Pronóstico de Series de Tiempo):** [`docs/E1/pronostico_series_tiempo.ipynb`](docs/E1/pronostico_series_tiempo.ipynb)
- **E2 (Geoespacial DENUE/OSM y Linaje):** [`docs/E2/geoespacial_linaje.ipynb`](docs/E2/geoespacial_linaje.ipynb)
- **E2 (Diseño Experimental Factorial $2^k$):** [`docs/E2/experimento_factorial_2k.ipynb`](docs/E2/experimento_factorial_2k.ipynb)
- **E3 (Análisis Multivariado PCA y MANOVA):** [`docs/E3/analisis_multivariado_pca_manova.ipynb`](docs/E3/analisis_multivariado_pca_manova.ipynb)

### 🗺️ Cartografía y Linaje Criptográfico
- **Mapa Interactivo Satelital Híbrido (Google Earth Style):** [`docs/E2/mapa_interactivo_zmvm.html`](docs/E2/mapa_interactivo_zmvm.html)
- **Mapa Coroplético de Alta Resolución (`PNG`):** [`docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png`](docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png)
- **Catálogo Maestro de Linaje (`Oro -> Bronce`):** [`data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv`](data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv)
