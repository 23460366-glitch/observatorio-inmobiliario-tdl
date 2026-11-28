# Datasheet for Datasets: Capa Oro y Capa Plata del Observatorio Inmobiliario (ZMVM & Colima – Villa de Álvarez)

**Estándar de Documentación:** *Datasheets for Datasets* (Gebru et al., 2021) & ISO/IEC 25012 (*Data Quality Model*)  
**Versión del Dataset:** `v3.2-gold-tdl` (Liberación `tag: e3` • Certificado **Sello Trusted Data Lab**)  
**Ficha Espejo Oficial E3:** [`docs/E3/datasheet.md`](../../../docs/E3/datasheet.md)  
**Licencias Abiertas:** **Creative Commons Attribution 4.0 International (`CC BY 4.0`)** + **Open Database License (`ODbL 1.0`)** + **Términos de Libre Uso INEGI / BANXICO**  
**Autores y Curadores:**  
- **Juan Antonio Ortiz Hinojosa**  
- **Diego Alberto Virgen Cuéllar**  

---

## 1. Motivación (*Motivation*)

1. **¿Con qué propósito se creó este conjunto de datos?**
   - Se creó para resolver la asimetría de información y la falta de series históricas limpias, cruzadas con indicadores macroeconómicos oficiales y equipamiento urbano georreferenciado, en el mercado de alquiler residencial de la **Zona Metropolitana del Valle de México (ZMVM, 16 colonias)** y la **Zona Metropolitana de Colima – Villa de Álvarez (8 sectores estratégicos)**.
   - Permite responder con rigor estadístico el pronóstico trimestral del precio por metro cuadrado (`E1`), la simulación *What-If* de políticas de descuento en contratos de 24 meses (`E2`), la optimización algorítmica y comparación multivariada PCA/MANOVA del rendimiento anual bruto (*Yield %*, `E3`) y la toma de decisiones comerciales B2B (`E4`).
2. **¿Quién creó el dataset y con qué modelo de costos?**
   - Desarrollado por **Juan Antonio Ortiz Hinojosa** y **Diego Alberto Virgen Cuéllar** dentro del proyecto integrador **Trusted Data Lab**, manteniendo estrictamente **Costo Operativo \$0.00 USD** y cero llaves comerciales expuestas.

---

## 2. Composición (*Composition*)

| Archivo en `data/gold/inmobiliario/` y `data/silver/inmobiliario/` | Filas | Columnas | Granularidad / Unidad de Observación | Propósito Analítico Principal |
| :--- | :-: | :-: | :--- | :--- |
| [`oro_e1_pronostico_mensual_trimestral.csv`](oro_e1_pronostico_mensual_trimestral.csv) | 36 | 22 | 1 fila por mes (`2023-11` a `2026-10`) | Modelos SES, Holt, Holt-Winters y SARIMA cruzados con INPC Vivienda, TIIE 28d y FIX. |
| [`oro_e2_simulacion_whatif_24m.csv`](oro_e2_simulacion_whatif_24m.csv) | 28 | 22 | `(modalidad_contrato, descuento_pct, subzona_id)` | Simulación *What-If* de vacancia, ocupación e ingreso efectivo acumulado a 24 meses. |
| [`oro_e3_comparacion_multivariada_yield.csv`](oro_e3_comparacion_multivariada_yield.csv) | 12 | 26 | Diseño factorial $4 \times 3$: `(subzona_id, tipo_inmueble)` | Comparación multivariada (ANOVA / MANOVA / PCA) de *Yield %*, precio/$m^2$ y equipamiento. |
| [`oro_geoespacial_colonias_denue_osm.csv`](oro_geoespacial_colonias_denue_osm.csv) | 16 | 28 | 1 fila por colonia/AGEB (`cve_ageb_inegi`) en ZMVM | Cartografía coroplética, Biplot PCA, densidad DENUE en 500m y distancia en metros a transporte OSM. |
| [`oro_colima_zm.csv`](oro_colima_zm.csv) | 8 | 39 | 1 fila por zona clave en Colima – Villa de Álvarez | Plusvalía a 36 meses, *Yield %*, densidad DENUE/UdeC y vialidades primarias OSM. |
| [`oro_geoespacial_maestro_unificado.geojson`](oro_geoespacial_maestro_unificado.geojson) | 24 | 20 | 24 polígonos unificados (`ZMVM` + `Colima-VdeA`) | Capa geoespacial maestra para visor satelital `Folium` y cámara 3D `PyDeck`. |
| [`catalogo_linaje_oro_a_bronce.csv`](catalogo_linaje_oro_a_bronce.csv) | 100 | 13 | 1 fila por cada registro de las 5 tablas Oro (`92 + 8`) | Trazabilidad 100% hacia IDs `PROP-*`, archivos Bronce, timestamps UTC y hashes `SHA-256`. |
| [`comparativa_optimizacion_e3.csv`](comparativa_optimizacion_e3.csv) | 5 | 7 | Métricas Antes vs. Después del pipeline E3 | Benchmark reproducible de tiempo (`5.36x`), memoria Heap (`-73.02%`), RAM (`-94.58%`) y errores (`-100%`). |
| [`rentas_zmvm_plata_geolocalizado_e2.csv`](../../silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv) | 1,291 | 44 | Ofertas validadas y georreferenciadas (ZMVM, 36m) | Serie granular limpia post-`Pandera` sin valores nulos ($0\%$). |
| [`rentas_colima_plata_limpio.csv`](../../silver/inmobiliario/rentas_colima_plata_limpio.csv) | 864 | 28 | Ofertas validadas y georreferenciadas (Colima, 36m) | Serie granular limpia post-`Pandera` para Colima y Villa de Álvarez ($0\%$ nulos). |

