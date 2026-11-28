# Ficha de Entrega Técnica — Entrega E2 (`tag: e2`)

**Proyecto Integrador:** Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional (ZMVM & Colima – Villa de Álvarez) — *Trusted Data Lab*  
**Unidad:** Unidad 4 — Fuentes Especializadas GIS, Mapa Satelital Maestro con Sistema UI Figma (Íconos SVG), Diseño Experimental $2^k$, Evaluación Normativa ISO y Linaje Completo  
**Tag de Liberación:** `e2`  
**Sistema de Diseño UI/UX en Figma:** [`Observatorio Inmobiliario TDL — PropTech Design System & App`](https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX)  

---

## 1. Integrantes del Equipo y Bitácoras PSP

| Nombre Completo | Rol en Entrega E2 | Bitácora de Tiempo (PSP) | Bitácora de Defectos (PSP) |
| :--- | :--- | :--- | :--- |
| **Juan Antonio Ortiz Hinojosa** | Fuente Geoespacial (`GeoPandas`, DENUE INEGI, MGN y OpenStreetMap), Mapa Satelital Maestro Unificado (ZMVM + Colima) con Sistema UI Figma (0 emojis, íconos SVG), Diseño Factorial $2^3$ y Simulador *What-If* | [`calidad/tiempo-juan-antonio-ortiz-hinojosa.csv`](../../calidad/tiempo-juan-antonio-ortiz-hinojosa.csv) | [`calidad/defectos-juan-antonio-ortiz-hinojosa.csv`](../../calidad/defectos-juan-antonio-ortiz-hinojosa.csv) |
| **Diego Alberto Virgen Cuéllar** | Linaje Criptográfico `SHA-256` (`Bronce -> Plata -> Oro`), Declaración de Ética (`docs/etica-datos.md`), Evaluación ISO 25010/25012 (`docs/evaluacion-iso-E2.md`) y Auditoría Cruzada (`docs/auditoria-cruzada-E2.md`) | [`calidad/tiempo-diego-alberto-virgen-cuellar.csv`](../../calidad/tiempo-diego-alberto-virgen-cuellar.csv) | [`calidad/defectos-diego-alberto-virgen-cuellar.csv`](../../calidad/defectos-diego-alberto-virgen-cuellar.csv) |

---

## 2. Matriz de Evidencias Sincronizadas de las 3 Materias (Entrega `E2`)

