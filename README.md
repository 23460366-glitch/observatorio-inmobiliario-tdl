# 🏢 Observatorio del Mercado Inmobiliario y Renta Habitacional (ZMVM)

Repositorio oficial del **Proyecto Integrador** enfocado en el análisis econométrico, simulación *what-if*, comparación multivariada e integración geoespacial del mercado de alquiler residencial en la Zona Metropolitana del Valle de México (ZMVM).

## 👥 Integrantes del Equipo
- **Juan Antonio Ortiz Hinojosa**
- **Diego Alberto Virgen Cuéllar**

---

## 📂 Estructura del Repositorio (Entregas `e0`, `e1` y `e2`)

```text
observatorio-inmobiliario/
├── .github/
│   └── workflows/
│       └── bronze_capture.yml                                    # Pipeline CI/CD (Bronce -> Plata -> Geoespacial -> Oro + Linaje)
├── calidad/
│   ├── defectos-diego-alberto-virgen-cuellar.csv                 # Bitácora PSP de defectos (E0 + E1 + E2)
│   ├── defectos-juan-antonio-ortiz-hinojosa.csv                  # Bitácora PSP de defectos (E0 + E1 + E2)
│   ├── tiempo-diego-alberto-virgen-cuellar.csv                   # Bitácora PSP de tiempos (E0 + E1 + E2)
│   └── tiempo-juan-antonio-ortiz-hinojosa.csv                    # Bitácora PSP de tiempos (E0 + E1 + E2)
├── data/
│   ├── bronze/
│   │   └── inmobiliario/
│   │       ├── macro_banxico_inegi_36m.json                      # 36 meses de INPC Vivienda, TIIE 28d y FIX
│   │       ├── rentas_zmvm_historico_36m.json                    # 36 meses de ofertas crudas en la ZMVM
│   │       ├── geoespacial_denue_osm_zmvm.geojson                # Polígonos AGEB/Colonias MGN INEGI + Unidades DENUE (E2)
│   │       ├── estaciones_transporte_osm_zmvm.geojson            # Nodos de transporte masivo OpenStreetMap (E2)
│   │       ├── geoespacial_metadata_e2.json                      # Metadatos y auditoría robots.txt de INEGI y OSM (E2)
│   │       ├── serie_consolidada_36m.csv                         # Serie mensual consolidada en crudo
│   │       └── snapshots/
│   │           └── captura_2026-10.json
│   ├── silver/
│   │   └── inmobiliario/
│   │       ├── rentas_zmvm_plata_limpio.csv                      # 1,291 registros validados, imputados y escalados (E1)
│   │       ├── rentas_zmvm_plata_geolocalizado_e2.csv            # 1,291 registros enriquecidos con GeoPandas y Linaje (E2)
│   │       ├── cuarentena_inmobiliario.csv                       # 8 registros inválidos en cuarentena con motivo (E1)
│   │       └── cuarentena_inmobiliario.json
│   └── gold/
│       └── inmobiliario/
│           ├── oro_e1_pronostico_mensual_trimestral.csv          # Cubo Oro para E1 con columnas de linaje a Bronce
│           ├── oro_e2_simulacion_whatif_24m.csv                  # Cubo Oro para E2 con columnas de linaje a Bronce
│           ├── oro_e3_comparacion_multivariada_yield.csv         # Cubo Oro para E3 con columnas de linaje a Bronce
│           ├── oro_geoespacial_colonias_denue_osm.csv            # Cubo Oro Geoespacial (16 colonias DENUE+OSM+Linaje) (E2)
│           ├── catalogo_linaje_oro_a_bronce.csv                  # Catálogo maestro de trazabilidad 100% Oro -> Bronce (E2)
│           ├── catalogo_linaje_oro_a_bronce.json
│           ├── reporte_auditoria_pipeline_e1.json
│           └── reporte_auditoria_pipeline_e2.json
├── docs/
│   ├── E0/
│   │   ├── propuesta.md                                          # Propuesta extensa del Observatorio (E0)
│   │   └── ENTREGA.md                                            # Ficha de entrega técnica E0
│   ├── E1/
│   │   ├── limpieza.ipynb                                        # Notebook ejecutado de Limpieza y Preprocesamiento (E1)
│   │   └── ENTREGA.md                                            # Ficha de entrega técnica E1
│   ├── E2/
│   │   ├── geoespacial_linaje.ipynb                              # Notebook ejecutado de GeoPandas y Linaje de Datos (E2)
│   │   ├── mapa_coropletico_precio_equipamiento_zmvm.png         # Cartografía dual Precio/m2 vs DENUE y Transporte OSM (E2)
│   │   ├── mapa_interactivo_zmvm.html                            # Mapa interactivo Folium HTML (E2)
│   │   └── ENTREGA.md                                            # Ficha de entrega técnica E2
│   ├── etica-datos.md                                            # Declaración de Ética, Legalidad y Privacidad (E2)
│   ├── relatoria-E1.md                                           # Relatoría técnica de etapa E1
│   └── relatoria-E2.md                                           # Relatoría técnica de etapa E2
├── src/
│   ├── extract_bronze.py                                         # Extractor ético de Capa Bronce
│   ├── pipeline_e1.py                                            # Pipeline E1 (Integración, Pandera, Plata y Oro)
│   ├── pipeline_e2.py                                            # Pipeline E2 (GeoPandas DENUE/OSM, Cartografía y Linaje)
│   ├── build_notebook_e1.py
│   └── build_notebook_e2.py
├── requirements.txt
└── README.md
```

---

## 🔗 Accesos Directos a los Entregables

### 📦 Entrega `E2` (`tag: e2`)
1. 🗺️ **Notebook Ejecutado (GeoPandas + Linaje Completo):** [`docs/E2/geoespacial_linaje.ipynb`](docs/E2/geoespacial_linaje.ipynb)
2. 🖼️ **Visualización Cartográfica Coroplética (`PNG`):** [`docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png`](docs/E2/mapa_coropletico_precio_equipamiento_zmvm.png)
3. 🌐 **Mapa Interactivo (`Folium HTML`):** [`docs/E2/mapa_interactivo_zmvm.html`](docs/E2/mapa_interactivo_zmvm.html)
4. ⚖️ **Declaración de Ética y Legalidad:** [`docs/etica-datos.md`](docs/etica-datos.md)
5. 🔗 **Catálogo Maestro de Linaje (`Oro -> Bronce`):** [`data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv`](data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv)
6. 📋 **Ficha Técnica de Entrega E2:** [`docs/E2/ENTREGA.md`](docs/E2/ENTREGA.md)
7. 📝 **Relatoría de Etapa E2:** [`docs/relatoria-E2.md`](docs/relatoria-E2.md)

### 📦 Entrega `E1` (`tag: e1`)
1. 📓 **Notebook de Limpieza y Preprocesamiento:** [`docs/E1/limpieza.ipynb`](docs/E1/limpieza.ipynb)
2. 📋 **Ficha Técnica de Entrega E1:** [`docs/E1/ENTREGA.md`](docs/E1/ENTREGA.md)
3. 📝 **Relatoría de Etapa E1:** [`docs/relatoria-E1.md`](docs/relatoria-E1.md)

### 📦 Entrega `E0` (`tag: e0`)
1. 📄 **Propuesta del Observatorio:** [`docs/E0/propuesta.md`](docs/E0/propuesta.md)
2. 📋 **Ficha de Entrega Técnica E0:** [`docs/E0/ENTREGA.md`](docs/E0/ENTREGA.md)
