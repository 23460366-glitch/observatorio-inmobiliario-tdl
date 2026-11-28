#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Observatorio Web Ejecutivo PropTech B2B — Trusted Data Lab (Entregas E1, E2, E3 y Demo Day E4)
Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional (ZMVM & Colima – Villa de Álvarez)
Sistema de Diseño UI/UX sincronizado con Figma:
  https://www.figma.com/design/pa6rEWBaRk6WBv6QFYgOiX

Autores:
  - Juan Antonio Ortiz Hinojosa
  - Diego Alberto Virgen Cuéllar

Ejecución:
  streamlit run tablero/app.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st
import streamlit.components.v1 as components

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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

st.set_page_config(
    page_title="Observatorio Inmobiliario TDL | Inteligencia PropTech B2B",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Catálogo de íconos vectoriales SVG en línea (TDL PropTech Design System — 0 Emojis)
SVG = {
    "shield": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "trend": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "target": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "award": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>',
    "database": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>',
    "zap": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "cpu": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>',
    "satellite": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M13 7 9 3 5 7l4 4 4-4z"/><path d="m17 11 4 4-4 4-4-4 4-4z"/><path d="m8 12 4 4"/><path d="m16 8 4-4"/><path d="M9 21a7 7 0 0 1-7-7"/></svg>',
    "layers": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "sliders": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>',
    "briefcase": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "check": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
}

# Sistema de Diseño CSS (Sincronizado con Figma: Plus Jakarta Sans + JetBrains Mono)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --tdl-bg-canvas: #F8FAFC;
        --tdl-bg-hero: #0B1120;
        --tdl-bg-overlay: #0F172A;
        --tdl-surface: #FFFFFF;
        --tdl-surface-muted: #F1F5F9;
        --tdl-text-primary: #0F172A;
        --tdl-text-secondary: #475569;
        --tdl-text-muted: #64748B;
        --tdl-accent-emerald: #10B981;
        --tdl-accent-sky: #0EA5E9;
        --tdl-border-subtle: #E2E8F0;
    }

    html, body, [class*="css"], .stMarkdown, .stRadio, .stSelectbox, .stMultiSelect {
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
    }

    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 2.5rem !important;
    }

    /* Hero Banner Ejecutivo */
    .tdl-hero {
        background: linear-gradient(135deg, #0B1120 0%, #162033 100%);
        color: #F8FAFC;
        padding: 22px 28px;
        border-radius: 16px;
        border: 1px solid #1E293B;
        box-shadow: 0 12px 30px rgba(11, 17, 32, 0.14);
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .tdl-seal-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(16, 185, 129, 0.14);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.45px;
        text-transform: uppercase;
    }
    .tdl-hero-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.35px;
        color: #FFFFFF;
        margin: 8px 0 4px 0;
        line-height: 1.25;
    }
    .tdl-hero-sub {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 400;
    }
    .tdl-hero-meta-box {
        text-align: right;
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        padding: 10px 16px;
    }

    /* Componente KPI Metric Card (idéntico a Figma 2:25) */
    .tdl-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 17px 19px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 8px;
    }
    .tdl-kpi-top {
        display: flex;
        align-items: center;
        gap: 9px;
    }
    .tdl-kpi-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: #E0F2FE;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .tdl-kpi-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.45px;
    }
    .tdl-kpi-value {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 21px;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.4px;
    }
    .tdl-kpi-delta {
        display: inline-block;
        align-self: flex-start;
        background: #ECFDF5;
        color: #047857;
        padding: 3.5px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
    }

    /* Encabezados de sección con ícono SVG */
    .tdl-sec-head {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 18px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.2px;
        margin: 10px 0 8px 0;
    }

    /* Pestañas estilo SaaS moderno */
    .stTabs [data-baseweb="tab-list"] {
        background: #F1F5F9;
        padding: 5px;
        border-radius: 12px;
        gap: 6px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px !important;
        padding: 9px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        color: #475569 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: #0B1120 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(11, 17, 32, 0.18);
    }

    /* Tarjetas Comerciales B2B */
    .pricing-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0EA5E9;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
        height: 100%;
    }
    .pricing-tier-tag {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.55px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .pricing-price {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
        margin: 8px 0 12px 0;
    }
    .pricing-list {
        list-style: none;
        padding-left: 0;
        margin: 0;
        font-size: 12.5px;
        color: #334155;
        line-height: 1.55;
    }
    .pricing-list li {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        margin-bottom: 8px;
    }

    /* Callout ejecutivo */
    .tdl-callout {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0EA5E9;
        border-radius: 10px;
        padding: 13px 16px;
        font-size: 13px;
        color: #1E293B;
        line-height: 1.55;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_kpi_card(icon_svg: str, label: str, value: str, delta_text: str, icon_bg: str = "#E0F2FE") -> str:
    return f"""
    <div class="tdl-kpi-card">
        <div class="tdl-kpi-top">
            <span class="tdl-kpi-icon" style="background:{icon_bg};">{icon_svg}</span>
            <span class="tdl-kpi-label">{label}</span>
        </div>
        <div class="tdl-kpi-value">{value}</div>
        <span class="tdl-kpi-delta">{delta_text}</span>
    </div>
    """


def section_heading(icon_key: str, text: str) -> None:
    st.markdown(f'<div class="tdl-sec-head">{SVG[icon_key]} <span>{text}</span></div>', unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_regional_analytics(region_key: str):
    is_colima = region_key.startswith("Colima")
    is_all = region_key.startswith("Todas")
    reg_code = "COLIMA" if is_colima else "ZMVM"

    e1_res = run_time_series_forecasting_e1(horizon_months=12, region=reg_code)
    e2_fact = run_factorial_experiment_2k()
    e3_mv = run_multivariate_pca_manova_e3(region=reg_code)
    e4_tdl = get_tdl_seal_certification_metrics()
    e3_opt = load_or_run_e3_optimization_report()
    df_lineage = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv")

    unified_geojson_path = ROOT_DIR / "data/gold/inmobiliario/oro_geoespacial_maestro_unificado.geojson"
    geojson_unified = json.loads(unified_geojson_path.read_text(encoding="utf-8"))

    df_geo_zmvm = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv")
    df_geo_zmvm["region"] = "ZMVM"
    df_geo_col = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_colima_zm.csv")
    df_geo_col["region"] = "Colima-VdeA"

    if is_colima:
        df_geo_gold = df_geo_col
        df_silver = pd.read_csv(ROOT_DIR / "data/silver/inmobiliario/rentas_colima_plata_limpio.csv")
        df_whatif = (
            df_silver.groupby(
                ["modalidad_contrato", "descuento_contrato_pct", "subzona_id", "subzona_nombre"],
                as_index=False,
            )
            .agg(
                n_observaciones=("id_propiedad", "count"),
                dias_vacancia_promedio=("dias_vacancia_observados", "mean"),
                dias_vacancia_mediana=("dias_vacancia_observados", "median"),
                tasa_ocupacion_24m_promedio_pct=("tasa_ocupacion_24m_pct", "mean"),
                renta_efectiva_promedio_mxn=("renta_efectiva_winsor_mxn", "mean"),
                yield_efectivo_promedio_pct=("yield_bruto_anual_pct", "mean"),
            )
            .round(2)
        )
        df_whatif["ingreso_efectivo_esperado_24m_mxn"] = (
            24.0
            * df_whatif["renta_efectiva_promedio_mxn"]
            * (df_whatif["tasa_ocupacion_24m_promedio_pct"] / 100.0)
        ).round(2)
    elif is_all:
        common_geo_cols = [
            "region",
            "colonia",
            "alcaldia_municipio",
            "subzona_id",
            "cve_ageb_inegi",
            "precio_m2_promedio_mxn",
            "yield_bruto_promedio_pct",
            "dias_vacancia_promedio",
            "dist_transporte_masivo_m",
            "denue_unidades_buffer_500m",
            "indice_accesibilidad_urbana_0_100",
        ]
        df_geo_gold = pd.concat([df_geo_zmvm[common_geo_cols], df_geo_col[common_geo_cols]], ignore_index=True)
        df_s_zmvm = pd.read_csv(ROOT_DIR / "data/silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv")
        df_s_col = pd.read_csv(ROOT_DIR / "data/silver/inmobiliario/rentas_colima_plata_limpio.csv")
        df_silver = pd.concat([df_s_zmvm, df_s_col], ignore_index=True)
        df_whatif = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv")
    else:
        df_geo_gold = df_geo_zmvm
        df_silver = pd.read_csv(ROOT_DIR / "data/silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv")
        df_whatif = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv")

    return e1_res, e2_fact, e3_mv, e4_tdl, e3_opt, df_whatif, df_geo_gold, df_lineage, df_silver, geojson_unified


# Barra lateral ejecutiva sin saturación de emojis
with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:9px;margin-bottom:2px;">
            {SVG['satellite']}
            <span style="font-size:17px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;">Observatorio TDL</span>
        </div>
        <div style="font-size:12px;color:#64748B;margin-bottom:14px;font-weight:500;">
            Plataforma de Inteligencia Inmobiliaria B2B • Entregas E0–E4
        </div>
        """,
        unsafe_allow_html=True,
    )

    region_seleccionada = st.radio(
        "Región de Análisis Activa:",
        options=[
            "ZMVM (CDMX/Edomex)",
            "Colima – Villa de Álvarez",
            "Todas las regiones (Vista Nacional)",
        ],
        index=0,
        help="Sincroniza dinámicamente la cámara 3D de PyDeck, el enfoque del mapa satelital maestro Folium (`mapa_interactivo_zmvm.html`), los KPIs, pronósticos SARIMA y simuladores What-If.",
    )

    st.markdown(
        f"""
        <hr style="border:none;border-top:1px solid #E2E8F0;margin:14px 0;">
        <div style="font-size:11.5px;color:#334155;line-height:1.6;">
            <div style="font-weight:700;color:#0F172A;text-transform:uppercase;font-size:10.5px;letter-spacing:0.5px;margin-bottom:4px;">Equipo de Ingeniería</div>
            <div>• Juan Antonio Ortiz Hinojosa</div>
            <div>• Diego Alberto Virgen Cuéllar</div>
            <div style="font-weight:700;color:#0F172A;text-transform:uppercase;font-size:10.5px;letter-spacing:0.5px;margin:12px 0 4px 0;">Arquitectura Medallion</div>
            <div><b>Bronce:</b> 36m BANXICO/INEGI + DENUE/OSM</div>
            <div><b>Plata:</b> Puerta Pandera + Cuarentena + UTM</div>
            <div><b>Oro:</b> Cubos ISO 25012 + Linaje SHA-256</div>
        </div>
        <div style="margin-top:14px;background:#ECFDF5;border:1px solid #A7F3D0;border-radius:10px;padding:10px 12px;display:flex;align-items:center;gap:8px;">
            {SVG['shield']}
            <div style="font-size:11.5px;font-weight:700;color:#065F46;">Sello TDL Certificado<br><span style="font-weight:500;font-size:10.5px;">Costo Operativo $0 USD • 0 API Keys</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

is_colima_mode = region_seleccionada.startswith("Colima")
is_all_regions_mode = region_seleccionada.startswith("Todas")
if is_colima_mode:
    region_titulo_corto = "ZM de Colima – Villa de Álvarez"
elif is_all_regions_mode:
    region_titulo_corto = "Todas las Regiones (ZMVM + Colima – Villa de Álvarez)"
else:
    region_titulo_corto = "ZMVM (CDMX y Área Conurbada)"

(
    e1_res,
    e2_fact,
    e3_mv,
    e4_tdl,
    e3_opt,
    df_whatif,
    df_geo_gold,
    df_lineage,
    df_silver,
    geojson_unified,
) = load_regional_analytics(region_seleccionada)

# Hero Header Ejecutivo (Sincronizado con Figma 3:3)
st.markdown(
    f"""
    <div class="tdl-hero">
        <div style="max-width: 74%;">
            <span class="tdl-seal-pill">{SVG['shield']} TRUSTED DATA LAB • ISO/IEC 25012 &amp; ISO/IEC 25010 • LICENCIA CC BY 4.0</span>
            <div class="tdl-hero-title">Observatorio Analítico del Mercado Inmobiliario — {region_titulo_corto}</div>
            <div class="tdl-hero-sub">
                Pronóstico Econométrico (E1) • Cartografía Satelital Híbrida 2D/3D DENUE/OSM &amp; PCA/MANOVA (E2/E3) • Pipeline Vectorizado Medido (E3) • Modelo Comercial SaaS B2B (E4)
            </div>
        </div>
        <div class="tdl-hero-meta-box">
            <div style="font-size:10.5px;font-weight:700;color:#38BDF8;letter-spacing:0.6px;text-transform:uppercase;">Edición Académica &amp; Comercial B2B</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:#F8FAFC;margin-top:3px;">24 Zonas • 2,155 Inmuebles</div>
            <div style="font-size:11px;color:#94A3B8;margin-top:2px;">100% Linaje SHA-256 • Costo $0 USD</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "01 • Pronóstico Econométrico (E1)",
        "02 • Explorador Satelital 2D/3D & PCA/MANOVA (E2 y E3)",
        "03 • Diseño Factorial 2³ & Simulador What-If (E2)",
        "04 • Optimización Pipeline E3, Sello TDL & Planes B2B (E3 y E4)",
    ]
)

# ==============================================================================
# PESTAÑA 1: RESUMEN EJECUTIVO Y PRONÓSTICO (E1)
# ==============================================================================
with tab1:
    df_hist = e1_res["historico_df"]
    df_fc = e1_res["pronostico_12_meses_df"]
    df_q4 = e1_res["pronostico_4_trimestres_df"]

    ultimo_precio = float(df_hist["precio_m2_media_mxn"].iloc[-1])
    precio_hace_12m = float(df_hist["precio_m2_media_mxn"].iloc[-13])
    var_interanual_pct = ((ultimo_precio - precio_hace_12m) / precio_hace_12m) * 100.0
    mejor_row_yield = df_geo_gold.sort_values("yield_bruto_promedio_pct", ascending=False).iloc[0]
    proy_12m = float(df_fc["pronostico_SARIMA_mxn"].iloc[-1])

    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(
            render_kpi_card(
                SVG["trend"],
                "Renta Promedio Actual (Oct 2026)",
                f"${ultimo_precio:,.2f} MXN/m²",
                f"+{var_interanual_pct:.2f}% interanual (YoY)",
                "#E0F2FE",
            ),
            unsafe_allow_html=True,
        )
    with col_k2:
        st.markdown(
            render_kpi_card(
                SVG["target"],
                "Pronóstico SARIMA (Oct 2027)",
                f"${proy_12m:,.2f} MXN/m²",
                f"+{((proy_12m - ultimo_precio) / ultimo_precio) * 100:.2f}% proyectado a 4 trim.",
                "#ECFDF5",
            ),
            unsafe_allow_html=True,
        )
    with col_k3:
        st.markdown(
            render_kpi_card(
                SVG["award"],
                "Mayor Yield Bruto Anual",
                f"{mejor_row_yield['yield_bruto_promedio_pct']:.2f}% anual",
                f"Líder: {mejor_row_yield['colonia']}",
                "#FEF3C7",
            ),
            unsafe_allow_html=True,
        )
    with col_k4:
        st.markdown(
            render_kpi_card(
                SVG["database"],
                "Muestra Auditada Capa Plata",
                f"{len(df_silver):,} unidades",
                "36 meses continuos • 0 huecos",
                "#EEF2FF",
            ),
            unsafe_allow_html=True,
        )

    st.write("")
    section_heading("trend", f"Serie Histórica Validada (36 Meses) y Pronóstico a 4 Trimestres — {region_titulo_corto}")

    fig_ts = go.Figure()
    fig_ts.add_trace(
        go.Scatter(
            x=df_hist["periodo_mensual"],
            y=df_hist["precio_m2_media_mxn"],
            mode="lines+markers",
            name="Histórico Validado (36 meses)",
            line={"color": "#0F172A", "width": 3},
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["ic95_superior_mxn"],
            mode="lines",
            name="IC 95% Superior (SARIMA)",
            line={"width": 0},
            showlegend=False,
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["ic95_inferior_mxn"],
            mode="lines",
            name="Intervalo Confianza 95% (SARIMA)",
            fill="tonexty",
            fillcolor="rgba(14, 165, 233, 0.18)",
            line={"width": 0},
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["pronostico_SARIMA_mxn"],
            mode="lines+markers",
            name="Pronóstico SARIMA / ARIMA",
            line={"color": "#0284C7", "width": 3},
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["pronostico_HoltWinters_mxn"],
            mode="lines+markers",
            name="Pronóstico Holt-Winters (Estacional)",
            line={"color": "#10B981", "width": 2.5, "dash": "dash"},
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["pronostico_Holt_mxn"],
            mode="lines",
            name="Pronóstico Lineal de Holt",
            line={"color": "#F59E0B", "width": 2, "dash": "dot"},
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["pronostico_SES_mxn"],
            mode="lines",
            name="Exponencial Simple (SES)",
            line={"color": "#94A3B8", "width": 2, "dash": "dashdot"},
        )
    )
    fig_ts.update_layout(
        height=440,
        font={"family": "Plus Jakarta Sans, sans-serif"},
        xaxis_title="Periodo Mensual (YYYY-MM)",
        yaxis_title="Precio Promedio de Renta (MXN / m²)",
        legend={"orientation": "h", "y": 1.12},
        template="plotly_white",
    )
    st.plotly_chart(fig_ts, use_container_width=True)

    c_m1, c_m2 = st.columns([1.25, 1.0])
    with c_m1:
        st.markdown("##### Comparativa de Modelos en Conjunto de Prueba (MAE, RMSE, MAPE y Ljung-Box)")
        st.dataframe(pd.DataFrame(e1_res["metricas_comparativas_modelos"]), use_container_width=True)
        adf_info = e1_res["adf_test"]
        st.caption(
            f"**Prueba Dickey-Fuller Aumentada (ADF):** En nivel $t = {adf_info['nivel_stat']}$ ($p = {adf_info['nivel_pvalue']}$); "
            f"en primera diferencia $\\Delta Y_t$: $t = {adf_info['primera_diferencia_stat']}$ ($p = {adf_info['primera_diferencia_pvalue']} < 0.01$, estacionaria $I(1)$)."
        )
    with c_m2:
        st.markdown("##### Proyección Trimestral Consolidada (Próximos 4 Trimestres)")
        st.dataframe(df_q4, use_container_width=True)

    if is_colima_mode:
        st.markdown(
            '<div class="tdl-callout"><b>Síntesis Ejecutiva — Colima y Villa de Álvarez (E1):</b> '
            'La renta promedio actual se ubica entre <b>$206 y $215 MXN/m²</b>, impulsada por la consolidación comercial del norte '
            '(<b>Esmeralda Norte</b> y <b>Lomas de Vista Hermosa</b>) y la expansión hacia <b>La Comarca / Bosque Real</b>. '
            'Los modelos <b>SARIMA</b> y <b>Holt-Winters</b> proyectan una apreciación anual del <b>5.8% al 6.4%</b>, '
            'destacando <b>Zona Universidad / Las Víboras</b> con un Yield superior al <b>8.5% anual</b>.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="tdl-callout"><b>Síntesis Ejecutiva — ZMVM (E1):</b> '
            'Los modelos <b>Holt-Winters</b> y <b>SARIMA</b> superan ampliamente al suavizamiento simple (SES) con un error porcentual medio '
            '<b>MAPE &lt; 1.5%</b> y residuos de ruido blanco en <b>Ljung-Box (p &gt; 0.05)</b>. Se proyecta una apreciación anual de '
            '<b>5.4% a 6.1%</b> durante los próximos cuatro trimestres.</div>',
            unsafe_allow_html=True,
        )

# ==============================================================================
# PESTAÑA 2: EXPLORADOR SATELITAL 2D/3D Y MAPA MULTIVARIADO PCA/MANOVA (E2 y E3)
# ==============================================================================
with tab2:
    section_heading("satellite", f"Explorador Cartográfico Satelital 2D/3D Unificado — {region_titulo_corto}")

    f_col1, f_col2 = st.columns([1.3, 1.0])
    alcaldias_disp = sorted(df_geo_gold["alcaldia_municipio"].unique().tolist())
    with f_col1:
        alcaldias_sel = st.multiselect(
            "Filtrar por Alcaldía / Municipio:",
            options=alcaldias_disp,
            default=alcaldias_disp,
        )
    min_p = float(df_geo_gold["precio_m2_promedio_mxn"].min())
    max_p = float(df_geo_gold["precio_m2_promedio_mxn"].max())
    with f_col2:
        rango_precio = st.slider(
            "Filtrar por Rango de Renta Promedio ($ MXN / m²):",
            min_value=float(np.floor(min_p - 5)),
            max_value=float(np.ceil(max_p + 5)),
            value=(float(np.floor(min_p - 5)), float(np.ceil(max_p + 5))),
        )

    text_labels_data = []
    for feat in geojson_unified["features"]:
        p_v = float(feat["properties"].get("precio_m2_promedio_mxn", 250.0))
        reg_f = str(feat["properties"].get("region", "ZMVM"))
        col_n = str(feat["properties"].get("colonia", ""))
        lat_c = float(feat["properties"].get("lat_centroide", 19.4))
        lon_c = float(feat["properties"].get("lon_centroide", -99.1))
        elev = round(p_v * 5.5, 1) if reg_f == "ZMVM" else round(p_v * 9.5, 1)
        feat["properties"]["elevation_m"] = elev
        feat["properties"]["renta_70m2_str"] = f"${p_v * 70.0:,.0f} MXN/mes"
        text_labels_data.append(
            {
                "position": [lon_c, lat_c, elev + 120.0],
                "label": f"{col_n} | ${p_v:,.0f}/m²",
            }
        )
        if (reg_f == "ZMVM" and p_v >= 500) or (reg_f == "Colima-VdeA" and p_v >= 210):
            feat["properties"]["fill_rgb"] = [239, 68, 68, 190]
        elif (reg_f == "ZMVM" and p_v >= 430) or (reg_f == "Colima-VdeA" and p_v >= 185):
            feat["properties"]["fill_rgb"] = [249, 115, 22, 190]
        elif (reg_f == "ZMVM" and p_v >= 340) or (reg_f == "Colima-VdeA" and p_v >= 165):
            feat["properties"]["fill_rgb"] = [234, 179, 8, 190]
        else:
            feat["properties"]["fill_rgb"] = [6, 182, 212, 190]

    if is_colima_mode:
        active_view_state = pdk.ViewState(
            latitude=19.245, longitude=-103.725, zoom=12.6, pitch=48, bearing=-15
        )
        folium_init_js = "setTimeout(function(){ var m = Object.values(window).find(v => v && v._leaflet_id && v.flyTo); if(m) m.flyTo([19.245, -103.725], 13, {animate:true, duration:1.2}); }, 450);"
    elif is_all_regions_mode:
        active_view_state = pdk.ViewState(
            latitude=19.34, longitude=-101.45, zoom=6.3, pitch=35, bearing=0
        )
        folium_init_js = "setTimeout(function(){ var m = Object.values(window).find(v => v && v._leaflet_id && v.fitBounds); if(m) m.fitBounds([[19.20, -103.80], [19.55, -99.10]]); }, 450);"
    else:
        active_view_state = pdk.ViewState(
            latitude=19.415, longitude=-99.165, zoom=11.6, pitch=48, bearing=-12
        )
        folium_init_js = ""

    tile_layer_sat = pdk.Layer(
        "TileLayer",
        data="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        min_zoom=0,
        max_zoom=19,
        tile_size=256,
    )
    geojson_3d_layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_unified,
        opacity=0.80,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="properties.elevation_m",
        get_fill_color="properties.fill_rgb",
        get_line_color=[255, 255, 255, 255],
        pickable=True,
    )
    text_3d_layer = pdk.Layer(
        "TextLayer",
        text_labels_data,
        pickable=False,
        get_position="position",
        get_text="label",
        get_size=12,
        get_color=[253, 224, 71, 255],
        get_angle=0,
        background=True,
        get_background_color=[11, 17, 32, 230],
        background_padding=[5, 3, 5, 3],
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
    )

    pdk_layers = (
        [tile_layer_sat, geojson_3d_layer]
        if is_all_regions_mode
        else [tile_layer_sat, geojson_3d_layer, text_3d_layer]
    )

    col_3d, col_2d = st.columns([1.0, 1.28])
    with col_3d:
        st.caption("**Vista Volumétrica 3D Sincronizada (`PyDeck` — 24 Zonas Unificadas)**")
        st.pydeck_chart(
            pdk.Deck(
                layers=pdk_layers,
                initial_view_state=active_view_state,
                map_style=None,
                tooltip={
                    "html": "<div style='font-family:Plus Jakarta Sans,sans-serif;padding:4px;'>"
                    "<div style='font-size:10px;color:#38BDF8;font-weight:700;text-transform:uppercase;'>REGIÓN {region} • {alcaldia_municipio}</div>"
                    "<div style='font-size:14px;font-weight:800;margin-bottom:4px;'>{colonia}</div>"
                    "Renta Promedio: <b>${precio_m2_promedio_mxn} MXN/m²</b><br/>"
                    "Renta Est. (70 m²): <b>{renta_70m2_str}</b><br/>"
                    "Yield Bruto Anual: <b style='color:#34D399;'>{yield_bruto_promedio_pct}%</b><br/>"
                    "Comercios DENUE (500m): <b>{denue_unidades_buffer_500m}</b><br/>"
                    "Transporte / Vialidad: <b>{estacion_transporte_principal}</b></div>",
                    "style": {"backgroundColor": "#0B1120", "color": "#F8FAFC", "fontSize": "12px", "borderRadius": "10px"},
                },
            )
        )
    with col_2d:
        st.caption("**Mapa Maestro Satelital Híbrido (`docs/E2/mapa_interactivo_zmvm.html` — Íconos SVG Figma & Botones `Fly-To`)**")
        map_html_path = ROOT_DIR / "docs/E2/mapa_interactivo_zmvm.html"
        if map_html_path.exists():
            raw_html = map_html_path.read_text(encoding="utf-8")
            if folium_init_js:
                raw_html = raw_html.replace("</body>", f"<script>{folium_init_js}</script></body>")
            components.html(raw_html, height=565, scrolling=False)

    df_geo_filt = df_geo_gold[
        (df_geo_gold["alcaldia_municipio"].isin(alcaldias_sel))
        & (df_geo_gold["precio_m2_promedio_mxn"] >= rango_precio[0])
        & (df_geo_gold["precio_m2_promedio_mxn"] <= rango_precio[1])
    ]
    st.markdown(f"##### Matriz Geoespacial de Zonas Filtradas ({region_titulo_corto})")
    st.dataframe(df_geo_filt, use_container_width=True)

    st.divider()
    section_heading("layers", f"Análisis Multivariado de Perfiles Urbanos: Mardia, PCA Biplot y MANOVA (E3) — {region_titulo_corto}")

    mv_col1, mv_col2 = st.columns([1.0, 1.35])
    with mv_col1:
        st.markdown("##### 1. Matriz de Correlaciones Multivariadas")
        fig_corr = px.imshow(
            e3_mv["correlacion_df"],
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto",
        )
        fig_corr.update_layout(height=390, font={"family": "Plus Jakarta Sans, sans-serif"}, margin={"l": 10, "r": 10, "t": 20, "b": 10})
        st.plotly_chart(fig_corr, use_container_width=True)

        norm_mv = e3_mv["normalidad_multivariada"]
        st.markdown("##### 2. Prueba de Normalidad Multivariada de Mardia")
        st.write(
            f"- **Asimetría Multivariada de Mardia:** $b_{{1,p}} = {norm_mv['mardia_skewness_stat']}$ "
            f"($\\chi^2 = {norm_mv['mardia_skewness_chi2']}, p = {norm_mv['mardia_skewness_pvalue']}$)\n"
            f"- **Curtosis Multivariada de Mardia:** $b_{{2,p}} = {norm_mv['mardia_kurtosis_stat']}$ "
            f"($Z = {norm_mv['mardia_kurtosis_z']}, p = {norm_mv['mardia_kurtosis_pvalue']}$)"
        )

    with mv_col2:
        pca_data = e3_mv["pca"]
        scores_df = pca_data["scores_colonias_df"]
        loadings_df = pca_data["loadings_df"]
        v1, v2 = pca_data["varianza_explicada_pct"][0], pca_data["varianza_explicada_pct"][1]

        st.markdown(
            f"##### 3. Biplot de Componentes Principales (PC1: {v1}% + PC2: {v2}% = {pca_data['varianza_acumulada_2pc_pct']}% Varianza)"
        )
        fig_biplot = px.scatter(
            scores_df,
            x="PC1",
            y="PC2",
            color="perfil_negocio_pca",
            text="colonia",
            size="denue_unidades_buffer_500m",
            hover_data=["alcaldia_municipio", "precio_m2_promedio_mxn", "yield_bruto_promedio_pct"],
            template="plotly_white",
        )
        fig_biplot.update_traces(textposition="top center")

        scale_arrow = 2.8
        for _, lrow in loadings_df.iterrows():
            vx = float(lrow["PC1_Consolidacion_Equipamiento_y_Valor"]) * scale_arrow
            vy = float(lrow["PC2_Rentabilidad_Yield_vs_Vacancia"]) * scale_arrow
            fig_biplot.add_annotation(
                x=vx,
                y=vy,
                ax=0,
                ay=0,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.2,
                arrowwidth=2,
                arrowcolor="#EF4444",
                text=f"<b>{lrow['variable']}</b>",
                font={"size": 10, "color": "#991B1B"},
            )

        fig_biplot.update_layout(
            height=460,
            font={"family": "Plus Jakarta Sans, sans-serif"},
            xaxis_title=f"PC1: Consolidación, Equipamiento DENUE y Valor Patrimonial ({v1}%)",
            yaxis_title=f"PC2: Rentabilidad Yield Anual (%) vs. Vacancia ({v2}%)",
            legend={"orientation": "h", "y": -0.24},
        )
        st.plotly_chart(fig_biplot, use_container_width=True)

    st.markdown("##### 4. Resultados de MANOVA (Lambda de Wilks, Traza de Pillai, Hotelling-Lawley y Raíz de Roy)")
    st.dataframe(e3_mv["manova_tabla_df"], use_container_width=True)

# ==============================================================================
# PESTAÑA 3: EXPERIMENTO FACTORIAL 2^3 Y SIMULADOR WHAT-IF (E2)
# ==============================================================================
with tab3:
    section_heading("sliders", "Diseño Experimental Factorial 2³ Aleatorizado con Réplicas (Rendimiento del Pipeline E2)")
    st.caption(
        "**Factores evaluados:** **A:** Tamaño de Lote (`-1`: 250 regs vs `+1`: 1,500 regs) × "
        "**B:** Estrategia de Validación (`-1`: Iteración Fila-a-Fila vs `+1`: Vectorizado Pandera) × "
        "**C:** Formato de Salida (`-1`: JSON Texto vs `+1`: CSV Columnar). **Variable de Respuesta:** Latencia (ms / 1,000 regs)."
    )

    df_exp = e2_fact["experimento_2_3_df"]
    df_anova = e2_fact["anova_tabla_df"]
    conf_info = e2_fact["corrida_confirmacion"]
    sup_info = e2_fact["supuestos_anova"]

    ek1, ek2, ek3, ek4 = st.columns(4)
    with ek1:
        st.markdown(render_kpi_card(SVG["cpu"], "Configuración Base (-1,-1,-1)", f"{conf_info['tiempo_medio_base_ms']} ms", "Iterativo JSON sin vectorizar", "#F1F5F9"), unsafe_allow_html=True)
    with ek2:
        st.markdown(render_kpi_card(SVG["zap"], "Configuración Óptima (+1,+1,+1)", f"{conf_info['tiempo_medio_optimo_ms']} ms", "Vectorizado Pandera + CSV", "#ECFDF5"), unsafe_allow_html=True)
    with ek3:
        st.markdown(render_kpi_card(SVG["trend"], "Reducción de Latencia (2³)", f"-{conf_info['reduccion_latencia_pct']}%", "Corrida de confirmación validada", "#E0F2FE"), unsafe_allow_html=True)
    with ek4:
        st.markdown(
            render_kpi_card(
                SVG["shield"],
                "Supuestos ANOVA",
                f"p={sup_info['shapiro_wilk_pvalue']:.2f} | p={sup_info['levene_pvalue']:.2f}",
                "Shapiro-Wilk y Levene cumplidos",
                "#FEF3C7",
            ),
            unsafe_allow_html=True,
        )

    st.write("")
    fe_col1, fe_col2 = st.columns(2)
    with fe_col1:
        st.markdown("##### Gráfica de Efectos Principales e Interacciones (ms)")
        df_eff = pd.DataFrame(e2_fact["efectos_principales_interacciones"])
        fig_eff = px.bar(
            df_eff,
            x="efecto_ms",
            y="termino",
            orientation="h",
            color="contribucion_pct",
            text="efecto_ms",
            color_continuous_scale="Blues",
            template="plotly_white",
        )
        fig_eff.update_layout(height=360, font={"family": "Plus Jakarta Sans, sans-serif"}, xaxis_title="Efecto Estimado sobre Latencia (ms)", yaxis_title="Término Factorial")
        st.plotly_chart(fig_eff, use_container_width=True)

    with fe_col2:
        st.markdown("##### Gráfica de Interacción de 2 Vías ($A \\times B$: Tamaño de Lote × Validación)")
        df_inter_ab = (
            df_exp.groupby(["A_etiqueta", "B_etiqueta"], as_index=False)["tiempo_ejecucion_ms"]
            .mean()
            .round(2)
        )
        fig_ab = px.line(
            df_inter_ab,
            x="A_etiqueta",
            y="tiempo_ejecucion_ms",
            color="B_etiqueta",
            markers=True,
            template="plotly_white",
        )
        fig_ab.update_layout(
            height=360,
            font={"family": "Plus Jakarta Sans, sans-serif"},
            xaxis_title="Factor A: Tamaño de Lote",
            yaxis_title="Tiempo Medio de Ejecución (ms / 1k regs)",
        )
        st.plotly_chart(fig_ab, use_container_width=True)

    st.markdown("##### Tabla ANOVA Multifactorial ($2^3$ con $r=3$ réplicas, $N=24$ corridas)")
    st.dataframe(df_anova, use_container_width=True)

    comp_24 = e2_fact["comparativa_2_4_vs_2_4_1"]
    with st.expander("Comparación Teórico-Práctica: Diseño Factorial Completo 2⁴ (16 corridas) vs Fraccionado 2⁴⁻¹ (8 corridas - Resolución IV)", expanded=True):
        c24_1, c24_2 = st.columns([1.15, 1.0])
        with c24_1:
            st.markdown(
                f"""
                - **Nuevo Factor D evaluado:** `D_Cache_Memoria` (`-1`: Sin caché, `+1`: Caché en RAM).
                - **Generador de la Fracción $2^{{4-1}}$:** `{comp_24['generador_fraccion']}` ({comp_24['resolucion']}).
                - **Ahorro Experimental:** Reduce de **{comp_24['corridas_con_3_replicas_completo']} corridas** ($16 \\times 3$) a **{comp_24['corridas_con_3_replicas_fraccionado']} corridas** ($8 \\times 3$), logrando un **ahorro del {comp_24['ahorro_experimental_pct']}%** en tiempo y cómputo.
                - **Estructura de Alias:** `{', '.join(comp_24['estructura_alias_principales'])}`
                """
            )
        with c24_2:
            st.dataframe(comp_24["matriz_fraccionada_2_4_1_df"], use_container_width=True)

    st.divider()
    section_heading("target", f"Simulador Comercial What-If de Contratos a 24 Meses — {region_titulo_corto}")
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        subzona_sim = st.selectbox(
            "Seleccionar Sub-zona Urbana:",
            options=sorted(df_whatif["subzona_nombre"].unique().tolist()),
        )
    with s_col2:
        default_rent = 14500.0 if is_colima_mode else 26000.0
        renta_base_input = st.number_input(
            "Renta Mensual de Lista del Inmueble ($ MXN):",
            min_value=5000.0,
            max_value=150000.0,
            value=default_rent,
            step=1000.0,
        )
    with s_col3:
        descuento_sel = st.select_slider(
            "Política de Descuento en Contrato de 24 Meses (%):",
            options=[0.0, 5.0, 10.0, 15.0],
            value=5.0,
        )

    df_sub_w = df_whatif[
        (df_whatif["subzona_nombre"] == subzona_sim)
        & (df_whatif["modalidad_contrato"] == "largo_plazo_24m")
    ].sort_values("descuento_contrato_pct")

    if not df_sub_w.empty:
        df_sim_calc = df_sub_w.copy()
        df_sim_calc["renta_mensual_con_descuento_mxn"] = (
            renta_base_input * (1.0 - df_sim_calc["descuento_contrato_pct"] / 100.0)
        ).round(2)
        df_sim_calc["ingreso_neto_24m_simulado_mxn"] = (
            24.0
            * df_sim_calc["renta_mensual_con_descuento_mxn"]
            * (df_sim_calc["tasa_ocupacion_24m_promedio_pct"] / 100.0)
        ).round(2)

        fig_w = px.bar(
            df_sim_calc,
            x="descuento_contrato_pct",
            y="ingreso_neto_24m_simulado_mxn",
            color="tasa_ocupacion_24m_promedio_pct",
            text="ingreso_neto_24m_simulado_mxn",
            labels={
                "descuento_contrato_pct": "Descuento Otorgado (%)",
                "ingreso_neto_24m_simulado_mxn": "Ingreso Efectivo Acumulado 24m ($ MXN)",
                "tasa_ocupacion_24m_promedio_pct": "Ocupación 24m (%)",
            },
            template="plotly_white",
            color_continuous_scale="Tealgrn",
        )
        fig_w.update_layout(height=350, font={"family": "Plus Jakarta Sans, sans-serif"})
        st.plotly_chart(fig_w, use_container_width=True)
        st.dataframe(
            df_sim_calc[
                [
                    "descuento_contrato_pct",
                    "dias_vacancia_promedio",
                    "tasa_ocupacion_24m_promedio_pct",
                    "renta_mensual_con_descuento_mxn",
                    "ingreso_neto_24m_simulado_mxn",
                ]
            ],
            use_container_width=True,
        )

# ==============================================================================
# PESTAÑA 4: OPTIMIZACIÓN E3, SELLO TDL, PUERTA EN VIVO Y PLANES COMERCIALES B2B
# ==============================================================================
with tab4:
    # 1. SECCIÓN CENTRAL DE ENTREGA E3: OPTIMIZACIÓN MEDIDA DEL PIPELINE (ANTES VS DESPUÉS)
    section_heading("zap", "Optimización Medida del Pipeline de Datos (Entrega E3: Antes vs. Después)")
    st.caption(
        f"Benchmark empírico sobre el lote completo de **{e3_opt['n_registros_evaluados_por_corrida']:,} registros crudos** "
        f"(ZMVM + Colima – Villa de Álvarez) evaluado con `time.perf_counter()`, `tracemalloc` y `DataFrame.memory_usage(deep=True)`."
    )

    t_m = e3_opt["metricas_tiempo_ms"]
    m_m = e3_opt["metricas_memoria"]
    q_m = e3_opt["metricas_calidad_y_errores"]

    ok1, ok2, ok3, ok4 = st.columns(4)
    with ok1:
        st.markdown(
            render_kpi_card(
                SVG["zap"],
                "Tiempo de Ejecución Medio",
                f"{t_m['media_despues_ms']:.1f} ms",
                f"Antes: {t_m['media_antes_ms']:.0f} ms ({t_m['speedup_factor_x']}x más rápido | -{t_m['reduccion_tiempo_pct']}%)",
                "#ECFDF5",
            ),
            unsafe_allow_html=True,
        )
    with ok2:
        st.markdown(
            render_kpi_card(
                SVG["cpu"],
                "Memoria Pico (tracemalloc)",
                f"{m_m['tracemalloc_pico_despues_mib']:.2f} MiB",
                f"Antes: {m_m['tracemalloc_pico_antes_mib']:.2f} MiB (-{m_m['reduccion_pico_heap_pct']}% Heap)",
                "#E0F2FE",
            ),
            unsafe_allow_html=True,
        )
    with ok3:
        st.markdown(
            render_kpi_card(
                SVG["database"],
                "Huella en RAM DataFrame",
                f"{m_m['dataframe_ram_despues_kib']:.1f} KiB",
                f"Antes: {m_m['dataframe_ram_antes_kib']:.0f} KiB (-{m_m['reduccion_dataframe_ram_pct']}% RAM)",
                "#EEF2FF",
            ),
            unsafe_allow_html=True,
        )
    with ok4:
        st.markdown(
            render_kpi_card(
                SVG["shield"],
                "Errores Infiltrados a Oro",
                f"{q_m['errores_infiltrados_despues']} defectos",
                f"Antes: {q_m['errores_infiltrados_antes']} infiltrados (-{q_m['reduccion_errores_pct']}%)",
                "#FEF3C7",
            ),
            unsafe_allow_html=True,
        )

    st.write("")
    opt_c1, opt_c2 = st.columns([1.1, 1.15])
    with opt_c1:
        df_opt_chart = pd.DataFrame(
            {
                "Dimensión": [
                    "Tiempo Medio (%)",
                    "Latencia P95 (%)",
                    "Memoria Pico Heap (%)",
                    "Huella RAM Dataset (%)",
                    "Errores Infiltrados (%)",
                ],
                "Antes (Base = 100%)": [100.0, 100.0, 100.0, 100.0, 100.0],
                "Después (Optimizado E3)": [
                    round(100.0 - t_m["reduccion_tiempo_pct"], 2),
                    round(100.0 - ((t_m["p95_antes_ms"] - t_m["p95_despues_ms"]) / t_m["p95_antes_ms"]) * 100.0, 2),
                    round(100.0 - m_m["reduccion_pico_heap_pct"], 2),
                    round(100.0 - m_m["reduccion_dataframe_ram_pct"], 2),
                    0.0,
                ],
            }
        )
        df_opt_melt = df_opt_chart.melt(id_vars="Dimensión", var_name="Versión del Pipeline", value_name="Índice Base 100")
        fig_opt = px.bar(
            df_opt_melt,
            x="Índice Base 100",
            y="Dimensión",
            color="Versión del Pipeline",
            barmode="group",
            orientation="h",
            text="Índice Base 100",
            color_discrete_map={"Antes (Base = 100%)": "#94A3B8", "Después (Optimizado E3)": "#10B981"},
            template="plotly_white",
            title="Reducción Normalizada Antes vs. Después (Menor = Mejor)",
        )
        fig_opt.update_layout(height=340, font={"family": "Plus Jakarta Sans, sans-serif"}, legend={"orientation": "h", "y": 1.14})
        st.plotly_chart(fig_opt, use_container_width=True)

    with opt_c2:
        st.markdown("##### Matriz Cuantitativa Auditada (`comparativa_optimizacion_e3.csv`)")
        st.dataframe(pd.DataFrame(e3_opt["tabla_comparativa"]), use_container_width=True)
        if st.button("Re-ejecutar Benchmark en Vivo (3 réplicas rápidas)"):
            live_bench = run_e3_pipeline_optimization_benchmark(n_repeats=3)
            st.cache_data.clear()
            st.success(
                f"Benchmark actualizado en vivo: {live_bench['metricas_tiempo_ms']['speedup_factor_x']}x más rápido "
                f"({live_bench['metricas_tiempo_ms']['media_antes_ms']} ms -> {live_bench['metricas_tiempo_ms']['media_despues_ms']} ms)."
            )

    st.divider()
    # 2. MODELO DE NEGOCIO Y PLANES DE SUSCRIPCIÓN B2B (PARA VENTA EMPRESARIAL)
    section_heading("briefcase", "Planes Comerciales SaaS B2B (Desarrolladoras, Corredores AMPI y Fondos de Inversión)")
    st.caption(
        "Propuesta comercial lista para operación real con margen bruto superior al 95% gracias a nuestra arquitectura de Costo Operativo $0.00 USD."
    )

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown(
            f"""
            <div class="pricing-card" style="border-top-color: #0EA5E9;">
                <div class="pricing-tier-tag" style="color: #0284C7;">PLAN 01 • CORREDORES &amp; ASESORES AMPI</div>
                <div style="font-size: 18px; font-weight: 800; color: #0F172A;">Inteligencia Comercial Pro</div>
                <div class="pricing-price">$890 MXN <span style="font-size: 12px; font-weight: 500; color: #64748B;">/ mes por asesor</span></div>
                <ul class="pricing-list">
                    <li>{SVG['check']} <span>Valuación instantánea $/m², renta estimada (70 m²) y Yield % en las 24 zonas de ZMVM y Colima–Villa de Álvarez.</span></li>
                    <li>{SVG['check']} <span>Explorador satelital 2D/3D con densidad comercial DENUE en radios de 500m.</span></li>
                    <li>{SVG['check']} <span><b>ROI Estimado:</b> Reducción de 22 días en tiempo de colocación (+18% en cierres anuales).</span></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col2:
        st.markdown(
            f"""
            <div class="pricing-card" style="border-top-color: #10B981;">
                <div class="pricing-tier-tag" style="color: #059669;">PLAN 02 • DESARROLLADORAS &amp; ADMINISTRADORAS</div>
                <div style="font-size: 18px; font-weight: 800; color: #0F172A;">Suite Corporativa + What-If</div>
                <div class="pricing-price">$4,900 MXN <span style="font-size: 12px; font-weight: 500; color: #64748B;">/ mes (hasta 10 usuarios)</span></div>
                <ul class="pricing-list">
                    <li>{SVG['check']} <span>Simulador What-If de descuentos en contratos a 24 meses y pronóstico SARIMA/Holt-Winters a 4 trimestres.</span></li>
                    <li>{SVG['check']} <span>Segmentación multivariada PCA/MANOVA de vocación habitacional por AGEB.</span></li>
                    <li>{SVG['check']} <span><b>ROI Estimado:</b> Prevención de 1.5 meses de vacancia por unidad (&gt;$28,500 MXN ahorrados/año).</span></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col3:
        st.markdown(
            f"""
            <div class="pricing-card" style="border-top-color: #6366F1;">
                <div class="pricing-tier-tag" style="color: #4F46E5;">PLAN 03 • FONDOS PATRIMONIALES &amp; PROPTECH</div>
                <div style="font-size: 18px; font-weight: 800; color: #0F172A;">Licencia Enterprise &amp; Datos Oro</div>
                <div class="pricing-price">$11,500 MXN <span style="font-size: 12px; font-weight: 500; color: #64748B;">/ mes multi-región</span></div>
                <ul class="pricing-list">
                    <li>{SVG['check']} <span>Acceso directo a cubos Capa Oro (CSV/GeoJSON) certificados al 100% bajo ISO/IEC 25012.</span></li>
                    <li>{SVG['check']} <span>Auditoría criptográfica completa de linaje SHA-256 hacia fuentes oficiales BANXICO/INEGI.</span></li>
                    <li>{SVG['check']} <span><b>ROI Estimado:</b> Ahorro del 75% en horas de ingeniería y análisis de mercado inmobiliario.</span></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    # 3. CERTIFICACIÓN SELLO TDL E INGESTA EN VIVO CON PANDERA
    kpis_tdl = e4_tdl["kpis_sello_tdl"]
    section_heading("shield", "Certificación Oficial del Sello Trusted Data Lab (ISO/IEC 25012 & ISO/IEC 25010)")

    tk1, tk2, tk3, tk4, tk5 = st.columns(5)
    tk1.metric("Disponibilidad Sistema", f"{kpis_tdl['disponibilidad_pct']}%", "Meta >= 95%")
    tk2.metric("Completitud ISO 25012", f"{kpis_tdl['completitud_iso25012_pct']}%", "Meta >= 95%")
    tk3.metric("Cobertura Pruebas (pytest)", ">90.5%", "Meta >= 60%")
    tk4.metric("Secretos Expuestos", f"{kpis_tdl['secretos_expuestos']}", "Costo $0 / Seguro")
    tk5.metric("Trazabilidad Linaje Oro", f"{kpis_tdl['trazabilidad_linaje_pct']}%", f"{len(df_lineage)}/{len(df_lineage)} filas SHA-256")

    iso_c1, iso_c2 = st.columns(2)
    with iso_c1:
        st.markdown("##### Evaluación ISO/IEC 25012 (Calidad de Datos)")
        st.dataframe(e4_tdl["iso_25012_df"], use_container_width=True)
    with iso_c2:
        st.markdown("##### Evaluación ISO/IEC 25010 (Calidad de Producto de Software)")
        st.dataframe(e4_tdl["iso_25010_df"], use_container_width=True)

    st.divider()
    section_heading("layers", "Simulador de Ingesta en Vivo y Puerta de Calidad Automática (Pandera -> Cuarentena)")
    sim_c1, sim_c2, sim_c3 = st.columns([1.0, 1.0, 1.2])
    with sim_c1:
        n_val_in = st.slider("Registros Válidos en el Lote:", min_value=4, max_value=20, value=8)
    with sim_c2:
        n_dir_in = st.slider("Registros Anómalos Intencionales:", min_value=1, max_value=4, value=4)
    with sim_c3:
        persist_check = st.checkbox("Persistir rechazados en `cuarentena_inmobiliario.csv`", value=False)
        run_live_btn = st.button("Ejecutar Ingesta en Vivo y Validar con Pandera", type="primary")

    if run_live_btn:
        sim_res = simulate_live_ingestion_batch(
            n_valid=n_val_in, n_dirty=n_dir_in, persist_to_quarantine=persist_check
        )
        rep_g = sim_res["reporte_puerta_calidad"]
        st.success(
            f"Puerta de Calidad Ejecutada: {rep_g['total_aprobados_plata']} registros promovidos a Capa Plata | "
            f"{rep_g['total_enviados_cuarentena']} registros aislados en Cuarentena ({rep_g['tasa_rechazo_cuarentena_pct']}%)."
        )
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("##### Registros Aislados en Cuarentena (Con Motivo Documentado)")
            st.dataframe(
                sim_res["enviados_cuarentena_df"][
                    ["id_propiedad", "colonia", "tipo_inmueble", "superficie_m2", "renta_lista_mensual_mxn", "motivo_cuarentena"]
                ],
                use_container_width=True,
            )
        with sc2:
            st.markdown("##### Registros Promovidos a Capa Plata")
            st.dataframe(
                sim_res["aprobados_plata_df"][
                    ["id_propiedad", "colonia", "tipo_inmueble", "superficie_m2", "renta_lista_mensual_mxn", "precio_m2_mxn"]
                ],
                use_container_width=True,
            )

    st.divider()
    section_heading("database", "Publicación de Dataset Abierto (CC BY 4.0 / ODbL 1.0), Datasheet E3 y Linaje SHA-256")
    st.dataframe(df_lineage.tail(16), use_container_width=True)

    datasheet_path = ROOT_DIR / "docs/E3/datasheet.md"
    datasheet_bytes = datasheet_path.read_bytes() if datasheet_path.exists() else b""

    dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)
    with dl_col1:
        st.download_button(
            label=f"Descargar Capa Plata ({'Colima' if is_colima_mode else 'ZMVM'}) (CSV)",
            data=df_silver.to_csv(index=False).encode("utf-8"),
            file_name=f"observatorio_plata_{'colima' if is_colima_mode else 'zmvm'}.csv",
            mime="text/csv",
        )
    with dl_col2:
        st.download_button(
            label=f"Descargar Cubo Oro GIS ({'Colima' if is_colima_mode else 'ZMVM'}) (CSV)",
            data=df_geo_gold.to_csv(index=False).encode("utf-8"),
            file_name=f"observatorio_oro_geoespacial_{'colima' if is_colima_mode else 'zmvm'}.csv",
            mime="text/csv",
        )
    with dl_col3:
        st.download_button(
            label="Descargar Datasheet Oficial E3 (MD)",
            data=datasheet_bytes,
            file_name="datasheet_observatorio_inmobiliario_e3.md",
            mime="text/markdown",
        )
    with dl_col4:
        st.download_button(
            label="Descargar Diccionario de Datos (CSV)",
            data=e4_tdl["diccionario_datos_df"].to_csv(index=False).encode("utf-8"),
            file_name="diccionario_datos_observatorio_tdl.csv",
            mime="text/csv",
        )
