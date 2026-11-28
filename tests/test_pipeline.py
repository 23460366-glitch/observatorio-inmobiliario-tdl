#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de Pruebas Automatizadas (Unitarias, Integridad de Datos, Cuarentena, Linaje y Estadística)
Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM — Trusted Data Lab
Autores:
  - Juan Antonio Ortiz Hinojosa
  - Diego Alberto Virgen Cuéllar
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import pytest

from src.analytics_e3_e4 import (
    get_tdl_seal_certification_metrics,
    run_factorial_experiment_2k,
    run_multivariate_pca_manova_e3,
    run_time_series_forecasting_e1,
    simulate_live_ingestion_batch,
)
from src.benchmark_optimizacion_e3 import (
    load_or_run_e3_optimization_report,
    run_e3_pipeline_optimization_benchmark,
)
from src.extract_bronze import (
    check_robots_txt,
    fetch_banxico_macro_series,
    generate_36_month_periods,
    generate_rental_market_bronze_series,
    main as main_extract_bronze,
)
from src.pipeline_e1 import (
    build_gold_layer_datasets,
    build_pandera_pre_silver_schema,
    detect_and_treat_outliers,
    diagnose_and_impute_missing_values,
    load_and_integrate_sources,
    main as main_pipeline_e1,
    normalize_banxico_date_to_ym,
    parse_currency_or_float,
    run_full_e1_pipeline,
    run_quality_gate_with_quarantine,
    transform_scale_discretize_and_hierarchies,
)
from src.pipeline_e2 import (
    build_colima_geospatial_gold_and_map,
    compute_sha256_short,
    create_colonia_polygon,
    enrich_silver_with_geopandas_and_lineage,
    extract_geospatial_bronze_source,
    generate_cartographic_visualizations,
    main as main_pipeline_e2,
    run_full_e2_pipeline,
    update_gold_layer_with_full_lineage,
)

BASE_DIR = Path(__file__).resolve().parent.parent


def test_bronze_extraction_and_periods():
    """Verifica que la Capa Bronce genere al menos 36 periodos mensuales consecutivos y audite robots.txt."""
    periods = generate_36_month_periods(end_year=2026, end_month=10, n_months=36)
    assert len(periods) == 36
    assert periods[0] == "2023-11"
    assert periods[-1] == "2026-10"

    robots = check_robots_txt("https://www.banxico.org.mx", "/SieAPIRest/service/v1/")
    assert "allowed" in robots
    assert robots["crawl_delay_seconds"] >= 1.0

    macro_records, macro_meta = fetch_banxico_macro_series(periods)
    assert len(macro_records) == 36
    assert "inpc_vivienda_zmvm" in macro_records[0]

    monthly_agg, listings_bronze, market_meta = generate_rental_market_bronze_series(periods, macro_records)
    assert len(monthly_agg) == 36
    assert len(listings_bronze) >= 1200
    assert market_meta["total_periodos_mensuales"] == 36


def test_parsers_and_integration_e1():
    """Verifica la limpieza de tipos monetarios, fechas BANXICO y la integración M:1 de fuentes."""
    assert parse_currency_or_float("$32,450.50 MXN") == 32450.50
    assert parse_currency_or_float(18500) == 18500.0
    assert pd.isna(parse_currency_or_float(None))
    assert pd.isna(parse_currency_or_float("N/E"))
    assert normalize_banxico_date_to_ym("01/11/2023", "2023-11") == "2023-11"
    assert normalize_banxico_date_to_ym(None, "2024-05") == "2024-05"

    df_merged, rep = load_and_integrate_sources()
    assert len(df_merged) >= 1200
    assert rep["registros_sin_match_macro"] == 0
    assert rep["conflictos_moneda_string_resueltos"] > 0
    assert rep["conflictos_categoria_tipo_inmueble_resueltos"] > 0


def test_pandera_quality_gate_and_quarantine():
    """Verifica que la Puerta de Calidad de Pandera envíe registros inválidos a cuarentena con motivo documentado."""
    df_merged, _ = load_and_integrate_sources()
    schema = build_pandera_pre_silver_schema()
    assert schema is not None

    df_valid, df_quarantine, gate_rep = run_quality_gate_with_quarantine(df_merged)
    assert len(df_valid) >= 1200
    assert len(df_quarantine) > 0
    assert "motivo_cuarentena" in df_quarantine.columns
    assert gate_rep["total_aprobados_plata"] + gate_rep["total_enviados_cuarentena"] == gate_rep["total_evaluados"]
    assert (df_valid["renta_lista_mensual_mxn"] > 1500.0).all()


