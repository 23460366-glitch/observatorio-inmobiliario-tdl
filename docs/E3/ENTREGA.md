# 📋 Ficha de Entrega Técnica — Entrega E3 y Demo Day E4 (`tag: e3` / Sello TDL)

**Proyecto Integrador:** Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM (*Trusted Data Lab*)  
**Unidad:** Análisis Multivariado (PCA y MANOVA), Modelos de Calidad de Procesos (MoProSoft/CMMI/PSP), DataOps, Datasheet y Certificación **Sello TDL**  
**Tag de Liberación:** `e3`  
**Fecha de Corte:** 21 de noviembre de 2026  

---

## 1. Integrantes del Equipo y Bitácoras PSP Consolidadas (`E0`–`E3`)

| Nombre Completo | Rol en Entrega E3 y Demo Day | Bitácora de Tiempo (PSP) | Bitácora de Defectos (PSP) |
| :--- | :--- | :--- | :--- |
| **Juan Antonio Ortiz Hinojosa** | Análisis Multivariado (Normalidad de Mardia, Mahalanobis, PCA Biplot y MANOVA Wilks/Pillai), Notebook `E3` y Observatorio Web Público en Streamlit (`tablero/app.py`) | [`calidad/tiempo-juan-antonio-ortiz-hinojosa.csv`](../../calidad/tiempo-juan-antonio-ortiz-hinojosa.csv) | [`calidad/defectos-juan-antonio-ortiz-hinojosa.csv`](../../calidad/defectos-juan-antonio-ortiz-hinojosa.csv) |
| **Diego Alberto Virgen Cuéllar** | Evaluación de Procesos (ISO 9001, MoProSoft, SPICE, CMMI), Retrospectiva Cuantitativa PSP, DataOps, Datasheet de Capa Oro (`DATASHEET.md`), Suite `pytest` ($89.54\%$ cov) y Certificación Sello TDL | [`calidad/tiempo-diego-alberto-virgen-cuellar.csv`](../../calidad/tiempo-diego-alberto-virgen-cuellar.csv) | [`calidad/defectos-diego-alberto-virgen-cuellar.csv`](../../calidad/defectos-diego-alberto-virgen-cuellar.csv) |

---

## 2. Matriz de Evidencias Sincronizadas de las 3 Materias (Entrega `E3` y Demo Day `E4`)

