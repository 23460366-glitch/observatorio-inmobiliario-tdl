# Datasheet for Datasets: Capa Oro y Capa Plata del Observatorio Inmobiliario (ZMVM & Colima – Villa de Álvarez)

**Estándar de Documentación:** *Datasheets for Datasets* (Gebru et al., 2021) & ISO/IEC 25012 (*Data Quality Model*)  
**Versión del Dataset:** `v3.2-gold-tdl` (Liberación `tag: e3` • Certificado **Sello Trusted Data Lab**)  
**Ubicación de los Conjuntos de Datos Publicados:**  
- Capa Oro Analítica y Geoespacial: [`data/gold/inmobiliario/`](../../data/gold/inmobiliario/)  
- Capa Plata Auditada: [`data/silver/inmobiliario/`](../../data/silver/inmobiliario/)  
**Licencias Abiertas:** **Creative Commons Attribution 4.0 International (`CC BY 4.0`)** + **Open Database License (`ODbL 1.0`)** + **Términos de Libre Uso INEGI / BANXICO**  
**Autores y Curadores:**  
- **Juan Antonio Ortiz Hinojosa**  
- **Diego Alberto Virgen Cuéllar**  

---

## 1. Motivación (*Motivation*)

1. **¿Con qué propósito se creó este conjunto de datos?**
   - Se creó para eliminar la asimetría de información y la carencia de series históricas limpias, georreferenciadas y cruzadas con indicadores macroeconómicos oficiales en el mercado de renta habitacional de México, cubriendo dos mercados estratégicos contrastantes:
     1. **Zona Metropolitana del Valle de México (ZMVM):** 16 colonias representativas en Miguel Hidalgo, Cuauhtémoc, Benito Juárez y Naucalpan.
     2. **Zona Metropolitana de Colima – Villa de Álvarez:** 8 sectores de alta demanda residencial, comercial y universitaria (UdeC).
   - Respalda decisiones académicas y corporativas (B2B PropTech) en cuatro ejes cuantitativos: pronóstico econométrico trimestral (`E1`), simulación experimental *What-If* de contratos a 24 meses (`E2`), optimización del pipeline y análisis multivariado PCA/MANOVA de rentabilidad *Yield %* (`E3`), y operación comercial SaaS certificada (`E4`).
2. **¿Quién creó el dataset y en nombre de qué entidad?**
   - Fue diseñado, procesado y auditado por **Juan Antonio Ortiz Hinojosa** y **Diego Alberto Virgen Cuéllar** dentro del proyecto integrador **Trusted Data Lab**.
3. **¿Existe financiamiento externo o dependencia de APIs de pago?**
   - **No.** El dataset y su arquitectura automatizada operan con **Costo Operativo \$0.00 USD**, empleando exclusivamente fuentes abiertas gubernamentales y comunitarias sin llaves comerciales ni secretos expuestos.

---

## 2. Composición (*Composition*)

1. **¿Qué representan las instancias que componen el dataset publicado?**
   - Cada instancia en **Capa Plata** representa una oferta validada de arrendamiento residencial mensual enriquecida con variables macroeconómicas (BANXICO/INEGI) y métricas espaciales exactas en metros (`EPSG:32614`).
   - Cada instancia en **Capa Oro** representa un cubo agregado multidimensional o polígono geoespacial certificado con **100% de trazabilidad criptográfica `SHA-256`** hacia sus registros fuente en Capa Bronce.

