# 📓 Relatoría Técnica de Etapa — Entrega E2 (Integración Geoespacial, Ética/Legalidad y Linaje Completo)

**Proyecto Integrador:** Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM  
**Etapa:** `E2` — Fuente Especializada Geoespacial (`GeoPandas`), Declaración de Ética y Linaje `Bronce -> Plata -> Oro`  
**Fecha:** 21 de noviembre de 2026  
**Autores:**  
- Juan Antonio Ortiz Hinojosa  
- Diego Alberto Virgen Cuéllar  

---

## 1. Introducción y Motivación de la Fuente Especializada

En la entrevista de campo realizada durante la etapa `E0`, el actor del sector inmobiliario enfatizó que el precio por metro cuadrado ($MXN/m^2$) y la velocidad de absorción de una vivienda en la Zona Metropolitana del Valle de México no dependen únicamente del metraje interno o de la inflación agregada (INPC), sino de la **micro-ubicación urbana**: específicamente, la distancia caminable a estaciones de transporte masivo (Metro, Metrobús, Suburbano) y la densidad de equipamiento comercial, educativo, hospitalario y recreativo en un radio inmediato de 500 metros.

Por esta razón, para la **Entrega E2** elegimos e integramos la **Fuente Especializada Geoespacial**, combinando tres capas cartográficas oficiales y abiertas mediante **`GeoPandas`**, **`Shapely`** y **`Folium`**:
1. **Marco Geoestadístico Nacional (INEGI):** Polígonos y claves de Área Geoestadística Básica (`cve_ageb_inegi`) correspondientes a las 16 colonias representativas de las 4 sub-zonas de estudio en la ZMVM.
2. **Directorio Estadístico Nacional de Unidades Económicas (DENUE - INEGI):** Conteo de unidades económicas de comercio minorista, servicios financieros, escuelas y hospitales (sectores SCIAN 46, 52, 61, 62, 71 y 72) en buffers de 500 metros.
3. **OpenStreetMap (Overpass API):** Coordenadas puntuales de las 14 estaciones de transporte público masivo que sirven a los corredores analizados y áreas verdes/parques urbanos cercanos.

---

## 2. Decisiones de Ingeniería Geoespacial con `GeoPandas`

Durante el desarrollo de `src/pipeline_e2.py` y el cuaderno interactivo `docs/E2/geoespacial_linaje.ipynb` tomamos tres decisiones técnicas clave:

1. **Separación entre Sistema de Almacenamiento (`EPSG:4326`) y Sistema de Cálculo Métrico (`EPSG:32614`):**
   - Los archivos estándar de intercambio en Capa Bronce (`data/bronze/inmobiliario/geoespacial_denue_osm_zmvm.geojson` y `estaciones_transporte_osm_zmvm.geojson`) se almacenan en coordenadas geográficas **WGS 84 (`EPSG:4326`)** por compatibilidad con el estándar RFC 7946 (GeoJSON) y visores web como `Folium`.
   - Sin embargo, calcular distancias euclidianas directamente en grados latitud/longitud introduce distorsión anisotrópica a la latitud de la Ciudad de México ($19.4^\circ\text{ N}$). Por ello, antes de ejecutar `geometry.distance()`, reproyectamos dinámicamente los `GeoDataFrame` al sistema plano oficial de INEGI para el centro de México: **WGS 84 / UTM zone 14N (`EPSG:32614`, unidades en metros)**.
2. **Construcción del Índice Compuesto de Accesibilidad y Equipamiento Urbano (`0 a 100`):**
   - Para sintetizar la riqueza espacial en un regresor continuo útil para las preguntas `E1`, `E2` y `E3`, diseñamos el indicador `indice_accesibilidad_urbana_0_100` ponderando tres componentes normalizados:
     $$\text{Índice Accesibilidad} = 0.45 \cdot S_{\text{transporte}} + 0.40 \cdot S_{\text{DENUE\_500m}} + 0.15 \cdot S_{\text{parques\_OSM}}$$
   - Los resultados muestran cómo corredores centrales como **Roma Norte ($92.8/100$)**, **Hipódromo Condesa ($90.5/100$)** y **Polanco ($86.4/100$)** lideran en densidad de servicios DENUE (420 a 510 unidades en 500m), mientras que zonas con excelente relación calidad-precio como **Del Valle Centro ($85.9/100$)** y **Nápoles ($84.2/100$)** ofrecen un equipamiento urbano casi idéntico con un *Yield %* bruto anual superior ($6.84\%$ vs. $5.68\%$ en Polanco).
