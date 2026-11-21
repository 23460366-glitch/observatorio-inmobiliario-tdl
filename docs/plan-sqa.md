# 🛡️ Plan de Aseguramiento de la Calidad del Software y de los Datos (Plan SQA — Estándar IEEE 730)

**Proyecto Integrador:** Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM (*Trusted Data Lab*)  
**Código del Documento:** `TDL-SQA-IEEE730-v1.0`  
**Etapa:** Entrega E1 (con cobertura continua sobre E0, E1, E2, E3 y Demo Day E4)  
**Estándar de Referencia:** IEEE Std 730-2014 (*IEEE Standard for Software Quality Assurance Processes*)  
**Autores y Responsables:**  
- **Diego Alberto Virgen Cuéllar** — *Líder de Aseguramiento de Calidad (SQA Lead), Arquitectura de Pipeline y DevSecOps*  
- **Juan Antonio Ortiz Hinojosa** — *Líder de Ingeniería Estadística, Calidad Geoespacial (GIS) y Validación Analítica*  

---

## 1. Propósito y Alcance (Secciones 1 y 2 IEEE 730)

### 1.1 Propósito
El propósito de este **Plan de Aseguramiento de la Calidad del Software (SQA Plan)** es establecer las actividades, estándares, métricas de fiabilidad, controles de seguridad y puertas de calidad automatizadas que garantizan que el software (`src/`, `tablero/app.py`, `tests/`) y los activos de datos (`data/bronze/`, `data/silver/`, `data/gold/`) del **Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM** cumplan con los requisitos funcionales, estadísticos y normativos para obtener la certificación del **Sello Trusted Data Lab (TDL)** a costo operativo **\$0 USD**.

### 1.2 Alcance
Este plan aplica a la totalidad de los componentes del repositorio `observatorio-inmobiliario-tdl`:
1. **Máquina de Captura Ética (Capa Bronce):** `src/extract_bronze.py` y su programación automatizada en `.github/workflows/captura_diaria.yml` y `.github/workflows/bronze_capture.yml`.
2. **Pipeline de Limpieza Estadística y Puerta de Calidad (`Pandera`) hacia Capa Plata y Oro:** `src/pipeline_e1.py`, `data/silver/inmobiliario/cuarentena_inmobiliario.csv` y `data/silver/inmobiliario/rentas_zmvm_plata_limpio.csv`.
3. **Integración Geoespacial (`GeoPandas` + DENUE INEGI + OpenStreetMap) y Linaje Criptográfico (`SHA-256`):** `src/pipeline_e2.py`, `docs/E2/mapa_interactivo_zmvm.html` y `data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv`.
4. **Motor Analítico (Pronóstico E1, Factorial $2^3$ E2, PCA/MANOVA E3) y Tablero Web Público (`Streamlit`):** `src/analytics_e3_e4.py` y `tablero/app.py`.

---

## 2. Documentos de Referencia y Estándares Aplicables (Sección 3 IEEE 730)

| Estándar / Norma | Ámbito de Aplicación en el Observatorio | Mecanismo de Verificación en el Repositorio |
| :--- | :--- | :--- |
| **IEEE Std 730-2014** | Estructura y gobierno del proceso de Aseguramiento de Calidad del Software (SQA). | Presente documento (`docs/plan-sqa.md`) y auditorías por etapa (`ENTREGA.md`). |
| **ISO/IEC 25010:2023 (SQuaRE)** | Modelo de calidad del producto de software (8 características: adecuación funcional, eficiencia, fiabilidad, seguridad, mantenibilidad, etc.). | Evaluado cuantitativamente en [`docs/evaluacion-iso-E2.md`](evaluacion-iso-E2.md) y Pestaña 4 de `tablero/app.py`. |
| **ISO/IEC 25012:2008 (SQuaRE)** | Modelo de calidad de datos (Exactitud, Completitud, Consistencia, Credibilidad y Actualidad). | Contratos declarativos en `Pandera` (`src/pipeline_e1.py`) y métricas sobre `data/gold/`. |
| **PSP (Personal Software Process)** | Disciplina individual de estimación de tiempos y registro/remoción temprana de defectos. | Bitácoras CSV en `calidad/tiempo-*.csv` y `calidad/defectos-*.csv`. |
| **PEP 8 / Ruff Linter** | Estándar de estilo, análisis estático y prevención de errores sintácticos en Python 3.11+. | Ejecución obligatoria de `ruff check src tests tablero` en `.github/workflows/ci.yml`. |

---

## 3. Gestión, Organización y Roles del Equipo (Sección 4 IEEE 730)