- **Datos faltantes:** **0.00% de celdas nulas** en Capa Plata y Capa Oro; 36 meses continuos sin brechas (`2023-11` a `2026-10`).
- **Privacidad (PII):** **Cero datos personales.** Identificadores seudonimizados (`PROP-*`) y *spatial cloaking* ($\pm 250\text{ m}$) conforme a la LFPDPPP.

---

## 3. Proceso de Recolección (*Collection Process*)

1. **Macroeconomía (BANXICO SIE / INEGI BIE):** Series mensuales TIIE 28d (`SF43783`), INPC General (`SP1`), INPC Vivienda (`SP74625`) y FIX (`SF43718`).
2. **Oferta Habitacional (ZMVM & Colima–Villa de Álvarez):** Snapshots históricos mensuales de 24 colonias/sectores durante 36 meses (`src/extract_bronze.py`).
3. **Geoespacial (INEGI MGN + DENUE + OpenStreetMap):** Polígonos AGEB, unidades económicas en radios de $500\text{ m}$ y nodos de transporte/vialidades primarias verificando `robots.txt` y `crawl-delay >= 1.5s`.

---

## 4. Preprocesamiento, Puerta de Calidad y Optimización (`Preprocessing & Cleaning`)

- **Vectorización y tipado (`src/pipeline_e1.py`, `src/benchmark_optimizacion_e3.py`):** Parseo monetario regex precompilado, cruce hash $O(N)$, *downcasting* (`float32`, `int16`, `category`) y proyección columnar (`-94.58%` huella RAM).
- **Puerta `Pandera` y Cuarentena:** Aislamiento del $100\%$ de registros fuera de rango o duplicados en `data/silver/inmobiliario/cuarentena_inmobiliario.csv` (**cero borrado silencioso**).
- **Imputación (MCAR/MAR/MNAR) y Winsorización:** Moda condicional (`estacionamientos`), mediana estratificada (`superficie_m2`), razón mediana + `flag_mnar_mantenimiento` (`cuota_mantenimiento_mxn`) y Winsorización $P_{1\%}-P_{99\%}$.
- **Cálculo Métrico GIS (`src/pipeline_e2.py`):** Distancias exactas en metros en proyección **`EPSG:32614` (UTM Zona 14N)**.

---

## 5. Usos Recomendados y No Recomendados (*Uses*)

- **Recomendados:** Valuación comercial e inteligencia de rentas B2B (AMPI, desarrolladoras, fondos e inquilinos), modelado econométrico SARIMA/Holt-Winters y estudios urbanos multivariados (PCA/MANOVA).
- **No Recomendados:** Fijación colusoria o especulativa de precios de alquiler, peritajes jurídicos individuales de predios sin inspección física o *scoring* crediticio personal.

---

## 6. Distribución y Licencia Abierta (*Distribution & Maintenance*)

- Distribuido en `CSV` (`UTF-8`) y `GeoJSON` (`EPSG:4326`) bajo licencia **Creative Commons Attribution 4.0 International (`CC BY 4.0`)**, **Open Database License (`ODbL 1.0`)** para derivados OSM y **Términos de Libre Uso INEGI/BANXICO**, con integración continua en `.github/workflows/ci.yml` y `.github/workflows/captura_diaria.yml`.
