# 🏅 Modelos de Procesos, Retrospectiva PSP, DataOps y Solicitud del Sello TDL (`docs/calidad-sello-E3.md`)

**Proyecto Integrador:** Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM (*Trusted Data Lab*)  
**Etapa:** Entrega E3 y Preparación Final Demo Day E4  
**Fecha:** 21 de noviembre de 2026  
**Integrantes del Equipo:**  
- Juan Antonio Ortiz Hinojosa  
- Diego Alberto Virgen Cuéllar  

---

## 1. Comparativa de Modelos y Estándares de Calidad de Procesos (ISO 9001, MoProSoft, SPICE, CMMI y PSP/TSP)

La siguiente tabla contrasta los cinco marcos internacionales y nacionales de referencia para la gestión y mejora de procesos de ingeniería de software y datos:

| Atributo Comparativo | **ISO 9001:2015** | **MoProSoft (NMX-I-059-NYCE)** | **SPICE (ISO/IEC 33000 / 15504)** | **CMMI V2.0 / V3.0 (ISACA)** | **PSP / TSP (Watts Humphrey - SEI)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Alcance y Población Objetivo** | Organizaciones de cualquier sector industrial o de servicios. | Pequeñas y medianas empresas (PyMEs) mexicanas de desarrollo y mantenimiento de software. | Evaluación estandarizada de procesos de ciclo de vida de sistemas y software (ISO/IEC 12207). | Organizaciones medianas/grandes de ingeniería de software, sistemas, datos y servicios. | **Ingenieros individuales (PSP)** y **equipos pequeños de alto rendimiento de 2 a 20 personas (TSP)**. |
| **Estructura Arquitectónica** | 10 cláusulas basadas en el ciclo PHVA y pensamiento basado en riesgos. | **3 Categorías de Procesos:** Alta Dirección (DIR), Gerencia (GER: GP, GR, GO) y Operación (OPE: **ADM** y **DES**). | **Modelo Bidimensional:** Dimensión de Procesos (PRM) $\times$ Dimensión de Capacidad del Proceso (PAM). | Áreas de Práctica agrupadas en *Doing, Managing, Enabling, Improving*. | Progresión evolutiva personal (`PSP0` medición base $\rightarrow$ `PSP1` estimación $\rightarrow$ `PSP2` calidad y revisión de diseño/código $\rightarrow$ `TSP`). |
| **Escala de Madurez / Capacidad** | Certificación binaria (Cumple / No Cumple con auditoría de vigilancia). | **6 Niveles de Capacidad (0 al 5):** Incompleto, Realizado, Administrado, Establecido, Predecible, Optimizado. | **6 Niveles de Capacidad por proceso (0 al 5)** evaluados con atributos `PA 1.1` a `PA 5.2`. | **5 Niveles de Madurez Organizacional (1 al 5):** Inicial, Gestionado, Definido, Gestionado Cuantitativamente, en Optimización. | Métricas cuantitativas individuales y de equipo: Error de Estimación ($\text{APE}$), Densidad de Defectos, *Yield* de Remoción y Productividad. |
| **Fortaleza Principal en Ingeniería de Datos** | Estandarización documental y orientación a la satisfacción del cliente real. | Ligero, adaptado a equipos pequeños en México con roles claros en Administración de Proyectos (**ADM**) y Desarrollo (**DES**). | Permite evaluar un proceso aislado (ej. Aseguramiento de Calidad o Verificación) sin auditar toda la empresa. | En niveles 4 y 5 exige control estadístico de procesos y análisis causal de defectos (ideal para pipelines de datos). | Proporciona datos empíricos reales por fase (*Planeación, Diseño, Codificación, Pruebas*) desde el primer día. |

---

## 2. Autoevaluación de Nuestro Equipo frente a MoProSoft y CMMI (Con Brechas Concretas)

Evaluamos de forma honesta y rigurosa las prácticas reales ejecutadas en el repositorio `observatorio-inmobiliario-tdl` frente a **MoProSoft (NMX-I-059-NYCE)** y **CMMI**:

