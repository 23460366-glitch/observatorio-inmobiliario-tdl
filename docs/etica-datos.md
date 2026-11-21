# ⚖️ Declaración de Ética, Legalidad, Gobernanza y Privacidad de Datos (`docs/etica-datos.md`)

**Proyecto Integrador — Entrega E2 (Unidad 4)**  
**Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM**  
**Fecha de Emisión:** 21 de noviembre de 2026  
**Integrantes Responsables:**  
- Juan Antonio Ortiz Hinojosa  
- Diego Alberto Virgen Cuéllar  

---

## 1. Propósito y Alcance de la Declaración

El presente documento establece el marco jurídico, ético, técnico y de gobernanza bajo el cual opera el **Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la Zona Metropolitana del Valle de México (OAMIRH - ZMVM)**. Su alcance abarca la totalidad del ciclo de vida del dato en nuestro repositorio: desde la captura automatizada en la **Capa Bronce** (`data/bronze/inmobiliario/`), la validación y envío a cuarentena en la **Capa Plata** (`data/silver/inmobiliario/`), hasta la explotación analítica y cartográfica en la **Capa Oro** (`data/gold/inmobiliario/`).

---

## 2. Inventario de Fuentes de Datos, Términos de Uso y Licenciamiento

El observatorio integra **tres familias de fuentes de datos** (macroeconómica, mercado habitacional y geoespacial especializada), todas de carácter público o abierto y utilizadas en estricto apego a sus licencias originales:

| # | Fuente de Datos | Entidad / Proveedor | Licencia y Marco Legal Aplicable | Condiciones de Reutilización y Atribución |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Indicadores Macroeconómicos (`SF43783` TIIE 28d, `SP1` INPC General, `SP74625` INPC Vivienda, `SF43718` FIX)** | Banco de México (BANXICO SIE-API REST) e INEGI (BIE) | **Términos de Libre Uso de Datos Abiertos del Gobierno de México** y Condiciones del Portal SIE-BANXICO | Permite consulta automatizada, almacenamiento, derivación estadística y publicación académica/comercial citando expresamente: *"Fuente: Banco de México (SIE) e INEGI"*. |
| **2** | **Ofertas y Series Históricas del Mercado de Rentas Residenciales en la ZMVM (36 meses)** | Repositorios Abiertos de Vivienda (Snapshots Properati México / Datos Abiertos CDMX / Índices SHF) | **Creative Commons Attribution 4.0 International (`CC BY 4.0`) / Licencia MIT** | Permite copia, redistribución, mezcla y transformación para cualquier fin, siempre que se otorgue el crédito correspondiente, se indique si se hicieron cambios y se eliminen identificadores personales. |
| **3** | **Fuente Especializada Geoespacial: Unidades Económicas DENUE, Polígonos AGEB y Red de Transporte Masivo** | INEGI (API DENUE y Marco Geoestadístico Nacional) + OpenStreetMap (Overpass API) | **Términos de Libre Uso del INEGI** + **Open Database License (`ODbL 1.0`) de OpenStreetMap Foundation** | INEGI exige citar al Instituto y no alterar la semántica oficial de las claves geoestadísticas (`CVE_AGEB`). OpenStreetMap (`ODbL 1.0`) exige atribución visible (*"© OpenStreetMap contributors"*) y mantener libres las capas derivadas. |

---

## 3. Análisis Técnico y Cumplimiento de Directivas `robots.txt`

Para garantizar una recolección ética (*Ethical Data Harvesting*) que no degrade la disponibilidad de los servidores públicos ni viole restricciones de acceso automatizado, nuestros scripts (`src/extract_bronze.py` y `src/pipeline_e2.py`) ejecutan una **auditoría programática previa** mediante el módulo estándar `urllib.robotparser.RobotFileParser`.

### 3.1 Matriz de Auditoría `robots.txt` por Dominio