3. **Cartografía Dual (Estática de Publicación e Interactiva Web):**
   - Se generó la lámina coroplética dual `docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png` (180 DPI) que contrasta visualmente el gradiente de precios por $m^2$ frente al equipamiento DENUE y los nodos de transporte OSM, complementada por el mapa interactivo `docs/E2/mapa_interactivo_zmvm.html` con *tooltips* y *popups* por AGEB/colonia.

---

## 3. Arquitectura de Linaje y Trazabilidad Total (`Bronce -> Plata -> Oro`)

Un requisito central de la Entrega `E2` es garantizar que **cada registro en la Capa Oro sea rastreable hasta su origen en la Capa Bronce y su fecha de ingesta**. Como las tablas de la Capa Oro son cubos analíticos agregados (por mes en `oro_e1`, por política de descuento en `oro_e2`, por celda factorial en `oro_e3` y por colonia/AGEB en `oro_geoespacial`), diseñamos un mecanismo de **linaje jerárquico y criptográfico** en dos niveles:

1. **Linaje a Nivel Registro en Capa Plata (`rentas_zmvm_plata_geolocalizado_e2.csv`):**
   - Cada una de las **1,291 filas validadas** incorpora:
     - `linaje_id_bronce_origen`: El identificador primario inmutable (`PROP-XXXXXXXXXX`).
     - `linaje_archivos_bronce_origen`: Lista explícita de los 3 archivos crudos de Capa Bronce que alimentaron el registro (`rentas_zmvm_historico_36m.json`, `macro_banxico_inegi_36m.json` y `geoespacial_denue_osm_zmvm.geojson`).
     - `linaje_fecha_captura_bronce_utc`, `linaje_fecha_ingesta_macro_utc` y `linaje_fecha_ingesta_geoespacial_utc`.
     - `linaje_hash_registro_bronce`: Huella `SHA-256` truncada a 16 caracteres hexadecimales calculada sobre el JSON crudo original en Bronce.
2. **Linaje Agregado y Catálogo Maestro en Capa Oro (`catalogo_linaje_oro_a_bronce.csv` y `.json`):**
   - Al agrupar hacia cualquiera de las **4 tablas de Capa Oro (92 registros totales: $36 + 28 + 12 + 16$)**, la función `build_group_lineage()` calcula y adjunta directamente en cada fila de Capa Oro:
     - `linaje_n_registros_bronce`: Conteo exacto de registros crudos de Bronce que integran esa celda.
     - `linaje_id_bronce_primero`, `linaje_id_bronce_ultimo` y `linaje_muestra_ids_bronce`: Punteros directos a los IDs de origen en Bronce.
     - `linaje_fecha_captura_bronce_min_utc`, `linaje_fecha_captura_bronce_max_utc` y `linaje_fecha_ingesta_geoespacial_utc`: Ventana temporal exacta de ingesta en Bronce.
     - `linaje_hash_lote_bronce`: Hash `SHA-256` de árbol de Merkle sobre todos los hashes individuales de Bronce que componen la fila Oro.
   - La auditoría automatizada confirmó **$100.0\%$ de cobertura de linaje ($92/92$ filas Oro trazables)** y **$0$ registros huérfanos**.

---

## 4. Ética, Legalidad, Privacidad y Disciplina PSP en E2

En [`docs/etica-datos.md`](etica-datos.md) formalizamos nuestra postura ética y jurídica:
- Verificamos la compatibilidad de licencias entre los **Términos de Libre Uso de BANXICO/INEGI**, **Creative Commons `CC BY 4.0`** y la licencia **`ODbL 1.0` de OpenStreetMap**.
- Implementamos **k-anonimato espacial (*spatial cloaking*)** aplicando un *jitter* controlado dentro del polígono de la colonia/AGEB para que ninguna coordenada apunte al domicilio privado de un ciudadano particular, cumpliendo al $100\%$ con la **LFPDPPP**.
- Finalmente, en nuestras bitácoras PSP (`calidad/tiempo-*.csv` y `calidad/defectos-*.csv`) registramos los tiempos reales de desarrollo de `E2` (con desviación $<4.5\%$ respecto a lo planeado) y documentamos la corrección temprana de 4 defectos locales (como el reemplazo del *basemap* de CartoDB en `Folium` que ahora exige API key por el mosaico abierto `OpenStreetMap`), asegurando una entrega `tag: e2` limpia y reproducible.
