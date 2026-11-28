# Relatoría Técnica de Etapa — Entrega E3 (Optimización Medida del Pipeline, Publicación de Dataset Abierto, Análisis Multivariado y Diseño UI PropTech en Figma)

**Proyecto Integrador:** Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional (ZMVM & Colima – Villa de Álvarez)  
**Etapa:** `E3` — Optimización Cuantitativa del Pipeline, *Datasheet for Datasets*, PCA/MANOVA, Modelos de Procesos y Sistema UI Figma  
**Tag de Liberación:** `e3`  
**Autores:**  
- **Juan Antonio Ortiz Hinojosa**  
- **Diego Alberto Virgen Cuéllar**  

---

## 1. Objetivo de la Etapa E3 y Enfoque Dual (Académico + Comercial B2B)

El objetivo central de la **Entrega E3** consistió en transformar nuestro prototipo funcional de ingeniería de datos en una plataforma de grado productivo con **mejoras de desempeño empíricamente verificables**, publicando formalmente los conjuntos de datos curados de la Capa Oro bajo licencia abierta con su ficha técnica estandarizada ([`docs/E3/datasheet.md`](E3/datasheet.md)) y elevando el diseño visual de los artefactos interactivos mediante **Figma MCP** ([Sistema UI TDL PropTech en Figma](https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX)).

Este enfoque responde simultáneamente a dos audiencias exigentes:
1. **Evaluación Académica Tripartita (3 Profesores):** Ingeniería de Datos (optimización algorítmica, DataOps y publicación abierta), Estadística Aplicada (normalidad de Mardia, distancias de Mahalanobis, PCA Biplot y MANOVA Wilks/Pillai) y Calidad en los Sistemas de Información (MoProSoft, CMMI, ISO 9001, retrospectiva PSP y Sello TDL).
2. **Presentación Comercial B2B (Empresas Inmobiliarias, Desarrolladoras y AMPI):** Interfaz ejecutiva estilo SaaS financiero/PropTech, libre de saturación de emojis, con íconos vectoriales SVG limpios, tipografía corporativa (`Plus Jakarta Sans` + `JetBrains Mono`) y modelo de suscripción sin costos de infraestructura cloud (\$0.00 USD).

---

## 2. Optimización Formal y Medida del Pipeline (`Antes vs. Después`)

Guiados por los hallazgos del experimento factorial $2^3$ de la etapa previa (donde el factor *Estrategia de Validación y Procesamiento* explicó más del $60\%$ de la varianza en latencia), implementamos y auditamos en [`src/benchmark_optimizacion_e3.py`](../src/benchmark_optimizacion_e3.py) cinco refactorizaciones estructurales sobre el lote combinado real de **2,163 registros crudos** (`1,299 ZMVM + 864 Colima – Villa de Álvarez`) evaluados en $R = 7$ corridas repetidas con `time.perf_counter()`, `tracemalloc` y `DataFrame.memory_usage(deep=True)`:

1. **Eliminación total de bucles fila-a-fila (`iterrows`) por vectorización en C (`NumPy`/`Pandas`):** El parseo monetario con expresión regular precompilada (`Series.str.replace` + `pd.to_numeric`) sustituyó la conversión secuencial en Python.
2. **Cruce hash indexado $O(N)$ vs. búsqueda lineal $O(N \times M)$:** Las series macroeconómicas de BANXICO/INEGI se indexan en memoria por `periodo_mensual` y se proyectan mediante `Series.map()`.
3. **Puerta de Calidad Vectorizada (`Pandera` + máscaras booleanas $O(N)$):** Sustituyó filtros manuales dispersos por validación esquemática declarativa que desvía el $100\%$ de las anomalías a `cuarentena_inmobiliario.csv` con motivo explícito.
4. **Imputación estratificada sin bucles (`groupby().transform('median')`) y Winsorización `np.clip` ($P_{1\%}-P_{99\%}$).**
5. **Compactación de tipos (*downcasting*) y proyección columnar:** Conversión de `float64 -> float32`, `int64 -> int16` y cadenas repetitivas (`colonia`, `alcaldia_municipio`, `tipo_inmueble`, `periodo_mensual`) al tipo diccionario `category`.

### Resultados Cuantitativos Auditados ([`reporte_optimizacion_e3.json`](../data/gold/inmobiliario/reporte_optimizacion_e3.json))