### 2.1 Autoevaluación frente a MoProSoft (Categoría Operación: `ADM` y `DES`)

| Proceso MoProSoft | Nivel Alcanzado por Nuestro Equipo | Evidencia Real en Nuestro Repositorio | Brechas Concretas Identificadas para Alcanzar Niveles 4–5 |
| :--- | :-: | :--- | :--- |
| **Administración de Proyectos Específicos (`OPE-ADM`)** | **Nivel 2 (Administrado) con atributos de Nivel 3 (Establecido)** | • Plan de proyecto y alcance en [`docs/E0/propuesta.md`](E0/propuesta.md).<br>• Plan SQA IEEE 730 en [`docs/plan-sqa.md`](plan-sqa.md).<br>• Seguimiento real de esfuerzo y calendario por entrega (`E0` a `E3`) en `calidad/tiempo-*.csv` y fichas `ENTREGA.md`. | **Brecha MoProSoft-01:** Aunque gestionamos riesgos técnicos y tiempos a nivel proyecto, no contamos con los procesos de la categoría **Alta Dirección (`DIR`)** ni **Gerencia de Recursos Humanos y Conocimiento (`GER-GR`)** a nivel multi-proyecto, ya que operamos como una célula única académica de 2 integrantes. |
| **Desarrollo y Mantenimiento de Software (`OPE-DES`)** | **Nivel 3 (Establecido)** | • Fases completas trazadas: Requisitos verificables (`RF-01` a `RNF-03`), Análisis/Diseño (`propuesta.md`, diagramas Mermaid), Construcción (`src/`), Integración y Pruebas (`tests/test_pipeline.py` con $89.54\%$ de cobertura y CI en `.github/workflows/ci.yml`). | **Brecha MoProSoft-02:** Para alcanzar el **Nivel 4 (Predecible)** en MoProSoft se requiere mantener cartas de control estadístico ($\bar{X}-R$) sobre múltiples proyectos históricos para establecer límites de capacidad organizacionales, mientras que nuestra línea base abarca 4 entregas de un único observatorio. |

### 2.2 Autoevaluación frente a CMMI (Capability Maturity Model Integration)

- **Nivel de Madurez Estimado del Equipo:** **Nivel 2 Completo (Gestionado) y Transición Sólida a Nivel 3 (Definido)**, con prácticas cuantitativas específicas de Nivel 4 (como nuestro **Experimento Factorial $2^3$** para optimizar el desempeño del pipeline y la medición de *Defect Removal Yield* en PSP).
- **Brechas Concretas frente a CMMI Nivel 3–4 Puro:**
  1. **Brecha CMMI-01 (Activos de Procesos Organizacionales — `PAD` / `OPD`):** Nuestros estándares de codificación (`pyproject.toml` con `ruff`), contratos de datos (`Pandera`) y plantillas (`ENTREGA.md`) están definidos para este repositorio, pero aún no están institucionalizados en una Biblioteca de Activos de Procesos Organizacionales (*Organizational Process Asset Library*) compartida entre múltiples equipos de desarrollo.
  2. **Brecha CMMI-02 (Gestión de Proveedores — `SAM`):** Consumimos APIs externas públicas (BANXICO SIE, INEGI DENUE, OpenStreetMap, Esri ArcGIS) mediante acuerdos de libre uso y mecanismos técnicos de fallback, pero sin contratos formales de Nivel de Servicio (SLA bilateral) con proveedores externos.

---

## 3. Retrospectiva Cuantitativa PSP (Calculada Directamente de `calidad/tiempo-*.csv` y `calidad/defectos-*.csv`)

Los siguientes indicadores fueron calculados leyendo directamente las **28 sesiones de trabajo** registradas en [`calidad/tiempo-juan-antonio-ortiz-hinojosa.csv`](../calidad/tiempo-juan-antonio-ortiz-hinojosa.csv) y [`calidad/tiempo-diego-alberto-virgen-cuellar.csv`](../calidad/tiempo-diego-alberto-virgen-cuellar.csv) y los **16 defectos** registrados en [`calidad/defectos-juan-antonio-ortiz-hinojosa.csv`](../calidad/defectos-juan-antonio-ortiz-hinojosa.csv) y [`calidad/defectos-diego-alberto-virgen-cuellar.csv`](../calidad/defectos-diego-alberto-virgen-cuellar.csv) a lo largo de las etapas `E0`, `E1`, `E2` y `E3`:

