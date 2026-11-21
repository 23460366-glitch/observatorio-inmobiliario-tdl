# 📄 Datasheet for Datasets: Capa Oro del Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM

**Estándar de Documentación:** *Datasheets for Datasets* (Gebru et al., 2021) & ISO/IEC 25012 (*Data Quality Model*)  
**Versión del Dataset:** `v3.0-gold-tdl` (Certificado con **Sello Trusted Data Lab**)  
**Ubicación en el Repositorio:** `data/gold/inmobiliario/` y `data/silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv`  
**Fecha de Publicación:** 21 de noviembre de 2026  
**Autores y Curadores:**  
- Juan Antonio Ortiz Hinojosa  
- Diego Alberto Virgen Cuéllar  

---

## 1. Motivación (*Motivation*)

1. **¿Con qué propósito se creó este conjunto de datos?**
   - Se creó para resolver la asimetría de información y la falta de series históricas limpias, cruzadas con indicadores macroeconómicos y equipamiento urbano georreferenciado, en el mercado de alquiler residencial de la **Zona Metropolitana del Valle de México (ZMVM)**. Permite responder con rigor estadístico tres preguntas fundamentales: pronóstico trimestral del precio por metro cuadrado (`E1`), simulación *what-if* de políticas de descuento en contratos de 24 meses (`E2`) y comparación multivariada del rendimiento anual bruto (*Yield %*) por tipología de inmueble y sub-zona urbana (`E3`).
2. **¿Quién creó el dataset y en nombre de qué entidad?**
   - Fue desarrollado por **Juan Antonio Ortiz Hinojosa** y **Diego Alberto Virgen Cuéllar** como activo central de datos abiertos del proyecto integrador **Trusted Data Lab (Entregas E0 a E4)**.
3. **¿Existe financiamiento o dependencia de APIs comerciales?**
   - **No.** El dataset y todo su pipeline de actualización operan bajo una arquitectura de **Costo Operativo \$0 USD**, utilizando exclusivamente fuentes públicas/abiertas oficiales (BANXICO SIE, INEGI BIE/DENUE/MGN y OpenStreetMap) sin requerir llaves de pago.

---

## 2. Composición (*Composition*)

1. **¿Qué representan las instancias que componen el dataset?**
   - La **Capa Plata Geolocalizada** ([`rentas_zmvm_plata_geolocalizado_e2.csv`](../../silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv)) contiene **$1,291$ instancias validadas de ofertas de renta habitacional** a lo largo de 36 meses consecutivos (`2023-11` a `2026-10`).
   - La **Capa Oro** (`data/gold/inmobiliario/`) está compuesta por **4 cubos analíticos certificados ($92$ registros agregados totales)** y **1 catálogo maestro de linaje**:

| Archivo en `data/gold/inmobiliario/` | Filas | Columnas | Granularidad / Unidad de Observación | Propósito Analítico Principal |
| :--- | :-: | :-: | :--- | :--- |
| [`oro_e1_pronostico_mensual_trimestral.csv`](oro_e1_pronostico_mensual_trimestral.csv) | $36$ | $22$ | 1 fila por mes (`2023-11` a `2026-10`) | Modelos de series de tiempo (SES, Holt, Holt-Winters, SARIMA) cruzados con INPC Vivienda, TIIE 28d y FIX. |
| [`oro_e2_simulacion_whatif_24m.csv`](oro_e2_simulacion_whatif_24m.csv) | $28$ | $22$ | 1 fila por `(modalidad_contrato, descuento_pct, subzona_id)` | Simulación *What-If* de vacancia, tasa de ocupación e ingreso efectivo acumulado a 24 meses. |
| [`oro_e3_comparacion_multivariada_yield.csv`](oro_e3_comparacion_multivariada_yield.csv) | $12$ | $26$ | Diseño factorial $4 \times 3$: `(subzona_id, tipo_inmueble)` | Comparación multivariada (ANOVA / MANOVA / PCA) de *Yield %*, precio/$m^2$ y equipamiento urbano. |
| [`oro_geoespacial_colonias_denue_osm.csv`](oro_geoespacial_colonias_denue_osm.csv) | $16$ | $28$ | 1 fila por colonia/AGEB (`cve_ageb_inegi`) en la ZMVM | Cartografía coroplética, Biplot PCA por colonia, densidad DENUE en 500m y distancia en metros a transporte OSM. |
| [`catalogo_linaje_oro_a_bronce.csv`](catalogo_linaje_oro_a_bronce.csv) | $92$ | $13$ | 1 fila por cada registro de las 4 tablas de Capa Oro | Auditoría 100% trazable hacia los IDs primarios (`PROP-*`), archivos crudos en Capa Bronce, fechas UTC y hashes `SHA-256`. |

2. **¿Existen datos faltantes o brechas temporales?**
   - **No ($0\%$ de celdas nulas en Capa Plata y Capa Oro).** La serie temporal cubre el $100\%$ de los 36 meses consecutivos sin huecos. Los valores faltantes presentes en la Capa Bronce cruda fueron diagnosticados e imputados en `E1` según su mecanismo estadístico (MCAR, MAR y MNAR).
3. **¿Contiene información confidencial o datos personales identificables (PII)?**
   - **Cero datos personales.** No incluye nombres, teléfonos, correos ni direcciones postales exactas. Los identificadores son hashes irreversibles (`PROP-XXXXXXXXXX`) y las coordenadas geográficas aplican **k-anonimato espacial (*spatial cloaking* de $\pm 250\text{ m}$)** dentro del polígono del AGEB/colonia.

---

## 3. Proceso de Recopilación y Captura (*Collection Process*)

