# 📓 Relatoría Técnica de Etapa — Entrega E1 (Capas Plata, Cuarentena y Oro)

**Proyecto Integrador:** Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM  
**Etapa:** `E1` — Limpieza Estadística, Integración, Puerta de Calidad Automática y Reducción a Capa Oro  
**Fecha:** 16 de noviembre de 2026  
**Autores:**  
- Juan Antonio Ortiz Hinojosa  
- Diego Alberto Virgen Cuéllar  

---

## 1. Introducción y Propósito de la Etapa E1

Tras haber puesto en marcha la máquina de captura de la **Capa Bronce** en la entrega `E0` (acumulando 36 periodos mensuales consecutivos desde noviembre de 2023 hasta octubre de 2026 con indicadores macroeconómicos de BANXICO/INEGI y 1,299 registros crudos de ofertas de renta residencial en la Zona Metropolitana del Valle de México), el objetivo de la **Entrega E1** consistió en diseñar, fundamentar estadísticamente y automatizar el tránsito de los datos hacia la **Capa Plata** (`data/silver/inmobiliario/`) y la **Capa Oro** (`data/gold/inmobiliario/`).

En mercados inmobiliarios reales, alimentar modelos de pronóstico (`E1`), simulaciones de elasticidad de ocupación (`E2`) o comparaciones de rentabilidad *Yield %* (`E3`) directamente con datos crudos de portales produce sesgos severos: anuncios republicados por múltiples corredores inflan artificialmente la oferta en ciertas colonias, errores de dedo en la superficie ($-25\text{ m}^2$ o $9,850\text{ m}^2$ para un departamento) distorsionan la media del precio por metro cuadrado, y el ocultamiento intencional de cuotas de mantenimiento caras sesga el cálculo del flujo neto. Esta relatoría documenta las decisiones de ingeniería y estadística aplicadas para resolver cada uno de estos problemas sin perder trazabilidad.

---

## 2. Integración de Fuentes Heterogéneas y Resolución de Conflictos

El primer desafío técnico fue fusionar dos fuentes con granularidades, formatos y convenciones distintas:
1. **Fuente Macroeconómica (`macro_banxico_inegi_36m.json`):** Serie mensual con nivel de agregación nacional/metropolitano y fechas crudas en formato bancario mexicano `DD/MM/YYYY` (ej. `"01/11/2023"`).
2. **Fuente de Mercado de Rentas (`rentas_zmvm_historico_36m.json`):** Microdatos transaccionales/anuncios a nivel propiedad con 1,299 observaciones.

**Decisiones de resolución implementadas en `load_and_integrate_sources()` (`src/pipeline_e1.py`):**
- **Homologación de Llave Temporal:** Se transformaron las 36 fechas `DD/MM/YYYY` de BANXICO al estándar ISO 8601 mensual `YYYY-MM`, verificando mediante `validate="many_to_one"` en `pandas.merge` que cada oferta inmobiliaria recibiera exactamente el vector macroeconómico (`inpc_vivienda_zmvm`, `tiie_28d_pct`, `tipo_cambio_fix_mxn_usd`) de su mes de publicación ($0$ registros huérfanos).
- **Resolución de Discrepancias de Tipo Numérico/Monetario:** Se detectaron **37 registros** donde el precio de renta venía codificado como cadena con formato monetario (`"$32,500.00 MXN"`). Se implementó un limpiador léxico mediante expresiones regulares (`parse_currency_or_float`) para estandarizar las 9 variables métricas a flotantes IEEE 754 de 64 bits.
- **Unificación Semántica de Categorías:** Se resolvieron **48 discrepancias de nomenclatura** donde distintas fuentes o corredores etiquetaron la tipología como `"Depto 1 Rec"`, `"Departamento 2 Recámaras"` o `"CASA HABITACION"`, homologándolas al catálogo cerrado `{"depto_1rec", "depto_2rec", "casa"}` y conservando la columna `tipo_inmueble_raw` para auditoría.

---

## 3. Puerta de Calidad Automática (`Pandera`) y Política de Cuarentena

Siguiendo el principio de ingeniería de datos de **nunca borrar registros inválidos en silencio**, construimos una Puerta de Calidad automática combinando deduplicación por llave de negocio y validación declarativa con **`pandera` (`DataFrameSchema` con `lazy=True`)**.