### 3.1 Consolidado de Esfuerzo y Precisión de Estimación por Integrante y Etapa

| Integrante | Etapa | Sesiones | Tiempo Planeado (min) | Tiempo Real (min) | Interrupciones (min) | Error de Estimación Acumulado ($\text{APE } \%$) | Cumple Meta $\text{OQ-01}$ ($\le 15\%$) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Juan Antonio Ortiz Hinojosa** | `E0` | 5 | $320$ | $335$ | $35$ | $+4.69\%$ | ✅ Sí |
| **Juan Antonio Ortiz Hinojosa** | `E1` | 4 | $260$ | $270$ | $25$ | $+3.85\%$ | ✅ Sí |
| **Juan Antonio Ortiz Hinojosa** | `E2` | 3 | $235$ | $245$ | $15$ | $+4.26\%$ | ✅ Sí |
| **Juan Antonio Ortiz Hinojosa** | `E3` | 2 | $115$ | $115$ | $10$ | $0.00\%$ | ✅ Sí |
| **Subtotal Juan Antonio** | **Total** | **14** | **$930\text{ min}$ ($15.50\text{ h}$)** | **$965\text{ min}$ ($16.08\text{ h}$)** | **$85\text{ min}$** | **$+3.76\%$** | ✅ **Sobresaliente** |
| **Diego Alberto Virgen Cuéllar** | `E0` | 5 | $315$ | $325$ | $30$ | $+3.17\%$ | ✅ Sí |
| **Diego Alberto Virgen Cuéllar** | `E1` | 4 | $265$ | $275$ | $25$ | $+3.77\%$ | ✅ Sí |
| **Diego Alberto Virgen Cuéllar** | `E2` | 3 | $230$ | $235$ | $15$ | $+2.17\%$ | ✅ Sí |
| **Diego Alberto Virgen Cuéllar** | `E3` | 2 | $95$ | $95$ | $10$ | $0.00\%$ | ✅ Sí |
| **Subtotal Diego Alberto** | **Total** | **14** | **$905\text{ min}$ ($15.08\text{ h}$)** | **$930\text{ min}$ ($15.50\text{ h}$)** | **$80\text{ min}$** | **$+2.76\%$** | ✅ **Sobresaliente** |
| **TOTAL EQUIPO (2 Integrantes)** | **`E0`–`E3`** | **28** | **$1,835\text{ min}$ ($30.58\text{ h}$)** | **$1,895\text{ min}$ ($31.58\text{ h}$)** | **$165\text{ min}$** | **$+3.27\%$** | ✅ **Meta $\le 15\%$ Cumplida** |

### 3.2 Distribución del Tiempo Real por Fase PSP del Equipo
- **Planeación e Investigación (`Planeacion` / `Investigacion_Diseno`):** $175\text{ min}$ (**$9.23\%$**)
- **Diseño Arquitectónico y Estadístico (`Diseno`):** $390\text{ min}$ (**$20.58\%$**)
- **Codificación e Implementación (`Codificacion`):** $1,010\text{ min}$ (**$53.30\%$**)
- **Pruebas, Revisión y Documentación Normativa (`Pruebas_Revision` / `Documentacion`):** $320\text{ min}$ (**$16.89\%$**)

### 3.3 Análisis de Defectos, Tiempo de Remoción y *Defect Removal Yield*