def test_missing_values_outliers_and_gold_e1():
    """Verifica el diagnóstico e imputación MCAR/MAR/MNAR, detección de atípicos, escalado y Capa Oro E1."""
    df_merged, _ = load_and_integrate_sources()
    df_valid, _, _ = run_quality_gate_with_quarantine(df_merged)

    df_imp, miss_rep = diagnose_and_impute_missing_values(df_valid)
    assert df_imp["estacionamientos"].isna().sum() == 0
    assert df_imp["superficie_m2"].isna().sum() == 0
    assert df_imp["cuota_mantenimiento_mxn"].isna().sum() == 0
    assert "flag_mnar_mantenimiento" in df_imp.columns
    assert miss_rep["diagnostico_mecanismos"]["superficie_m2_MAR"]["p_value"] < 0.05

    df_out, out_rep = detect_and_treat_outliers(df_imp)
    assert "precio_m2_winsor_mxn" in df_out.columns
    assert out_rep["precio_m2_max_despues_winsor"] <= out_rep["precio_m2_max_antes_winsor"]

    df_tr, tr_rep = transform_scale_discretize_and_hierarchies(df_out)
    assert "precio_m2_mxn_minmax" in df_tr.columns
    assert "precio_m2_mxn_zscore" in df_tr.columns
    assert "jerarquia_ubicacion_completa" in df_tr.columns

    gold_datasets, red_rep = build_gold_layer_datasets(df_tr)
    assert red_rep["filas_oro_e1_series_tiempo"] == 36
    assert "oro_e2_simulacion_whatif_24m" in gold_datasets
    assert "oro_e3_comparacion_multivariada_yield" in gold_datasets


def test_geospatial_and_full_lineage_e2():
    """Verifica GeoPandas UTM 14N, linaje 100% Oro->Bronce y mapa interactivo estilo Google Earth sin watermark CARTO."""
    poly = create_colonia_polygon(19.4335, -99.1945)
    assert poly.is_valid
    assert len(poly.exterior.coords) >= 20
    assert len(compute_sha256_short("test_payload")) == 16

    gdf_col, gdf_est, geo_meta = extract_geospatial_bronze_source()
    assert len(gdf_col) == 16
    assert len(gdf_est) == 14

    gdf_silver_geo, sp_sum = enrich_silver_with_geopandas_and_lineage(gdf_col, gdf_est, geo_meta)
    assert sp_sum["total_inmuebles_georreferenciados"] == len(gdf_silver_geo)
    assert "dist_transporte_masivo_m" in gdf_silver_geo.columns
    assert "linaje_hash_registro_bronce" in gdf_silver_geo.columns

    lin_sum = update_gold_layer_with_full_lineage(gdf_silver_geo)
    assert lin_sum["registros_oro_con_linaje_completo_pct"] == 100.0
    assert lin_sum["registros_oro_huerfanos"] == 0
    build_colima_geospatial_gold_and_map()

    cart_out = generate_cartographic_visualizations(gdf_col, gdf_est)
    html_content = (BASE_DIR / cart_out["mapa_interactivo_zmvm_html" if "mapa_interactivo_zmvm_html" in cart_out else "mapa_interactivo_html"]).read_text(encoding="utf-8")
    assert "World_Imagery" in html_content
    assert "World_Boundaries_and_Places" in html_content
    assert "cartocdn.com" not in html_content


