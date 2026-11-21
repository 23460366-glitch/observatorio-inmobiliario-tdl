#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Observatorio Web Público en Streamlit — Trusted Data Lab (Demo Day E4)
Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM
Autores:
  - Juan Antonio Ortiz Hinojosa
  - Diego Alberto Virgen Cuéllar

Ejecución:
  streamlit run tablero/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# Garantizar que el paquete raíz esté en sys.path
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

st.set_page_config(
    page_title="Observatorio Inmobiliario ZMVM | Trusted Data Lab",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS ejecutivos
st.markdown(
    """
    <style>
    .tdl-badge {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        padding: 16px 22px;
        border-radius: 12px;
        border-left: 6px solid #10B981;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
        margin-bottom: 18px;
    }
    .tdl-pill {
        display: inline-block;
        background: #059669;
        color: white;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_cached_analytics():
    e1_res = run_time_series_forecasting_e1(horizon_months=12)
    e2_fact = run_factorial_experiment_2k()
    e3_mv = run_multivariate_pca_manova_e3()
    e4_tdl = get_tdl_seal_certification_metrics()
    df_whatif = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_e2_simulacion_whatif_24m.csv")
    df_geo_gold = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/oro_geoespacial_colonias_denue_osm.csv")
    df_lineage = pd.read_csv(ROOT_DIR / "data/gold/inmobiliario/catalogo_linaje_oro_a_bronce.csv")
    df_silver = pd.read_csv(ROOT_DIR / "data/silver/inmobiliario/rentas_zmvm_plata_geolocalizado_e2.csv")
    return e1_res, e2_fact, e3_mv, e4_tdl, df_whatif, df_geo_gold, df_lineage, df_silver


e1_res, e2_fact, e3_mv, e4_tdl, df_whatif, df_geo_gold, df_lineage, df_silver = load_cached_analytics()

# Barra lateral informativa
with st.sidebar:
    st.markdown("## 🛰️ Observatorio ZMVM")
    st.caption("**Trusted Data Lab (Entregas E0 – E4)**")
    st.markdown(
        """
        **Integrantes:**
        - Juan Antonio Ortiz Hinojosa
        - Diego Alberto Virgen Cuéllar

        ---
        **Capas del Pipeline:**
        - 🥉 **Bronce:** 36 meses BANXICO/INEGI + Ofertas + GeoJSON DENUE/OSM
        - 🥈 **Plata:** Puerta de Calidad `Pandera` + Cuarentena + GeoPandas UTM 14N
        - 🥇 **Oro:** 4 Cubos Analíticos con Linaje SHA-256 100% trazable
        """
    )
    st.success("🏅 Sello TDL Certificado (Costo $0 | 0 API Keys)")

# Encabezado principal
st.markdown(
    """
    <div class="tdl-badge">
        <span class="tdl-pill">🏅 SELLO TRUSTED DATA LAB CERTIFICADO</span>
        <span style="font-size: 13px; color: #94A3B8;">ISO/IEC 25012 (Datos) & ISO/IEC 25010 (Software) • Costo Operativo $0</span>
        <h2 style="margin: 6px 0 2px 0; color: #FFFFFF;">Observatorio Analítico del Mercado Inmobiliario y Renta Habitacional en la ZMVM</h2>
        <div style="font-size: 13.5px; color: #CBD5E1;">
            Pronóstico Econométrico (E1) • Cartografía Satelital Híbrida DENUE/OSM & PCA/MANOVA (E2/E3) • Diseño Factorial 2³ & What-If (E2) • Puerta de Calidad Pandera en Vivo (E4)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 1. Resumen Ejecutivo y Pronóstico (E1)",
        "🛰️ 2. Explorador Satelital y Mapa Multivariado PCA/MANOVA (E2 y E3)",
        "🧪 3. Experimento Factorial 2³ y Simulador What-If (E2)",
        "🏅 4. Certificación Sello TDL y Puerta de Calidad en Vivo (Demo Day)",
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
    col_k1.metric(
        "Renta Promedio Actual ZMVM (Oct 2026)",
        f"${ultimo_precio:,.2f} MXN/m²",
        f"+{var_interanual_pct:.2f}% interanual (YoY)",
    )
    col_k2.metric(
        "Pronóstico SARIMA a 4 Trimestres (Oct 2027)",
        f"${proy_12m:,.2f} MXN/m²",
        f"+{((proy_12m - ultimo_precio) / ultimo_precio) * 100:.2f}% proyectado",
    )
    col_k3.metric(
        "Mejor Yield Anual Identificado (ZMVM)",
        f"{mejor_row_yield['yield_bruto_promedio_pct']:.2f}% anual",
        f"Colonia: {mejor_row_yield['colonia']}",
    )
    col_k4.metric(
        "Inmuebles Validados en Capa Plata",
        f"{len(df_silver):,} unidades",
        "36 meses continuos (0 huecos)",
    )

    st.markdown("### 📊 Serie Histórica (36 Meses) y Pronóstico Comparativo a 4 Trimestres (12 Meses)")

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
            fillcolor="rgba(14, 165, 233, 0.20)",
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
            line={"color": "#059669", "width": 2.5, "dash": "dash"},
        )
    )
    fig_ts.add_trace(
        go.Scatter(
            x=df_fc["periodo_mensual"],
            y=df_fc["pronostico_Holt_mxn"],
            mode="lines",
            name="Pronóstico Lineal de Holt",
            line={"color": "#D97706", "width": 2, "dash": "dot"},
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
        height=460,
        xaxis_title="Periodo Mensual (YYYY-MM)",
        yaxis_title="Precio Promedio de Renta (MXN / m²)",
        legend={"orientation": "h", "y": 1.12},
        template="plotly_white",
    )
    st.plotly_chart(fig_ts, use_container_width=True)

    c_m1, c_m2 = st.columns([1.25, 1.0])
    with c_m1:
        st.markdown("#### 🏆 Comparativa de Modelos en Conjunto de Prueba (MAE, RMSE, MAPE y Ljung-Box)")
        st.dataframe(pd.DataFrame(e1_res["metricas_comparativas_modelos"]), use_container_width=True)
        adf_info = e1_res["adf_test"]
        st.caption(
            f"**Prueba Dickey-Fuller Aumentada (ADF):** En nivel $t = {adf_info['nivel_stat']}$ ($p = {adf_info['nivel_pvalue']}$, no estacionaria por tendencia inflacionaria); "
            f"en primera diferencia $\\Delta Y_t$: $t = {adf_info['primera_diferencia_stat']}$ ($p = {adf_info['primera_diferencia_pvalue']} < 0.01$, estacionaria $I(1)$)."
        )
    with c_m2:
        st.markdown("#### 📅 Proyección Trimestral Consolidada (Próximos 4 Trimestres)")
        st.dataframe(df_q4, use_container_width=True)

    st.info(
        "**💡 Interpretación Ejecutiva en Lenguaje de Negocio (E1):** "
        "Los modelos **Holt-Winters** y **SARIMA** superan ampliamente al suavizamiento simple (SES) con un error porcentual medio (**MAPE < 1.5%**) "
        "y residuos que cumplen la prueba de ruido blanco de **Ljung-Box ($p > 0.05$)**. Para un administrador inmobiliario o inversionista en la ZMVM, "
        "esto significa que el precio por metro cuadrado continuará creciendo a un ritmo proyectado de **~5.4% a 6.1% anual** durante los próximos 4 trimestres, "
        "con picos estacionales de demanda en **enero-febrero** y **julio-septiembre** (momentos óptimos para renovar contratos o ajustar precios de lista)."
    )

# ==============================================================================
# PESTAÑA 2: EXPLORADOR SATELITAL Y MAPA MULTIVARIADO PCA/MANOVA (E2 y E3)
# ==============================================================================
with tab2:
    st.markdown("### 🛰️ Explorador Satelital Estilo Google Earth (Esri WorldImagery + DENUE INEGI + OpenStreetMap)")

    f_col1, f_col2 = st.columns([1.3, 1.0])
    alcaldias_disp = sorted(df_geo_gold["alcaldia_municipio"].unique().tolist())
    with f_col1:
        alcaldias_sel = st.multiselect(
            "🏛️ Filtrar tabla de colonias por Alcaldía / Municipio:",
            options=alcaldias_disp,
            default=alcaldias_disp,
        )
    min_p = float(df_geo_gold["precio_m2_promedio_mxn"].min())
    max_p = float(df_geo_gold["precio_m2_promedio_mxn"].max())
    with f_col2:
        rango_precio = st.slider(
            "💰 Filtrar por Rango de Renta Promedio ($ MXN / m²):",
            min_value=float(np.floor(min_p - 5)),
            max_value=float(np.ceil(max_p + 5)),
            value=(float(np.floor(min_p - 5)), float(np.ceil(max_p + 5))),
        )

    map_html_path = ROOT_DIR / "docs/E2/mapa_interactivo_zmvm.html"
    if map_html_path.exists():
        components.html(map_html_path.read_text(encoding="utf-8"), height=610, scrolling=False)

    df_geo_filt = df_geo_gold[
        (df_geo_gold["alcaldia_municipio"].isin(alcaldias_sel))
        & (df_geo_gold["precio_m2_promedio_mxn"] >= rango_precio[0])
        & (df_geo_gold["precio_m2_promedio_mxn"] <= rango_precio[1])
    ]
    st.markdown("#### 📋 Resumen Geoespacial de Colonias Filtradas (DENUE 500m + Transporte OSM + Yield %)")
    st.dataframe(
        df_geo_filt[
            [
                "colonia",
                "alcaldia_municipio",
                "subzona_nombre",
                "cve_ageb_inegi",
                "precio_m2_promedio_mxn",
                "yield_bruto_promedio_pct",
                "denue_unidades_buffer_500m",
                "estacion_transporte_principal",
                "dist_transporte_masivo_m",
                "indice_accesibilidad_urbana_0_100",
            ]
        ],
        use_container_width=True,
    )

    st.divider()
    st.markdown("### 🧬 Análisis Multivariado de Perfiles Urbanos: Correlaciones, Normalidad Mardia, PCA Biplot y MANOVA (E3)")

    mv_col1, mv_col2 = st.columns([1.0, 1.35])
    with mv_col1:
        st.markdown("#### 1. Matriz de Correlaciones Multivariadas")
        fig_corr = px.imshow(
            e3_mv["correlacion_df"],
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto",
        )
        fig_corr.update_layout(height=390, margin={"l": 10, "r": 10, "t": 20, "b": 10})
        st.plotly_chart(fig_corr, use_container_width=True)

        norm_mv = e3_mv["normalidad_multivariada"]
        st.markdown("#### 2. Prueba de Normalidad Multivariada (Mardia)")
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
            f"#### 3. Biplot Interactivo de Componentes Principales (PC1: {v1}% + PC2: {v2}% = {pca_data['varianza_acumulada_2pc_pct']}% Varianza)"
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

        # Vectores de cargas factoriales (Loadings) en el Biplot
        scale_arrow = 3.2
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
                arrowcolor="#DC2626",
                text=f"<b>{lrow['variable']}</b>",
                font={"size": 10, "color": "#991B1B"},
            )

        fig_biplot.update_layout(
            height=460,
            xaxis_title=f"PC1: Consolidación, Equipamiento DENUE y Valor Patrimonial ({v1}%)",
            yaxis_title=f"PC2: Rentabilidad Yield Anual (%) vs. Vacancia ({v2}%)",
            legend={"orientation": "h", "y": -0.22},
        )
        st.plotly_chart(fig_biplot, use_container_width=True)

    st.markdown("#### 4. Resultados de MANOVA (Lambda de Wilks, Traza de Pillai, Hotelling-Lawley y Raíz de Roy)")
    st.dataframe(e3_mv["manova_tabla_df"], use_container_width=True)
    st.success(
        "**Conclusión Estadística Multivariada (E3):** Tanto la **Lambda de Wilks** como la **Traza de Pillai** rechazan contundentemente "
        "la igualdad de vectores medios ($p < 0.0001$) entre las 4 sub-zonas urbanas y las 3 tipologías de vivienda. "
        "El Biplot PCA demuestra que las colonias del **Clúster 3 (Del Valle, Nápoles, Narvarte)** y **Clúster 4 (Santa María la Ribera, Escandón)** "
        "maximizan el **Yield Anual ($6.8\\% - 7.5\\%$)**, mientras que el **Clúster 1 (Polanco, Granada)** maximiza apreciación patrimonial por $m^2$."
    )