Al tratarse de un equipo de alta cohesión de **2 integrantes**, se establece un esquema de **revisión por pares cruzada obligatoria (*Four-Eyes Principle*)**: ningún integrante aprueba ni etiqueta una liberación (`e0`, `e1`, `e2`, `e3`) sin que el otro integrante haya ejecutado y verificado las pruebas locales y la bitácora PSP.

| Integrante | Rol Principal SQA e Ingeniería | Responsabilidades Específicas de Calidad |
| :--- | :--- | :--- |
| **Diego Alberto Virgen Cuéllar** | **Líder SQA, Arquitectura de Datos, Puerta de Calidad (`Pandera`) y DevSecOps** | • Diseño y mantenimiento de los esquemas `DataFrameSchema` en `Pandera` y política de cuarentena (`cuarentena_inmobiliario.csv`).<br>• Administración de los flujos CI/CD en GitHub Actions (`ci.yml`, `captura_diaria.yml`, `bronze_capture.yml`).<br>• Auditoría de seguridad (cero secretos expuestos, `pip-audit`/`gitleaks`), linaje `SHA-256` y consolidación normativa ISO/SQA. |
| **Juan Antonio Ortiz Hinojosa** | **Líder de Calidad Estadística, Geoespacial (`GeoPandas`) y Producto Analítico (`Streamlit`)** | • Verificación matemática del diagnóstico MCAR/MAR/MNAR, Winsorización de atípicos y modelos SARIMA/Holt-Winters.<br>• Aseguramiento de calidad cartográfica en `EPSG:32614` (UTM 14N) y visor satelital híbrido sin bloqueos de API Key.<br>• Pruebas funcionales del tablero `tablero/app.py` y validación de reproducibilidad de los 5 notebooks `.ipynb`. |

---

## 4. Tabla de Requerimientos Verificables del Observatorio (Sección 5 IEEE 730)

Cada requerimiento funcional (RF) y no funcional / de calidad (RNF) del observatorio posee un criterio cuantitativo de aceptación y una prueba automatizada en [`tests/test_pipeline.py`](../tests/test_pipeline.py):

| ID Req. | Tipo | Descripción del Requerimiento Verificable | Criterio / Umbral Cuantitativo de Aceptación | Prueba Automatizada / Evidencia | Estado |
| :--- | :-: | :--- | :--- | :--- | :-: |
| **RF-01** | Funcional | Captura ética automatizada de series macroeconómicas (BANXICO/INEGI) y mercado de rentas ZMVM en Capa Bronce. | Serie continua de **$\ge 36$ periodos mensuales consecutivos** (`2023-11` a `2026-10`) y auditoría `robots.txt` con `crawl_delay >= 1.0s`. | `test_bronze_extraction_and_periods` en `tests/test_pipeline.py` | ✅ Verificado |
| **RF-02** | Funcional | Integración relacional M:1 y resolución automática de conflictos de esquema, fechas (`DD/MM/YYYY` $\rightarrow$ `YYYY-MM`) y monedas en texto. | **$0$ registros huérfanos** sin empate macroeconómico; $100\%$ de cadenas monetarias convertidas a `float64`. | `test_parsers_and_integration_e1` en `tests/test_pipeline.py` | ✅ Verificado |
| **RF-03** | Funcional | Puerta de Calidad automática con `Pandera` y envío a cuarentena documentada antes de promover a Capa Plata. | **$0$ borrados silenciosos**: todo registro fuera de rango ($m^2 \notin [20, 1200]$, $\text{renta} \le 1500$) o duplicado se guarda en `cuarentena_inmobiliario.csv` con `motivo_cuarentena`. | `test_pandera_quality_gate_and_quarantine` en `tests/test_pipeline.py` | ✅ Verificado |
| **RF-04** | Funcional | Diagnóstico estadístico ($\chi^2$ y $t$ de Welch) e imputación diferenciada de valores faltantes MCAR, MAR y MNAR. | **$100.0\%$ de completitud** en Capa Plata (`0` valores `NaN` tras imputación) conservando la bandera `flag_mnar_mantenimiento`. | `test_missing_values_outliers_and_gold_e1` en `tests/test_pipeline.py` | ✅ Verificado |
| **RF-05** | Funcional | Enriquecimiento geoespacial con DENUE (INEGI), Marco Geoestadístico (`cve_ageb_inegi`) y transporte masivo OpenStreetMap en `GeoPandas`. | Cálculo exacto en metros bajo proyección **`EPSG:32614` (UTM 14N)** para los $1,291$ inmuebles y mapa satelital híbrido sin marcas de agua ni errores `403`. | `test_geospatial_and_full_lineage_e2` en `tests/test_pipeline.py` | ✅ Verificado |
| **RF-06** | Funcional | Linaje y trazabilidad completa de extremo a extremo desde cada celda de Capa Oro hasta sus registros origen en Capa Bronce. | **$100.0\%$ de registros en Capa Oro ($92/92$)** con `linaje_hash_lote_bronce` (`SHA-256`), IDs primarios (`PROP-*`) y timestamps UTC de ingesta ($0$ huérfanos). | `test_geospatial_and_full_lineage_e2` y `catalogo_linaje_oro_a_bronce.csv` | ✅ Verificado |
| **RF-07** | Funcional | Modelos de la Triléctica Estadística (Pronóstico E1, Factorial $2^3$ y What-If E2, PCA y MANOVA E3) y Tablero Web en Streamlit. | MAPE $< 5\%$ y Ljung-Box $p > 0.05$ en SARIMA/Holt-Winters; varianza explicada PCA $\ge 70\%$ en 2 componentes; 4 pestañas operativas en `tablero/app.py`. | `test_statistical_analytics_e1_e2_e3_e4` y `tablero/app.py` | ✅ Verificado |
| **RNF-01** | Calidad / Pruebas | Cobertura de código mediante pruebas unitarias y de integración automatizadas con `pytest-cov` y análisis estático con `ruff`. | **Cobertura en `src/` $\ge 60.0\%$** (meta Sello TDL) y **$0$ errores de linter `ruff`**. *(Resultado actual: **$89.54\%$ de cobertura**)*. | `.github/workflows/ci.yml` y `pytest --cov=src` | ✅ Verificado ($89.54\%$) |
| **RNF-02** | Fiabilidad | Disponibilidad operativa del pipeline automatizado y resiliencia ante caídas o falta de token externo. | **Disponibilidad $\ge 95.0\%$**, `MTTR` $< 30\text{ min}$ y mecanismo de fallback certificado cuando `BANXICO_TOKEN` no está presente. | Sección 5 de este documento (`Availability = 99.83%`) | ✅ Verificado |
| **RNF-03** | Seguridad / Costo | Operación estrictamente gratuita (**Costo \$0 USD**), sin secretos expuestos en el código fuente y con privacidad LFPDPPP. | **$0$ credenciales o API keys hardcodeadas** verificadas por expresión regular/scanner y coordenadas con *k-anonimato espacial* ($\pm 250\text{ m}$). | `test_entrypoints_and_zero_hardcoded_secrets` y [`docs/etica-datos.md`](etica-datos.md) | ✅ Verificado |

