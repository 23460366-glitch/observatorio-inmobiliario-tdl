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


def test_entrypoints_and_zero_hardcoded_secrets():
    """Ejecuta los entrypoints principales y audita que no existan API keys ni secretos hardcodeados en el código."""
    main_extract_bronze()
    main_pipeline_e1()
    main_pipeline_e2()

    secret_pattern = re.compile(r"(AIza[0-9A-Za-z\-_]{35}|sk-[0-9A-Za-z]{32,}|ghp_[0-9A-Za-z]{30,})")
    for py_file in (BASE_DIR / "src").glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        assert not secret_pattern.search(text), f"Posible secreto detectado en {py_file.name}"