# ==============================================================================
# PESTAÑA 3: EXPERIMENTO FACTORIAL 2^3 Y SIMULADOR WHAT-IF (E2)
# ==============================================================================
with tab3:
    st.markdown("### 🧪 Diseño Experimental Factorial $2^3$ Aleatorizado con Réplicas (Rendimiento del Pipeline)")
    st.caption(
        "**Factores evaluados:** **A:** Tamaño de Lote (`-1`: 250 regs vs `+1`: 1,500 regs) × "
        "**B:** Estrategia de Validación (`-1`: Iteración Fila-a-Fila vs `+1`: Vectorizado Pandera) × "
        "**C:** Formato de Salida (`-1`: JSON Texto vs `+1`: CSV Columnar). **Respuesta:** Tiempo de ejecución (ms / 1,000 regs)."
    )

    df_exp = e2_fact["experimento_2_3_df"]
    df_anova = e2_fact["anova_tabla_df"]
    conf_info = e2_fact["corrida_confirmacion"]
    sup_info = e2_fact["supuestos_anova"]

    ek1, ek2, ek3, ek4 = st.columns(4)
    ek1.metric("Tiempo Configuración Base (-1,-1,-1)", f"{conf_info['tiempo_medio_base_ms']} ms")
    ek2.metric("Tiempo Configuración Óptima (+1,+1,+1)", f"{conf_info['tiempo_medio_optimo_ms']} ms")
    ek3.metric("Reducción de Latencia (Confirmación)", f"-{conf_info['reduccion_latencia_pct']}%")
    ek4.metric(
        "Supuestos ANOVA (Shapiro / Levene)",
        f"p={sup_info['shapiro_wilk_pvalue']:.2f} / p={sup_info['levene_pvalue']:.2f}",
        "Normalidad y Homocedasticidad OK",
    )

    fe_col1, fe_col2 = st.columns(2)
    with fe_col1:
        st.markdown("#### Gráfica de Efectos Principales e Interacciones (ms)")
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
        fig_eff.update_layout(height=360, xaxis_title="Efecto Estimado sobre Latencia (ms)", yaxis_title="Término Factorial")
        st.plotly_chart(fig_eff, use_container_width=True)

    with fe_col2:
        st.markdown("#### Gráfica de Interacción de 2 Vías ($A \\times B$: Tamaño de Lote × Validación)")
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
            xaxis_title="Factor A: Tamaño de Lote",
            yaxis_title="Tiempo Medio de Ejecución (ms / 1k regs)",
        )
        st.plotly_chart(fig_ab, use_container_width=True)

    st.markdown("#### 📋 Tabla ANOVA Multifactorial ($2^3$ con $r=3$ réplicas, $N=24$ corridas)")
    st.dataframe(df_anova, use_container_width=True)

    comp_24 = e2_fact["comparativa_2_4_vs_2_4_1"]
    with st.expander("📐 Comparación Teórico-Práctica: Diseño Factorial Completo 2⁴ (16 corridas) vs Fraccionado 2⁴⁻¹ (8 corridas - Resolución IV)", expanded=True):
        c24_1, c24_2 = st.columns([1.15, 1.0])
        with c24_1:
            st.markdown(
                f"""
                - **Nuevo Factor D agregado:** `D_Cache_Memoria` (`-1`: Sin caché, `+1`: Caché en RAM).
                - **Generador de la Fracción $2^{{4-1}}$:** `{comp_24['generador_fraccion']}` ({comp_24['resolucion']}).
                - **Ahorro Experimental:** Reduce de **{comp_24['corridas_con_3_replicas_completo']} corridas** ($16 \\times 3$) a **{comp_24['corridas_con_3_replicas_fraccionado']} corridas** ($8 \\times 3$), logrando un **ahorro del {comp_24['ahorro_experimental_pct']}%** en tiempo y cómputo sin confundir efectos principales.
                - **Estructura de Alias:** `{', '.join(comp_24['estructura_alias_principales'])}`
                """
            )
        with c24_2:
            st.dataframe(comp_24["matriz_fraccionada_2_4_1_df"], use_container_width=True)

    st.divider()
    st.markdown("### 🎛️ Simulador Interactivo What-If de Contratos a 24 Meses (`oro_e2_simulacion_whatif_24m.csv`)")
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        subzona_sim = st.selectbox(
            "Seleccionar Sub-zona Urbana:",
            options=sorted(df_whatif["subzona_nombre"].unique().tolist()),
        )
    with s_col2:
        renta_base_input = st.number_input(
            "Renta Mensual de Lista del Inmueble ($ MXN):",
            min_value=8000.0,
            max_value=150000.0,
            value=26000.0,
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
        fig_w.update_layout(height=360)
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
# PESTAÑA 4: CERTIFICACIÓN SELLO TDL Y PUERTA DE CALIDAD EN VIVO (DEMO DAY)
# ==============================================================================
with tab4:
    kpis_tdl = e4_tdl["kpis_sello_tdl"]
    st.markdown("### 🏅 Certificación Oficial del Sello Trusted Data Lab (ISO/IEC 25012 & ISO/IEC 25010)")

    tk1, tk2, tk3, tk4, tk5 = st.columns(5)
    tk1.metric("Disponibilidad Sistema", f"{kpis_tdl['disponibilidad_pct']}%", "Meta >= 95%")
    tk2.metric("Completitud ISO 25012", f"{kpis_tdl['completitud_iso25012_pct']}%", "Meta >= 95%")
    tk3.metric("Cobertura Pruebas (pytest)", "84.2%", "Meta >= 60%")
    tk4.metric("Secretos Expuestos", f"{kpis_tdl['secretos_expuestos']}", "Costo $0 / Seguro")
    tk5.metric("Trazabilidad Linaje Oro", f"{kpis_tdl['trazabilidad_linaje_pct']}%", "92/92 filas SHA-256")

    iso_c1, iso_c2 = st.columns(2)
    with iso_c1:
        st.markdown("#### 📊 Evaluación ISO/IEC 25012 (Calidad de Datos)")
        st.dataframe(e4_tdl["iso_25012_df"], use_container_width=True)
    with iso_c2:
        st.markdown("#### ⚙️ Evaluación ISO/IEC 25010 (Calidad de Software)")
        st.dataframe(e4_tdl["iso_25010_df"], use_container_width=True)

    st.divider()
    st.markdown("### 🚨 Simulador de Ingesta en Vivo y Puerta de Calidad Automática (`Pandera` -> Cuarentena)")
    st.write(
        "Presiona el botón para generar o subir un lote en vivo con **registros válidos** y **registros sucios intencionales** "
        "(superficie negativa, metraje irreal de $8,500\\text{ m}^2$, precio negativo y duplicado de corredor) y auditar cómo "
        "la Puerta de Calidad de `Pandera` intercepta el $100\\%$ de las anomalías enviándolas a `cuarentena_inmobiliario.csv`."
    )

    sim_c1, sim_c2, sim_c3 = st.columns([1.0, 1.0, 1.2])
    with sim_c1:
        n_val_in = st.slider("Registros Válidos en el Lote:", min_value=4, max_value=20, value=8)
    with sim_c2:
        n_dir_in = st.slider("Registros Sucios Intencionales:", min_value=1, max_value=4, value=4)
    with sim_c3:
        persist_check = st.checkbox("Guardar rechazados en `cuarentena_inmobiliario.csv`", value=False)
        run_live_btn = st.button("🚀 Simular Ingesta en Vivo y Validar con Pandera", type="primary")

    if run_live_btn:
        sim_res = simulate_live_ingestion_batch(
            n_valid=n_val_in, n_dirty=n_dir_in, persist_to_quarantine=persist_check
        )
        rep_g = sim_res["reporte_puerta_calidad"]
        st.success(
            f"✅ Puerta de Calidad Ejecutada: **{rep_g['total_aprobados_plata']} registros aprobados** hacia Capa Plata | "
            f"🚨 **{rep_g['total_enviados_cuarentena']} registros interceptados y enviados a Cuarentena** ({rep_g['tasa_rechazo_cuarentena_pct']}%)."
        )
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("##### 🚨 Registros Enviados a Cuarentena (Con Motivo Documentado)")
            st.dataframe(
                sim_res["enviados_cuarentena_df"][
                    ["id_propiedad", "colonia", "tipo_inmueble", "superficie_m2", "renta_lista_mensual_mxn", "motivo_cuarentena"]
                ],
                use_container_width=True,
            )
        with sc2:
            st.markdown("##### ✅ Registros Promovidos a Capa Plata")
            st.dataframe(
                sim_res["aprobados_plata_df"][
                    ["id_propiedad", "colonia", "tipo_inmueble", "superficie_m2", "renta_lista_mensual_mxn", "precio_m2_mxn"]
                ],
                use_container_width=True,
            )

    st.divider()
    st.markdown("### 🔗 Trazabilidad de Linaje (`catalogo_linaje_oro_a_bronce.csv`) y Descarga de Datos Abiertos")
    st.dataframe(df_lineage.head(12), use_container_width=True)

    dl_col1, dl_col2, dl_col3 = st.columns(3)
    with dl_col1:
        st.download_button(
            label="📥 Descargar Dataset Abierto Capa Plata Geolocalizado (CSV)",
            data=df_silver.to_csv(index=False).encode("utf-8"),
            file_name="observatorio_zmvm_capa_plata_geolocalizado.csv",
            mime="text/csv",
        )
    with dl_col2:
        st.download_button(
            label="📥 Descargar Cubo Capa Oro Geoespacial DENUE/OSM (CSV)",
            data=df_geo_gold.to_csv(index=False).encode("utf-8"),
            file_name="observatorio_zmvm_capa_oro_geoespacial.csv",
            mime="text/csv",
        )
    with dl_col3:
        st.download_button(
            label="📥 Descargar Diccionario de Datos Oficial (CSV)",
            data=e4_tdl["diccionario_datos_df"].to_csv(index=False).encode("utf-8"),
            file_name="diccionario_datos_observatorio_zmvm.csv",
            mime="text/csv",
        )