---

## 5. Métricas de Fiabilidad del Sistema: MTBF, MTTR y Disponibilidad (Sección 6 IEEE 730)

Para evaluar objetivamente la fiabilidad del pipeline del observatorio a lo largo de las ventanas operativas de desarrollo e integración continua (desde el inicio de `E0` el 5 de noviembre de 2026 hasta el corte del 21 de noviembre de 2026, equivalente a **$16\text{ días} = 384\text{ horas}$ de operación continua monitorizada**), se registraron los incidentes en las bitácoras PSP (`calidad/defectos-*.csv`):

- **Tiempo Total de Operación Monitorizada ($T_{\text{total}}$):** $384\text{ horas}$ ($23,040\text{ minutos}$).
- **Número de Incidentes en Integración / CI ($N_{\text{fallos}}$):** Durante el periodo ocurrieron únicamente **$2$ incidentes de entorno/integración** antes de la estabilización completa (`DEF-DAV-01`: timeout de 8s en consulta `robots.txt` y `DEF-DAV-02`: ajuste de `permissions: contents: write` en GitHub Actions). El resto de los defectos registrados en PSP fueron detectados y removidos en pruebas unitarias locales antes de subir a producción.
- **Tiempo Total de Reparación / Inactividad ($T_{\text{downtime}}$):** $10\text{ min} + 7\text{ min} = 17\text{ minutos}$ ($0.2833\text{ horas}$).

### 5.1 Cálculo Formal de Indicadores de Fiabilidad

1. **Tiempo Medio Entre Fallos (*MTBF — Mean Time Between Failures*):**
   $$\text{MTBF} = \frac{T_{\text{total}} - T_{\text{downtime}}}{N_{\text{fallos}}} = \frac{384 - 0.2833}{2} = \mathbf{191.86\text{ horas}} \quad (\approx 8\text{ días continuos sin incidentes})$$
2. **Tiempo Medio de Recuperación / Reparación (*MTTR — Mean Time To Repair*):**
   $$\text{MTTR} = \frac{T_{\text{downtime}}}{N_{\text{fallos}}} = \frac{17\text{ minutos}}{2} = \mathbf{8.50\text{ minutos}} \quad (\mathbf{0.1417\text{ horas}})$$
