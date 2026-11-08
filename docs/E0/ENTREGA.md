# 📋 Ficha de Entrega Técnica — Entrega E0 (`tag: e0`)

**Proyecto Integrador:** Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM  
**Tag de Liberación:** `e0`  
**Fecha de Corte:** 8 de noviembre de 2026  

---

## 1. Integrantes del Equipo

| Nombre Completo | Rol en Entrega E0 | Bitácora de Tiempo (PSP) | Bitácora de Defectos (PSP) |
| :--- | :--- | :--- | :--- |
| **Juan Antonio Ortiz Hinojosa** | Definición del Observatorio, Entrevista de Campo, Triléctica Estadística y Extractor BANXICO | [`calidad/tiempo-juan-antonio-ortiz-hinojosa.csv`](../../calidad/tiempo-juan-antonio-ortiz-hinojosa.csv) | [`calidad/defectos-juan-antonio-ortiz-hinojosa.csv`](../../calidad/defectos-juan-antonio-ortiz-hinojosa.csv) |
| **Diego Alberto Virgen Cuéllar** | Viabilidad Legal/Ética, Pipeline de Capa Bronce, Automatización GitHub Actions y Métricas PSP | [`calidad/tiempo-diego-alberto-virgen-cuellar.csv`](../../calidad/tiempo-diego-alberto-virgen-cuellar.csv) | [`calidad/defectos-diego-alberto-virgen-cuellar.csv`](../../calidad/defectos-diego-alberto-virgen-cuellar.csv) |

---

## 2. Resumen Ejecutivo de la Entrega E0

En esta entrega inicial (`e0`) se dejó formalmente constituido y operando el **Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional (OAMIRH - ZMVM)**:

1. **Problema y Validación de Campo:** Se formuló la pregunta detonadora sobre cómo la inflación habitacional (INPC Vivienda), el costo crediticio (TIIE 28 días) y la ubicación/tipología determinan el precio por $m^2$, la vacancia y el rendimiento anual (*Yield %*) en la Zona Metropolitana del Valle de México. El problema se validó mediante una entrevista de campo de 22 minutos con un administrador activo de carteras inmobiliarias en CDMX.
2. **Triléctica Estadística Definida:**
   - **E1 (Pronóstico):** Proyección a 4 trimestres del precio residencial por $m^2$ ($MXN/m^2$) vía modelos SARIMAX con regresores macroeconómicos.
   - **E2 (Experimentación / What-if):** Simulación de impacto en tasa de ocupación e ingreso neto al aplicar descuentos de 5%, 10% y 15% sobre precio de lista bajo contratos de 24 meses.
   - **E3 (Comparación Multivariada):** Análisis factorial del rendimiento anual bruto (*Yield %*) segmentando por tipo de inmueble (`depto_1rec`, `depto_2rec`, `casa`) y 4 sub-zonas urbanas de la ZMVM.
3. **Máquina de Captura en Capa Bronce:** Se programó el extractor ético `src/extract_bronze.py` orquestado mensualmente mediante GitHub Actions (`.github/workflows/bronze_capture.yml`) y se descargó la serie histórica inicial de **36 periodos mensuales consecutivos (`2023-11` a `2026-10`)** con 1,298 registros crudos de ofertas en `data/bronze/inmobiliario/`.

---

## 3. Matriz de Trazabilidad y Verificación de Entregables (`E0`)

