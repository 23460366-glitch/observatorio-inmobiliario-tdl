# 📊 Reporte Ejecutivo de Inteligencia Inmobiliaria: Plusvalía, Rentabilidad (Yield %) y Estrategia de Colocación 2026–2027

**Documento Comercial — Entrega E4 (Demo Day | Sello Trusted Data Lab Certificado)**  
**Dirigido a:** Asociaciones Inmobiliarias (AMPI Colima / CDMX), Desarrolladoras Habitacionales (Lega Desarrollos, Desarrolladora San Ricardo, Grupos Patrimoniales) e Inversionistas Privados  
**Elaborado por:** Juan Antonio Ortiz Hinojosa & Diego Alberto Virgen Cuéllar  
**Cobertura Analítica:** 36 meses continuos auditados (`Nov 2023 – Oct 2026`) + Proyección a 4 Trimestres (`Q1–Q4 2027`)  

---

## 1. Resumen Ejecutivo para Toma de Decisiones

El mercado de renta habitacional en México atraviesa un ciclo de **alta demanda estructural**: mientras las tasas hipotecarias (referenciadas a la TIIE de 28 días entre $9.1\%$ y $11.5\%$) moderan la compra inmediata de vivienda, la demanda de alquiler residencial y corporativo ha absorbido la oferta disponible tanto en metrópolis consolidadas (**ZMVM**) como en polos regionales de alto crecimiento (**Zona Metropolitana de Colima – Villa de Álvarez**).

A partir de más de **2,150 registros validados** bajo la norma internacional de calidad de datos **ISO/IEC 25012** y cruzados con el inventario comercial del **DENUE (INEGI)**, vialidades de **OpenStreetMap** e inflación habitacional del **Banco de México**, presentamos los **3 hallazgos estratégicos** con sus intervalos de confianza al $95\%$ para orientar decisiones de inversión, desarrollo y fijación de rentas en los próximos 12 meses.

---

## 2. Los 3 Hallazgos Principales de Plusvalía y Rentabilidad (Con Intervalos de Confianza al 95%)

### Hallazgo 1: En Colima – Villa de Álvarez, el Corredor Universitario (UdeC) y la Expansión Norponiente Superan en Rentabilidad Bruta (*Yield %*) al Segmento Tradicional
- **Evidencia Cuantitativa (`oro_colima_zm.csv`):**
  - **Máximo Flujo de Efectivo (*Yield* Anual):** La **Zona Universidad / Las Víboras (Colima)** registra el mayor rendimiento bruto anual de toda la zona metropolitana con **$8.46\%$ anual** ($\text{IC } 95\%: [8.21\%, 8.71\%]$) y el menor tiempo de vacancia del mercado (**$13.7\text{ días}$**, ocupación efectiva del **$96.7\%$**), impulsado por la concentración de 32 centros educativos/universitarios y 260 comercios DENUE en un radio de 500 metros.
  - **Líderes en Valor Patrimonial y Plusvalía por $m^2$:** El corredor norte encabezado por **Esmeralda Norte ($\$231.02\text{ MXN/m}^2$, $\text{IC } 95\%: [\$224.10, \$237.90]$)**, **Lomas de Vista Hermosa ($\$229.37\text{ MXN/m}^2$, plusvalía acumulada de $+17.9\%$ en 36 meses)** y **Jardines de las Lomas ($\$219.12\text{ MXN/m}^2$)** consolida los tickets mensuales más altos ($\$22,100$ a $\$23,750\text{ MXN/mes}$) con un *Yield* patrimonial estable de **$7.13\%$ a $7.17\%$**.
  - **Polo de Expansión en Villa de Álvarez:** **La Comarca / Bosque Real ($\$195.74\text{ MXN/m}^2$, *Yield* de $7.98\%$)** y **Real Bugambilias ($\$180.35\text{ MXN/m}^2$, *Yield* de $8.02\%$, plusvalía de $+19.2\%$)** representan el mejor balance entre apreciación de tierra nueva y retorno por renta sobre el eje de **Av. Pablo Silva García y Tercer Anillo Periférico**.

| Zona / Colonia (Colima – Villa de Álvarez) | Municipio | Renta Promedio ($\text{MXN/m}^2$) | Renta Mensual Media | Yield Bruto Anual (%) | Plusvalía 36m (%) | Vacancia Media (Días) | Comercios DENUE (500m) |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| **Esmeralda Norte** | Colima | **$231.02** | $23,546 | 7.17% | +16.03% | 20.8 d | 215 |
| **Lomas de Vista Hermosa** | Colima | **$229.37** | $23,744 | 7.17% | +17.90% | 21.1 d | 175 |
| **Jardines de las Lomas** | Colima | **$219.12** | $22,174 | 7.13% | +16.27% | 20.9 d | 165 |
| **La Comarca / Bosque Real** | Villa de Álvarez | **$195.74** | $20,246 | **7.98%** | +17.44% | 18.9 d | 155 |
| **Real Bugambilias** | Villa de Álvarez | **$180.35** | $18,247 | **8.02%** | **+19.19%** | 18.9 d | 190 |
| **Esmeralda Sur** | Colima | **$171.95** | $17,595 | 7.68% | +14.25% | 18.4 d | 240 |
| **Zona Centro Colima** | Colima | **$171.06** | $17,278 | 7.61% | **+20.89%** | 17.6 d | **385** |
| **Zona Universidad / Las Víboras** | Colima | **$161.71** | $17,014 | **8.46%** | +20.26% | **13.7 d** | 260 |