| Materia / Eje del Proyecto Integrador | Entregable Requerido por Rúbrica (`E2`) | Archivo / Notebook / Mapa / Evidencia Exacta en el Repositorio | Estado y Resultado Cuantitativo |
| :--- | :--- | :--- | :--- |
| **1. Ingeniería de Datos y GIS** | **Fuente Especializada Integrada (Geoespacial):** DENUE (INEGI), Marco Geoestadístico (`cve_ageb_inegi`) y OpenStreetMap mediante `GeoPandas` con proyección métrica `EPSG:32614` (UTM 14N). | • [`src/pipeline_e2.py`](../../src/pipeline_e2.py)<br>• [`docs/E2/geoespacial_linaje.ipynb`](geoespacial_linaje.ipynb)<br>• [`data/gold/inmobiliario/oro_geoespacial_maestro_unificado.geojson`](../../data/gold/inmobiliario/oro_geoespacial_maestro_unificado.geojson)<br>• [`data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv`](../../data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv)<br>• [`data/gold/inmobiliario/oro_colima_zm.csv`](../../data/gold/inmobiliario/oro_colima_zm.csv) | **100% Cumplido:** 24 zonas georreferenciadas unificadas (`16 ZMVM + 8 Colima-VdeA`), 20 nodos de transporte/vialidad OSM y 2,155 inmuebles enriquecidos con distancia exacta en metros, densidad DENUE en 500m e Índice de Accesibilidad (`0-100`). |
| **1. Ingeniería de Datos, GIS y Diseño UI Figma** | **Mapa Satelital Maestro Unificado (`Esri.WorldImagery`) con Tipografía e Íconos SVG Figma:** Sin marcas de agua CARTO, sin errores `403`, con navegación rápida `flyTo`, etiquetas permanentes de precio auto-ocultables (`zoom < 11`) y tarjetas ejecutivas libres de emojis. | • [`docs/E2/mapa_interactivo_zmvm.html`](mapa_interactivo_zmvm.html)<br>• [`docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png`](mapa_coropletico_precio_equipamiento_zmvm.png)<br>• [Diseño Maestro en Figma](https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX) | **100% Cumplido:** Tipografía corporativa `Plus Jakarta Sans` + `JetBrains Mono`, **0 emojis** reemplazados al 100% por íconos vectoriales SVG, tarjetas *glassmorphism* de alta legibilidad y costo \$0 USD (0 API keys). |
| **1. Ingeniería de Datos y Gobernanza** | **Declaración de Ética y Legalidad (`docs/etica-datos.md`):** Términos de uso, auditoría `robots.txt`, licencias (`ODbL 1.0`, `CC BY 4.0`, Libre Uso INEGI/BANXICO), privacidad LFPDPPP y mitigación de sesgos. | • [`docs/etica-datos.md`](../etica-datos.md)<br>• [`data/bronze/inmobiliario/geoespacial_metadata_e2.json`](../../data/bronze/inmobiliario/geoespacial_metadata_e2.json) | **100% Cumplido:** Auditoría `robots.txt` programática, *k-anonimato espacial* ($\pm 250\text{ m}$), 0 datos personales (PII) y tabla de mitigación de 4 sesgos estadísticos. |
| **1. Ingeniería de Datos y Gobernanza** | **Linaje y Trazabilidad Completa (`Bronce -> Plata -> Oro`):** Cada registro en Capa Oro rastreable hasta su archivo origen en Bronce, IDs primarios y fecha de ingesta. | • [`data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv`](../../data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv)<br>• [`data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.json`](../../data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.json)<br>• [`docs/relatoria-E2.md`](../relatoria-E2.md) | **100% Cumplido:** **100 de 100 registros de Capa Oro ($100\%$)** (`92 ZMVM + 8 Colima`) trazables con hash `SHA-256` (`linaje_hash_lote_bronce`), IDs `PROP-*` y timestamps UTC ($0$ huérfanos). |
| **2. Estadística Aplicada / Diseño Experimental (`E2`)** | **Experimento Factorial $2^3$ y Simulación What-If (`E2`):** Diseño $2^3$ aleatorizado con 3 réplicas ($N=24$), ANOVA con interacción, validación de supuestos (Shapiro-Wilk y Levene), corrida de confirmación y comparativa **$2^4$ vs $2^{4-1}$ fraccionada**. | • [`docs/E2/experimento_factorial_2k.ipynb`](experimento_factorial_2k.ipynb)<br>• [`src/analytics_e3_e4.py`](../../src/analytics_e3_e4.py)<br>• [`data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv`](../../data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv)<br>• Pestaña 3 de [`tablero/app.py`](../../tablero/app.py) | **100% Cumplido:** Reducción de latencia del **$52.17\%$** en corrida de confirmación ($249.4\text{ ms} \rightarrow 119.3\text{ ms}$), ahorro experimental del $50\%$ en diseño $2^{4-1}$ (Resolución IV, $I=ABCD$) y simulador interactivo a 24 meses. |
| **3. Calidad en los Sistemas de Información (ISO & Auditoría)** | **Evaluación Normativa ISO/IEC 25010 e ISO/IEC 25012 y Reporte de Auditoría Cruzada (`docs/evaluacion-iso-E2.md` y `docs/auditoria-cruzada-E2.md`).** | • [`docs/evaluacion-iso-E2.md`](../evaluacion-iso-E2.md)<br>• [`docs/auditoria-cruzada-E2.md`](../auditoria-cruzada-E2.md)<br>• [`docs/plan-sqa.md`](../plan-sqa.md) | **100% Cumplido:** Las 8 características de ISO/IEC 25010 y las 5 dimensiones inherentes de ISO/IEC 25012 evaluadas ($100\%$ completitud y consistencia; **$0$ hallazgos críticos abiertos**). |

---

## 3. Vista Cartográfica Generada (`GeoPandas` + DENUE INEGI + OpenStreetMap)

![Mapa Coroplético ZMVM - Precio por m2, Transporte OSM y Equipamiento DENUE](mapa_coropletico_precio_equipamiento_zmvm.png)
