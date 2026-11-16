# 🏢 Observatorio del Mercado Inmobiliario y Renta Habitacional (ZMVM)

Repositorio oficial del **Proyecto Integrador** enfocado en el análisis econométrico, simulación *what-if* y comparación multivariada del mercado de alquiler residencial en la Zona Metropolitana del Valle de México (ZMVM).

## 👥 Integrantes del Equipo
- **Juan Antonio Ortiz Hinojosa**
- **Diego Alberto Virgen Cuéllar**

---

## 📂 Estructura del Repositorio (Entregas `e0` y `e1`)

```text
observatorio-inmobiliario/
├── .github/
│   └── workflows/
│       └── bronze_capture.yml                                    # Pipeline CI/CD (Bronce -> Pandera -> Plata -> Oro)
├── calidad/
│   ├── defectos-diego-alberto-virgen-cuellar.csv                 # Bitácora PSP de defectos (E0 + E1)
│   ├── defectos-juan-antonio-ortiz-hinojosa.csv                  # Bitácora PSP de defectos (E0 + E1)
│   ├── tiempo-diego-alberto-virgen-cuellar.csv                   # Bitácora PSP de tiempos (E0 + E1)
│   └── tiempo-juan-antonio-ortiz-hinojosa.csv                    # Bitácora PSP de tiempos (E0 + E1)
├── data/
│   ├── bronze/
│   │   └── inmobiliario/
│   │       ├── macro_banxico_inegi_36m.json                      # 36 meses de INPC Vivienda, TIIE 28d y FIX
│   │       ├── rentas_zmvm_historico_36m.json                    # 36 meses de ofertas crudas en la ZMVM
│   │       ├── serie_consolidada_36m.csv                         # Serie mensual consolidada en crudo
│   │       └── snapshots/
│   │           └── captura_2026-10.json
│   ├── silver/
│   │   └── inmobiliario/
│   │       ├── rentas_zmvm_plata_limpio.csv                      # 1,291 registros validados, imputados y escalados
│   │       ├── cuarentena_inmobiliario.csv                       # 8 registros inválidos en cuarentena con motivo
│   │       └── cuarentena_inmobiliario.json                      # Auditoría detallada de la Puerta de Calidad Pandera
│   └── gold/
│       └── inmobiliario/
│           ├── oro_e1_pronostico_mensual_trimestral.csv          # Cubo Oro para E1 (Pronóstico 36 meses)
│           ├── oro_e2_simulacion_whatif_24m.csv                  # Cubo Oro para E2 (What-if descuentos 24m)
│           ├── oro_e3_comparacion_multivariada_yield.csv         # Cubo Oro para E3 (ANOVA Tipología x Sub-zona)
│           └── reporte_auditoria_pipeline_e1.json                # Métricas completas de ejecución del pipeline E1
├── docs/
│   ├── E0/
│   │   ├── propuesta.md                                          # Propuesta extensa del Observatorio (E0)
│   │   └── ENTREGA.md                                            # Ficha de entrega técnica E0
│   ├── E1/
│   │   ├── limpieza.ipynb                                        # Notebook ejecutado de Limpieza y Preprocesamiento (E1)
│   │   └── ENTREGA.md                                            # Ficha de entrega técnica E1
│   └── relatoria-E1.md                                           # Relatoría técnica y estadística de la etapa E1
├── src/
│   ├── extract_bronze.py                                         # Extractor ético de Capa Bronce
│   ├── pipeline_e1.py                                            # Pipeline E1 (Integración, Pandera, Plata y Oro)
│   └── build_notebook_e1.py                                      # Generador reproducible de docs/E1/limpieza.ipynb
├── requirements.txt
└── README.md
```

---

## 🔗 Accesos Directos a los Entregables

### 📦 Entrega `E1` (`tag: e1`)
1. 📓 **Notebook de Limpieza y Preprocesamiento:** [`docs/E1/limpieza.ipynb`](docs/E1/limpieza.ipynb)
2. ⚙️ **Script del Pipeline E1 (Pandera + Plata + Oro):** [`src/pipeline_e1.py`](src/pipeline_e1.py)
3. 📋 **Ficha Técnica de Entrega E1:** [`docs/E1/ENTREGA.md`](docs/E1/ENTREGA.md)
4. 📝 **Relatoría de Etapa E1:** [`docs/relatoria-E1.md`](docs/relatoria-E1.md)
5. 🚨 **Registros en Cuarentena (con motivo documentado):** [`data/silver/inmobiliario/cuarentena_inmobiliario.csv`](data/silver/inmobiliario/cuarentena_inmobiliario.csv)
6. 🥈 **Datos Limpios en Capa Plata:** [`data/silver/inmobiliario/rentas_zmvm_plata_limpio.csv`](data/silver/inmobiliario/rentas_zmvm_plata_limpio.csv)
7. 🥇 **Cubos Analíticos en Capa Oro (`E1`, `E2`, `E3`):** [`data/gold/inmobiliario/`](data/gold/inmobiliario/)

### 📦 Entrega `E0` (`tag: e0`)
1. 📄 **Propuesta del Observatorio:** [`docs/E0/propuesta.md`](docs/E0/propuesta.md)
2. 📋 **Ficha de Entrega Técnica E0:** [`docs/E0/ENTREGA.md`](docs/E0/ENTREGA.md)
3. ⚙️ **Extractor Ético (Capa Bronce):** [`src/extract_bronze.py`](src/extract_bronze.py)