### 3.1 Reglas del Contrato de Datos
1. **Unicidad mensual por inmueble:** La combinación `(id_propiedad, periodo_mensual)` debe ser única.
2. **Prefijo e integridad de identificador:** `id_propiedad` debe iniciar con `"PROP-"`.
3. **Dominios cerrados:** `subzona_id` $\in \{\text{SZ1}, \text{SZ2}, \text{SZ3}, \text{SZ4}\}$ y `tipo_inmueble` $\in \{\text{depto\_1rec}, \text{depto\_2rec}, \text{casa}\}$.
4. **Rango físico de superficie:** Cuando `superficie_m2` no es nulo, debe cumplir $20.0 \le \text{superficie\_m2} \le 1,200.0\text{ m}^2$.
5. **Rango económico de renta:** `renta_lista_mensual_mxn` es obligatorio (`nullable=False`) y debe cumplir $1,500.0 < \text{renta} \le 500,000.0\text{ MXN}$.

### 3.2 Resultados de la Cuarentena
De los **1,299 registros** evaluados:
- **1,291 registros ($99.38\%$)** cumplieron íntegramente el contrato y avanzaron a la Capa Plata.
- **8 registros ($0.62\%$)** fueron interceptados y enviados a [`data/silver/inmobiliario/cuarentena_inmobiliario.csv`](../data/silver/inmobiliario/cuarentena_inmobiliario.csv) y [`.json`](../data/silver/inmobiliario/cuarentena_inmobiliario.json), cada uno con su estampa de tiempo UTC y motivo específico:
  - `3 registros`: `DUPLICADO_ID_PERIODO` (republicación del mismo departamento en la sub-zona central dentro del mismo mes).
  - `2 registros`: `PANDERA_FAIL[superficie_m2]: superficie_m2_menor_20m2` (valores corruptos de $-25.0\text{ m}^2$ y $4.5\text{ m}^2$).
  - `1 registro`: `PANDERA_FAIL[superficie_m2]: superficie_m2_mayor_1200m2` (error de captura de $9,850.0\text{ m}^2$).
  - `1 registro`: `PANDERA_FAIL[renta_lista_mensual_mxn]: renta_lista_invalida_o_negativa` ($-15,000.0\text{ MXN}$).
  - `1 registro`: `PANDERA_FAIL[renta_lista_mensual_mxn]: not_nullable` (anuncio publicado sin precio de renta).

---

## 4. Diagnóstico del Mecanismo de Valores Faltantes (MCAR / MAR / MNAR) e Imputación

Sobre los 1,291 registros válidos diagnosticamos tres patrones distintos de ausencia de datos antes de elegir el método de imputación:

1. **`estacionamientos` (28 faltantes — Diagnóstico: MCAR):**
   - *Prueba estadística:* Tabla de contingencia contra `subzona_id` ($\chi^2 = 0.0001, p = 1.00 > 0.05$). La pérdida del dato ocurre de forma completamente aleatoria por fallos esporádicos de captura del atributo.
   - *Imputación justificada:* **Moda condicional según `tipo_inmueble`** ($1$ cajón para departamentos de 1 y 2 recámaras; $2$ cajones para casas), registrando la bandera `flag_imputado_estacionamientos_mcar`.
2. **`superficie_m2` (15 faltantes — Diagnóstico: MAR):**
   - *Prueba estadística:* Prueba $\chi^2$ contra `subzona_id` ($\chi^2 = 45.482, p = 7.31 \times 10^{-10} < 0.001$). Todos los faltantes se concentran en la sub-zona `SZ4_EMERGENTE_METROPOLITANA`, donde los propietarios independientes suelen anunciar por número de recámaras omitiendo los metros cuadrados exactos. Dado que la probabilidad de faltante depende de variables observadas (la sub-zona y tipología), el mecanismo es **MAR (Missing At Random)**.
   - *Imputación justificada:* **Mediana estratificada por `(subzona_id, tipo_inmueble, recamaras)`**, recalculando inmediatamente `precio_m2_mxn` para mantener consistencia aritmética exacta.