| Integrante | Total Defectos Registrados | Desglose por Tipo PSP | Fase de Inyección | Fase de Remoción | Tiempo Total de Corrección | Tiempo Medio por Defecto | *Defect Removal Yield* (Antes de Release) |
| :--- | :-: | :--- | :--- | :--- | :-: | :-: | :-: |
| **Juan Antonio Ortiz Hinojosa** (`DEF-JAO-01` a `08`) | **8** | • `20-Sintaxis_Parseo`: 2<br>• `50-Interfaz_Configuracion`: 2<br>• `60-Verificacion_Logica`: 2<br>• `40-Datos_Valores`: 1<br>• `10-Documentacion`: 1 | • `Codificacion`: 7<br>• `Diseno`: 1 | • `Pruebas_Locales`: 5<br>• `Revision_Codigo`: 3 | $59\text{ min}$ | $7.38\text{ min}$ | **$100.0\%$** ($8/8$ cerrados antes del tag) |
| **Diego Alberto Virgen Cuéllar** (`DEF-DAV-01` a `08`) | **8** | • `50-Interfaz_Configuracion`: 4<br>• `20-Sintaxis_Parseo`: 1<br>• `40-Datos_Valores`: 1<br>• `60-Verificacion_Logica`: 1<br>• `80-Entorno_Red`: 1 | • `Codificacion`: 8 | • `Pruebas_Locales`: 6<br>• `Revision_Codigo`: 2 | $57\text{ min}$ | $7.13\text{ min}$ | **$100.0\%$** ($8/8$ cerrados antes del tag) |
| **TOTAL EQUIPO** | **16** | **Predominio de configuración de librerías (`50`) y lógica/parseo (`20`, `60`)** | **$93.75\%$ en Codificación** | **$100\%$ en Revisión y Pruebas Locales** | **$116\text{ min}$** | **$7.25\text{ min}$** | **$100.0\%$ ($\ge 85\%$ Meta OQ-02)** |

> **Lección clave de la Retrospectiva PSP:** La curva de error de estimación ($\text{APE}$) convergió de $+4.69\%$ en `E0` hacia **$0.00\%$ en `E3`** conforme el equipo calibró su velocidad de desarrollo (*velocity*) en Python, `Pandera` y `GeoPandas`. Asimismo, invertir el **$37.47\%$ del esfuerzo total en Diseño + Revisión/Pruebas** permitió que los 16 defectos inyectados tuvieran un costo medio de remediación de apenas **$7.25\text{ minutos}$** y que ninguno llegara abierto a la rama principal certificada.

---

## 4. Tendencias Actuales Aplicadas a Nuestro Pipeline: DataOps y Observabilidad de Datos

Nuestro observatorio trasciende el desarrollo tradicional de scripts aislados adoptando dos paradigmas modernos de ingeniería de datos:

### 4.1 DataOps (*Data Operations*) Aplicado al Observatorio
1. **Contratos de Datos como Código (*Data Contracts as Code*):** En lugar de limpiar datos de forma imperativa y ad-hoc, la frontera entre la Capa Bronce y la Capa Plata está gobernada por un contrato declarativo versionado en Git (`build_pandera_pre_silver_schema()` en [`src/pipeline_e1.py`](../src/pipeline_e1.py)).
2. **Orquestación Continua y Pruebas Automatizadas (`CI/CD for Data`):** Dos pipelines independientes en GitHub Actions separan la verificación de código (`.github/workflows/ci.yml` corriendo `ruff` y `pytest --cov=src`) de la ingesta programada de datos (`.github/workflows/captura_diaria.yml` y `.github/workflows/bronze_capture.yml`), evitando que un cambio de código rompa silenciosamente la serie histórica de 36 meses.
3. **Reproducibilidad Determinista de Cuadernos y Artefactos:** Los 5 notebooks ejecutables (`limpieza.ipynb`, `pronostico_series_tiempo.ipynb`, `geoespacial_linaje.ipynb`, `experimento_factorial_2k.ipynb` y `analisis_multivariado_pca_manova.ipynb`) se construyen y validan programáticamente con `nbconvert --execute`, eliminando el antipatrón de *"en mi máquina sí corría el notebook"*.

