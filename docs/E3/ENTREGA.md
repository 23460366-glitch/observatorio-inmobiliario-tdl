# Ficha de Entrega Técnica — Entrega E3 y Demo Day E4 (`tag: e3` / Sello TDL)

**Proyecto Integrador:** Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional (ZMVM & Colima – Villa de Álvarez) — *Trusted Data Lab*  
**Unidad:** Unidad 4 (15% E3) — Optimización Medida del Pipeline, Publicación de Dataset Abierto y Datasheet (`docs/E3/datasheet.md`), Análisis Multivariado (PCA/MANOVA), Modelos de Procesos y Rediseño Ejecutivo B2B con Figma  
**Tag de Liberación:** `e3`  
**Sistema de Diseño UI/UX en Figma:** [`Observatorio Inmobiliario TDL — PropTech Design System & App`](https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX)  

---

## 1. Integrantes del Equipo y Bitácoras PSP Consolidadas (`E0`–`E3`)

| Nombre Completo | Rol en Entrega E3 y Demo Day | Bitácora de Tiempo (PSP) | Bitácora de Defectos (PSP) |
| :--- | :--- | :--- | :--- |
| **Juan Antonio Ortiz Hinojosa** | Benchmark de Optimización del Pipeline (`src/benchmark_optimizacion_e3.py`), Análisis Multivariado (Mardia, Mahalanobis, PCA Biplot y MANOVA), Sistema de Diseño Figma y Rediseño SaaS B2B de `tablero/app.py` | [`calidad/tiempo-juan-antonio-ortiz-hinojosa.csv`](../../calidad/tiempo-juan-antonio-ortiz-hinojosa.csv) | [`calidad/defectos-juan-antonio-ortiz-hinojosa.csv`](../../calidad/defectos-juan-antonio-ortiz-hinojosa.csv) |
| **Diego Alberto Virgen Cuéllar** | Publicación de Dataset Abierto y Ficha Técnica (`docs/E3/datasheet.md`), Relatoría `docs/relatoria-E3.md`, Evaluación de Procesos (ISO 9001, MoProSoft, SPICE, CMMI), DataOps, Suite `pytest` ($>90\%$ cov) y Sello TDL | [`calidad/tiempo-diego-alberto-virgen-cuellar.csv`](../../calidad/tiempo-diego-alberto-virgen-cuellar.csv) | [`calidad/defectos-diego-alberto-virgen-cuellar.csv`](../../calidad/defectos-diego-alberto-virgen-cuellar.csv) |

---

## 2. Entregables Centrales de Ingeniería de Datos — Entrega `E3` (`tag: e3`)

| # | Entregable Oficial `E3` | Evidencia Exacta en el Repositorio | Resultado Cuantitativo Auditado |
| :-: | :--- | :--- | :--- |
| **1** | **Optimización Medida del Pipeline (Antes vs. Después en Tiempo, Memoria y Errores)** | • [`src/benchmark_optimizacion_e3.py`](../../src/benchmark_optimizacion_e3.py)<br>• [`data/gold/inmobiliario/reporte_optimizacion_e3.json`](../../data/gold/inmobiliario/reporte_optimizacion_e3.json)<br>• [`data/gold/inmobiliario/comparativa_optimizacion_e3.csv`](../../data/gold/inmobiliario/comparativa_optimizacion_e3.csv)<br>• Pestaña 4 de [`tablero/app.py`](../../tablero/app.py) | • **Tiempo Medio:** $3,422.95\text{ ms} \rightarrow \mathbf{638.17\text{ ms}}$ (**$-81.36\%$ / $5.36\times$ más rápido**)<br>• **Memoria Pico (`tracemalloc`):** $9.492\text{ MiB} \rightarrow \mathbf{2.561\text{ MiB}}$ (**$-73.02\%$**)<br>• **Huella RAM DataFrame:** $4,110.08\text{ KiB} \rightarrow \mathbf{222.61\text{ KiB}}$ (**$-94.58\%$**)<br>• **Errores Infiltrados:** $207 \rightarrow \mathbf{0\text{ defectos}}$ (**$-100.0\%$**) |
| **2** | **Publicación de Dataset Limpio con Licencia Abierta y Datasheet (`docs/E3/datasheet.md`)** | • [`docs/E3/datasheet.md`](datasheet.md)<br>• [`data/gold/inmobiliario/DATASHEET.md`](../../data/gold/inmobiliario/DATASHEET.md)<br>• Cubos Oro en [`data/gold/inmobiliario/`](../../data/gold/inmobiliario/) (`CC BY 4.0` / `ODbL 1.0`) | **100 registros en Capa Oro** (`92 ZMVM + 8 Colima`), **24 zonas en GeoJSON maestro** y **2,155 inmuebles en Capa Plata** con $0\%$ nulos, $0$ PII y licencia abierta verificada. |
| **3** | **Ficha de Entrega (`docs/E3/ENTREGA.md`) y Relatoría de Etapa (`docs/relatoria-E3.md`)** | • [`docs/E3/ENTREGA.md`](ENTREGA.md)<br>• [`docs/relatoria-E3.md`](../relatoria-E3.md) | Documentación técnica completa de decisiones de vectorización, compactación en memoria, publicación abierta y diseño UI B2B en Figma. |