| Dimensión Auditada (`N = 2,163` registros, `7` réplicas) | Antes (Pipeline Base Iterativo) | Después (Pipeline Optimizado E3) | Mejora Absoluta | Mejora Relativa / Factor |
| :--- | :-: | :-: | :-: | :-: |
| **Tiempo Medio de Ejecución** | $3,422.95\text{ ms}$ | **$638.17\text{ ms}$** | $-2,784.78\text{ ms}$ | **$-81.36\%$ ($5.36\times$ más rápido)** |
| **Latencia P95 del Lote Completo** | $3,815.14\text{ ms}$ | **$733.91\text{ ms}$** | $-3,081.23\text{ ms}$ | **$-80.76\%$ ($5.20\times$ menor P95)** |
| **Uso Pico de Memoria Dinámica (`tracemalloc` Heap)** | $9.492\text{ MiB}$ | **$2.561\text{ MiB}$** | $-6.931\text{ MiB}$ | **$-73.02\%$ pico de memoria** |
| **Huella en RAM del Dataset Procesado** | $4,110.08\text{ KiB}$ | **$222.61\text{ KiB}$** | $-3,887.47\text{ KiB}$ | **$-94.58\%$ huella en RAM** |
| **Errores y Defectos Infiltrados a Capa Analítica** | $207\text{ defectos}$ | **$0\text{ defectos}$** | $-207\text{ defectos}$ | **$-100.00\%$ ($8$ en cuarentena, $0$ nulos)** |

> **Desglose de la reducción del 100% de errores infiltrados:** En el pipeline sin optimizar se infiltraban silenciosamente **3 duplicados** primarios, **3 superficies** físicamente implausibles ($<20\text{ m}^2$ o $>1,200\text{ m}^2$), **2 rentas inválidas** ($\le \$1,500$), **48 etiquetas tipológicas heterogéneas** y **151 celdas nulas** sin imputar ($207$ defectos totales). Tras la optimización E3, los 8 registros corruptos quedan aislados en cuarentena con trazabilidad, las 48 categorías quedan homologadas y las 151 celdas faltantes se imputan según su mecanismo estadístico (MCAR/MAR/MNAR), entregando **0 errores en Capa Plata y Capa Oro**.

---

## 3. Publicación de Dataset Abierto y Datasheet Estandarizado (`docs/E3/datasheet.md`)

En [`docs/E3/datasheet.md`](E3/datasheet.md) (sincronizado con [`data/gold/inmobiliario/DATASHEET.md`](../data/gold/inmobiliario/DATASHEET.md)) documentamos bajo el estándar internacional *Datasheets for Datasets* (Gebru et al., 2021) los cubos analíticos y geoespaciales publicados bajo licencias **`CC BY 4.0`** y **`ODbL 1.0`**:
- **100 registros auditados en Capa Oro** (`92` de ZMVM + `8` de Colima – Villa de Álvarez) con **100% de completitud ISO/IEC 25012** y **100% de linaje `SHA-256`** en `catalogo_linaje_oro_a_bronce.csv`.
- **24 polígonos georreferenciados unificados** en `oro_geoespacial_maestro_unificado.geojson` y **2,155 inmuebles validados en Capa Plata** (`1,291 ZMVM + 864 Colima`) listos para descarga abierta desde el repositorio y desde `tablero/app.py`.

---

## 4. Análisis Multivariado (`PCA` & `MANOVA`) y Rediseño UI/UX con Figma MCP

1. **Hallazgos Multivariados (`docs/E3/analisis_multivariado_pca_manova.ipynb`):**
   - Las primeras dos componentes principales capturan más del **$83.6\%$ de la varianza total** en ZMVM (y $>82\%$ en Colima–Villa de Álvarez), separando ortogonalmente **PC1 (Consolidación Urbana, Equipamiento DENUE y Precio/$m^2$)** frente a **PC2 (Rentabilidad *Yield* Anual vs. Días de Vacancia)**.
   - El **MANOVA multifactorial** (Lambda de Wilks y Traza de Pillai, $p < 0.0001$) demuestra diferencias multivariadas estadísticamente significativas entre sub-zonas y tipologías habitacionales, fundamentando los perfiles comerciales de inversión.
2. **Sistema de Diseño Ejecutivo en Figma y Modernización Visual (`E2` + `tablero/app.py`):**
   - Creamos en Figma el archivo maestro [**Observatorio Inmobiliario TDL — PropTech Design System & App**](https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX) con colecciones formales de tokens (`TDL PropTech Colors` y `TDL Spacing & Radius`) y componentes reutilizables (`KPI Metric Card`, `Map FlyTo Pill` y `Map Zone Popup Card`).
   - En el mapa maestro [`docs/E2/mapa_interactivo_zmvm.html`](E2/mapa_interactivo_zmvm.html) mantuvimos intacta toda la cartografía satelital híbrida (`Esri.WorldImagery` + DENUE + OSM + `flyTo`), reemplazando el $100\%$ de los emojis por **íconos vectoriales SVG en línea** y renovando las tarjetas flotantes, *tooltips* de precio por $m^2$ y *popups* con tipografía `Plus Jakarta Sans` y `JetBrains Mono`.
   - Finalmente, trasladamos esta misma identidad visual B2B a la aplicación web ejecutiva [`tablero/app.py`](../tablero/app.py), integrando la vista interactiva de optimización del pipeline E3, la descarga directa del dataset abierto y los planes comerciales SaaS listos para demostración ante sinodales e inversionistas.