3. **Disponibilidad Operativa del Sistema (*System Availability $A$*):**
   $$A = \left( \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} \right) \times 100 = \left( \frac{191.8583}{191.8583 + 0.1417} \right) \times 100 = \mathbf{99.926\%} \ge 95.0\% \text{ (Meta Sello TDL)}$$

---

## 6. Seguridad DevSecOps: Auditoría de Secretos (`gitleaks`) y Dependencias (`pip-audit`)

El observatorio implementa una arquitectura **Zero-Secrets & Zero-Cost**:

1. **Prevención y Escaneo de Secretos (`gitleaks` / Regex CI Check):**
   - Ningún archivo del repositorio contiene llaves privadas, tokens de BANXICO, ni API keys de servicios cartográficos (se eliminaron por completo proveedores que solicitan llave como CartoDB con API key o Google Maps comercial, utilizando **Esri ArcGIS World Imagery & Reference Overlays** y **OpenStreetMap** públicos).
   - El token opcional `BANXICO_TOKEN` se inyecta exclusivamente mediante variables de entorno efímeras (`os.environ.get("BANXICO_TOKEN")` desde GitHub Secrets `${{ secrets.BANXICO_TOKEN }}`).
   - La prueba automatizada `test_entrypoints_and_zero_hardcoded_secrets` en `tests/test_pipeline.py` escanea el código fuente en cada ejecución de `pytest` garantizando **$0$ secretos expuestos**.
2. **Auditoría de Vulnerabilidades en Dependencias (`pip-audit`):**
   - El archivo [`requirements.txt`](../requirements.txt) fija cotas mínimas seguras de paquetes científicos mantenidos activamente (`pandas>=2.1.0`, `numpy>=1.26.0`, `scipy>=1.11.0`, `scikit-learn>=1.4.0`, `statsmodels>=0.14.0`, `pandera>=0.20.0`, `geopandas>=0.14.0`, `streamlit>=1.32.0`), con **$0$ vulnerabilidades críticas abiertas**.

---

## 7. Matriz de Gestión de Riesgos Técnicos y de Calidad (Sección 7 IEEE 730)

| ID Riesgo | Descripción del Riesgo | Probabilidad | Impacto | Nivel | Estrategia de Mitigación y Plan de Contingencia Implementado |
| :--- | :--- | :-: | :-: | :-: | :--- |
| **RSQ-01** | Indisponibilidad temporal o falta de token en la API REST del SIE de BANXICO durante la ejecución en GitHub Actions. | Media | Alto | **Alto** | `fetch_banxico_macro_series()` en `src/extract_bronze.py` implementa un bloque `try/except` con *timeout* de 15s y conmutación automática (*graceful fallback*) a la serie histórica certificada de 36 meses, garantizando $100\%$ de continuidad en CI/CD. |
| **RSQ-02** | Ingesta de anuncios inmobiliarios con errores graves de captura (superficies negativas, metrajes $>1,200\text{ m}^2$ o precios nulos/negativos) que corrompan los modelos SARIMA o PCA. | Alta | Crítico | **Crítico** | Puerta de Calidad automática con `Pandera` (`lazy=True`) en `src/pipeline_e1.py`. Los registros corruptos nunca entran a Capa Plata ni se borran en silencio: se aíslan en `data/silver/inmobiliario/cuarentena_inmobiliario.csv` con su motivo documentado. |
| **RSQ-03** | Bloqueo `HTTP 403` o marcas de agua `"API KEY REQUIRED"` en los mosaicos cartográficos al visualizar el mapa interactivo localmente o en Streamlit. | Media | Medio | **Medio** | Reingeniería en `src/pipeline_e2.py` usando mosaicos satelitales híbridos abiertos de **Esri WorldImagery + Esri Reference Overlays** y **OpenStreetMap**, verificados por `test_geospatial_and_full_lineage_e2` para asegurar $0$ referencias a `cartocdn.com`. |
| **RSQ-04** | Pérdida de trazabilidad al agregar microdatos en los cubos analíticos de la Capa Oro (`E1`, `E2`, `E3` y `Geoespacial`). | Baja | Alto | **Medio** | Propagación automática de linaje criptográfico (`SHA-256`) y generación del catálogo maestro `data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv` auditado al $100\%$ ($0$ huérfanos). |
| **RSQ-05** | Regresión funcional o caída de cobertura de pruebas por debajo del $60\%$ al agregar nuevos módulos estadísticos. | Baja | Alto | **Medio** | Workflow `.github/workflows/ci.yml` que bloquea cualquier cambio si `ruff check` falla o si `pytest --cov=src --cov-fail-under=60` reporta menos del $60\%$ (actualmente en **$89.54\%$**). |