---

### Hallazgo 2: Pronóstico 2027 — Apreciación Sostenida de $+5.8\%$ a $+6.4\%$ Anual en Rentas por $m^2$ sin Señales de Burbuja
- **Evidencia Cuantitativa (Modelos SARIMA y Holt-Winters con $\text{MAPE} < 1.5\%$):**
  - En **Colima – Villa de Álvarez**, la renta media metropolitana pasará de **$\$195.04\text{ MXN/m}^2$** al cierre de 2026 a un rango proyectado de **$\$206.40\text{ a }\$208.15\text{ MXN/m}^2$** hacia el cuarto trimestre de 2027 ($\text{IC } 95\%: [\$199.80, \$214.50\text{ MXN/m}^2]$).
  - En la **ZMVM (CDMX / Área Conurbada)**, la renta media pasará de **$\$429.41\text{ MXN/m}^2$** (Oct 2026) a **$\$453.54\text{ MXN/m}^2$** en Q4 2027 ($\text{IC } 95\%: [\$445.06, \$462.01\text{ MXN/m}^2]$), donde colonias en consolidación como **Santa María la Ribera, Escandón y Del Valle** entregan de **$120\text{ a }180\text{ puntos base}$ más de Yield anual** ($6.8\%–7.5\%$) que el corredor ultra-prime de Polanco ($5.6\%$).

---

### Hallazgo 3: Estrategia Comercial *What-If* — Un Descuento del 5% en Contratos de 24 Meses Maximiza el Flujo Neto del Propietario
- **Evidencia del Simulador a 24 Meses:**
  - Mantener un inmueble sobrevalorado esperando el *"precio de lista lleno"* en contratos anuales tradicionales provoca entre **28 y 42 días de vacancia por rotación** más el costo de comisión de recolocación anual (1 mes de renta).
  - Otorgar un **descuento táctico del $5.0\%$** a cambio de un **contrato de permanencia de 24 meses** reduce el tiempo de colocación en **$34\%$**, eleva la tasa de ocupación efectiva por encima del **$95.8\%$** y genera un **ingreso neto acumulado superior entre $+\$18,500\text{ y }+\$32,000\text{ MXN}$ por unidad** frente al esquema sin descuento con rotación anual. Descuentos mayores ($\ge 15\%$) ya no se compensan con menor vacancia y erosionan el flujo total.

---

## 3. Recomendaciones Accionables de Inversión por Perfil de Cliente

1. **Para Desarrolladoras en Colima – Villa de Álvarez (ej. Lega Desarrollos / San Ricardo):**
   - **Producto vertical compacto ($1\text{ y }2\text{ recámaras}, 48–78\text{ m}^2$):** Priorizar predios a menos de $400\text{ m}$ del eje **Av. Universidad / Tercer Anillo** y **Av. Constitución Norte**, donde la prima de precio por $m^2$ en departamentos compactos es **+$14\%$ superior** a la vivienda horizontal tradicional y la absorción ocurre en menos de 3 semanas.
   - **Vivienda horizontal patrimonial ($140–210\text{ m}^2$):** Enfocar reservas territoriales en el corredor **La Comarca / Bosque Real – Real Bugambilias**, capitalizando el diferencial de *Yield* ($8.0\%$) frente a zonas norte ya saturadas.
2. **Para Agencias y Corredores Asociados (AMPI Colima y CDMX):**
   - Utilizar la matriz *What-If* de 24 meses durante la captación de exclusivas para justificar ante propietarios ajustes iniciales de precio del $5\%$, reduciendo el inventario estancado ($>45\text{ días}$) en más de un tercio.
3. **Para Inversionistas Patrimoniales:**
   - Diversificar cartera combinando **activos de flujo alto** (*Yield* $>8.0\%$ en Zona Universidad UdeC, Real Bugambilias o Santa María la Ribera en CDMX) con **activos de resguardo patrimonial** (Esmeralda Norte, Lomas de Vista Hermosa o Del Valle/Roma en CDMX), indexando renovaciones anuales estrictamente al subíndice **INPC Vivienda** más prima de equipamiento urbano.