| Capa | Archivo Publicado | Filas | Columnas | Granularidad / Unidad de Observación | Propósito Analítico y Comercial |
| :---: | :--- | :-: | :-: | :--- | :--- |
| **Oro** | [`oro_e1_pronostico_mensual_trimestral.csv`](../../data/gold/inmobiliario/oro_e1_pronostico_mensual_trimestral.csv) | 36 | 22 | 1 fila por mes (`2023-11` a `2026-10`) | Series de tiempo SES, Holt, Holt-Winters y SARIMA cruzadas con TIIE 28d, INPC Vivienda y FIX. |
| **Oro** | [`oro_e2_simulacion_whatif_24m.csv`](../../data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv) | 28 | 22 | `(modalidad_contrato, descuento_pct, subzona_id)` | Simulación *What-If* de vacancia, ocupación e ingreso efectivo acumulado a 24 meses. |
| **Oro** | [`oro_e3_comparacion_multivariada_yield.csv`](../../data/gold/inmobiliario/oro_e3_comparacion_multivariada_yield.csv) | 12 | 26 | Diseño $4 \times 3$: `(subzona_id, tipo_inmueble)` | Análisis multivariado (Mardia, Mahalanobis, PCA Biplot y MANOVA Wilks/Pillai) de *Yield %*. |
| **Oro** | [`oro_geoespacial_colonias_denue_osm.csv`](../../data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv) | 16 | 28 | 1 fila por colonia / AGEB en ZMVM | Cartografía coroplética, densidad DENUE en 500m y distancia métrica a Metro/Metrobús OSM. |
| **Oro** | [`oro_colima_zm.csv`](../../data/gold/inmobiliario/oro_colima_zm.csv) | 8 | 39 | 1 fila por zona estratégica en Colima – Villa de Álvarez | Inteligencia comercial local (AMPI / desarrolladoras), plusvalía a 36 meses, *Yield %* y equipamiento UdeC/DENUE. |
| **Oro (GIS)** | [`oro_geoespacial_maestro_unificado.geojson`](../../data/gold/inmobiliario/oro_geoespacial_maestro_unificado.geojson) | 24 | 20 | 24 polígonos (`16 ZMVM + 8 Colima-VdeA`) en `EPSG:4326` | Fuente geoespacial única para el mapa satelital maestro `Folium` y la cámara 3D `PyDeck`. |
| **Oro (Linaje)** | [`catalogo_linaje_oro_a_bronce.csv`](../../data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv) | 100 | 13 | 1 fila por cada registro de las 5 tablas Oro (`92 ZMVM + 8 Colima`) | Auditoría completa `Oro -> Bronce` con IDs primarios `PROP-*`, lotes origen, fechas UTC y hashes `SHA-256`. |
| **Oro (E3 Perf)** | [`comparativa_optimizacion_e3.csv`](../../data/gold/inmobiliario/comparativa_optimizacion_e3.csv) | 5 | 7 | Métricas Antes vs. Después del pipeline | Evidencia cuantitativa de reducción de tiempo, memoria RAM/Heap y defectos en la Entrega E3. |
| **Plata** | [`rentas_zmvm_plata_geolocalizado_e2.csv`](../../data/silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv) | 1,291 | 44 | Ofertas limpias y georreferenciadas (ZMVM, 36m) | Base granular auditada post-`Pandera` para modelado econométrico y espacial en ZMVM. |
| **Plata** | [`rentas_colima_plata_limpio.csv`](../../data/silver/inmobiliario/rentas_colima_plata_limpio.csv) | 864 | 28 | Ofertas limpias y georreferenciadas (Colima-VdeA, 36m) | Base granular auditada post-`Pandera` para Colima y Villa de Álvarez (36 meses continuos). |
| **Cuarentena** | [`cuarentena_inmobiliario.csv`](../../data/silver/inmobiliario/cuarentena_inmobiliario.csv) | $\ge 8$ | 24 | Registros rechazados con columna `motivo_cuarentena` | Evidencia auditable de política de **cero borrado silencioso** ante anomalías de esquema o rango. |

2. **¿Existen datos faltantes o huecos temporales?**
   - **No (`0.00%` de celdas nulas en todas las tablas de Capa Oro y Capa Plata).** La cobertura temporal abarca **36 periodos mensuales continuos (`2023-11` a `2026-10`, 0 huecos)**.
3. **¿Contiene información confidencial o datos personales identificables (PII)?**
   - **Cero PII.** Cumple estrictamente con la LFPDPPP: no almacena nombres de propietarios, teléfonos, correos electrónicos ni números exteriores exactos. Todos los identificadores son seudónimos deterministas (`PROP-*`) y las coordenadas emplean **k-anonimato espacial (*spatial cloaking* de $\pm 250\text{ m}$)** a nivel centroide de colonia/AGEB.

---

## 3. Proceso de Recolección (*Collection Process*)

1. **¿Cómo se recolectaron e integraron los datos?**
   - **Fuente Macroeconómica Oficial (BANXICO SIE & INEGI BIE):** Series mensuales de TIIE a 28 días (`SF43783`), INPC General (`SP1`), INPC Alquiler de Vivienda (`SP74625`) y Tipo de Cambio FIX (`SF43718`).
   - **Fuente Inmobiliaria Residencial (ZMVM & Colima–Villa de Álvarez):** Snapshots históricos estructurados de ofertas residenciales en 24 zonas urbanas durante 36 meses consecutivos (`src/extract_bronze.py`).
   - **Fuente Geoespacial Especializada (DENUE INEGI + MGN + OpenStreetMap):** Polígonos y claves `cve_ageb_inegi` del Marco Geoestadístico Nacional, densidad de unidades económicas comerciales/educativas en buffers de $500\text{ m}$ (DENUE SCIAN) y nodos de transporte masivo / vialidades primarias en OpenStreetMap (`src/pipeline_e2.py`).
2. **¿Qué controles éticos y técnicos rigen la recolección?**
   - Verificación programática de `robots.txt` (`urllib.robotparser`), respeto de `crawl-delay >= 1.5s`, cabeceras identificables del proyecto académico y programación desatendida mediante GitHub Actions (`.github/workflows/captura_diaria.yml` y `.github/workflows/bronze_capture.yml`).

---

## 4. Preprocesamiento, Limpieza y Optimización (`E1`–`E3`) (*Preprocessing / Cleaning / Labeling*)

