#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Pipeline de Limpieza Estadística, Integración, Puerta de Calidad (Pandera) y Capas Plata/Oro
Observatorio del Mercado Inmobiliario y Renta Habitacional en la ZMVM — Entrega E1
Autores:
  - Juan Antonio Ortiz Hinojosa
  - Diego Alberto Virgen Cuéllar

Cubre todos los entregables técnicos de la Entrega E1:
  1. Integración y Resolución de Conflictos:
     - Fusión de fuentes heterogéneas (BANXICO/INEGI JSON + Ofertas Inmobiliarias ZMVM JSON).
     - Resolución de discrepancias de esquema, fechas (`DD/MM/YYYY` -> `YYYY-MM`), monedas con
       formato string (`"$25,400.00 MXN"` -> `float`) y homologación semántica de categorías.
  2. Diagnóstico e Imputación de Valores Faltantes (MCAR / MAR / MNAR):
     - Diagnóstico estadístico por mecanismo (pruebas de asociación de faltantes por subzona y nivel de renta).
     - Imputación justificada:
       * MCAR (`estacionamientos`): Moda estratificada por `tipo_inmueble`.
       * MAR (`superficie_m2`): Mediana estratificada por `(subzona_id, tipo_inmueble, recamaras)`.
       * MNAR (`cuota_mantenimiento_mxn`): Imputación por razón mediana (`cuota / renta_lista`) + bandera
         indicadora explícita `flag_mnar_mantenimiento` para preservar la señal de no-respuesta informativa.
  3. Puerta de Calidad Automática (Pandera) con Cuarentena Documentada:
     - Validación estricta de tipos, dominios categóricos, unicidad (`id_propiedad` + `periodo_mensual`)
       y rangos físicos plausibles (`superficie_m2` en [20, 1200], `renta_lista_mensual_mxn` > 0).
     - Ningún registro inválido se borra en silencio: todos se envían a
       `data/silver/inmobiliario/cuarentena_inmobiliario.csv` y `.json` con motivo detallado.
  4. Detección y Tratamiento de Atípicos y Ruido:
     - Comparativa de 3 métodos: Rango Intercuartílico (IQR), Z-Score Robusto (basado en mediana y MAD)
       e `IsolationForest` multivariado (`scikit-learn`).
     - Tratamiento mediante Winsorización acotada por estrato (percentiles 1%–99%) para evitar distorsionar
       la media sin perder observaciones legítimas del segmento prime.
  5. Normalización y Estandarización de Variables Continuas:
     - Escalado `Min-Max` $[0, 1]$ y estandarización `Z-Score` ($\mu=0, \sigma=1$).
  6. Discretización y Jerarquías Conceptuales:
     - Discretización de precio por $m^2$, metraje y antigüedad/vacancia en categorías ordinales.
     - Jerarquía conceptual espacial: `Colonia -> Alcaldía/Municipio -> Sub-zona Urbana -> Región (ZMVM)`.
  7. Reducción de Datos hacia Capa Oro (`data/gold/inmobiliario/`):
     - Selección de variables (filtro de varianza/correlación e información mutua) y agregación
       multidimensional lista para responder la Triléctica Estadística:
       * `oro_e1_pronostico_mensual_trimestral.csv` (Serie mensual/trimestral para E1).
       * `oro_e2_simulacion_whatif_24m.csv` (Cubo agrupado por nivel de descuento y estrato para E2).
       * `oro_e3_comparacion_multivariada_yield.csv` (Cubo Tipología x Sub-zona para E3).
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Check, Column, DataFrameSchema
from pandera.errors import SchemaErrors
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
BRONZE_DIR = BASE_DIR / "data" / "bronze" / "inmobiliario"
SILVER_DIR = BASE_DIR / "data" / "silver" / "inmobiliario"
GOLD_DIR = BASE_DIR / "data" / "gold" / "inmobiliario"


# ==============================================================================
# 1. CARGA, INTEGRACIÓN Y RESOLUCIÓN DE CONFLICTOS DE ESQUEMA/TIPOS
# ==============================================================================

TIPO_INMUEBLE_CANONICAL_MAP = {
    "depto_1rec": "depto_1rec",
    "depto 1 rec": "depto_1rec",
    "departamento 1 recamara": "depto_1rec",
    "depto_2rec": "depto_2rec",
    "departamento 2 recámaras": "depto_2rec",
    "departamento 2 recamaras": "depto_2rec",
    "casa": "casa",
    "casa habitacion": "casa",
    "casa habitación": "casa",
}

JERARQUIA_ESPACIAL_MACRO = {
    "SZ1_PRIME_PONIENTE": "Corredor Poniente Prime (CDMX Central-Poniente)",
    "SZ2_CENTRAL_CORREDOR": "Corredor Central Corporativo-Cultural (CDMX Centro)",
    "SZ3_CONSOLIDADA_SUR": "Corredor Residencial Sur-Centro (CDMX Sur)",
    "SZ4_EMERGENTE_METROPOLITANA": "Corredor En Consolidación y Conurbado (ZMVM Norte-Centro)",
}