---

## 3. Matriz Sincronizada de las 3 Materias y Presentación Comercial B2B (`E3` & `E4`)

| Materia / Eje del Proyecto Integrador | Entregable Requerido por Rúbrica | Archivo / Notebook / Aplicación / Evidencia | Estado y Resultado Auditado |
| :--- | :--- | :--- | :--- |
| **1. Ingeniería de Datos, DataOps y UI Ejecutiva Figma** | **App Web Ejecutiva en Streamlit (`tablero/app.py`) + Sistema de Diseño en Figma:** Tipografía `Plus Jakarta Sans` & `JetBrains Mono`, íconos vectoriales SVG sin emojis, benchmark E3 interactivo, puerta `Pandera` en vivo y planes comerciales B2B. | • [`tablero/app.py`](../../tablero/app.py)<br>• [`docs/E2/mapa_interactivo_zmvm.html`](../E2/mapa_interactivo_zmvm.html)<br>• [Archivo Figma TDL PropTech UI](https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX)<br>• [`docs/E4/reporte_inteligencia_cliente.md`](../E4/reporte_inteligencia_cliente.md) | **100% Cumplido:** Interfaz B2B lista para evaluación académica (3 profesores) y venta corporativa (AMPI / desarrolladoras / fondos) con costo operativo \$0 USD. |
| **1. Ingeniería de Datos y Automatización CI/CD** | **Suite Automatizada `pytest` ($\ge 60\%$), Linter `ruff` y Workflows GitHub Actions.** | • [`tests/test_pipeline.py`](../../tests/test_pipeline.py)<br>• [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)<br>• [`.github/workflows/captura_diaria.yml`](../../.github/workflows/captura_diaria.yml) | **100% Cumplido:** Cobertura superior al **$90\%$ en `src/`**, pruebas de regresión sobre optimización E3, datasheet y mapa libre de emojis, y $0$ errores de linter. |
| **2. Estadística Aplicada / Análisis Multivariado (`E3`)** | **Análisis Multivariado (`E3`):** Matriz de correlaciones, normalidad multivariada de Mardia + Q-Q Mahalanobis $D^2 \text{ vs } \chi^2_p$, PCA Biplot y MANOVA (Wilks y Pillai). | • [`docs/E3/analisis_multivariado_pca_manova.ipynb`](analisis_multivariado_pca_manova.ipynb)<br>• [`src/analytics_e3_e4.py`](../../src/analytics_e3_e4.py) | **100% Cumplido:** 2 PCs explican **$83.64\%$ de la varianza** ($95.2\%$ con 3 PCs); MANOVA confirma diferencias altamente significativas ($p < 0.0001$) por Sub-zona y Tipología. |
| **3. Calidad en los Sistemas de Información (Procesos & Sello TDL)** | **Comparativa ISO 9001, MoProSoft, SPICE, CMMI y PSP/TSP + Retrospectiva PSP + Sello TDL (`docs/calidad-sello-E3.md`).** | • [`docs/calidad-sello-E3.md`](../calidad-sello-E3.md)<br>• [`calidad/tiempo-*.csv`](../../calidad/) y [`calidad/defectos-*.csv`](../../calidad/) | **100% Cumplido:** Autoevaluación MoProSoft/CMMI documentada, retrospectiva cuantitativa PSP ($\text{APE}=3.27\%$) y todos los criterios del **Sello TDL** certificados. |

---

## 4. Resumen de Métricas Auditadas para el Sello Trusted Data Lab (Sello TDL)

| Indicador del Sello TDL | Meta Oficial | Resultado Auditado en Nuestro Repositorio | Estado |
| :--- | :-: | :-: | :-: |
| **Disponibilidad del Sistema** | $\ge 95.0\%$ | **$99.93\%$** | **CERTIFICADO** |
| **Completitud en Capa Oro (ISO/IEC 25012)** | $\ge 95.0\%$ | **$100.00\%$ ($0$ celdas nulas)** | **CERTIFICADO** |
| **Cobertura de Pruebas Automatizadas (`pytest`)** | $\ge 60.0\%$ | **$> 90.0\%$ en `src/`** | **CERTIFICADO** |
| **Secretos / API Keys de Pago Expuestos** | $0$ | **$0$ (Costo Operativo \$0 USD)** | **CERTIFICADO** |
| **Hallazgos Críticos Abiertos** | $0$ | **$0$ abiertos** | **CERTIFICADO** |
| **Linaje y Reproducibilidad (`Oro -> Bronce`)** | $100\%$ | **$100.00\%$ ($100/100$ filas con hash `SHA-256`)** | **CERTIFICADO** |