1. **Estandarización Vectorizada y Homologación (`E1` & `E3`):**
   - Limpieza vectorizada con expresiones regulares precompiladas en C (`Series.str.replace` + `pd.to_numeric`) para montos monetarios, normalización temporal `YYYY-MM`, cruce hash indexado $O(N)$ con series macroeconómicas y homologación al dominio canónico `{depto_1rec, depto_2rec, casa}`.
2. **Puerta de Calidad Esquemática (`Pandera`) y Aislamiento en Cuarentena:**
   - Validación automática de tipos, dominios cerrados, no duplicidad en `(id_propiedad, periodo_mensual)` y límites físicos plausibles ($20 \le \text{superficie\_m2} \le 1,200$; $1,500 < \text{renta\_lista\_mensual\_mxn} \le 500,000$). Todo registro anómalo se desvía con su diagnóstico a `cuarentena_inmobiliario.csv`.
3. **Imputación Estadística Diferenciada por Mecanismo (MCAR / MAR / MNAR):**
   - `estacionamientos` (**MCAR**, $p=1.00$): Moda condicional por tipología.
   - `superficie_m2` (**MAR**, $p=7.31\times 10^{-10}$): Mediana estratificada por `(subzona_id, tipo_inmueble, recamaras)`.
   - `cuota_mantenimiento_mxn` (**MNAR**, $p=1.56\times 10^{-29}$): Razón mediana zonal preservando la bandera indicadora `flag_mnar_mantenimiento`.
4. **Control de Valores Extremos, Proyección UTM y Compactación de Memoria (`E2` & `E3`):**
   - Detección cruzada con IQR, Z-Score Robusto (MAD) e `IsolationForest`, aplicando **Winsorización estratificada ($P_{1\%}-P_{99\%}$)**.
   - Cálculo exacto de distancias euclidianas en metros reproyectando geometrías de `EPSG:4326` a **`EPSG:32614` (UTM Zona 14N)**.
   - Optimización `E3` mediante *downcasting* (`float32`, `int16`, `category`) y reducción columnar hacia Capa Oro (`src/benchmark_optimizacion_e3.py`).

---

## 5. Casos de Uso Recomendados y No Recomendados (*Uses*)

### Casos de Uso Recomendados
- **Valuación Comercial e Inteligencia Inmobiliaria B2B:** Estimación objetiva de rentas por $m^2$, renta mensual esperada (ej. departamento tipo de $70\text{ m}^2$) y *Yield* bruto anual para asesores inmobiliarios (AMPI), desarrolladoras habitacionales, fondos patrimoniales e inquilinos en ZMVM y Colima–Villa de Álvarez.
- **Investigación Econométrica y Pronóstico de Series de Tiempo:** Entrenamiento y *backtesting* de modelos SARIMAX, suavizamiento exponencial Holt-Winters y elasticidad inflación-vivienda.
- **Planeación Urbana y Ciencia de Datos Geoespacial:** Estudios multivariados (PCA, MANOVA, clustering espacial) sobre accesibilidad al transporte público, densidad comercial DENUE y dinámica habitacional universitaria.

### Casos de Uso No Recomendados (Restricciones Éticas y Metodológicas)
- **Coordinación o Fijación Colusoria de Rentas (*Algorithmic Price Fixing*):** Prohibido su uso para concertar alzas artificiales de alquiler o vulnerar límites legales de actualización inflacionaria previstos en la legislación civil aplicable.
- **Avalúo Catastral o Peritaje Jurídico de un Predio Individual:** Debido a la agregación zonal y al *spatial cloaking* ($\pm 250\text{ m}$) aplicado por privacidad, las cifras representan equilibrios estadísticos de mercado a nivel colonia/AGEB y no sustituyen un avalúo físico pericial de una vivienda particular.
- **Decisiones Automatizadas de Crédito o *Scoring* de Inquilinos:** El dataset describe características físicas y económicas de zonas e inmuebles, nunca solvencia crediticia personal.

---

## 6. Distribución, Licencia Abierta y Mantenimiento (*Distribution & Maintenance*)

- **Acceso y Formatos Abiertos:** Publicado directamente en este repositorio bajo el release `tag: e3` en formatos interoperables `CSV` (`UTF-8`) y `GeoJSON` (`RFC 7946`), además de contar con botones de descarga directa en el Observatorio Web (`tablero/app.py`).
- **Esquema de Licenciamiento Abierto:**
  - **Datos tabulares curados, cubos analíticos y documentación:** **Creative Commons Attribution 4.0 International (`CC BY 4.0`)**.
  - **Atributos cartográficos derivados de OpenStreetMap:** **Open Database License (`ODbL 1.0`)** (*© OpenStreetMap contributors*).
  - **Insumos estadísticos y geoestadísticos nacionales:** **Términos de Libre Uso de datos abiertos de INEGI y Banco de México**.
- **Mantenimiento y Validación Continua (DataOps):** Auditado automáticamente en cada *commit* y captura programada mediante GitHub Actions (`ruff`, `pytest --cov=src` $> 90\%$ de cobertura y validación esquemática `Pandera`).