def test_statistical_analytics_e1_e2_e3_e4():
    """Verifica series de tiempo (4 modelos + Ljung-Box), factorial 2^3 y 2^(4-1), PCA/MANOVA y Sello TDL."""
    ts_res = run_time_series_forecasting_e1(horizon_months=12)
    assert len(ts_res["metricas_comparativas_modelos"]) == 4
    assert len(ts_res["pronostico_12_meses_df"]) == 12
    assert len(ts_res["pronostico_4_trimestres_df"]) >= 4

    fact_res = run_factorial_experiment_2k()
    assert len(fact_res["experimento_2_3_df"]) == 24
    assert fact_res["comparativa_2_4_vs_2_4_1"]["ahorro_experimental_pct"] == 50.0
    assert fact_res["corrida_confirmacion"]["reduccion_latencia_pct"] > 30.0

    mv_res = run_multivariate_pca_manova_e3()
    assert mv_res["pca"]["varianza_acumulada_2pc_pct"] > 70.0
    assert len(mv_res["manova_tabla_df"]) == 8
    assert mv_res["manova_tabla_df"]["Significativo_alpha_05"].all()

    tdl_res = get_tdl_seal_certification_metrics()
    assert tdl_res["kpis_sello_tdl"]["secretos_expuestos"] == 0
    assert tdl_res["kpis_sello_tdl"]["completitud_iso25012_pct"] >= 95.0

    sim_res = simulate_live_ingestion_batch(n_valid=6, n_dirty=4, persist_to_quarantine=False)
    assert sim_res["reporte_puerta_calidad"]["total_aprobados_plata"] == 6
    assert sim_res["reporte_puerta_calidad"]["total_enviados_cuarentena"] == 4


def test_colima_villa_de_alvarez_expansion_and_lineage():
    """
    Verifica la extracción, validación Pandera, Capa Oro (`oro_colima_zm.csv`, `oro_geoespacial_colima.geojson`
    y `oro_geoespacial_maestro_unificado.geojson`), completitud ISO/IEC 25012 (>= 95%), linaje en
    `catalogo_linaje_oro_a_bronce.csv`, mapa maestro unificado (`mapa_interactivo_zmvm.html` con botones `flyTo`
    y sin duplicado `mapa_interactivo_colima.html`), pronóstico y PCA/MANOVA para Colima – Villa de Álvarez.
    """
    oro_colima_csv = BASE_DIR / "data/gold/inmobiliario/oro_colima_zm.csv"
    oro_colima_geojson = BASE_DIR / "data/gold/inmobiliario/oro_geoespacial_colima.geojson"
    oro_unified_geojson = BASE_DIR / "data/gold/inmobiliario/oro_geoespacial_maestro_unificado.geojson"
    mapa_maestro_html = BASE_DIR / "docs/E2/mapa_interactivo_zmvm.html"
    mapa_colima_dup_html = BASE_DIR / "docs/E2/mapa_interactivo_colima.html"
    reporte_cliente_md = BASE_DIR / "docs/E4/reporte_inteligencia_cliente.md"

    assert oro_colima_csv.exists()
    assert oro_colima_geojson.exists()
    assert oro_unified_geojson.exists()
    assert mapa_maestro_html.exists()
    assert not mapa_colima_dup_html.exists(), "El archivo duplicado mapa_interactivo_colima.html no debe existir"
    assert reporte_cliente_md.exists()

    # Verificar que el GeoJSON maestro unificado contiene las 24 zonas (16 ZMVM + 8 Colima-VdeA) con columna region
    unified_data = json.loads(oro_unified_geojson.read_text(encoding="utf-8"))
    assert len(unified_data["features"]) == 24
    regions_set = {f["properties"]["region"] for f in unified_data["features"]}
    assert regions_set == {"ZMVM", "Colima-VdeA"}

    # Verificar que el mapa maestro HTML contiene los 3 botones flyTo/fitBounds, etiquetas permanent=True y renta 70 m²
    master_html_text = mapa_maestro_html.read_text(encoding="utf-8")
    assert "flyTo([19.415, -99.165], 12" in master_html_text
    assert "flyTo([19.245, -103.725], 13" in master_html_text
    assert "fitBounds([[19.20, -103.80], [19.55, -99.10]]" in master_html_text
    assert "tdl-zone-tooltip" in master_html_text
    assert "syncZoneTooltipsWithZoom" in master_html_text
    assert "Renta Mensual Estimada (dept. 70 m²):" in master_html_text
    assert "Esmeralda Norte" in master_html_text
    assert "Polanco" in master_html_text

    df_col_gold = pd.read_csv(oro_colima_csv, encoding="utf-8")
    assert len(df_col_gold) == 8
    expected_colonias = {
        "Esmeralda Norte",
        "Esmeralda Sur",
        "Lomas de Vista Hermosa",
        "Jardines de las Lomas",
        "Zona Centro Colima",
        "Zona Universidad / Las Víboras",
        "Real Bugambilias",
        "La Comarca / Bosque Real",
    }
    assert set(df_col_gold["colonia"].tolist()) == expected_colonias

    # Completitud ISO/IEC 25012 >= 95% (100% real)
    completeness_colima = (1.0 - float(df_col_gold.isna().sum().sum()) / float(df_col_gold.size)) * 100.0
    assert completeness_colima >= 95.0

    # Verificar trazabilidad en catalogo_linaje_oro_a_bronce.csv
    df_lineage = pd.read_csv(BASE_DIR / "data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv", encoding="utf-8")
    colima_lineage = df_lineage[df_lineage["tabla_capa_oro"] == "data/gold/inmobiliario/oro_colima_zm.csv"]
    assert len(colima_lineage) == 8
    assert colima_lineage["hash_lote_bronce"].str.startswith("SHA256:").all()

    # Verificar que los datos de la ZMVM siguen intactos
    df_zmvm_gold = pd.read_csv(BASE_DIR / "data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv", encoding="utf-8")
    assert len(df_zmvm_gold) == 16

    # Verificar motor de pronóstico y PCA/MANOVA en modo Colima
    ts_col = run_time_series_forecasting_e1(horizon_months=12, region="COLIMA")
    assert len(ts_col["pronostico_12_meses_df"]) == 12
    mv_col = run_multivariate_pca_manova_e3(region="COLIMA")
    assert len(mv_col["pca"]["scores_colonias_df"]) == 8
    assert mv_col["pca"]["varianza_acumulada_2pc_pct"] > 70.0