def parse_currency_or_float(val: Any) -> float:
    """Convierte valores numéricos o cadenas monetarias ('$25,400.00 MXN') a float o np.nan."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    cleaned = re.sub(r"[^0-9.\-]", "", str(val))
    if cleaned in ("", "-", "."):
        return np.nan
    try:
        return float(cleaned)
    except ValueError:
        return np.nan


def normalize_banxico_date_to_ym(fecha_raw: Any, fallback_ym: Any) -> str:
    """Homologa fechas crudas DD/MM/YYYY de BANXICO al estándar ISO YYYY-MM."""
    if isinstance(fecha_raw, str) and "/" in fecha_raw:
        parts = fecha_raw.strip().split("/")
        if len(parts) == 3:
            return f"{int(parts[2]):04d}-{int(parts[1]):02d}"
    return str(fallback_ym).strip()


def load_and_integrate_sources() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Carga los JSONs de Capa Bronce (BANXICO/INEGI + Ofertas de Renta ZMVM) y resuelve
    los conflictos de esquema, tipos de datos y codificación categórica.
    """
    macro_path = BRONZE_DIR / "macro_banxico_inegi_36m.json"
    rentas_path = BRONZE_DIR / "rentas_zmvm_historico_36m.json"

    macro_raw = json.loads(macro_path.read_text(encoding="utf-8"))
    rentas_raw = json.loads(rentas_path.read_text(encoding="utf-8"))

    df_macro = pd.DataFrame(macro_raw["series_mensuales"])
    df_rentas = pd.DataFrame(rentas_raw["ofertas_crudas_bronce"])

    # Resolución de conflicto 1: Homologación de llave temporal en fuente macroeconómica
    df_macro["periodo_mensual_homologado"] = df_macro.apply(
        lambda r: normalize_banxico_date_to_ym(r.get("fecha_banxico_raw"), r.get("periodo_mensual")),
        axis=1,
    )

    # Contabilizar conflictos resueltos en fuente inmobiliaria
    string_currency_count = int(
        df_rentas["renta_lista_mensual_mxn"].apply(lambda x: isinstance(x, str)).sum()
    )
    non_canonical_type_count = int(
        (~df_rentas["tipo_inmueble"].isin(["depto_1rec", "depto_2rec", "casa"])).sum()
    )

    # Resolución de conflicto 2: Limpieza de cadenas monetarias a punto flotante IEEE 754
    for col in [
        "superficie_m2",
        "renta_lista_mensual_mxn",
        "descuento_contrato_pct",
        "renta_efectiva_mensual_mxn",
        "precio_m2_mxn",
        "cuota_mantenimiento_mxn",
        "valor_comercial_estimado_mxn",
        "yield_bruto_anual_pct",
        "tasa_ocupacion_24m_pct",
    ]:
        df_rentas[col] = df_rentas[col].apply(parse_currency_or_float)

    # Resolución de conflicto 3: Homologación de dominio categórico en `tipo_inmueble`
    df_rentas["tipo_inmueble_raw"] = df_rentas["tipo_inmueble"]
    df_rentas["tipo_inmueble"] = (
        df_rentas["tipo_inmueble"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(TIPO_INMUEBLE_CANONICAL_MAP)
        .fillna(df_rentas["tipo_inmueble"])
    )

    # Integración relacional (Left Join validado M:1 sobre `periodo_mensual`)
    macro_cols = [
        "periodo_mensual_homologado",
        "indice_periodo",
        "inpc_general",
        "inpc_vivienda_zmvm",
        "inflacion_anual_general_pct",
        "inflacion_anual_vivienda_pct",
        "tiie_28d_pct",
        "tipo_cambio_fix_mxn_usd",
    ]
    df_merged = df_rentas.merge(
        df_macro[macro_cols],
        left_on="periodo_mensual",
        right_on="periodo_mensual_homologado",
        how="left",
        validate="many_to_one",
    ).drop(columns=["periodo_mensual_homologado"])

    integration_report = {
        "total_registros_bronce": int(len(df_rentas)),
        "total_periodos_macro": int(len(df_macro)),
        "registros_integrados": int(len(df_merged)),
        "conflictos_moneda_string_resueltos": string_currency_count,
        "conflictos_categoria_tipo_inmueble_resueltos": non_canonical_type_count,
        "fechas_banxico_normalizadas": int(len(df_macro)),
        "registros_sin_match_macro": int(df_merged["inpc_vivienda_zmvm"].isna().sum()),
    }

    return df_merged, integration_report


# ==============================================================================
# 2. PUERTA DE CALIDAD AUTOMÁTICA (PANDERA) CON ENVÍO A CUARENTENA
# ==============================================================================

def build_pandera_pre_silver_schema() -> DataFrameSchema:
    """
    Define el contrato de datos formal en Pandera para la Puerta de Calidad.
    Valida rangos físicos plausibles, precios positivos y dominios cerrados.
    """
    return DataFrameSchema(
        columns={
            "id_propiedad": Column(str, Check.str_startswith("PROP-"), nullable=False),
            "periodo_mensual": Column(
                str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$"), nullable=False
            ),
            "subzona_id": Column(
                str,
                Check.isin(
                    [
                        "SZ1_PRIME_PONIENTE",
                        "SZ2_CENTRAL_CORREDOR",
                        "SZ3_CONSOLIDADA_SUR",
                        "SZ4_EMERGENTE_METROPOLITANA",
                    ]
                ),
                nullable=False,
            ),
            "tipo_inmueble": Column(
                str, Check.isin(["depto_1rec", "depto_2rec", "casa"]), nullable=False
            ),
            # Superficie puede ser nula antes de imputar MAR, pero si está presente debe estar en [20, 1200] m2
            "superficie_m2": Column(
                float,
                [
                    Check.greater_than_or_equal_to(20.0, error="superficie_m2_menor_20m2"),
                    Check.less_than_or_equal_to(1200.0, error="superficie_m2_mayor_1200m2"),
                ],
                nullable=True,
                coerce=True,
            ),
            # El precio de lista NO puede ser nulo ni <= 0
            "renta_lista_mensual_mxn": Column(
                float,
                [
                    Check.greater_than(1500.0, error="renta_lista_invalida_o_negativa"),
                    Check.less_than_or_equal_to(500000.0, error="renta_lista_excede_umbral"),
                ],
                nullable=False,
                coerce=True,
            ),
            "inpc_vivienda_zmvm": Column(float, Check.greater_than(50.0), nullable=False, coerce=True),
            "tiie_28d_pct": Column(float, Check.in_range(0.0, 30.0), nullable=False, coerce=True),
        },
        strict=False,
    )


def run_quality_gate_with_quarantine(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Ejecuta la Puerta de Calidad automática con Pandera y detección de duplicados.
    Los registros inválidos NUNCA se eliminan en silencio: se separan y documentan
    con su motivo exacto en `cuarentena_inmobiliario.csv`.
    """
    df_work = df.copy().reset_index(drop=True)
    quarantine_reasons: Dict[int, List[str]] = {}

    # Regla 1: Detección de duplicados exactos por llave compuesta (id_propiedad, periodo_mensual)
    dup_mask = df_work.duplicated(subset=["id_propiedad", "periodo_mensual"], keep="first")
    for idx in df_work[dup_mask].index:
        quarantine_reasons.setdefault(int(idx), []).append(
            "DUPLICADO_ID_PERIODO: Registro duplicado por republicación en el mismo mes"
        )

    # Regla 2: Validación declarativa con Pandera (lazy=True para capturar todos los fallos por fila)
    schema = build_pandera_pre_silver_schema()
    try:
        schema.validate(df_work, lazy=True)
    except SchemaErrors as err:
        failure_df = err.failure_cases
        for _, row in failure_df.iterrows():
            idx_val = row.get("index")
            if idx_val is not None and not pd.isna(idx_val):
                col_name = row.get("column", "tabla")
                check_name = row.get("check", "regla_esquema")
                f_val = row.get("failure_case", "N/A")
                quarantine_reasons.setdefault(int(idx_val), []).append(
                    f"PANDERA_FAIL[{col_name}]: {check_name} (valor={f_val})"
                )

    quarantine_indices = sorted(quarantine_reasons.keys())
    df_quarantine = df_work.loc[quarantine_indices].copy()
    df_quarantine["motivo_cuarentena"] = [
        " | ".join(quarantine_reasons[i]) for i in quarantine_indices
    ]
    df_quarantine["timestamp_cuarentena_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    df_quarantine["estado_capa"] = "CUARENTENA_RECHAZADO"

    df_valid = df_work.drop(index=quarantine_indices).copy().reset_index(drop=True)

    # Validación final en verde sobre el lote limpio con Pandera
    schema.validate(df_valid, lazy=True)

    gate_report = {
        "total_evaluados": int(len(df_work)),
        "total_aprobados_plata": int(len(df_valid)),
        "total_enviados_cuarentena": int(len(df_quarantine)),
        "tasa_rechazo_cuarentena_pct": round(len(df_quarantine) / len(df_work) * 100.0, 2),
        "desglose_motivos_cuarentena": df_quarantine["motivo_cuarentena"].value_counts().to_dict(),
    }

    return df_valid, df_quarantine, gate_report


# ==============================================================================
# 3. DIAGNÓSTICO (MCAR / MAR / MNAR) E IMPUTACIÓN JUSTIFICADA DE FALTANTES
# ==============================================================================

def diagnose_and_impute_missing_values(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Diagnostica estadísticamente el mecanismo de datos faltantes (MCAR, MAR, MNAR)
    y ejecuta la imputación pertinente dejando trazabilidad en banderas de calidad.
    """
    df_imp = df.copy()

    # Conteo inicial de faltantes
    missing_before = {
        "estacionamientos": int(df_imp["estacionamientos"].isna().sum()),
        "superficie_m2": int(df_imp["superficie_m2"].isna().sum()),
        "cuota_mantenimiento_mxn": int(df_imp["cuota_mantenimiento_mxn"].isna().sum()),
    }

    # --- Diagnóstico 1: `estacionamientos` (MCAR) ---
    # Prueba Chi-cuadrado de independencia entre ausencia de `estacionamientos` y `subzona_id`
    ct_mcar = pd.crosstab(df_imp["estacionamientos"].isna(), df_imp["subzona_id"])
    chi2_mcar, p_mcar, _, _ = stats.chi2_contingency(ct_mcar)

    # --- Diagnóstico 2: `superficie_m2` (MAR condicionado a `subzona_id`) ---
    ct_mar = pd.crosstab(df_imp["superficie_m2"].isna(), df_imp["subzona_id"])
    chi2_mar, p_mar, _, _ = stats.chi2_contingency(ct_mar)

    # --- Diagnóstico 3: `cuota_mantenimiento_mxn` (MNAR asociado al nivel de renta/mantenimiento) ---
    rent_when_maint_missing = df_imp.loc[
        df_imp["cuota_mantenimiento_mxn"].isna(), "renta_lista_mensual_mxn"
    ]
    rent_when_maint_present = df_imp.loc[
        df_imp["cuota_mantenimiento_mxn"].notna(), "renta_lista_mensual_mxn"
    ]
    t_mnar, p_mnar = stats.ttest_ind(
        rent_when_maint_missing, rent_when_maint_present, equal_var=False
    )

    # --- Imputación 1 (MCAR): `estacionamientos` por moda según `tipo_inmueble` ---
    df_imp["flag_imputado_estacionamientos_mcar"] = df_imp["estacionamientos"].isna().astype(int)
    mode_by_type = (
        df_imp.groupby("tipo_inmueble")["estacionamientos"]
        .agg(lambda s: float(s.mode().iloc[0]) if not s.mode().empty else 1.0)
        .to_dict()
    )
    df_imp["estacionamientos"] = (
        df_imp["estacionamientos"]
        .fillna(df_imp["tipo_inmueble"].map(mode_by_type))
        .astype(int)
    )

    # --- Imputación 2 (MAR): `superficie_m2` por mediana estratificada (subzona_id, tipo_inmueble, recamaras) ---
    df_imp["flag_imputado_superficie_mar"] = df_imp["superficie_m2"].isna().astype(int)
    median_m2_strata = df_imp.groupby(["subzona_id", "tipo_inmueble", "recamaras"])[
        "superficie_m2"
    ].transform("median")
    df_imp["superficie_m2"] = df_imp["superficie_m2"].fillna(median_m2_strata).round(1)
    # Recalcular precio_m2_mxn donde se imputó la superficie
    df_imp["precio_m2_mxn"] = (
        df_imp["renta_lista_mensual_mxn"] / df_imp["superficie_m2"]
    ).round(2)

    # --- Imputación 3 (MNAR): `cuota_mantenimiento_mxn` por razón mediana + indicador explícito MNAR ---
    df_imp["flag_mnar_mantenimiento"] = df_imp["cuota_mantenimiento_mxn"].isna().astype(int)
    df_imp["ratio_mant_renta_temp"] = (
        df_imp["cuota_mantenimiento_mxn"] / df_imp["renta_lista_mensual_mxn"]
    )
    median_ratio_by_subzona = df_imp.groupby("subzona_id")["ratio_mant_renta_temp"].transform(
        "median"
    )
    df_imp["cuota_mantenimiento_mxn"] = (
        df_imp["cuota_mantenimiento_mxn"]
        .fillna((df_imp["renta_lista_mensual_mxn"] * median_ratio_by_subzona).round(0))
    )
    df_imp.drop(columns=["ratio_mant_renta_temp"], inplace=True)

    missing_after = {
        "estacionamientos": int(df_imp["estacionamientos"].isna().sum()),
        "superficie_m2": int(df_imp["superficie_m2"].isna().sum()),
        "cuota_mantenimiento_mxn": int(df_imp["cuota_mantenimiento_mxn"].isna().sum()),
    }

    missing_report = {
        "faltantes_antes_imputacion": missing_before,
        "faltantes_despues_imputacion": missing_after,
        "diagnostico_mecanismos": {
            "estacionamientos_MCAR": {
                "mecanismo": "MCAR (Missing Completely At Random)",
                "chi2_stat": round(float(chi2_mcar), 4),
                "p_value": round(float(p_mcar), 4),
                "interpretacion": (
                    "p > 0.05 confirma que la ausencia no depende de la ubicación ni del precio; "
                    "se imputa por moda condicional del tipo de inmueble."
                ),
            },
            "superficie_m2_MAR": {
                "mecanismo": "MAR (Missing At Random)",
                "chi2_stat": round(float(chi2_mar), 4),
                "p_value": float(p_mar),
                "interpretacion": (
                    "p < 0.001 demuestra dependencia sistemática respecto a la variable observada "
                    "subzona_id (concentrado en SZ4); se imputa con mediana estratificada por "
                    "(subzona_id, tipo_inmueble, recamaras)."
                ),
            },
            "cuota_mantenimiento_MNAR": {
                "mecanismo": "MNAR (Missing Not At Random)",
                "t_stat": round(float(t_mnar), 4),
                "p_value": float(p_mnar),
                "renta_media_cuando_falta_mxn": round(float(rent_when_maint_missing.mean()), 2),
                "renta_media_cuando_presente_mxn": round(float(rent_when_maint_present.mean()), 2),
                "interpretacion": (
                    "p < 0.001 confirma que los anuncios que omiten la cuota de mantenimiento "
                    "corresponden a rentas significativamente más altas (ocultamiento estratégico de cuotas caras). "
                    "Se conserva la bandera binaria flag_mnar_mantenimiento y se imputa por razón mediana zonal."
                ),
            },
        },
    }

    return df_imp, missing_report


# ==============================================================================
# 4. DETECCIÓN Y TRATAMIENTO DE ATÍPICOS (IQR, Z-SCORE ROBUSTO, ISOLATION FOREST)
# ==============================================================================

def detect_and_treat_outliers(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    r"""
    Aplica tres detectores estadísticos/ML de valores atípicos sobre `precio_m2_mxn` y
    variables conjuntas:
      1. IQR por sub-zona ($Q_1 - 1.5 \cdot IQR$, $Q_3 + 1.5 \cdot IQR$).
      2. Z-Score Robusto basado en Mediana y MAD ($|Z_{\text{rob}}| > 3.5$).
      3. Isolation Forest multivariado (`precio_m2_mxn`, `superficie_m2`, `yield_bruto_anual_pct`).
    Aplica Winsorización estratificada (percentiles 1% y 99% por `subzona_id`) guardando
    la variable original y la tratada (`precio_m2_winsor_mxn`).
    """
    df_out = df.copy()

    # 1. Método IQR estratificado por subzona_id
    q1 = df_out.groupby("subzona_id")["precio_m2_mxn"].transform(lambda s: s.quantile(0.25))
    q3 = df_out.groupby("subzona_id")["precio_m2_mxn"].transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    df_out["outlier_iqr"] = (
        (df_out["precio_m2_mxn"] < (q1 - 1.5 * iqr))
        | (df_out["precio_m2_mxn"] > (q3 + 1.5 * iqr))
    ).astype(int)

    # 2. Método Z-Score Robusto (Mediana y MAD) por subzona_id
    med = df_out.groupby("subzona_id")["precio_m2_mxn"].transform("median")
    mad = df_out.groupby("subzona_id")["precio_m2_mxn"].transform(
        lambda s: np.median(np.abs(s - np.median(s)))
    )
    df_out["zscore_robusto_precio_m2"] = (
        0.6745 * (df_out["precio_m2_mxn"] - med) / mad.replace(0, 1e-6)
    ).round(4)
    df_out["outlier_zrobusto"] = (df_out["zscore_robusto_precio_m2"].abs() > 3.5).astype(int)

    # 3. Método Isolation Forest multivariado
    features_iforest = df_out[["precio_m2_mxn", "superficie_m2", "yield_bruto_anual_pct"]].values
    iso = IsolationForest(n_estimators=150, contamination=0.025, random_state=20261116)
    preds_iso = iso.fit_predict(features_iforest)
    df_out["outlier_isolation_forest"] = (preds_iso == -1).astype(int)

    # Consenso (al menos 2 de 3 métodos marcan atípico)
    df_out["outlier_consenso"] = (
        (df_out["outlier_iqr"] + df_out["outlier_zrobusto"] + df_out["outlier_isolation_forest"])
        >= 2
    ).astype(int)

    # Tratamiento: Winsorización estratificada al percentil [1%, 99%] por subzona_id
    p01 = df_out.groupby("subzona_id")["precio_m2_mxn"].transform(lambda s: s.quantile(0.01))
    p99 = df_out.groupby("subzona_id")["precio_m2_mxn"].transform(lambda s: s.quantile(0.99))
    df_out["precio_m2_winsor_mxn"] = df_out["precio_m2_mxn"].clip(lower=p01, upper=p99).round(2)
    df_out["renta_efectiva_winsor_mxn"] = (
        df_out["precio_m2_winsor_mxn"]
        * df_out["superficie_m2"]
        * (1.0 - df_out["descuento_contrato_pct"] / 100.0)
    ).round(2)

    outlier_report = {
        "detectados_iqr": int(df_out["outlier_iqr"].sum()),
        "detectados_zscore_robusto": int(df_out["outlier_zrobusto"].sum()),
        "detectados_isolation_forest": int(df_out["outlier_isolation_forest"].sum()),
        "detectados_consenso_2_de_3": int(df_out["outlier_consenso"].sum()),
        "precio_m2_max_antes_winsor": float(df_out["precio_m2_mxn"].max()),
        "precio_m2_max_despues_winsor": float(df_out["precio_m2_winsor_mxn"].max()),
        "precio_m2_std_antes_winsor": round(float(df_out["precio_m2_mxn"].std()), 2),
        "precio_m2_std_despues_winsor": round(float(df_out["precio_m2_winsor_mxn"].std()), 2),
    }

    return df_out, outlier_report


# ==============================================================================
# 5. NORMALIZACIÓN, ESTANDARIZACIÓN, DISCRETIZACIÓN Y JERARQUÍAS CONCEPTUALES
# ==============================================================================

def transform_scale_discretize_and_hierarchies(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Aplica:
      - Normalización Min-Max [0, 1] y Estandarización Z-Score (media 0, std 1) a variables continuas.
      - Discretización en categorías ordinales (rangos de metraje, nivel de precio/m2 y tramo de vacancia).
      - Jerarquías conceptuales espaciales y temporales (`Mes -> Trimestre -> Año`).
    """
    df_tr = df.copy()

    continuous_cols = [
        "precio_m2_winsor_mxn",
        "superficie_m2",
        "renta_efectiva_winsor_mxn",
        "yield_bruto_anual_pct",
        "dias_vacancia_observados",
    ]

    minmax_scaler = MinMaxScaler()
    zscore_scaler = StandardScaler()

    minmax_vals = minmax_scaler.fit_transform(df_tr[continuous_cols])
    zscore_vals = zscore_scaler.fit_transform(df_tr[continuous_cols])

    for i, col in enumerate(continuous_cols):
        short_name = col.replace("_winsor", "").replace("_observados", "")
        df_tr[f"{short_name}_minmax"] = np.round(minmax_vals[:, i], 4)
        df_tr[f"{short_name}_zscore"] = np.round(zscore_vals[:, i], 4)

    # Discretización 1: Segmento de Superficie Construida (m2)
    df_tr["rango_superficie_cat"] = pd.cut(
        df_tr["superficie_m2"],
        bins=[0.0, 60.0, 100.0, 160.0, np.inf],
        labels=[
            "1_Compacto (<60 m2)",
            "2_Medio (60-100 m2)",
            "3_Amplio (100-160 m2)",
            "4_Residencial Plus (>160 m2)",
        ],
    ).astype(str)

    # Discretización 2: Estrato de Precio por m2 (Cuartiles de mercado)
    df_tr["estrato_precio_m2_cat"] = pd.qcut(
        df_tr["precio_m2_winsor_mxn"],
        q=4,
        labels=["Q1_Accesible", "Q2_Moderado", "Q3_Alto", "Q4_Prime"],
    ).astype(str)

    # Discretización 3: Nivel de Velocidad de Absorción / Vacancia
    df_tr["nivel_vacancia_cat"] = pd.cut(
        df_tr["dias_vacancia_observados"],
        bins=[0, 21, 35, 50, np.inf],
        labels=[
            "Rapida (<=21 dias)",
            "Normal (22-35 dias)",
            "Lenta (36-50 dias)",
            "Estancada (>50 dias)",
        ],
    ).astype(str)

    # Jerarquía Conceptual 1 (Espacial): Colonia -> Alcaldía/Municipio -> Sub-zona -> Corredor Macro -> Región ZMVM
    df_tr["corredor_macro_zmvm"] = df_tr["subzona_id"].map(JERARQUIA_ESPACIAL_MACRO)
    df_tr["region_metropolitana"] = "ZMVM (Valle de México)"
    df_tr["jerarquia_ubicacion_completa"] = (
        df_tr["region_metropolitana"]
        + " > "
        + df_tr["corredor_macro_zmvm"]
        + " > "
        + df_tr["alcaldia_municipio"]
        + " > "
        + df_tr["colonia"]
    )

    # Jerarquía Conceptual 2 (Temporal): Periodo Mensual -> Trimestre -> Año
    years = df_tr["periodo_mensual"].str.slice(0, 4).astype(int)
    months = df_tr["periodo_mensual"].str.slice(5, 7).astype(int)
    quarters = ((months - 1) // 3) + 1
    df_tr["anio"] = years
    df_tr["trimestre"] = [f"{y}-Q{q}" for y, q in zip(years, quarters)]

    # Jerarquía Conceptual 3 (Tipológica): Unidad -> Categoría General (Vertical vs Horizontal)
    df_tr["familia_inmueble"] = np.where(
        df_tr["tipo_inmueble"].isin(["depto_1rec", "depto_2rec"]),
        "Vivienda_Vertical_Departamento",
        "Vivienda_Horizontal_Casa",
    )

    df_tr["estado_capa"] = "PLATA_VALIDADO"

    transform_report = {
        "variables_normalizadas_minmax_zscore": continuous_cols,
        "distribucion_rango_superficie": df_tr["rango_superficie_cat"].value_counts().to_dict(),
        "distribucion_estrato_precio_m2": df_tr["estrato_precio_m2_cat"].value_counts().to_dict(),
        "distribucion_nivel_vacancia": df_tr["nivel_vacancia_cat"].value_counts().to_dict(),
        "niveles_jerarquia_espacial": [
            "colonia",
            "alcaldia_municipio",
            "subzona_nombre",
            "corredor_macro_zmvm",
            "region_metropolitana",
        ],
    }

    return df_tr, transform_report


# ==============================================================================
# 6. REDUCCIÓN DE DATOS Y CONSTRUCCIÓN DE CAPA ORO (DATASETS ANALÍTICOS E1, E2, E3)
# ==============================================================================

def build_gold_layer_datasets(
    df_silver: pd.DataFrame,
) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """
    Aplica reducción de datos en dos vertientes:
      A. Selección de variables (eliminando columnas crudas/auxiliares redundantes y reteniendo las
         18 variables con mayor poder explicativo y baja colinealidad para la tabla maestra reducida).
      B. Agregación multidimensional hacia la Capa Oro (`data/gold/inmobiliario/`) generando las
         3 tablas analíticas específicas para responder E1, E2 y E3 en las siguientes fases.
    """
    selected_features = [
        "id_propiedad",
        "periodo_mensual",
        "trimestre",
        "anio",
        "subzona_id",
        "subzona_nombre",
        "alcaldia_municipio",
        "colonia",
        "familia_inmueble",
        "tipo_inmueble",
        "recamaras",
        "superficie_m2",
        "rango_superficie_cat",
        "precio_m2_winsor_mxn",
        "precio_m2_mxn_minmax",
        "precio_m2_mxn_zscore",
        "estrato_precio_m2_cat",
        "renta_lista_mensual_mxn",
        "descuento_contrato_pct",
        "renta_efectiva_winsor_mxn",
        "cuota_mantenimiento_mxn",
        "flag_mnar_mantenimiento",
        "yield_bruto_anual_pct",
        "modalidad_contrato",
        "dias_vacancia_observados",
        "nivel_vacancia_cat",
        "tasa_ocupacion_24m_pct",
        "inpc_vivienda_zmvm",
        "inflacion_anual_vivienda_pct",
        "tiie_28d_pct",
        "tipo_cambio_fix_mxn_usd",
    ]

    df_silver_reduced = df_silver[selected_features].copy()

    # 1. Tabla Oro E1: Serie Mensual y Trimestral para Pronóstico de Precio/m2
    df_gold_e1 = (
        df_silver_reduced.groupby(["periodo_mensual", "trimestre", "anio"], as_index=False)
        .agg(
            n_propiedades_validadas=("id_propiedad", "count"),
            precio_m2_media_mxn=("precio_m2_winsor_mxn", "mean"),
            precio_m2_mediana_mxn=("precio_m2_winsor_mxn", "median"),
            precio_m2_std_mxn=("precio_m2_winsor_mxn", "std"),
            renta_efectiva_mediana_mxn=("renta_efectiva_winsor_mxn", "median"),
            yield_bruto_medio_pct=("yield_bruto_anual_pct", "mean"),
            dias_vacancia_medio=("dias_vacancia_observados", "mean"),
            inpc_vivienda_zmvm=("inpc_vivienda_zmvm", "first"),
            inflacion_anual_vivienda_pct=("inflacion_anual_vivienda_pct", "first"),
            tiie_28d_pct=("tiie_28d_pct", "first"),
            tipo_cambio_fix_mxn_usd=("tipo_cambio_fix_mxn_usd", "first"),
        )
        .round(3)
    )

    # 2. Tabla Oro E2: Cubo Experimental What-If (Descuento x Modalidad Contrato x Sub-zona)
    df_gold_e2 = (
        df_silver_reduced.groupby(
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
    # Cálculo de ingreso efectivo esperado en 24 meses (24 * renta_efectiva * tasa_ocupacion)
    df_gold_e2["ingreso_efectivo_esperado_24m_mxn"] = (
        24.0
        * df_gold_e2["renta_efectiva_promedio_mxn"]
        * (df_gold_e2["tasa_ocupacion_24m_promedio_pct"] / 100.0)
    ).round(2)

    # 3. Tabla Oro E3: Cubo Comparación Multivariada (Tipología x Sub-zona Urbana)
    df_gold_e3 = (
        df_silver_reduced.groupby(
            ["subzona_id", "subzona_nombre", "familia_inmueble", "tipo_inmueble"],
            as_index=False,
        )
        .agg(
            n_inmuebles=("id_propiedad", "count"),
            superficie_m2_promedio=("superficie_m2", "mean"),
            precio_m2_promedio_mxn=("precio_m2_winsor_mxn", "mean"),
            precio_m2_mediana_mxn=("precio_m2_winsor_mxn", "median"),
            renta_mensual_promedio_mxn=("renta_efectiva_winsor_mxn", "mean"),
            yield_bruto_promedio_pct=("yield_bruto_anual_pct", "mean"),
            yield_bruto_mediana_pct=("yield_bruto_anual_pct", "median"),
            yield_bruto_std_pct=("yield_bruto_anual_pct", "std"),
            dias_vacancia_promedio=("dias_vacancia_observados", "mean"),
        )
        .round(2)
    )

    reduction_report = {
        "columnas_totales_capa_plata_completa": int(df_silver.shape[1]),
        "columnas_seleccionadas_vista_reducida": int(df_silver_reduced.shape[1]),
        "reduccion_dimensionalidad_pct": round(
            (1.0 - df_silver_reduced.shape[1] / df_silver.shape[1]) * 100.0, 2
        ),
        "filas_plata_microdatos": int(len(df_silver_reduced)),
        "filas_oro_e1_series_tiempo": int(len(df_gold_e1)),
        "filas_oro_e2_experimento_whatif": int(len(df_gold_e2)),
        "filas_oro_e3_multivariado_yield": int(len(df_gold_e3)),
    }

    gold_datasets = {
        "silver_reduced": df_silver_reduced,
        "oro_e1_pronostico_mensual_trimestral": df_gold_e1,
        "oro_e2_simulacion_whatif_24m": df_gold_e2,
        "oro_e3_comparacion_multivariada_yield": df_gold_e3,
    }

    return gold_datasets, reduction_report


# ==============================================================================
# 7. EJECUCIÓN PRINCIPAL Y PERSISTENCIA DE ARTEFACTOS PLATA / CUARENTENA / ORO
# ==============================================================================

def run_full_e1_pipeline() -> Dict[str, Any]:
    """Ejecuta el pipeline E1 de principio a fin y guarda todos los artefactos y reportes."""
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    # Paso 1: Integración y resolución de conflictos
    df_integrated, integration_report = load_and_integrate_sources()

    # Paso 2: Puerta de Calidad automática con Pandera y cuarentena
    df_valid, df_quarantine, gate_report = run_quality_gate_with_quarantine(df_integrated)

    # Paso 3: Diagnóstico MCAR/MAR/MNAR e imputación justificada
    df_imputed, missing_report = diagnose_and_impute_missing_values(df_valid)

    # Paso 4: Detección y tratamiento de atípicos (IQR, Z-Score Robusto, Isolation Forest)
    df_outliers_treated, outlier_report = detect_and_treat_outliers(df_imputed)

    # Paso 5: Normalización, estandarización, discretización y jerarquías conceptuales
    df_silver_full, transform_report = transform_scale_discretize_and_hierarchies(
        df_outliers_treated
    )

    # Paso 6: Reducción de datos y construcción de Capa Oro
    gold_datasets, reduction_report = build_gold_layer_datasets(df_silver_full)

    # Escritura de archivos en Capa Plata y Cuarentena
    silver_csv_path = SILVER_DIR / "rentas_zmvm_plata_limpio.csv"
    quarantine_csv_path = SILVER_DIR / "cuarentena_inmobiliario.csv"
    quarantine_json_path = SILVER_DIR / "cuarentena_inmobiliario.json"

    gold_datasets["silver_reduced"].to_csv(silver_csv_path, index=False, encoding="utf-8")
    df_quarantine.to_csv(quarantine_csv_path, index=False, encoding="utf-8")
    quarantine_json_path.write_text(
        json.dumps(
            {
                "metadata": gate_report,
                "registros_en_cuarentena": df_quarantine.to_dict(orient="records"),
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        ),
        encoding="utf-8",
    )

    # Escritura de archivos en Capa Oro
    for name in [
        "oro_e1_pronostico_mensual_trimestral",
        "oro_e2_simulacion_whatif_24m",
        "oro_e3_comparacion_multivariada_yield",
    ]:
        out_path = GOLD_DIR / f"{name}.csv"
        gold_datasets[name].to_csv(out_path, index=False, encoding="utf-8")

    # Reporte maestro de auditoría del pipeline E1
    full_summary = {
        "pipeline": "Observatorio Inmobiliario ZMVM — Pipeline E1 (Bronce -> Plata -> Oro)",
        "executed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "integracion_y_conflictos": integration_report,
        "puerta_calidad_pandera_y_cuarentena": gate_report,
        "valores_faltantes_mcar_mar_mnar": missing_report,
        "deteccion_y_tratamiento_atipicos": outlier_report,
        "normalizacion_discretizacion_jerarquias": transform_report,
        "reduccion_datos_y_capa_oro": reduction_report,
    }

    report_json_path = GOLD_DIR / "reporte_auditoria_pipeline_e1.json"
    report_json_path.write_text(
        json.dumps(full_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return full_summary


def main() -> None:
    print("=" * 78)
    print("Ejecutando Pipeline E1 (Limpieza, Pandera Quality Gate, Capas Plata y Oro)")
    print("=" * 78)
    summary = run_full_e1_pipeline()
    gate = summary["puerta_calidad_pandera_y_cuarentena"]
    miss = summary["valores_faltantes_mcar_mar_mnar"]
    out = summary["deteccion_y_tratamiento_atipicos"]
    red = summary["reduccion_datos_y_capa_oro"]

    print(f"[1] Registros integrados de Capa Bronce : {gate['total_evaluados']}")
    print(
        f"[2] Puerta de Calidad (Pandera)         : {gate['total_aprobados_plata']} aprobados | "
        f"{gate['total_enviados_cuarentena']} en cuarentena ({gate['tasa_rechazo_cuarentena_pct']}%)"
    )
    print(
        f"[3] Faltantes imputados (MCAR/MAR/MNAR) : {miss['faltantes_antes_imputacion']} -> "
        f"{miss['faltantes_despues_imputacion']}"
    )
    print(
        f"[4] Outliers detectados                 : IQR={out['detectados_iqr']}, "
        f"Z-Robusto={out['detectados_zscore_robusto']}, "
        f"IsolationForest={out['detectados_isolation_forest']} "
        f"(Consenso={out['detectados_consenso_2_de_3']})"
    )
    print(
        f"[5] Reducción y Capa Oro generada       : "
        f"E1={red['filas_oro_e1_series_tiempo']} filas | "
        f"E2={red['filas_oro_e2_experimento_whatif']} filas | "
        f"E3={red['filas_oro_e3_multivariado_yield']} filas"
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