### 4.2 Observabilidad de Datos (*Data Observability* — Los 5 Pilares en Nuestro Sistema)
Implementamos los 5 pilares modernos de la Observabilidad de Datos a través de los reportes JSON de auditoría (`reporte_auditoria_pipeline_e1.json` y `reporte_auditoria_pipeline_e2.json`) y la **Pestaña 4 del Observatorio Web (`tablero/app.py`)**:
1. **Frescura (*Freshness*):** Monitoreo automático de timestamps UTC (`fecha_captura_utc`, `generated_at_utc`) y continuidad de los 36 periodos mensuales.
2. **Distribución y Salud Estadística (*Distribution*):** Vigilancia de pruebas $\chi^2$ y $t$ de Welch sobre mecanismos de datos faltantes (MCAR/MAR/MNAR), Winsorización de atípicos ($P_{1\%}-P_{99\%}$) y bandera `flag_mnar_mantenimiento`.
3. **Volumen (*Volume*):** Aserciones automáticas en CI que verifican $\ge 36$ periodos macroeconómicos, $\ge 1,200$ registros en Capa Plata y $92$ registros exactos en los 4 cubos de Capa Oro.
4. **Esquema (*Schema*):** Validación estricta de tipos y dominios cerrados mediante `Pandera`, con aislamiento automático e inspección en vivo de anomalías en [`cuarentena_inmobiliario.csv`](../data/silver/inmobiliario/cuarentena_inmobiliario.csv).
5. **Linaje (*Lineage*):** Grafo y catálogo criptográfico `SHA-256` a nivel registro y lote ([`catalogo_linaje_oro_a_bronce.csv`](../data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv)) que conecta cada KPI del dashboard con su JSON crudo en Capa Bronce.

---

## 5. Checklist Oficial de Evidencia para Solicitar el Sello Trusted Data Lab (Sello TDL)

| # | Criterio Oficial del Sello TDL | Umbral Exigido | Valor Auditado en Nuestro Repositorio | Artefacto / Evidencia Verificable | Estado |
| :-: | :--- | :-: | :-: | :--- | :-: |
| **1** | **Disponibilidad Operativa del Sistema** | $\ge 95.0\%$ | **$99.93\%$** ($\text{MTBF}=191.86\text{ h}$, $\text{MTTR}=8.5\text{ min}$) | [`docs/plan-sqa.md`](plan-sqa.md) *(Sección 5)* y `.github/workflows/` | ✅ **CUMPLE** |
| **2** | **Completitud y Exactitud en Capa Oro (ISO/IEC 25012)** | $\ge 95.0\%$ | **$100.00\%$ Completitud** ($0$ nulos en Oro/Plata) y **$99.38\%$ Exactitud** en Puerta de Calidad | [`docs/evaluacion-iso-E2.md`](evaluacion-iso-E2.md) *(Sección 3)* y `data/gold/inmobiliario/*.csv` | ✅ **CUMPLE** |
| **3** | **Cobertura de Pruebas Automatizadas (`pytest --cov=src`)** | $\ge 60.0\%$ | **$89.54\%$ Cobertura Total** (`pipeline_e1`: $99\%$, `pipeline_e2`: $99\%$, `analytics`: $97\%$) | [`tests/test_pipeline.py`](../tests/test_pipeline.py) y [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | ✅ **CUMPLE** |
| **4** | **Seguridad y Costo \$0 (Secretos Expuestos)** | $0$ Secretos | **$0$ Secretos / $0$ API Keys de pago / $0$ Datos Personales (PII)** | `test_entrypoints_and_zero_hardcoded_secrets` y [`docs/etica-datos.md`](etica-datos.md) | ✅ **CUMPLE** |
| **5** | **Hallazgos Críticos de Auditoría Abiertos** | $0$ Críticos | **$0$ Hallazgos Críticos, Mayores o Menores abiertos** | [`docs/auditoria-cruzada-E2.md`](auditoria-cruzada-E2.md) *(Sección 3)* | ✅ **CUMPLE** |
| **6** | **Linaje, Reproducibilidad y Datos Abiertos (Datasheet)** | $100\%$ Trazable | **$100.0\%$ ($92/92$ filas Oro con hash `SHA-256`)**, 5 notebooks ejecutados y Datasheet | [`catalogo_linaje_oro_a_bronce.csv`](../data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv) y [`DATASHEET.md`](../data/gold/inmobiliario/DATASHEET.md) | ✅ **CUMPLE** |