| # | Requisito Oficial de la Entrega E0 | Artefacto / Ruta en el Repositorio | Estado | Evidencia / Métrica de Verificación |
| :-: | :--- | :--- | :-: | :--- |
| **1.1** | Ficha del observatorio (Sector, región, pregunta detonadora y cliente potencial) | [`docs/E0/propuesta.md`](propuesta.md) *(Sección 1)* | ✅ Cumplido | Sector SCIAN 531/721, ZMVM, pregunta central y perfil de Property Manager / Inversionista. |
| **1.2** | Entrevista de campo ($\ge 15$ min): 5 preguntas realizadas a actor del sector y aprendizajes | [`docs/E0/propuesta.md`](propuesta.md) *(Sección 2)* | ✅ Cumplido | Entrevista de 22 min (5 preguntas + respuestas detalladas + 4 aprendizajes trazados a E1–E3 y Capa Plata). |
| **1.3** | Las 3 preguntas analíticas (E1 Pronóstico, E2 Experimentación, E3 Multivariado) | [`docs/E0/propuesta.md`](propuesta.md) *(Sección 3)* | ✅ Cumplido | Ecuaciones formales, factores, niveles y modelos estadísticos para E1, E2 y E3. |
| **1.4** | Plan de recopilación de datos ($\ge 2$ fuentes con análisis ético/legal, `robots.txt` y términos) | [`docs/E0/propuesta.md`](propuesta.md) *(Sección 4)* | ✅ Cumplido | Fuente 1: BANXICO SIE / INEGI. Fuente 2: Mercado de Rentas ZMVM. Auditoría `robots.txt` y LFPDPPP. |
| **2.1** | Extractor ético ejecutándose de forma automática con GitHub Actions | [`src/extract_bronze.py`](../../src/extract_bronze.py) y [`.github/workflows/bronze_capture.yml`](../../.github/workflows/bronze_capture.yml) | ✅ Cumplido | Cron mensual `0 6 1 * *` + `workflow_dispatch`, verificación de `robots.txt` y pausas de cortesía. |
| **2.2** | Serie histórica inicial descargada en datos crudos con al menos 36 periodos | [`data/bronze/inmobiliario/`](../../data/bronze/inmobiliario/) | ✅ Cumplido | **36 periodos mensuales consecutivos** (`2023-11` a `2026-10`) en JSON y CSV crudo (1,298 registros de propiedades). |
| **3.1** | Archivos de registro PSP abiertos por integrante (`tiempo-<nombre>.csv` y `defectos-<nombre>.csv`) | [`calidad/`](../../calidad/) | ✅ Cumplido | 4 archivos CSV activos con registros reales de Planeación, Diseño, Codificación y Pruebas de E0. |
| **3.2** | 3 objetivos de calidad medibles definidos | [`docs/E0/propuesta.md`](propuesta.md) *(Sección 5.3)* y Sección 4 de este documento | ✅ Cumplido | Objetivos `OQ-01` (Estimación $\le 15\%$), `OQ-02` (Defect Removal Yield $\ge 85\%$) y `OQ-03` (Completitud 100%). |
| **4.1** | Ficha de entrega técnica (`docs/E0/ENTREGA.md`) | [`docs/E0/ENTREGA.md`](ENTREGA.md) | ✅ Cumplido | Presente documento con arquitectura, métricas PSP consolidadas e instrucciones de reproducción. |

---

## 4. Evaluación Inicial de los 3 Objetivos de Calidad (PSP) en `E0`

A partir de los datos registrados en la carpeta `calidad/` durante el desarrollo de la Entrega E0, el desempeño de calidad del equipo fue el siguiente:

1. **OQ-01 — Precisión en la Estimación de Tiempo ($\text{Meta: APE} \le 15\%$):**
   - **Juan Antonio Ortiz Hinojosa:** Tiempo Planeado Total = $320\text{ min}$ | Tiempo Real Total = $335\text{ min}$ | Error Absoluto Porcentual Acumulado = **$4.69\%$** (Cumple meta $\le 15\%$).
   - **Diego Alberto Virgen Cuéllar:** Tiempo Planeado Total = $315\text{ min}$ | Tiempo Real Total = $325\text{ min}$ | Error Absoluto Porcentual Acumulado = **$3.17\%$** (Cumple meta $\le 15\%$).
2. **OQ-02 — Efectividad de Remoción de Defectos ($\text{Meta: Yield} \ge 85\%$ antes de CI):**
   - Defectos totales registrados en E0 = **6 defectos** (3 de Juan Antonio + 3 de Diego Alberto).
   - Defectos detectados y cerrados en revisión/pruebas locales antes de liberación = **6 de 6 ($100\%$)**; defectos abiertos en `tag: e0` = **$0$**.
3. **OQ-03 — Integridad y Completitud en Capa Bronce ($\text{Meta: } \ge 36 \text{ periodos sin huecos}$):**
   - Periodos presentes en `macro_banxico_inegi_36m.json` = **36 meses consecutivos (`2023-11` a `2026-10`)**.
   - Periodos presentes en `rentas_zmvm_historico_36m.json` = **36 meses consecutivos (`2023-11` a `2026-10`)**.
   - Errores de parseo JSON/CSV en corrida de validación = **$0\%$**.

---

## 5. Instrucciones para Reproducir Localmente la Máquina de Captura

Requisitos: Python $\ge 3.10$ (utiliza exclusivamente la biblioteca estándar de Python para garantizar portabilidad sin dependencias rotas en CI/CD).

```bash
# 1. Ejecutar el extractor ético de Capa Bronce
python src/extract_bronze.py

# 2. Verificar los artefactos generados en data/bronze/inmobiliario/
ls -la data/bronze/inmobiliario/
```
