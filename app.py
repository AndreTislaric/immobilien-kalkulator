import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import math
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Immobilien-Kalkulator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Apple-Style CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%);
    border-right: 1px solid #E5E5EA;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Cards */
.apple-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    border: 1px solid #E5E5EA;
    transition: box-shadow 0.3s ease;
}

.apple-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
}

.apple-card-accent {
    background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    color: white;
    box-shadow: 0 4px 16px rgba(0,122,255,0.3);
}

/* Metric Cards */
.metric-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    border: 1px solid #E5E5EA;
    margin-bottom: 12px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #1D1D1F;
    margin: 4px 0;
    letter-spacing: -0.5px;
}

.metric-label {
    font-size: 13px;
    font-weight: 500;
    color: #86868B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-sublabel {
    font-size: 12px;
    color: #86868B;
    margin-top: 4px;
}

/* Blue metric */
.metric-blue .metric-value { color: #007AFF; }
/* Green metric */
.metric-green .metric-value { color: #34C759; }
/* Orange metric */
.metric-orange .metric-value { color: #FF9500; }
/* Red metric */
.metric-red .metric-value { color: #FF3B30; }
/* Purple metric */
.metric-purple .metric-value { color: #5856D6; }

/* Section Headers */
.section-header {
    font-size: 22px;
    font-weight: 600;
    color: #1D1D1F;
    margin: 24px 0 16px 0;
    letter-spacing: -0.3px;
}

.section-subheader {
    font-size: 15px;
    color: #86868B;
    margin-top: -12px;
    margin-bottom: 16px;
}

/* Hero */
.hero-title {
    font-size: 34px;
    font-weight: 700;
    background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 17px;
    color: #86868B;
    margin-bottom: 24px;
    font-weight: 400;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    background: #F5F5F7;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #E5E5EA;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 500;
    font-size: 14px;
}

.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1px solid #D2D2D7 !important;
    font-family: 'Inter', sans-serif !important;
}

.stSlider > div > div > div {
    background: #007AFF !important;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    padding: 8px 24px;
    transition: all 0.2s ease;
    border: none;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,122,255,0.3);
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600;
    font-size: 15px;
    border-radius: 12px;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #E5E5EA;
    margin: 24px 0;
}

/* Saved calc pills */
.saved-pill {
    display: inline-block;
    background: #F5F5F7;
    border-radius: 20px;
    padding: 6px 16px;
    margin: 4px;
    font-size: 13px;
    font-weight: 500;
    color: #1D1D1F;
    border: 1px solid #E5E5EA;
    cursor: pointer;
}

.saved-pill:hover {
    background: #007AFF;
    color: white;
    border-color: #007AFF;
}

/* Info box */
.info-box {
    background: #EDF4FF;
    border-radius: 12px;
    padding: 16px;
    border-left: 4px solid #007AFF;
    margin: 12px 0;
    font-size: 14px;
    color: #1D1D1F;
}

/* Warning box */
.warning-box {
    background: #FFF8E6;
    border-radius: 12px;
    padding: 16px;
    border-left: 4px solid #FF9500;
    margin: 12px 0;
    font-size: 14px;
    color: #1D1D1F;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Nebenkosten nach Bundesland
# ─────────────────────────────────────────────
BUNDESLAENDER = {
    "Baden-Württemberg": {"grunderwerbsteuer": 5.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Bayern": {"grunderwerbsteuer": 3.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Berlin": {"grunderwerbsteuer": 6.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Brandenburg": {"grunderwerbsteuer": 6.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Bremen": {"grunderwerbsteuer": 5.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Hamburg": {"grunderwerbsteuer": 5.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Hessen": {"grunderwerbsteuer": 6.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Mecklenburg-Vorpommern": {"grunderwerbsteuer": 6.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Niedersachsen": {"grunderwerbsteuer": 5.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Nordrhein-Westfalen": {"grunderwerbsteuer": 6.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Rheinland-Pfalz": {"grunderwerbsteuer": 5.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Saarland": {"grunderwerbsteuer": 6.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Sachsen": {"grunderwerbsteuer": 5.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Sachsen-Anhalt": {"grunderwerbsteuer": 5.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Schleswig-Holstein": {"grunderwerbsteuer": 6.5, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
    "Thüringen": {"grunderwerbsteuer": 5.0, "notar": 1.5, "grundbuch": 0.5, "makler_kaeufer": 3.57},
}

# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "saved_calculations" not in st.session_state:
    st.session_state.saved_calculations = {}
if "loaded_calc" not in st.session_state:
    st.session_state.loaded_calc = None


# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────
def fmt_eur(val):
    """Format as Euro currency."""
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(val):
    return f"{val:.2f} %".replace(".", ",")


def calculate_nebenkosten(kaufpreis, bundesland, mit_makler=True):
    """Calculate Nebenkosten based on Bundesland."""
    bl = BUNDESLAENDER[bundesland]
    grunderwerbsteuer = kaufpreis * bl["grunderwerbsteuer"] / 100
    notar = kaufpreis * bl["notar"] / 100
    grundbuch = kaufpreis * bl["grundbuch"] / 100
    makler = kaufpreis * bl["makler_kaeufer"] / 100 if mit_makler else 0
    gesamt = grunderwerbsteuer + notar + grundbuch + makler
    return {
        "grunderwerbsteuer": grunderwerbsteuer,
        "grunderwerbsteuer_pct": bl["grunderwerbsteuer"],
        "notar": notar,
        "notar_pct": bl["notar"],
        "grundbuch": grundbuch,
        "grundbuch_pct": bl["grundbuch"],
        "makler": makler,
        "makler_pct": bl["makler_kaeufer"] if mit_makler else 0,
        "gesamt": gesamt,
        "gesamt_pct": bl["grunderwerbsteuer"] + bl["notar"] + bl["grundbuch"] + (bl["makler_kaeufer"] if mit_makler else 0),
    }


def calculate_annuity(darlehenssumme, zinssatz_pa, anfangstilgung_pa=None, monatliche_rate=None,
                       laufzeit_jahre=None, sondertilgung_pa=0, zinsbindung_jahre=None,
                       anschlusszins=None, startdatum=None):
    """
    Flexible annuity calculator.
    Provide either:
      - anfangstilgung_pa → computes monthly rate
      - monatliche_rate → computes effective tilgung
      - laufzeit_jahre → computes rate for exact payoff
    """
    if darlehenssumme <= 0:
        return None

    zins_monat = zinssatz_pa / 100 / 12

    # Determine monthly rate
    if monatliche_rate is not None and monatliche_rate > 0:
        rate = monatliche_rate
    elif anfangstilgung_pa is not None:
        rate = darlehenssumme * (zinssatz_pa / 100 + anfangstilgung_pa / 100) / 12
    elif laufzeit_jahre is not None and laufzeit_jahre > 0:
        n = laufzeit_jahre * 12
        if zins_monat > 0:
            rate = darlehenssumme * zins_monat * (1 + zins_monat)**n / ((1 + zins_monat)**n - 1)
        else:
            rate = darlehenssumme / n
    else:
        return None

    # Minimum check: rate must cover at least interest
    min_rate = darlehenssumme * zins_monat
    if rate <= min_rate:
        return {"error": "rate_too_low", "min_rate": min_rate}

    if startdatum is None:
        startdatum = date.today().replace(day=1) + relativedelta(months=1)

    # Build amortization schedule
    restschuld = darlehenssumme
    schedule = []
    total_zinsen = 0
    total_tilgung = 0
    monat = 0
    max_monate = 600  # 50 years cap
    current_zins_monat = zins_monat
    sondertilgung_monat = sondertilgung_pa / 12

    while restschuld > 0.01 and monat < max_monate:
        # Check for Zinsbindung end → switch to Anschlusszins
        if zinsbindung_jahre and anschlusszins and monat == zinsbindung_jahre * 12:
            current_zins_monat = anschlusszins / 100 / 12

        zinsanteil = restschuld * current_zins_monat
        tilgungsanteil = rate - zinsanteil

        # Add Sondertilgung
        effektive_sondertilgung = min(sondertilgung_monat, restschuld - tilgungsanteil) if sondertilgung_monat > 0 else 0
        if effektive_sondertilgung < 0:
            effektive_sondertilgung = 0

        tilgungsanteil_gesamt = tilgungsanteil + effektive_sondertilgung

        # Last payment adjustment
        if tilgungsanteil_gesamt >= restschuld:
            tilgungsanteil_gesamt = restschuld
            effektive_rate = zinsanteil + restschuld
        else:
            effektive_rate = rate + effektive_sondertilgung

        restschuld_neu = restschuld - tilgungsanteil_gesamt
        total_zinsen += zinsanteil
        total_tilgung += tilgungsanteil_gesamt
        monat += 1

        current_date = startdatum + relativedelta(months=monat - 1)

        schedule.append({
            "Monat": monat,
            "Datum": current_date,
            "Jahr": current_date.year,
            "Rate": effektive_rate,
            "Zinsanteil": zinsanteil,
            "Tilgungsanteil": tilgungsanteil,
            "Sondertilgung": effektive_sondertilgung,
            "Tilgung gesamt": tilgungsanteil_gesamt,
            "Restschuld": max(restschuld_neu, 0),
        })

        restschuld = max(restschuld_neu, 0)

    laufzeit_eff = monat / 12

    # Restschuld at Zinsbindung end
    restschuld_zinsbindung = None
    if zinsbindung_jahre and len(schedule) >= zinsbindung_jahre * 12:
        restschuld_zinsbindung = schedule[zinsbindung_jahre * 12 - 1]["Restschuld"]

    # Yearly aggregation
    df = pd.DataFrame(schedule)
    yearly = df.groupby("Jahr").agg(
        Zinsen=("Zinsanteil", "sum"),
        Tilgung=("Tilgung gesamt", "sum"),
        Sondertilgung=("Sondertilgung", "sum"),
        Restschuld=("Restschuld", "last"),
    ).reset_index()

    return {
        "darlehenssumme": darlehenssumme,
        "monatliche_rate": rate,
        "zinssatz": zinssatz_pa,
        "laufzeit_monate": monat,
        "laufzeit_jahre": laufzeit_eff,
        "total_zinsen": total_zinsen,
        "total_tilgung": total_tilgung,
        "total_kosten": total_zinsen + darlehenssumme,
        "restschuld_zinsbindung": restschuld_zinsbindung,
        "schedule": schedule,
        "yearly": yearly,
    }


def max_darlehen_from_rate(monatliche_rate, zinssatz_pa, laufzeit_jahre):
    """Reverse calculation: max loan from monthly rate."""
    zins_monat = zinssatz_pa / 100 / 12
    n = laufzeit_jahre * 12
    if zins_monat > 0:
        return monatliche_rate * ((1 + zins_monat)**n - 1) / (zins_monat * (1 + zins_monat)**n)
    else:
        return monatliche_rate * n


def render_metric(label, value, sublabel="", color_class=""):
    """Render a styled metric card."""
    return f"""
    <div class="metric-card {color_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sublabel">{sublabel}</div>
    </div>
    """


def render_plotly_theme(fig):
    """Apply Apple-style theme to plotly figure."""
    fig.update_layout(
        font_family="Inter, -apple-system, sans-serif",
        font_color="#1D1D1F",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E5E5EA",
            borderwidth=1,
            font=dict(size=12),
        ),
        xaxis=dict(gridcolor="#F0F0F0", zerolinecolor="#E5E5EA"),
        yaxis=dict(gridcolor="#F0F0F0", zerolinecolor="#E5E5EA"),
    )
    return fig


# ─────────────────────────────────────────────
# App Header
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">Immobilien-Kalkulator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Berechne, vergleiche und plane deinen Wohnungskauf — übersichtlich und interaktiv.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar: Saved Calculations
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💾 Gespeicherte Kalkulationen")

    if st.session_state.saved_calculations:
        calc_names = list(st.session_state.saved_calculations.keys())
        selected_calc = st.selectbox("Kalkulation laden", ["— Auswählen —"] + calc_names, key="load_select")

        col_load, col_del = st.columns(2)
        with col_load:
            if st.button("📂 Laden", use_container_width=True):
                if selected_calc != "— Auswählen —":
                    st.session_state.loaded_calc = st.session_state.saved_calculations[selected_calc]
                    st.rerun()
        with col_del:
            if st.button("🗑️ Löschen", use_container_width=True):
                if selected_calc != "— Auswählen —":
                    del st.session_state.saved_calculations[selected_calc]
                    st.rerun()

        st.markdown("---")
        for name, calc in st.session_state.saved_calculations.items():
            with st.expander(f"📋 {name}"):
                st.caption(f"Kaufpreis: {fmt_eur(calc.get('kaufpreis', 0))}")
                st.caption(f"Darlehen: {fmt_eur(calc.get('darlehenssumme', 0))}")
                st.caption(f"Rate: {fmt_eur(calc.get('monatliche_rate', 0))}")
                st.caption(f"Gespeichert: {calc.get('timestamp', '-')}")
    else:
        st.info("Noch keine Kalkulationen gespeichert.")

    st.markdown("---")

    # Export/Import
    st.markdown("### 📤 Export / Import")
    if st.session_state.saved_calculations:
        export_data = json.dumps(st.session_state.saved_calculations, default=str, indent=2, ensure_ascii=False)
        st.download_button(
            "⬇️ Alle exportieren (JSON)",
            data=export_data,
            file_name="kalkulationen.json",
            mime="application/json",
            use_container_width=True,
        )

    uploaded_file = st.file_uploader("JSON importieren", type="json", key="import_file")
    if uploaded_file:
        try:
            imported = json.loads(uploaded_file.read())
            st.session_state.saved_calculations.update(imported)
            st.success(f"{len(imported)} Kalkulation(en) importiert!")
            st.rerun()
        except Exception as e:
            st.error(f"Import fehlgeschlagen: {e}")


# ─────────────────────────────────────────────
# Main Tabs
# ─────────────────────────────────────────────
tab_calc, tab_reverse, tab_compare, tab_nk = st.tabs([
    "🏠 Kalkulation", "🔄 Rückwärtsrechnung", "📊 Vergleich", "💰 Nebenkosten"
])

# ═══════════════════════════════════════════════
# TAB 1: Main Calculator
# ═══════════════════════════════════════════════
with tab_calc:
    # Load saved values if present
    lc = st.session_state.loaded_calc or {}

    st.markdown('<div class="section-header">Grunddaten</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        kaufpreis = st.number_input(
            "Kaufpreis (€)", min_value=0, max_value=10_000_000,
            value=int(lc.get("kaufpreis", 350_000)), step=5_000,
            help="Kaufpreis der Immobilie", key="kp"
        )
        eigenkapital = st.number_input(
            "Eigenkapital (€)", min_value=0, max_value=10_000_000,
            value=int(lc.get("eigenkapital", 70_000)), step=5_000,
            help="Verfügbares Eigenkapital", key="ek"
        )
        bundesland = st.selectbox(
            "Bundesland", list(BUNDESLAENDER.keys()),
            index=list(BUNDESLAENDER.keys()).index(lc.get("bundesland", "Baden-Württemberg")),
            key="bl"
        )

    with col2:
        mit_makler = st.toggle("Makler einbeziehen", value=lc.get("mit_makler", True), key="makler_toggle")

        nk = calculate_nebenkosten(kaufpreis, bundesland, mit_makler)
        nebenkosten_custom = st.number_input(
            "Kaufnebenkosten (€)", min_value=0,
            value=int(lc.get("nebenkosten", int(nk["gesamt"]))), step=1_000,
            help=f"Automatisch berechnet: {fmt_eur(nk['gesamt'])} ({fmt_pct(nk['gesamt_pct'])})",
            key="nk_input"
        )

        gesamtkosten = kaufpreis + nebenkosten_custom
        darlehenssumme_auto = max(gesamtkosten - eigenkapital, 0)
        beleihung_pct = (darlehenssumme_auto / kaufpreis * 100) if kaufpreis > 0 else 0

    # Show Nebenkosten breakdown
    with st.expander("📋 Nebenkosten-Aufstellung"):
        nk_cols = st.columns(4)
        with nk_cols[0]:
            st.metric("Grunderwerbsteuer", fmt_eur(nk["grunderwerbsteuer"]), f"{fmt_pct(nk['grunderwerbsteuer_pct'])}")
        with nk_cols[1]:
            st.metric("Notar", fmt_eur(nk["notar"]), f"{fmt_pct(nk['notar_pct'])}")
        with nk_cols[2]:
            st.metric("Grundbuch", fmt_eur(nk["grundbuch"]), f"{fmt_pct(nk['grundbuch_pct'])}")
        with nk_cols[3]:
            st.metric("Makler", fmt_eur(nk["makler"]), f"{fmt_pct(nk['makler_pct'])}")

    st.markdown("---")

    # Financing Overview
    overview_cols = st.columns(3)
    with overview_cols[0]:
        st.markdown(render_metric("Gesamtkosten", fmt_eur(gesamtkosten), "Kaufpreis + Nebenkosten"), unsafe_allow_html=True)
    with overview_cols[1]:
        st.markdown(render_metric("Darlehenssumme", fmt_eur(darlehenssumme_auto),
                                   f"Beleihung: {beleihung_pct:.0f}%", "metric-blue"), unsafe_allow_html=True)
    with overview_cols[2]:
        ek_pct = (eigenkapital / gesamtkosten * 100) if gesamtkosten > 0 else 0
        color = "metric-green" if ek_pct >= 20 else "metric-orange" if ek_pct >= 10 else "metric-red"
        st.markdown(render_metric("EK-Quote", fmt_pct(ek_pct), f"{fmt_eur(eigenkapital)} Eigenkapital", color), unsafe_allow_html=True)

    if beleihung_pct > 100:
        st.markdown('<div class="warning-box">⚠️ <strong>Achtung:</strong> Die Beleihung übersteigt 100% des Kaufpreises. Du finanzierst auch die Nebenkosten mit. Das führt zu höheren Zinsen.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Finanzierung</div>', unsafe_allow_html=True)

    calc_mode = st.radio(
        "Berechnungsmodus",
        ["📐 Tilgungssatz vorgeben", "💶 Monatliche Rate vorgeben", "📅 Laufzeit vorgeben"],
        horizontal=True, key="calc_mode",
        index=["📐 Tilgungssatz vorgeben", "💶 Monatliche Rate vorgeben", "📅 Laufzeit vorgeben"].index(
            lc.get("calc_mode", "📐 Tilgungssatz vorgeben")
        ) if lc.get("calc_mode") in ["📐 Tilgungssatz vorgeben", "💶 Monatliche Rate vorgeben", "📅 Laufzeit vorgeben"] else 0
    )

    fin_col1, fin_col2 = st.columns(2)

    with fin_col1:
        zinssatz = st.number_input(
            "Sollzins p.a. (%)", min_value=0.0, max_value=15.0,
            value=float(lc.get("zinssatz", 3.5)), step=0.1, format="%.2f",
            key="zins"
        )
        darlehenssumme = st.number_input(
            "Darlehenssumme (€)", min_value=0, max_value=10_000_000,
            value=int(lc.get("darlehenssumme", int(darlehenssumme_auto))), step=5_000,
            key="darlehen"
        )

    with fin_col2:
        if "Tilgungssatz" in calc_mode:
            anfangstilgung = st.number_input(
                "Anfängliche Tilgung p.a. (%)", min_value=0.5, max_value=15.0,
                value=float(lc.get("anfangstilgung", 2.0)), step=0.1, format="%.2f",
                key="tilgung"
            )
        elif "Rate" in calc_mode:
            monatliche_rate_input = st.number_input(
                "Monatliche Rate (€)", min_value=100, max_value=50_000,
                value=int(lc.get("monatliche_rate_input", 1500)), step=50,
                key="rate_input"
            )
        else:  # Laufzeit
            laufzeit_input = st.number_input(
                "Gewünschte Laufzeit (Jahre)", min_value=1, max_value=50,
                value=int(lc.get("laufzeit_input", 25)), step=1,
                key="laufzeit_input"
            )

    # Advanced options
    with st.expander("⚙️ Erweiterte Optionen"):
        adv_col1, adv_col2 = st.columns(2)
        with adv_col1:
            sondertilgung = st.number_input(
                "Jährliche Sondertilgung (€)", min_value=0, max_value=500_000,
                value=int(lc.get("sondertilgung", 0)), step=1_000,
                key="sonder"
            )
            zinsbindung = st.number_input(
                "Zinsbindung (Jahre)", min_value=1, max_value=30,
                value=int(lc.get("zinsbindung", 10)), step=1,
                key="zinsbind"
            )
        with adv_col2:
            anschlusszins = st.number_input(
                "Anschlusszins nach Bindung (%)", min_value=0.0, max_value=15.0,
                value=float(lc.get("anschlusszins", 4.5)), step=0.1, format="%.2f",
                key="anschlusszins"
            )
            startdatum = st.date_input(
                "Startdatum der Finanzierung",
                value=date.today().replace(day=1) + relativedelta(months=1),
                key="startdatum"
            )

    # ─── Run Calculation ───
    if "Tilgungssatz" in calc_mode:
        result = calculate_annuity(
            darlehenssumme, zinssatz, anfangstilgung_pa=anfangstilgung,
            sondertilgung_pa=sondertilgung, zinsbindung_jahre=zinsbindung,
            anschlusszins=anschlusszins, startdatum=startdatum
        )
    elif "Rate" in calc_mode:
        result = calculate_annuity(
            darlehenssumme, zinssatz, monatliche_rate=monatliche_rate_input,
            sondertilgung_pa=sondertilgung, zinsbindung_jahre=zinsbindung,
            anschlusszins=anschlusszins, startdatum=startdatum
        )
    else:
        result = calculate_annuity(
            darlehenssumme, zinssatz, laufzeit_jahre=laufzeit_input,
            sondertilgung_pa=sondertilgung, zinsbindung_jahre=zinsbindung,
            anschlusszins=anschlusszins, startdatum=startdatum
        )

    if result is None:
        st.warning("Bitte Eingabewerte prüfen.")
    elif isinstance(result, dict) and result.get("error") == "rate_too_low":
        st.error(f"Die monatliche Rate muss mindestens {fmt_eur(result['min_rate'])} betragen, um die Zinsen zu decken.")
    else:
        st.markdown("---")
        st.markdown('<div class="section-header">Ergebnis</div>', unsafe_allow_html=True)

        # Key Results
        res_cols = st.columns(4)
        with res_cols[0]:
            st.markdown(render_metric("Monatliche Rate", fmt_eur(result["monatliche_rate"]),
                                       f"inkl. {fmt_eur(sondertilgung/12)} Sondertilgung/Monat" if sondertilgung else "",
                                       "metric-blue"), unsafe_allow_html=True)
        with res_cols[1]:
            st.markdown(render_metric("Laufzeit", f'{result["laufzeit_jahre"]:.1f} Jahre',
                                       f'{result["laufzeit_monate"]} Monate', "metric-purple"), unsafe_allow_html=True)
        with res_cols[2]:
            st.markdown(render_metric("Gezahlte Zinsen", fmt_eur(result["total_zinsen"]),
                                       f'{result["total_zinsen"]/darlehenssumme*100:.1f}% des Darlehens' if darlehenssumme > 0 else "",
                                       "metric-orange"), unsafe_allow_html=True)
        with res_cols[3]:
            st.markdown(render_metric("Gesamtkosten", fmt_eur(result["total_kosten"]),
                                       "Darlehen + Zinsen", "metric-red"), unsafe_allow_html=True)

        # Zinsbindung info
        if result["restschuld_zinsbindung"] is not None:
            st.markdown(f'<div class="info-box">📌 <strong>Restschuld nach {zinsbindung} Jahren Zinsbindung:</strong> {fmt_eur(result["restschuld_zinsbindung"])} — danach Anschlusszins {fmt_pct(anschlusszins)}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ─── Charts ───
        st.markdown('<div class="section-header">Visualisierungen</div>', unsafe_allow_html=True)

        chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
            "📈 Restschuld", "📊 Zins/Tilgung", "🍩 Kostenverteilung", "📋 Tilgungsplan"
        ])

        yearly = result["yearly"]

        with chart_tab1:
            fig_rest = go.Figure()
            fig_rest.add_trace(go.Scatter(
                x=yearly["Jahr"], y=yearly["Restschuld"],
                fill="tozeroy",
                fillcolor="rgba(0,122,255,0.1)",
                line=dict(color="#007AFF", width=3),
                name="Restschuld",
                hovertemplate="%{x}<br>Restschuld: %{y:,.0f} €<extra></extra>"
            ))
            if zinsbindung:
                zb_year = startdatum.year + zinsbindung
                fig_rest.add_vline(x=zb_year, line_dash="dash", line_color="#FF9500",
                                    annotation_text=f"Ende Zinsbindung ({zinsbindung}J)")
            fig_rest.update_layout(title="Restschuld über die Laufzeit",
                                    xaxis_title="Jahr", yaxis_title="Restschuld (€)",
                                    yaxis_tickformat=",", height=400)
            render_plotly_theme(fig_rest)
            st.plotly_chart(fig_rest, use_container_width=True)

        with chart_tab2:
            fig_zt = go.Figure()
            fig_zt.add_trace(go.Bar(
                x=yearly["Jahr"], y=yearly["Zinsen"],
                name="Zinsen", marker_color="#FF9500",
                hovertemplate="%{x}<br>Zinsen: %{y:,.0f} €<extra></extra>"
            ))
            fig_zt.add_trace(go.Bar(
                x=yearly["Jahr"], y=yearly["Tilgung"],
                name="Tilgung", marker_color="#007AFF",
                hovertemplate="%{x}<br>Tilgung: %{y:,.0f} €<extra></extra>"
            ))
            if sondertilgung > 0:
                fig_zt.add_trace(go.Bar(
                    x=yearly["Jahr"], y=yearly["Sondertilgung"],
                    name="Sondertilgung", marker_color="#34C759",
                    hovertemplate="%{x}<br>Sondertilgung: %{y:,.0f} €<extra></extra>"
                ))
            fig_zt.update_layout(title="Jährliche Zins- und Tilgungsanteile",
                                  barmode="stack", xaxis_title="Jahr",
                                  yaxis_title="Betrag (€)", yaxis_tickformat=",", height=400)
            render_plotly_theme(fig_zt)
            st.plotly_chart(fig_zt, use_container_width=True)

        with chart_tab3:
            labels = ["Darlehenssumme", "Gezahlte Zinsen"]
            values = [darlehenssumme, result["total_zinsen"]]
            if nebenkosten_custom > 0:
                labels.append("Kaufnebenkosten")
                values.append(nebenkosten_custom)

            fig_pie = go.Figure(go.Pie(
                labels=labels, values=values,
                hole=0.55,
                marker=dict(colors=["#007AFF", "#FF9500", "#5856D6"]),
                textinfo="label+percent",
                textfont=dict(size=13),
                hovertemplate="%{label}<br>%{value:,.0f} €<br>%{percent}<extra></extra>"
            ))
            fig_pie.update_layout(title="Gesamtkostenverteilung", height=400,
                                   annotations=[dict(text=f'<b>{fmt_eur(sum(values))}</b><br>Gesamt',
                                                      x=0.5, y=0.5, font_size=16, showarrow=False)])
            render_plotly_theme(fig_pie)
            st.plotly_chart(fig_pie, use_container_width=True)

        with chart_tab4:
            schedule_df = pd.DataFrame(result["schedule"])
            schedule_display = schedule_df.copy()
            schedule_display["Datum"] = schedule_display["Datum"].apply(lambda d: d.strftime("%m/%Y"))
            for col in ["Rate", "Zinsanteil", "Tilgungsanteil", "Sondertilgung", "Tilgung gesamt", "Restschuld"]:
                schedule_display[col] = schedule_display[col].apply(lambda x: f"{x:,.2f} €")

            st.dataframe(
                schedule_display[["Monat", "Datum", "Rate", "Zinsanteil", "Tilgungsanteil", "Sondertilgung", "Restschuld"]],
                use_container_width=True, height=400,
                hide_index=True,
            )

            csv = schedule_df.to_csv(index=False, sep=";", decimal=",")
            st.download_button("⬇️ Tilgungsplan als CSV", data=csv, file_name="tilgungsplan.csv",
                                mime="text/csv")

        # ─── Save Calculation ───
        st.markdown("---")
        st.markdown('<div class="section-header">Kalkulation speichern</div>', unsafe_allow_html=True)
        save_col1, save_col2 = st.columns([3, 1])
        with save_col1:
            save_name = st.text_input("Titel der Kalkulation", placeholder="z.B. 3-Zimmer München Schwabing",
                                       key="save_name")
        with save_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Speichern", use_container_width=True, type="primary"):
                if save_name:
                    st.session_state.saved_calculations[save_name] = {
                        "kaufpreis": kaufpreis,
                        "eigenkapital": eigenkapital,
                        "bundesland": bundesland,
                        "mit_makler": mit_makler,
                        "nebenkosten": nebenkosten_custom,
                        "darlehenssumme": darlehenssumme,
                        "zinssatz": zinssatz,
                        "calc_mode": calc_mode,
                        "anfangstilgung": anfangstilgung if "Tilgungssatz" in calc_mode else None,
                        "monatliche_rate_input": monatliche_rate_input if "Rate" in calc_mode else None,
                        "laufzeit_input": laufzeit_input if "Laufzeit" in calc_mode else None,
                        "sondertilgung": sondertilgung,
                        "zinsbindung": zinsbindung,
                        "anschlusszins": anschlusszins,
                        "monatliche_rate": result["monatliche_rate"],
                        "laufzeit_jahre": result["laufzeit_jahre"],
                        "total_zinsen": result["total_zinsen"],
                        "total_kosten": result["total_kosten"],
                        "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    }
                    st.success(f"✅ Kalkulation \"{save_name}\" gespeichert!")
                    st.rerun()
                else:
                    st.warning("Bitte einen Titel eingeben.")

    # Clear loaded calc
    if st.session_state.loaded_calc:
        st.session_state.loaded_calc = None


# ═══════════════════════════════════════════════
# TAB 2: Reverse Calculation
# ═══════════════════════════════════════════════
with tab_reverse:
    st.markdown('<div class="section-header">Rückwärtsrechnung</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Wie viel Immobilie kannst du dir leisten?</div>', unsafe_allow_html=True)

    rev_col1, rev_col2 = st.columns(2)
    with rev_col1:
        rev_budget = st.number_input(
            "Monatliches Budget für Kreditrate (€)", min_value=100, max_value=50_000,
            value=1_500, step=50, key="rev_budget"
        )
        rev_ek = st.number_input(
            "Verfügbares Eigenkapital (€)", min_value=0, max_value=5_000_000,
            value=80_000, step=5_000, key="rev_ek"
        )
    with rev_col2:
        rev_zins = st.number_input(
            "Erwarteter Zinssatz (%)", min_value=0.1, max_value=15.0,
            value=3.5, step=0.1, format="%.2f", key="rev_zins"
        )
        rev_laufzeit = st.number_input(
            "Gewünschte Laufzeit (Jahre)", min_value=5, max_value=50,
            value=25, step=1, key="rev_laufzeit"
        )
        rev_bl = st.selectbox("Bundesland", list(BUNDESLAENDER.keys()), key="rev_bl")

    rev_makler = st.toggle("Mit Makler", value=True, key="rev_makler")

    max_darl = max_darlehen_from_rate(rev_budget, rev_zins, rev_laufzeit)

    rev_nk_pct = BUNDESLAENDER[rev_bl]["grunderwerbsteuer"] + BUNDESLAENDER[rev_bl]["notar"] + BUNDESLAENDER[rev_bl]["grundbuch"]
    if rev_makler:
        rev_nk_pct += BUNDESLAENDER[rev_bl]["makler_kaeufer"]

    # Max Kaufpreis = (Eigenkapital + Darlehen) / (1 + NK%)
    max_kaufpreis = (rev_ek + max_darl) / (1 + rev_nk_pct / 100)
    rev_nk_betrag = max_kaufpreis * rev_nk_pct / 100

    st.markdown("---")

    rev_res_cols = st.columns(4)
    with rev_res_cols[0]:
        st.markdown(render_metric("Max. Kaufpreis", fmt_eur(max_kaufpreis), "", "metric-blue"), unsafe_allow_html=True)
    with rev_res_cols[1]:
        st.markdown(render_metric("Max. Darlehen", fmt_eur(max_darl), "", "metric-purple"), unsafe_allow_html=True)
    with rev_res_cols[2]:
        st.markdown(render_metric("Nebenkosten", fmt_eur(rev_nk_betrag), f"{fmt_pct(rev_nk_pct)}", "metric-orange"), unsafe_allow_html=True)
    with rev_res_cols[3]:
        rev_result = calculate_annuity(max_darl, rev_zins, monatliche_rate=rev_budget)
        if rev_result and not isinstance(rev_result, dict):
            st.markdown(render_metric("Gesamtzinsen", fmt_eur(rev_result["total_zinsen"]), "", "metric-red"), unsafe_allow_html=True)

    # Budget sensitivity
    st.markdown("---")
    st.markdown('<div class="section-header">Budgetsensitivität</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Wie verändert sich dein max. Kaufpreis mit der Rate?</div>', unsafe_allow_html=True)

    rates = list(range(max(500, rev_budget - 500), rev_budget + 600, 100))
    max_prices = []
    for r in rates:
        d = max_darlehen_from_rate(r, rev_zins, rev_laufzeit)
        mp = (rev_ek + d) / (1 + rev_nk_pct / 100)
        max_prices.append(mp)

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Bar(
        x=[f"{r:,}€" for r in rates], y=max_prices,
        marker_color=["#007AFF" if r == rev_budget else "#D1D1D6" for r in rates],
        hovertemplate="Rate: %{x}<br>Max. Kaufpreis: %{y:,.0f} €<extra></extra>"
    ))
    fig_sens.update_layout(title="Maximaler Kaufpreis nach monatlicher Rate",
                            xaxis_title="Monatliche Rate", yaxis_title="Max. Kaufpreis (€)",
                            yaxis_tickformat=",", height=400)
    render_plotly_theme(fig_sens)
    st.plotly_chart(fig_sens, use_container_width=True)

    # Zinssensitivität
    st.markdown('<div class="section-header">Zinssensitivität</div>', unsafe_allow_html=True)

    zins_range = [round(x * 0.5, 1) for x in range(max(1, int((rev_zins - 2) * 2)), int((rev_zins + 3) * 2) + 1)]
    zins_prices = []
    for z in zins_range:
        d = max_darlehen_from_rate(rev_budget, z, rev_laufzeit)
        mp = (rev_ek + d) / (1 + rev_nk_pct / 100)
        zins_prices.append(mp)

    fig_zins = go.Figure()
    fig_zins.add_trace(go.Scatter(
        x=zins_range, y=zins_prices,
        mode="lines+markers",
        line=dict(color="#FF9500", width=3),
        marker=dict(size=8, color=["#FF3B30" if z == rev_zins else "#FF9500" for z in zins_range]),
        hovertemplate="Zinssatz: %{x:.1f}%<br>Max. Kaufpreis: %{y:,.0f} €<extra></extra>"
    ))
    fig_zins.update_layout(title="Maximaler Kaufpreis nach Zinssatz",
                            xaxis_title="Zinssatz p.a. (%)", yaxis_title="Max. Kaufpreis (€)",
                            yaxis_tickformat=",", height=400)
    render_plotly_theme(fig_zins)
    st.plotly_chart(fig_zins, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 3: Comparison
# ═══════════════════════════════════════════════
with tab_compare:
    st.markdown('<div class="section-header">Szenario-Vergleich</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Vergleiche gespeicherte oder neue Szenarien direkt nebeneinander.</div>', unsafe_allow_html=True)

    if len(st.session_state.saved_calculations) < 1:
        st.info("Speichere mindestens eine Kalkulation im Hauptrechner, um Szenarien vergleichen zu können.")
    else:
        saved_names = list(st.session_state.saved_calculations.keys())
        selected_for_compare = st.multiselect(
            "Kalkulationen zum Vergleich auswählen", saved_names,
            default=saved_names[:min(3, len(saved_names))],
            key="compare_select"
        )

        if selected_for_compare:
            compare_data = {name: st.session_state.saved_calculations[name] for name in selected_for_compare}

            # Comparison table
            comp_rows = []
            for name, calc in compare_data.items():
                comp_rows.append({
                    "Szenario": name,
                    "Kaufpreis": fmt_eur(calc.get("kaufpreis", 0)),
                    "Eigenkapital": fmt_eur(calc.get("eigenkapital", 0)),
                    "Darlehen": fmt_eur(calc.get("darlehenssumme", 0)),
                    "Zinssatz": fmt_pct(calc.get("zinssatz", 0)),
                    "Monatl. Rate": fmt_eur(calc.get("monatliche_rate", 0)),
                    "Laufzeit": f'{calc.get("laufzeit_jahre", 0):.1f} J.',
                    "Gesamtzinsen": fmt_eur(calc.get("total_zinsen", 0)),
                    "Gesamtkosten": fmt_eur(calc.get("total_kosten", 0)),
                })

            st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)

            # Comparison charts
            st.markdown("---")

            names = list(compare_data.keys())
            colors = ["#007AFF", "#FF9500", "#34C759", "#5856D6", "#FF3B30"]

            # Monthly rate comparison
            fig_comp_rate = go.Figure()
            fig_comp_rate.add_trace(go.Bar(
                x=names,
                y=[compare_data[n].get("monatliche_rate", 0) for n in names],
                marker_color=colors[:len(names)],
                text=[fmt_eur(compare_data[n].get("monatliche_rate", 0)) for n in names],
                textposition="outside",
            ))
            fig_comp_rate.update_layout(title="Monatliche Rate im Vergleich", yaxis_title="€/Monat",
                                         yaxis_tickformat=",", height=400)
            render_plotly_theme(fig_comp_rate)
            st.plotly_chart(fig_comp_rate, use_container_width=True)

            # Total cost comparison
            fig_comp_cost = go.Figure()
            for i, name in enumerate(names):
                calc = compare_data[name]
                fig_comp_cost.add_trace(go.Bar(
                    x=[name], y=[calc.get("darlehenssumme", 0)],
                    name="Darlehen" if i == 0 else None,
                    marker_color="#007AFF", showlegend=(i == 0),
                    legendgroup="darlehen",
                ))
                fig_comp_cost.add_trace(go.Bar(
                    x=[name], y=[calc.get("total_zinsen", 0)],
                    name="Zinsen" if i == 0 else None,
                    marker_color="#FF9500", showlegend=(i == 0),
                    legendgroup="zinsen",
                ))
            fig_comp_cost.update_layout(title="Gesamtkosten: Darlehen vs. Zinsen",
                                         barmode="stack", yaxis_title="€",
                                         yaxis_tickformat=",", height=400)
            render_plotly_theme(fig_comp_cost)
            st.plotly_chart(fig_comp_cost, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 4: Nebenkosten Calculator
# ═══════════════════════════════════════════════
with tab_nk:
    st.markdown('<div class="section-header">Kaufnebenkosten-Rechner</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Berechne die Nebenkosten für jedes Bundesland.</div>', unsafe_allow_html=True)

    nk_col1, nk_col2 = st.columns(2)
    with nk_col1:
        nk_kaufpreis = st.number_input("Kaufpreis (€)", min_value=0, value=350_000, step=5_000, key="nk_kp")
    with nk_col2:
        nk_mit_makler = st.toggle("Mit Makler", value=True, key="nk_makler")

    # Table for all Bundesländer
    nk_rows = []
    for bl_name in BUNDESLAENDER:
        nk_data = calculate_nebenkosten(nk_kaufpreis, bl_name, nk_mit_makler)
        nk_rows.append({
            "Bundesland": bl_name,
            "GrErwSt": fmt_pct(nk_data["grunderwerbsteuer_pct"]),
            "GrErwSt (€)": fmt_eur(nk_data["grunderwerbsteuer"]),
            "Notar (€)": fmt_eur(nk_data["notar"]),
            "Grundbuch (€)": fmt_eur(nk_data["grundbuch"]),
            "Makler (€)": fmt_eur(nk_data["makler"]),
            "Gesamt (€)": fmt_eur(nk_data["gesamt"]),
            "Gesamt (%)": fmt_pct(nk_data["gesamt_pct"]),
            "_gesamt_val": nk_data["gesamt"],
        })

    nk_df = pd.DataFrame(nk_rows)

    st.dataframe(
        nk_df.drop(columns=["_gesamt_val"]),
        use_container_width=True, hide_index=True, height=600
    )

    # Chart
    fig_nk = go.Figure()
    nk_df_sorted = nk_df.sort_values("_gesamt_val")
    fig_nk.add_trace(go.Bar(
        y=nk_df_sorted["Bundesland"],
        x=nk_df_sorted["_gesamt_val"],
        orientation="h",
        marker_color=["#007AFF" if v == nk_df_sorted["_gesamt_val"].min()
                       else "#FF3B30" if v == nk_df_sorted["_gesamt_val"].max()
                       else "#D1D1D6" for v in nk_df_sorted["_gesamt_val"]],
        hovertemplate="%{y}<br>Nebenkosten: %{x:,.0f} €<extra></extra>"
    ))
    fig_nk.update_layout(title="Kaufnebenkosten nach Bundesland",
                          xaxis_title="Nebenkosten (€)", xaxis_tickformat=",",
                          height=500, margin=dict(l=180))
    render_plotly_theme(fig_nk)
    st.plotly_chart(fig_nk, use_container_width=True)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #86868B; font-size: 13px; padding: 16px;">
    Immobilien-Kalkulator · Alle Berechnungen ohne Gewähr · Keine Finanzberatung
</div>
""", unsafe_allow_html=True)