1. **¿Cómo se adquirieron los datos de cada fuente?**
   - **Fuente 1 (Macroeconomía):** Consulta automatizada al API REST del Sistema de Información Económica (SIE) de BANXICO e INEGI (`SF43783` TIIE 28d, `SP1` INPC General, `SP74625` INPC Vivienda ZMVM y `SF43718` Tipo de Cambio FIX).
   - **Fuente 2 (Mercado de Rentas ZMVM):** Integración de snapshots históricos abiertos de ofertas residenciales en 16 colonias de 4 sub-zonas de la ZMVM (Miguel Hidalgo, Cuauhtémoc, Benito Juárez y Naucalpan).
   - **Fuente 3 (Geoespacial Especializada):** Polígonos de AGEB del Marco Geoestadístico Nacional (INEGI), conteo de unidades económicas de servicios y comercio del DENUE (INEGI SCIAN) en buffers de 500m y estaciones de transporte masivo de OpenStreetMap (Overpass API).
2. **¿Qué mecanismos éticos se emplearon durante la captura?**
   - Verificación programática previa de `robots.txt` (`urllib.robotparser`), pausas de cortesía (`crawl_delay >= 1.5s`), ejecución programada no intrusiva vía GitHub Actions (`.github/workflows/captura_diaria.yml`) y cabecera `User-Agent` académica identificable.

---

## 4. Preprocesamiento, Limpieza y Puerta de Calidad (*Preprocessing / Cleaning / Labeling*)

Todo el flujo de transformación está automatizado en [`src/pipeline_e1.py`](../../../src/pipeline_e1.py) y [`src/pipeline_e2.py`](../../../src/pipeline_e2.py):

1. **Homologación y Resolución de Conflictos:** Conversión de fechas `DD/MM/YYYY` a `YYYY-MM`, parseo de 37 cadenas monetarias (`"$32,500.00 MXN"`) a `float64` y estandarización de 48 etiquetas categóricas al dominio canónico `{depto_1rec, depto_2rec, casa}`.
2. **Puerta de Calidad Automática (`Pandera`) y Cuarentena:** Validación de unicidad `(id_propiedad, periodo_mensual)` y rangos físicos ($20 \le \text{superficie\_m2} \le 1,200$, $\text{renta\_lista} > 1,500$). Los **8 registros inválidos ($0.62\%$)** fueron aislados con su motivo exacto en [`data/silver/inmobiliario/cuarentena_inmobiliario.csv`](../../silver/inmobiliario/cuarentena_inmobiliario.csv) (**política de cero borrado silencioso**).
3. **Imputación Estadística (MCAR / MAR / MNAR):**
   - `estacionamientos` (28 casos, **MCAR**, $p=1.00$): Moda condicional por tipología.
   - `superficie_m2` (15 casos, **MAR**, $p=7.31\times 10^{-10}$): Mediana estratificada por `(subzona_id, tipo_inmueble, recamaras)`.
   - `cuota_mantenimiento_mxn` (108 casos, **MNAR**, $p=1.56\times 10^{-29}$): Razón mediana zonal + bandera explícita `flag_mnar_mantenimiento`.
4. **Tratamiento de Atípicos y Proyección Cartográfica:** Triangulación con IQR, Z-Score Robusto (MAD) e `IsolationForest`, aplicando **Winsorización estratificada ($P_{1\%}-P_{99\%}$)** en `precio_m2_winsor_mxn`. Reproyección a **`EPSG:32614` (UTM Zona 14N)** en `GeoPandas` para distancias exactas en metros.

---

## 5. Usos Recomendados y No Recomendados (*Uses*)

### ✅ Usos Recomendados
- **Valuación y Estimación de Rentas por Colonia y Tipología:** Benchmarking cuantitativo para administradores de propiedades, arrendadores, inquilinos e investigadores urbanos en la ZMVM.
- **Modelado Econométrico y Series de Tiempo:** Entrenamiento y validación de modelos SARIMAX, Holt-Winters y regresión dinámica con variables macroeconómicas de BANXICO.
- **Planeación Urbana y Análisis Multivariado GIS:** Estudio de la relación entre equipamiento económico DENUE, proximidad al transporte público masivo (Metro/Metrobús) y rentabilidad habitacional (*Yield %*).

### 🚫 Usos No Recomendados (Restricciones Éticas)
- **Fijación Colusoria o Especulativa de Precios:** No debe utilizarse para coordinar incrementos artificiales de renta que vulneren los topes de actualización inflacionaria previstos en el Código Civil de la CDMX.
- **Inferencia a Nivel Domicilio Individual:** Dado que las coordenadas incorporan *spatial cloaking* ($\pm 250\text{ m}$) para proteger la privacidad (LFPDPPP), no debe emplearse para peritajes catastrales de un predio individual sin inspección física.

---

## 6. Distribución, Mantenimiento y Licencia Abierta (*Distribution & Maintenance*)

- **Formato de Distribución:** Archivos abiertos `CSV` (codificación `UTF-8`), `GeoJSON` (`EPSG:4326`) y descarga directa desde la Pestaña 4 del Observatorio Web en Streamlit (`tablero/app.py`).
- **Licencia Abierta del Dataset:** Publicado bajo licencia **Creative Commons Attribution 4.0 International (`CC BY 4.0`)** para los datos tabulares/analíticos, manteniendo la atribución a **BANXICO/INEGI (Términos de Libre Uso)** y **OpenStreetMap Contributors (`ODbL 1.0`)** para las capas geoespaciales derivadas.
- **Mantenimiento Automatizado:** Actualizado y verificado continuamente mediante los flujos de GitHub Actions `.github/workflows/captura_diaria.yml`, `.github/workflows/bronze_capture.yml` y `.github/workflows/ci.yml`.