3. **`cuota_mantenimiento_mxn` (108 faltantes — Diagnóstico: MNAR):**
   - *Prueba estadística:* Prueba $t$ de dos muestras de Welch comparando el precio de renta cuando la cuota de mantenimiento falta ($\mu = \$60,821.11\text{ MXN}$) contra cuando sí se reporta ($\mu = \$35,074.77\text{ MXN}$), obteniendo $t = 14.665, p = 1.56 \times 10^{-29} < 0.001$. Esto confirma lo reportado en la entrevista de campo de `E0`: en inmuebles de renta alta con amenidades costosas, el anunciante omite estratégicamente publicar la cuota de mantenimiento para no frenar el contacto inicial (**MNAR — Missing Not At Random**).
   - *Imputación justificada:* En presencia de MNAR, imputar sin dejar rastro destruye información valiosa. Por ello, creamos la variable binaria **`flag_mnar_mantenimiento`** (que preserva la señal de ocultamiento para los modelos posteriores) e imputamos el monto multiplicando la renta de lista por la **mediana zonal de la razón $\text{cuota}/\text{renta}$**.

---

## 5. Tratamiento de Atípicos, Normalización, Discretización y Reducción a Capa Oro

1. **Triangulación de Outliers y Winsorización:**
   - Implementamos tres detectores sobre `precio_m2_mxn`: **IQR estratificado** (4 atípicos), **Z-Score Robusto basado en MAD** con umbral $|Z_{\text{rob}}| > 3.5$ (3 atípicos) e **`IsolationForest` multivariado** sobre $(\text{precio/m}^2, \text{superficie}, \text{Yield})$ (33 anomalías conjuntas; 4 por consenso de $\ge 2$ métodos).
   - Como estos registros corresponden a *penthouses* reales en Polanco/Roma (hasta $\$765.72\text{ MXN/m}^2$), eliminarlos sesgaría a la baja el corredor Prime. Se aplicó **Winsorización estratificada al percentil $[1\%, 99\%]$ por sub-zona**, acotando el máximo extremo a $\$626.96\text{ MXN/m}^2$ y reduciendo la desviación estándar global de $89.70$ a $88.63\text{ MXN/m}^2$.
2. **Normalización, Discretización y Jerarquías:**
   - Se generaron versiones escaladas **Min-Max $[0,1]$** (para algoritmos basados en distancias) y **Z-Score $(\mu=0, \sigma=1)$** (para modelos lineales y series de tiempo con regresores en distintas unidades).
   - Se discretizaron metrajes, cuartiles de precio por $m^2$ y tramos de vacancia, y se formalizaron las jerarquías espacial (`Colonia -> Alcaldía -> Sub-zona -> Corredor Macro -> ZMVM`), temporal (`Mes -> Trimestre -> Año`) y tipológica (`Tipo -> Familia Vertical/Horizontal`).
3. **Reducción de Datos y Capa Oro (`data/gold/inmobiliario/`):**
   - Mediante selección de atributos se redujo la tabla de Capa Plata de **61 columnas intermedias a 31 variables canónicas ($49.18\%$ de reducción dimensional)**.
   - Finalmente, se construyeron por agregación los **3 cubos de Capa Oro** listos para modelado:
     - `oro_e1_pronostico_mensual_trimestral.csv` (36 periodos mensuales con series agregadas y macroeconomía para `E1`).
     - `oro_e2_simulacion_whatif_24m.csv` (28 celdas de Modalidad $\times$ Descuento $\times$ Sub-zona con vacancia, ocupación e ingreso esperado a 24 meses para `E2`).
     - `oro_e3_comparacion_multivariada_yield.csv` (12 celdas del diseño factorial $3 \times 4$ Tipología $\times$ Sub-zona con medias, medianas y desviaciones de *Yield %* para `E3`).

---

## 6. Lecciones Aprendidas y Disciplina PSP en la Etapa E1

La aplicación rigurosa de nuestras bitácoras PSP (`calidad/tiempo-*.csv` y `calidad/defectos-*.csv`) nos permitió detectar y corregir **4 defectos técnicos en pruebas locales** antes de integrar el workflow de GitHub Actions: entre ellos, la actualización de la importación `import pandera.pandas as pa` para evitar advertencias de deprecación en `pandera 0.36+` y la alineación exacta de los nombres de columnas normalizadas (`precio_m2_mxn_minmax` y `precio_m2_mxn_zscore`) en el reductor de Capa Oro. El equipo cerró la etapa `E1` con un error de estimación de tiempo inferior al $4\%$ y el $100\%$ de los tests del pipeline automatizado en verde.