| Materia / Eje del Proyecto Integrador | Entregable Requerido por Rúbrica (`E3` y `Demo Day`) | Archivo / Notebook / Aplicación / Evidencia Exacta en el Repositorio | Estado y Resultado Auditado |
| :--- | :--- | :--- | :--- |
| **1. Ingeniería de Datos, DataOps y Datos Abiertos** | **Ficha Técnica del Dataset Abierto (`DATASHEET.md`):** Motivación, composición de los 4 cubos de Capa Oro, proceso de captura, preprocesamiento, usos recomendados/no recomendados y licencia abierta (`CC BY 4.0` / `ODbL 1.0`). | • [`data/gold/inmobiliario/DATASHEET.md`](../../data/gold/inmobiliario/DATASHEET.md)<br>• [`data/gold/inmobiliario/oro_e1_pronostico_mensual_trimestral.csv`](../../data/gold/inmobiliario/oro_e1_pronostico_mensual_trimestral.csv)<br>• [`data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv`](../../data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv)<br>• [`data/gold/inmobiliario/oro_e3_comparacion_multivariada_yield.csv`](../../data/gold/inmobiliario/oro_e3_comparacion_multivariada_yield.csv)<br>• [`data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv`](../../data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv) | ✅ **100% Cumplido:** Documentación completa bajo el estándar *Datasheets for Datasets* y descarga directa en vivo desde la Pestaña 4 de `tablero/app.py`. |
| **1. Ingeniería de Datos, DataOps y Datos Abiertos** | **Observatorio Web Público en Streamlit (`tablero/app.py`) y Simulador de Ingesta en Vivo:** 4 pestañas ejecutivas (Pronóstico E1, Mapa Satelital Google Earth + PCA/MANOVA E2/E3, Factorial $2^3$ + What-If E2, y Certificación Sello TDL + Puerta de Calidad en Vivo). | • [`tablero/app.py`](../../tablero/app.py)<br>• [`src/analytics_e3_e4.py`](../../src/analytics_e3_e4.py)<br>• [`docs/E2/mapa_interactivo_zmvm.html`](../E2/mapa_interactivo_zmvm.html) | ✅ **100% Cumplido:** Aplicación interactiva de costo \$0 con botón **"🚀 Simular Ingesta en Vivo y Validar con Pandera"** que envía registros corruptos a `cuarentena_inmobiliario.csv`. |
| **1. Ingeniería de Datos, DataOps y Datos Abiertos** | **Automatización CI/CD y Captura Programada:** Linter `ruff`, suite `pytest --cov=src` ($\ge 60\%$) y workflows de GitHub Actions. | • [`tests/test_pipeline.py`](../../tests/test_pipeline.py)<br>• [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)<br>• [`.github/workflows/captura_diaria.yml`](../../.github/workflows/captura_diaria.yml)<br>• [`.github/workflows/bronze_capture.yml`](../../.github/workflows/bronze_capture.yml) | ✅ **100% Cumplido:** **Cobertura real = $89.54\%$** en `src/` ($7/7$ suites pasadas) y $0$ errores de linter en `ruff check src tests tablero`. |
| **2. Estadística Aplicada / Análisis Multivariado (`E3`)** | **Análisis Multivariado (`E3`):** Matriz de correlaciones, normalidad multivariada (Asimetría y Curtosis de Mardia + Q-Q Mahalanobis $D^2 \text{ vs } \chi^2_p$), PCA con varianza explicada y Biplot por perfil de negocio, y MANOVA (Lambda de Wilks y Traza de Pillai). | • [`docs/E3/analisis_multivariado_pca_manova.ipynb`](analisis_multivariado_pca_manova.ipynb)<br>• [`src/analytics_e3_e4.py`](../../src/analytics_e3_e4.py) *(función `run_multivariate_pca_manova_e3`)*<br>• Pestaña 2 de [`tablero/app.py`](../../tablero/app.py) | ✅ **100% Cumplido:** Las primeras 2 componentes principales explican el **$83.64\%$ de la varianza total** ($95.2\%$ con 3 PCs); MANOVA confirma diferencias altamente significativas ($p < 0.0001$) en Wilks y Pillai por Sub-zona y Tipología. |
| **3. Calidad en los Sistemas de Información (Procesos & Sello TDL)** | **Comparativa de Modelos de Procesos y Autoevaluación (`docs/calidad-sello-E3.md`):** Tabla comparativa ISO 9001, MoProSoft, SPICE (ISO/IEC 33000), CMMI y PSP/TSP + autoevaluación con brechas concretas. | • [`docs/calidad-sello-E3.md`](../calidad-sello-E3.md) *(Secciones 1 y 2)* | ✅ **100% Cumplido:** Autoevaluación detallada en MoProSoft (`OPE-ADM` Nivel 2–3, `OPE-DES` Nivel 3) y CMMI (Nivel 2–3) con brechas organizacionales documentadas. |
| **3. Calidad en los Sistemas de Información (Procesos & Sello TDL)** | **Retrospectiva Cuantitativa PSP, DataOps/Observabilidad y Checklist del Sello TDL (`docs/calidad-sello-E3.md`).** | • [`docs/calidad-sello-E3.md`](../calidad-sello-E3.md) *(Secciones 3, 4 y 5)*<br>• [`calidad/tiempo-*.csv`](../../calidad/) y [`calidad/defectos-*.csv`](../../calidad/) | ✅ **100% Cumplido:** Retrospectiva sobre 28 sesiones ($1,895\text{ min}$ reales vs $1,835\text{ min}$ planeados, $\text{APE}=3.27\%$) y 16 defectos ($100\%$ removidos antes de release). **Todos los criterios del Sello TDL cumplidos al 100%.** |

---

## 3. Resumen de Métricas Auditadas para el Sello Trusted Data Lab (Sello TDL)

| Indicador del Sello TDL | Meta Oficial | Resultado Auditado en Nuestro Repositorio | Estado |
| :--- | :-: | :-: | :-: |
| **Disponibilidad del Sistema** | $\ge 95.0\%$ | **$99.93\%$** | 🏅 **CERTIFICADO** |
| **Completitud en Capa Oro (ISO/IEC 25012)** | $\ge 95.0\%$ | **$100.00\%$ ($0$ celdas nulas)** | 🏅 **CERTIFICADO** |
| **Cobertura de Pruebas Automatizadas (`pytest`)** | $\ge 60.0\%$ | **$89.54\%$ en `src/`** | 🏅 **CERTIFICADO** |
| **Secretos / API Keys de Pago Expuestos** | $0$ | **$0$ (Costo Operativo \$0 USD)** | 🏅 **CERTIFICADO** |
| **Hallazgos Críticos Abiertos** | $0$ | **$0$ abiertos** | 🏅 **CERTIFICADO** |
| **Linaje y Reproducibilidad (`Oro -> Bronce`)** | $100\%$ | **$100.00\%$ ($92/92$ filas con hash `SHA-256`)** | 🏅 **CERTIFICADO** |