def test_e3_optimization_benchmark_and_svg_map():
    """
    Verifica los entregables de E3 (benchmark cuantitativo Antes vs. Después en tiempo, memoria y errores,
    `docs/E3/datasheet.md`, `docs/relatoria-E3.md`, `docs/E3/ENTREGA.md`) y el rediseño SVG sin emojis del mapa E2.
    """
    bench = run_e3_pipeline_optimization_benchmark(n_repeats=2)
    cached_bench = load_or_run_e3_optimization_report()
    assert cached_bench["n_registros_evaluados_por_corrida"] >= 2000

    assert bench["metricas_tiempo_ms"]["reduccion_tiempo_pct"] > 50.0
    assert bench["metricas_memoria"]["reduccion_pico_heap_pct"] > 30.0
    assert bench["metricas_memoria"]["reduccion_dataframe_ram_pct"] > 50.0
    assert bench["metricas_calidad_y_errores"]["errores_infiltrados_despues"] == 0
    assert bench["metricas_calidad_y_errores"]["reduccion_errores_pct"] == 100.0

    for rel_path in (
        "docs/E3/datasheet.md",
        "docs/E3/ENTREGA.md",
        "docs/relatoria-E3.md",
        "data/gold/inmobiliario/comparativa_optimizacion_e3.csv",
        "data/gold/inmobiliario/reporte_optimizacion_e3.json",
    ):
        p = BASE_DIR / rel_path
        assert p.exists() and p.stat().st_size > 200, f"Falta entregable requerido: {rel_path}"

    mapa_html = (BASE_DIR / "docs/E2/mapa_interactivo_zmvm.html").read_text(encoding="utf-8")
    assert "<svg" in mapa_html
    assert "Plus Jakarta Sans" in mapa_html
    assert "JetBrains Mono" in mapa_html
    for forbidden_emoji in ("🛰️", "🗺️", "🏙️", "🧭", "🌴", "🇲🇽", "🏪", "🚇", "📍", "🌎", "📊", "💡"):
        assert forbidden_emoji not in mapa_html, f"Emoji no permitido en el mapa E2: {forbidden_emoji}"


def test_entrypoints_and_zero_hardcoded_secrets():
    """Ejecuta los entrypoints principales y audita que no existan API keys ni secretos hardcodeados en el código."""
    main_extract_bronze()
    main_pipeline_e1()
    main_pipeline_e2()

    secret_pattern = re.compile(r"(AIza[0-9A-Za-z\-_]{35}|sk-[0-9A-Za-z]{32,}|ghp_[0-9A-Za-z]{30,})")
    for py_file in (BASE_DIR / "src").glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        assert not secret_pattern.search(text), f"Posible secreto detectado en {py_file.name}"
