from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="ClimaScope-PACA",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_TITLE = "ClimaScope-PACA"
APP_SUBTITLE = "Comprendre le climat local d’hier, projeter celui de demain, agir dès aujourd’hui."

FINAL_DIR = Path("data/processed/final")
CLIMATE_DIR = Path("data/processed/climate")


# =========================================================
# STYLE
# =========================================================
st.markdown(
    """
    <style>
    .main > div {
        padding-top: 1.2rem;
    }
    .hero-box {
        padding: 1.2rem 1.4rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #eef6ff 0%, #f8fbff 100%);
        border: 1px solid #d8e6f5;
        margin-bottom: 1rem;
    }
    .section-note {
        padding: 0.9rem 1rem;
        border-radius: 0.8rem;
        background-color: #f7f7f7;
        border-left: 4px solid #4f81bd;
        margin-bottom: 1rem;
    }
    .warning-note {
        padding: 0.9rem 1rem;
        border-radius: 0.8rem;
        background-color: #fff8e6;
        border-left: 4px solid #d4a017;
        margin-bottom: 1rem;
    }
    .small-muted {
        color: #666;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================
@st.cache_data
def load_data():
    hero_daily = pd.read_parquet(FINAL_DIR / "dashboard_hero_station_daily_v1.parquet")
    hero_annual = pd.read_parquet(FINAL_DIR / "dashboard_hero_station_annual_v1.parquet")
    dept_annual = pd.read_parquet(FINAL_DIR / "dashboard_department_annual_v1.parquet")
    return hero_daily, hero_annual, dept_annual


@st.cache_data
def load_optional_drias_projection():
    """
    Charge la projection DRIAS transformée si elle existe déjà.
    """
    parquet_candidate = CLIMATE_DIR / "drias_projection_pilot_v1.parquet"
    csv_candidate = CLIMATE_DIR / "drias_projection_pilot_v1.csv"

    if parquet_candidate.exists():
        return pd.read_parquet(parquet_candidate)

    if csv_candidate.exists():
        return pd.read_csv(csv_candidate, parse_dates=["date"])

    return None


def safe_period_filter(
    df: pd.DataFrame,
    year_col: str,
    start_year: int | None = None,
    end_year: int | None = None,
) -> pd.DataFrame:
    out = df.copy()
    if start_year is not None:
        out = out[out[year_col] >= start_year]
    if end_year is not None:
        out = out[out[year_col] <= end_year]
    return out.copy()


def latest_complete_year_from_daily(df: pd.DataFrame, min_days: int = 300) -> int:
    """
    Retourne la dernière année jugée "complète" à partir du nombre de jours disponibles.
    """
    counts = df.groupby("year")["date"].nunique()
    valid_years = counts[counts >= min_days]

    if valid_years.empty:
        return int(df["year"].max())

    return int(valid_years.index.max())


def compute_reference_delta(
    df: pd.DataFrame,
    value_col: str,
    recent_start: int = 1991,
    recent_end: int = 2020,
    last_year: int | None = None,
):
    tmp = df[[value_col, "year"]].dropna().copy()
    if tmp.empty:
        return None, None, None

    ref = tmp[(tmp["year"] >= recent_start) & (tmp["year"] <= recent_end)][value_col].mean()
    latest_year = int(last_year) if last_year is not None else int(tmp["year"].max())
    latest_value = tmp.loc[tmp["year"] == latest_year, value_col].mean()

    if pd.isna(ref) or pd.isna(latest_value):
        return latest_year, latest_value, None

    return latest_year, latest_value, latest_value - ref


def fmt_number(value, digits: int = 1, suffix: str = "") -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.{digits}f}{suffix}"


def build_line_chart(df, x, y, title, y_label=None):
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Année" if x == "year" else x,
        yaxis_title=y_label or y,
        title_font_size=20,
    )
    return fig


def build_daily_chart(df, x, y, title, y_label=None):
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Date",
        yaxis_title=y_label or y,
        title_font_size=18,
    )
    return fig


def annualize_drias_projection(drias_df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège la projection DRIAS journalière au niveau annuel.
    Attend:
    - date
    - tas_c
    - pr_mm_day
    """
    if drias_df is None or drias_df.empty:
        return pd.DataFrame()

    tmp = drias_df.copy()

    if "date" not in tmp.columns:
        return pd.DataFrame()

    tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
    tmp["year"] = tmp["date"].dt.year

    group_cols = ["year"]
    if "latitude" in tmp.columns and "longitude" in tmp.columns:
        group_cols = ["year", "latitude", "longitude"]

    annual_grid = (
        tmp.groupby(group_cols, dropna=False)
        .agg(
            avg_annual_temperature_c=("tas_c", "mean"),
            annual_precipitation_mm=("pr_mm_day", "sum"),
        )
        .reset_index()
    )

    annual_region = (
        annual_grid.groupby("year", dropna=False)
        .agg(
            avg_annual_temperature_c=("avg_annual_temperature_c", "mean"),
            annual_precipitation_mm=("annual_precipitation_mm", "mean"),
        )
        .reset_index()
        .sort_values("year")
    )

    return annual_region


def projection_snapshot(df: pd.DataFrame, target_year: int, value_col: str):
    if df is None or df.empty or value_col not in df.columns:
        return None

    tmp = df[["year", value_col]].dropna().copy()
    if tmp.empty:
        return None

    idx = (tmp["year"] - target_year).abs().idxmin()
    return float(tmp.loc[idx, value_col])

def build_observed_vs_projected(
    observed_df: pd.DataFrame,
    projected_df: pd.DataFrame,
    observed_start_year: int = 1991,
) -> pd.DataFrame:
    """
    Construit un dataset comparatif observé vs projeté.
    """
    observed = (
        observed_df[observed_df["year"] >= observed_start_year][
            ["year", "avg_annual_temperature_c", "annual_precipitation_mm"]
        ]
        .dropna(how="all")
        .copy()
    )
    observed["series"] = "Observé (Département 13)"

    projected = projected_df[
        ["year", "avg_annual_temperature_c", "annual_precipitation_mm"]
    ].dropna(how="all").copy()
    projected["series"] = "Projeté (DRIAS pilote RCP4.5)"

    return pd.concat([observed, projected], ignore_index=True)

def add_selected_year_marker(fig, year: int):
    fig.add_vline(
        x=year,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Année sélectionnée : {year}",
        annotation_position="top",
    )
    return fig

# =========================================================
# LOAD
# =========================================================
hero_daily, hero_annual, dept_annual = load_data()
drias_projection = load_optional_drias_projection()
drias_annual = annualize_drias_projection(drias_projection)

hero_station_name = (
    str(hero_annual["station_name"].iloc[0])
    if not hero_annual.empty
    else "MARSEILLE-OBS"
)

LAST_COMPLETE_YEAR = latest_complete_year_from_daily(hero_daily)

# Historique complet robuste = jusqu'à la dernière année complète
dept_annual_full = safe_period_filter(dept_annual, "year", end_year=LAST_COMPLETE_YEAR)
hero_annual_full = safe_period_filter(hero_annual, "year", end_year=LAST_COMPLETE_YEAR)

# Période principale de narration
dept_annual_main = safe_period_filter(dept_annual_full, "year", start_year=1950)
hero_annual_main = safe_period_filter(hero_annual_full, "year", start_year=1950)

# KPI
temp_year, temp_latest, temp_delta = compute_reference_delta(
    dept_annual_main,
    "avg_annual_temperature_c",
    last_year=LAST_COMPLETE_YEAR,
)
hot_year, hot_latest, hot_delta = compute_reference_delta(
    hero_annual_main,
    "hot_days_over_30",
    last_year=LAST_COMPLETE_YEAR,
)
dry_year, dry_latest, dry_delta = compute_reference_delta(
    hero_annual_main,
    "max_dry_spell_length",
    last_year=LAST_COMPLETE_YEAR,
)


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Navigation")
st.sidebar.markdown(f"**{APP_TITLE}**")
st.sidebar.caption("Prototype analytique climat-territoire")

year_min = int(hero_daily["year"].min())

selected_year = st.sidebar.selectbox(
    "Année à explorer (onglet Historique > journalier Marseille)",
    options=list(range(LAST_COMPLETE_YEAR, year_min - 1, -1)),
    index=0,
)

show_long_history = st.sidebar.checkbox("Afficher l’historique long complet", value=False)

if show_long_history:
    dept_plot_df = dept_annual_full.copy()
    hero_plot_df = hero_annual_full.copy()
else:
    dept_plot_df = dept_annual_main.copy()
    hero_plot_df = hero_annual_main.copy()

st.sidebar.markdown("---")
st.sidebar.markdown("**Méthodologie**")
st.sidebar.markdown(
    """
- Vue station héroïne : **Marseille-OBS**
- Vue territoire : **série composite départementale**
- Indicateurs calculés à partir des **stations disponibles**
- Dernière année complète utilisée : **{}**
""".format(LAST_COMPLETE_YEAR)
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Fichiers utilisés**")
st.sidebar.code(
    "\n".join(
        [
            "dashboard_hero_station_daily_v1.parquet",
            "dashboard_hero_station_annual_v1.parquet",
            "dashboard_department_annual_v1.parquet",
        ]
    )
)


# =========================================================
# HEADER
# =========================================================
st.title(APP_TITLE)
st.subheader(APP_SUBTITLE)

st.markdown(
    """
    <div class="hero-box">
        <b>Objectif du prototype</b><br>
        Montrer l’évolution climatique observée sur les Bouches-du-Rhône, mettre en avant une station héroïne
        à Marseille, puis intégrer les projections futures et des recommandations d’action concrètes.
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "Vue d’ensemble",
        "Historique",
        "Projections",
        "Actions",
        "Méthodologie",
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================
with tabs[0]:
    st.markdown("## Vue d’ensemble")

    c1, c2, c3 = st.columns(3)
    c1.metric(
        f"Température moyenne annuelle (département, {temp_year})",
        fmt_number(temp_latest, 2, " °C"),
        None if temp_delta is None else f"{temp_delta:+.2f} °C vs réf. 1991-2020",
    )
    c2.metric(
        f"Jours > 30°C ({hero_station_name}, {hot_year})",
        fmt_number(hot_latest, 0, ""),
        None if hot_delta is None else f"{hot_delta:+.1f} vs réf. 1991-2020",
    )
    c3.metric(
        f"Séquence sèche max ({hero_station_name}, {dry_year})",
        fmt_number(dry_latest, 0, " jours"),
        None if dry_delta is None else f"{dry_delta:+.1f} jours vs réf. 1991-2020",
    )

    st.markdown(
        f"""
        <div class="section-note">
        <b>Lecture rapide :</b> le tableau de bord suit l’évolution de la chaleur, des précipitations et des séquences sèches
        sur le département 13 et sur une station héroïne à Marseille.  
        Les indicateurs affichés ci-dessus utilisent la <b>dernière année complète disponible : {LAST_COMPLETE_YEAR}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        fig_temp_dept = build_line_chart(
            dept_plot_df,
            "year",
            "avg_annual_temperature_c",
            "Température moyenne annuelle — Département 13",
            "°C",
        )
        fig_temp_dept = add_selected_year_marker(fig_temp_dept, selected_year)
        st.plotly_chart(fig_temp_dept, use_container_width=True)

    with col_b:
        fig_hot_days = build_line_chart(
            hero_plot_df,
            "year",
            "hot_days_over_30",
            f"Jours > 30°C — {hero_station_name}",
            "Nombre de jours",
        )
        fig_hot_days = add_selected_year_marker(fig_hot_days, selected_year)
        st.plotly_chart(fig_hot_days, use_container_width=True)

    st.markdown(
        """
        **Interprétation métier**  
        - La température moyenne annuelle renseigne sur la tendance thermique globale du territoire.  
        - Le nombre de jours > 30°C est un indicateur directement lié aux chaleurs fortes, aux canicules et au confort thermique urbain.  
        """
    )

    col_c, col_d = st.columns(2)

    with col_c:
        fig_precip_dept = build_line_chart(
            dept_plot_df,
            "year",
            "annual_precipitation_mm",
            "Précipitations annuelles — Département 13",
            "mm/an",
        )
        fig_precip_dept = add_selected_year_marker(fig_precip_dept, selected_year)
        st.plotly_chart(fig_precip_dept, use_container_width=True)

    with col_d:
        fig_dry_spell = build_line_chart(
            hero_plot_df,
            "year",
            "max_dry_spell_length",
            f"Séquence sèche max — {hero_station_name}",
            "Jours",
        )
        fig_dry_spell = add_selected_year_marker(fig_dry_spell, selected_year)
        st.plotly_chart(fig_dry_spell, use_container_width=True)

    st.markdown(
        """
        **Interprétation métier**  
        - Les précipitations annuelles donnent un signal utile sur la ressource en eau, mais doivent être lues avec prudence sur les longues périodes.  
        - La séquence sèche maximale est un indicateur narratif fort : plus elle s’allonge, plus la pression sur l’eau, la végétation et le risque incendie augmente.
        """
    )


# =========================================================
# TAB 2 - HISTORICAL
# =========================================================
with tabs[1]:
    st.markdown("## Historique observé")

    st.markdown(
        """
        <div class="warning-note">
        <b>Note méthodologique :</b> la série départementale est une série composite indicative calculée à partir des stations
        disponibles selon les années. Elle est utile pour la narration territoriale du dashboard, mais ne remplace pas une série homogénéisée officielle.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Focus station héroïne")

    col1, col2 = st.columns(2)

    with col1:
        fig_frost = build_line_chart(
            hero_plot_df,
            "year",
            "frost_days",
            f"Jours de gel — {hero_station_name}",
            "Nombre de jours",
        )
        st.plotly_chart(fig_frost, use_container_width=True)

    with col2:
        fig_rr_dept = build_line_chart(
            dept_plot_df,
            "year",
            "dry_days",
            "Nombre moyen de jours secs — Département 13",
            "Nombre de jours",
        )
        st.plotly_chart(fig_rr_dept, use_container_width=True)

    st.markdown("### Exploration journalière — Marseille")

    hero_daily_filtered = hero_daily[hero_daily["year"] == selected_year].copy()

    col3, col4 = st.columns(2)

    with col3:
        fig_daily_temp = build_daily_chart(
            hero_daily_filtered,
            "date",
            "tm_c",
            f"Température journalière — {hero_station_name} ({selected_year})",
            "°C",
        )
        st.plotly_chart(fig_daily_temp, use_container_width=True)

    with col4:
        fig_daily_rr = build_daily_chart(
            hero_daily_filtered,
            "date",
            "rr_mm",
            f"Précipitations journalières — {hero_station_name} ({selected_year})",
            "mm/jour",
        )
        st.plotly_chart(fig_daily_rr, use_container_width=True)

    st.markdown(
        """
        **Pourquoi cette vue compte**  
        Cette section permet de passer du signal agrégé à la réalité locale : on voit comment une année donnée
        se distribue concrètement en jours chauds, jours secs ou épisodes de pluie.
        """
    )


# =========================================================
# TAB 3 - PROJECTIONS
# =========================================================
with tabs[2]:
    st.markdown("## Projections futures")
    st.markdown("### Projection pilote DRIAS — RCP4.5 — 2031–2060")

    if drias_annual is None or drias_annual.empty:
        st.info(
            "La section projections est prête, mais le dataset DRIAS dashboard-ready n’est pas encore branché ici. "
            "Ajoute d’abord `drias_projection_pilot_v1.parquet` ou `drias_projection_pilot_v1.csv` dans `data/processed/climate/`."
        )

        st.markdown(
            """
            **Ce que cette section affichera ensuite :**
            - température projetée 2035 / 2050 / 2060  
            - précipitations projetées  
            - comparaison observé vs projeté  
            - message d’interprétation territoire  
            """
        )
    else:
        st.markdown(
            """
            <div class="section-note">
            Cette vue s’appuie sur une projection DRIAS pilote <b>RCP4.5</b>, sur la période <b>2031–2060</b>.
            Elle sert de première brique prospective avant l’intégration complète de plusieurs scénarios.
            </div>
            """,
            unsafe_allow_html=True,
        )

        p1, p2, p3 = st.columns(3)
        p1.metric(
            "Température projetée ~2035",
            fmt_number(projection_snapshot(drias_annual, 2035, "avg_annual_temperature_c"), 2, " °C"),
        )
        p2.metric(
            "Température projetée ~2050",
            fmt_number(projection_snapshot(drias_annual, 2050, "avg_annual_temperature_c"), 2, " °C"),
        )
        p3.metric(
            "Température projetée ~2060",
            fmt_number(projection_snapshot(drias_annual, 2060, "avg_annual_temperature_c"), 2, " °C"),
        )

        colp1, colp2 = st.columns(2)

        with colp1:
            fig_proj_temp = build_line_chart(
                drias_annual,
                "year",
                "avg_annual_temperature_c",
                "Projection DRIAS — température moyenne annuelle",
                "°C",
            )
            st.plotly_chart(fig_proj_temp, use_container_width=True)

        with colp2:
            fig_proj_rr = build_line_chart(
                drias_annual,
                "year",
                "annual_precipitation_mm",
                "Projection DRIAS — précipitations annuelles",
                "mm/an",
            )
            st.plotly_chart(fig_proj_rr, use_container_width=True)

        st.markdown(
            """
            **Interprétation prospective**  
            Cette projection pilote suggère une évolution progressive du climat futur entre 2031 et 2060.  
            Elle doit être lue comme un outil d’aide à la décision, et non comme une certitude absolue.
            """
        )

        st.markdown("### Comparaison observé vs projeté")

        st.markdown(
            """
            <div class="section-note">
            <b>Synthèse :</b> la projection DRIAS pilote RCP4.5 sur 2031–2060 suggère une évolution progressive
            des températures et une variabilité persistante des précipitations. La comparaison avec l’observé
            doit être lue comme une aide à la décision, pas comme une continuité strictement homogène.
            </div>
            """,
            unsafe_allow_html=True,
        )

        comparison_df = build_observed_vs_projected(
            dept_annual_main,
            drias_annual,
            observed_start_year=1991,
        )

        colc1, colc2 = st.columns(2)

        with colc1:
            fig_compare_temp = px.line(
                comparison_df,
                x="year",
                y="avg_annual_temperature_c",
                color="series",
                title="Comparaison indicative — température",
            )
            fig_compare_temp.update_layout(
                margin=dict(l=20, r=20, t=60, b=20),
                xaxis_title="Année",
                yaxis_title="°C",
                title_font_size=18,
            )
            fig_compare_temp.add_vline(
                x=LAST_COMPLETE_YEAR,
                line_width=2,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"Fin observé : {LAST_COMPLETE_YEAR}",
                annotation_position="top",
            )
            st.plotly_chart(fig_compare_temp, use_container_width=True)

        with colc2:
            fig_compare_rr = px.line(
                comparison_df,
                x="year",
                y="annual_precipitation_mm",
                color="series",
                title="Comparaison indicative — précipitations",
            )
            fig_compare_rr.update_layout(
                margin=dict(l=20, r=20, t=60, b=20),
                xaxis_title="Année",
                yaxis_title="mm/an",
                title_font_size=18,
            )
            fig_compare_rr.add_vline(
                x=LAST_COMPLETE_YEAR,
                line_width=2,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"Fin observé : {LAST_COMPLETE_YEAR}",
                annotation_position="top",
            )
            st.plotly_chart(fig_compare_rr, use_container_width=True)

        st.markdown(
            """
            <div class="warning-note">
            <b>Prudence de lecture :</b> la comparaison ci-dessus rapproche une série observée composite départementale
            et une projection DRIAS pilote agrégée. Elle est utile pour la narration et l’aide à la décision,
            mais ne constitue pas une comparaison climatologique homogénéisée parfaite.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# TAB 4 - ACTIONS
# =========================================================
with tabs[3]:
    st.markdown("## Actions recommandées")

    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        st.markdown("### Citoyens")
        st.markdown(
            """
            - Adapter le logement aux fortes chaleurs  
            - Réduire l’exposition en période de canicule  
            - Économiser l’eau au quotidien  
            - Végétaliser les abords du logement quand c’est possible  
            """
        )

    with col_a2:
        st.markdown("### Collectivités")
        st.markdown(
            """
            - Développer les îlots de fraîcheur  
            - Renforcer la gestion locale de l’eau  
            - Prioriser les zones les plus exposées à la chaleur  
            - Prévenir le risque incendie en zones sensibles  
            """
        )

    with col_a3:
        st.markdown("### Territoire")
        st.markdown(
            """
            - Suivre les indicateurs chaleur / sécheresse dans la durée  
            - Intégrer l’adaptation dans l’aménagement  
            - Anticiper les tensions sur les ressources en eau  
            - Faire converger climat, urbanisme et prévention des risques  
            """
        )

    st.markdown(
        """
        <div class="section-note">
        <b>Positionnement du projet :</b> ClimaScope-PACA ne se limite pas à montrer ce qui change.
        Il cherche à traduire ces changements en priorités d’action lisibles pour le territoire.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# TAB 5 - METHODO
# =========================================================
with tabs[4]:
    st.markdown("## Méthodologie")
    st.markdown(
        """
        ### Sources mobilisées
        - Météo-France / data.gouv : observations quotidiennes  
        - CITEPA : émissions sectorielles  
        - DRIAS : projections climatiques futures  

        ### Niveaux d’analyse
        - **Station héroïne** : Marseille-OBS  
        - **Territoire** : Bouches-du-Rhône (agrégation indicative)

        ### Indicateurs principaux
        - température moyenne annuelle  
        - précipitations annuelles  
        - jours > 30°C  
        - jours de gel  
        - séquence sèche maximale  

        ### Prudence d’interprétation
        Les séries très longues doivent être lues avec prudence, car la couverture stationnelle varie selon les périodes.
        """
    )

    st.markdown(
        f"""
        <div class="small-muted">
        Prototype Streamlit — {APP_TITLE}
        </div>
        """,
        unsafe_allow_html=True,
    )