| Dominio / Endpoint | Ruta Consultada | Reglas `robots.txt` Verificadas | Política de Cortesía (*Politeness*) Implementada |
| :--- | :--- | :--- | :--- |
| `https://www.banxico.org.mx` | `/SieAPIRest/service/v1/series/...` | Endpoint REST oficial para consumo máquina-a-máquina. No existe directiva `Disallow` para `/SieAPIRest/`. Límite oficial: 100 peticiones/min por token. | • **Frecuencia:** 1 ejecución mensual (`cron: '0 6 1 * *'`).<br>• **Pausa entre llamadas (`crawl-delay`):** $\ge 1.5\text{ s}$.<br>• **Timeout defensivo:** $15\text{ s}$. |
| `https://datos.cdmx.gob.mx` | `/dataset/` y API CKAN | `User-Agent: *` permite acceso de lectura a catálogos y descargas abiertas (`Allow: /dataset/`). Restringe rutas administrativas (`Disallow: /user/`, `Disallow: /api/action/user_`). | • **Frecuencia:** 1 vez al mes.<br>• **Pausa de cortesía:** $\ge 2.0\text{ s}$.<br>• Ninguna ruta bajo `/user/` o `/admin/` es consultada. |
| `https://www.inegi.org.mx` | `/app/api/denue/v1/` y Marco Geoestadístico | API pública oficial del DENUE. Se prohíbe el raspado masivo concurrente de páginas HTML de consulta interactiva, promoviendo el uso de endpoints JSON/GeoJSON. | • **Consumo por lotes agregados a nivel colonia/AGEB**.<br>• Pausa mínima de $2.0\text{ s}$ y caché en Capa Bronce (`geoespacial_denue_osm_zmvm.geojson`). |
| `https://overpass-api.de` | `/api/interpreter` (OpenStreetMap) | La política de uso aceptable de Overpass API exige un `User-Agent` descriptivo con URL de contacto y evitar consultas pesadas repetitivas en bucles paralelos. | • **Cabecera transparente:** `ObservatorioInmobiliarioZMVM-AcademicBot/1.1 (+https://github.com/23460366-glitch/observatorio-inmobiliario-tdl)`.<br>• Persistencia local en GeoJSON para cero consultas redundantes. |

---

## 4. Privacidad por Diseño y Protección de Datos Personales (Cumplimiento LFPDPPP)

En el mercado inmobiliario mexicano, los anuncios publicados en portales suelen contener datos personales de propietarios, arrendadores o asesores inmobiliarios. En cumplimiento estricto con la **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)** y los principios internacionales de *Privacy by Design*, el observatorio implementa cuatro barreras técnicas:

1. **Cero Recolección de Datos Personales Identificables (PII):**
   - El pipeline **no captura, procesa ni almacena** nombres de personas físicas, números telefónicos, cuentas de WhatsApp, direcciones de correo electrónico, fotografías de rostros ni enlaces a perfiles individuales de corredores.
2. **Seudonimización Criptográfica Irreversible de Identificadores (`id_propiedad`):**
   - Cada oferta se identifica exclusivamente mediante un hash determinista truncado (`PROP-` + 10 caracteres hexadecimales derivados de `SHA-1` sobre atributos estructurales), impidiendo la reidentificación inversa del anuncio comercial original.
3. **K-Anonimato Espacial y Ofuscación Geográfica (*Spatial Cloaking*):**
   - Nunca se publican ni almacenan números exteriores/interiores ni domicilios exactos de las viviendas.
   - En la integración geoespacial de la Entrega `E2` (`src/pipeline_e2.py`), las coordenadas (`latitud_wgs84`, `longitud_wgs84`) se asignan con una **perturbación aleatoria acotada (*spatial jitter* de $\pm 250\text{ m}$)** alrededor del centroide del polígono de la colonia/AGEB (`cve_ageb_inegi`), garantizando que cada ubicación represente un entorno vecinal con $k > 20$ viviendas comparables (*k-anonimato geográfico*) sin exponer una residencia privada específica.
4. **Cero Datos de Redes Sociales Individuales:**
   - Todas las métricas urbanas del entorno provienen de conteos de establecimientos económicos públicos (DENUE SCIAN) e infraestructura de transporte/parques (OpenStreetMap), sin rastrear movilidad ni opiniones de ciudadanos individuales.

---

## 5. Identificación y Mitigación de Sesgos Estadísticos y Algorítmicos

Todo observatorio económico basado en ofertas de mercado está expuesto a sesgos estructurales. En la siguiente tabla documentamos los cuatro sesgos principales diagnosticados en nuestro dominio y los mecanismos técnicos implementados en `E1` y `E2` para mitigarlos:

| Tipo de Sesgo | Descripción del Riesgo en el Mercado Inmobiliario ZMVM | Estrategia Técnica de Mitigación Implementada en el Pipeline |
| :--- | :--- | :--- |
| **1. Sesgo de Supervivencia y Sobreprecio de Lista (*Asking Price & Survivorship Bias*)** | Los inmuebles publicados en portales a precios inflados ($+10\%$ a $+15\%$) permanecen activos durante meses y aparecen repetidamente en los cortes mensuales, mientras que las propiedades a precio justo se rentan en $<35$ días. | • **Deduplicación estricta en Puerta de Calidad (`Pandera`)** por llave `(id_propiedad, periodo_mensual)` enviando republicaciones a cuarentena.<br>• Inclusión explícita de `descuento_contrato_pct`, `renta_efectiva_winsor_mxn` y `dias_vacancia_observados` para separar el precio de lista del precio efectivo de cierre. |
| **2. Sesgo de Cobertura Digital y Sobrerrepresentación de Corredores Prime (*Geographic Selection Bias*)** | Los portales inmobiliarios concentran desproporcionadamente su oferta en colonias de alto ingreso (Polanco, Roma, Condesa), subrepresentando zonas en consolidación o municipios conurbados (Santa María la Ribera, Escandón, Satélite). | • **Diseño muestral estratificado balanceado** a través de 4 sub-zonas urbanas (`SZ1` a `SZ4`) y 3 tipologías (`depto_1rec`, `depto_2rec`, `casa`).<br>• **Imputación MAR estratificada por sub-zona** en lugar de usar promedios globales que contaminarían las colonias emergentes con metrajes de zonas Prime. |
| **3. Sesgo por No-Respuesta Informativa en Gastos Ocultos (*MNAR Bias en Mantenimiento*)** | Como demostramos en `E1` ($t = 14.67, p = 1.56 \times 10^{-29}$), los inmuebles con rentas altas omiten intencionalmente la cuota de mantenimiento cuando ésta supera los $\$3,800\text{ MXN}$. Ignorar este mecanismo subestimaría el costo real de habitación. | • Creación de la variable indicadora explícita **`flag_mnar_mantenimiento`** en Capa Plata e imputación mediante la razón mediana zonal $\text{cuota}/\text{renta}$, preservando la señal estadística del ocultamiento. |
| **4. Sesgo de Falacia Ecológica y Distorsión Cartográfica (*MAUP & Projection Bias*)** | Calcular distancias en grados geográficos (`EPSG:4326`) en la latitud de la CDMX ($19.4^\circ\text{ N}$) introduce errores geométricos en el eje Este-Oeste ($\cos(19.4^\circ) \approx 0.943$). | • **Reproyección cartográfica rigurosa en `GeoPandas` al sistema métrico oficial `EPSG:32614` (WGS 84 / UTM zone 14N)** antes de calcular distancias euclidianas al transporte masivo y buffers de 500 metros del DENUE. |

---

## 6. Gobernanza, Auditoría de Cuarentena y Responsabilidad Social

1. **Prohibición de Borrado Silencioso (*Zero Silent Drop Policy*):** Ningún dato anómalo o fuera de norma se oculta o elimina sin registro. Todo rechazo de la Puerta de Calidad queda permanentemente auditable en [`data/silver/inmobiliario/cuarentena_inmobiliario.csv`](../data/silver/inmobiliario/cuarentena_inmobiliario.csv) con su regla infringida y estampa de tiempo UTC.
2. **Transparencia y Reproducibilidad Abierta:** Todo el código de captura (`src/extract_bronze.py`), limpieza (`src/pipeline_e1.py`) e integración geoespacial y linaje (`src/pipeline_e2.py`) es de código abierto, determinista (semillas fijas documentadas) y verificable mediante ejecución automatizada en GitHub Actions.
3. **Uso Socialmente Responsable de las Proyecciones:** Los modelos e indicadores de este observatorio tienen fines académicos y de transparencia informativa para equilibrar la asimetría de información entre arrendadores, administradores e inquilinos en la ZMVM; no deben emplearse para prácticas colusorias de fijación de precios ni desplazamiento forzado de comunidades residentes.
