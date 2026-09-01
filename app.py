import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go


# ============================================================
# Page configuration
# ============================================================
st.set_page_config(
    page_title="Purchasing Customer Prediction System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Global styling — Executive / Eye-catching dashboard
# ============================================================
st.markdown(
    """
    <style>
        /* ---------- Design tokens ---------- */
        :root {
            --bg: #070B14;
            --surface: #101827;
            --surface-2: #141F33;
            --surface-3: #19263D;
            --cyan: #22D3EE;
            --cyan-2: #06B6D4;
            --purple: #8B5CF6;
            --green: #34D399;
            --red: #FB7185;
            --white: #F8FAFC;
            --text: #CBD5E1;
            --muted: #7F8EA3;
            --line: rgba(148,163,184,.14);
        }

        /* ---------- App background ---------- */
        .stApp {
            background:
                radial-gradient(700px 360px at 100% 0%, rgba(139,92,246,.16), transparent 65%),
                radial-gradient(650px 420px at 0% 15%, rgba(34,211,238,.10), transparent 65%),
                var(--bg);
        }

        /* Streamlit application chrome */
        header[data-testid="stHeader"] {
            background: #0b1220 !important;
            border-bottom: 1px solid var(--line);
        }

        header[data-testid="stHeader"] [data-testid="stToolbar"] {
            background: transparent !important;
        }

        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] svg {
            color: #cbd5e1 !important;
        }

        .block-container {
            max-width: 1500px;
            padding: 1.7rem 2.2rem 2.2rem;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #09101D 0%, #0D1727 100%);
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] .block-container {
            padding: 1.6rem 1.1rem;
        }

        .side-brand {
            padding: .35rem .2rem 1.25rem;
            border-bottom: 1px solid var(--line);
            margin-bottom: 1.25rem;
        }

        .side-brand .logo {
            width: 42px;
            height: 42px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--cyan), var(--purple));
            font-size: 1.35rem;
            box-shadow: 0 10px 25px rgba(34,211,238,.18);
            margin-bottom: .55rem;
        }

        .side-brand h3 {
            margin: 0;
            color: white !important;
            font-size: 1rem;
        }

        .side-brand p {
            margin: .25rem 0 0;
            color: var(--muted);
            font-size: .74rem;
        }

        /* ---------- Hero ---------- */
        .hero {
            position: relative;
            overflow: hidden;
            min-height: 215px;
            padding: 2.35rem 2.6rem;
            border-radius: 26px;
            border: 1px solid rgba(148,163,184,.16);
            background:
                linear-gradient(115deg, rgba(13,24,42,.98), rgba(21,32,56,.94)),
                radial-gradient(circle at 90% 15%, rgba(34,211,238,.25), transparent 28%);
            box-shadow: 0 25px 70px rgba(0,0,0,.28);
            margin-bottom: 1.2rem;
        }

        .hero:before {
            content: "";
            position: absolute;
            width: 330px;
            height: 330px;
            right: -125px;
            top: -175px;
            border-radius: 50%;
            border: 1px solid rgba(34,211,238,.22);
            box-shadow:
                0 0 0 28px rgba(34,211,238,.035),
                0 0 0 58px rgba(139,92,246,.025);
        }

        .hero:after {
            content: "";
            position: absolute;
            width: 180px;
            height: 180px;
            right: 8%;
            bottom: -135px;
            border-radius: 50%;
            background: rgba(139,92,246,.12);
            filter: blur(8px);
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 900px;
        }

        .hero-stats {
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin-top: 1.2rem;
        }

        .hero-stat {
            display: inline-flex;
            align-items: center;
            gap: .42rem;
            padding: .42rem .7rem;
            border: 1px solid rgba(148,163,184,.18);
            border-radius: 10px;
            background: rgba(5,12,25,.22);
            color: #c9d8eb;
            font-size: .72rem;
            font-weight: 650;
        }

        .hero-stat strong {
            color: white;
            font-size: .76rem;
        }

        .hero-stat-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--cyan);
            box-shadow: 0 0 0 4px rgba(34,211,238,.12);
        }

        .hero-kicker {
            color: #67E8F9;
            font-size: .72rem;
            letter-spacing: .18em;
            font-weight: 850;
            text-transform: uppercase;
        }

        .hero h1 {
            color: white;
            font-size: 2.55rem;
            line-height: 1.08;
            font-weight: 900;
            letter-spacing: -.045em;
            margin: .55rem 0 .7rem;
        }

        .hero p {
            color: #AEBCCE;
            font-size: .96rem;
            line-height: 1.7;
            margin: 0;
            max-width: 820px;
        }

        .hero-badge {
            display: inline-flex;
            margin-top: 1.15rem;
            padding: .38rem .7rem;
            border-radius: 999px;
            background: rgba(34,211,238,.08);
            border: 1px solid rgba(34,211,238,.20);
            color: #A5F3FC;
            font-size: .72rem;
            font-weight: 750;
        }

        /* ---------- KPI cards ---------- */
        .kpi {
            position: relative;
            overflow: hidden;
            min-height: 105px;
            padding: 1.05rem 1.15rem;
            border-radius: 17px;
            border: 1px solid var(--line);
            background: linear-gradient(145deg, rgba(20,31,51,.96), rgba(13,22,37,.96));
            box-shadow: 0 14px 35px rgba(0,0,0,.14);
        }

        .kpi:after {
            content: "";
            position: absolute;
            width: 75px;
            height: 75px;
            right: -28px;
            top: -28px;
            border-radius: 50%;
            border: 1px solid rgba(34,211,238,.12);
        }

        .kpi-icon {
            font-size: 1.05rem;
            margin-bottom: .45rem;
        }

        .kpi-label {
            color: var(--muted);
            font-size: .68rem;
            font-weight: 800;
            letter-spacing: .12em;
        }

        .kpi-value {
            color: white;
            font-size: 1.18rem;
            font-weight: 850;
            margin-top: .25rem;
        }

        .kpi-detail {
            color: #64748B;
            font-size: .69rem;
            margin-top: .1rem;
        }

        /* ---------- Section headers ---------- */
        .section-head {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            margin: 1.35rem 0 .7rem;
        }

        .section-head h2 {
            color: white;
            font-size: 1.12rem;
            font-weight: 850;
            margin: 0;
            letter-spacing: -.02em;
        }

        .section-head p {
            color: var(--muted);
            font-size: .75rem;
            margin: .18rem 0 0;
        }

        .section-pill {
            color: #A5F3FC;
            border: 1px solid rgba(34,211,238,.18);
            background: rgba(34,211,238,.06);
            border-radius: 999px;
            padding: .28rem .55rem;
            font-size: .65rem;
            font-weight: 750;
        }

        /* ---------- Input panels ---------- */
        .panel {
            background: linear-gradient(145deg, rgba(16,24,39,.97), rgba(13,21,35,.97));
            border: 1px solid var(--line);
            border-radius: 19px;
            padding: 1.05rem 1.15rem .45rem;
            box-shadow: 0 12px 32px rgba(0,0,0,.13);
        }

        .panel-title {
            color: #F8FAFC;
            font-size: .92rem;
            font-weight: 820;
            margin-bottom: .75rem;
        }

        .panel-note {
            color: #6F8097;
            font-size: .72rem;
            line-height: 1.45;
            margin: -.45rem 0 .9rem;
        }

        /* ---------- Inputs ---------- */
        label[data-testid="stWidgetLabel"] p {
            color: #B9C6D7 !important;
            font-size: .76rem !important;
            font-weight: 650 !important;
        }

        div[data-baseweb="select"] > div,
        div[data-testid="stNumberInput"] > div > div {
            background: #0D1727 !important;
            border: 1px solid rgba(148,163,184,.16) !important;
            border-radius: 10px !important;
        }

        div[data-baseweb="select"] > div:focus-within,
        div[data-testid="stNumberInput"] > div > div:focus-within {
            border-color: rgba(34,211,238,.60) !important;
            box-shadow: 0 0 0 2px rgba(34,211,238,.08);
        }

        /* ---------- CTA ---------- */
        .cta-note {
            color: #7F8EA3;
            font-size: .74rem;
            text-align: center;
            margin: 1.15rem 0 .4rem;
        }

        .stButton > button {
            min-height: 3.15rem;
            border: 0 !important;
            border-radius: 13px !important;
            background: linear-gradient(100deg, #0891B2 0%, #22D3EE 50%, #8B5CF6 100%) !important;
            color: #06111D !important;
            font-size: 1rem !important;
            font-weight: 900 !important;
            letter-spacing: .01em;
            box-shadow: 0 14px 35px rgba(34,211,238,.18);
            transition: transform .18s ease, box-shadow .18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 42px rgba(34,211,238,.28);
        }

        /* ---------- Result ---------- */
        .result-wrap {
            border-radius: 21px;
            border: 1px solid var(--line);
            background: linear-gradient(145deg, rgba(16,24,39,.98), rgba(13,21,35,.98));
            padding: 1rem;
        }

        .result-positive, .result-negative {
            padding: 1.55rem 1.2rem;
            border-radius: 17px;
            text-align: center;
        }

        .result-positive {
            background: linear-gradient(135deg, rgba(6,78,59,.72), rgba(16,185,129,.13));
            border: 1px solid rgba(52,211,153,.20);
        }

        .result-negative {
            background: linear-gradient(135deg, rgba(127,29,29,.72), rgba(251,113,133,.12));
            border: 1px solid rgba(251,113,133,.20);
        }

        .result-positive h2, .result-negative h2 {
            color: white;
            font-size: 1.3rem;
            font-weight: 900;
            margin: 0 0 .3rem;
        }

        .result-positive p, .result-negative p {
            color: #B8C5D5;
            font-size: .8rem;
            margin: 0;
        }

        div[data-testid="stMetric"] {
            background: #0D1727;
            border: 1px solid var(--line);
            border-radius: 13px;
            padding: .7rem .8rem;
        }

        div[data-testid="stMetricLabel"] {
            color: #7F8EA3 !important;
            font-size: .7rem !important;
        }

        div[data-testid="stMetricValue"] {
            color: white !important;
            font-size: 1.35rem !important;
            font-weight: 850 !important;
        }

        /* ---------- Footer ---------- */
        .footer {
            text-align: center;
            color: #536277;
            font-size: .68rem;
            padding: .25rem 0 0;
        }

        @media (max-width: 900px) {
            /* Streamlit keeps the expanded sidebar as an overlay on narrow screens. */
            section[data-testid="stSidebar"] { display: none; }
            .block-container { padding: 1rem; }
            .hero { padding: 1.7rem; }
            .hero h1 { font-size: 1.9rem; }
            .hero-stats { margin-top: .95rem; }
            .hero-stat { font-size: .67rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Load trained model and encoder
# ============================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load("model.pkl")
    encoder = joblib.load("encoder.pkl")
    return model, encoder


try:
    model, encoder = load_artifacts()
except FileNotFoundError:
    st.error(
        "model.pkl or encoder.pkl was not found.\n\n"
        "Place both files in the same folder as app.py."
    )
    st.stop()


# ============================================================
# Hero header
# ============================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-kicker">AI • E-COMMERCE ANALYTICS</div>
            <h1>Turn browsing behavior into buying insight.</h1>
            <p>Build a clear conversion signal from each visitor session. Add browsing data, estimate purchase probability, and make your next decision with confidence.</p>
            <div class="hero-badge">● LIVE PREDICTION • DECISION TREE MODEL</div>
            <div class="hero-stats">
                <div class="hero-stat"><span class="hero-stat-dot"></span><strong>17 signals</strong> scored per visitor</div>
                <div class="hero-stat"><strong>35% threshold</strong> for purchase intent</div>
                <div class="hero-stat"><strong>Instant output</strong> probability + decision</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Executive overview
kpi_cols = st.columns(4)
kpi_data = [
    ("🧠", "MODEL", "Decision Tree", "Classification engine", "#22D3EE"),
    ("🎯", "THRESHOLD", "35%", "Purchase decision cutoff", "#A78BFA"),
    ("📊", "INPUT SIGNALS", "17", "Visitor behavior variables", "#54D9A8"),
    ("⚡", "OUTPUT", "Probability", "Revenue likelihood", "#F8C66D"),
]
for col, (icon, label, value, detail, accent) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(
            f'<div class="kpi" style="--accent:{accent}"><div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-detail">{detail}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <div class="logo">🛒</div>
            <h3>Customer Intelligence</h3>
            <p>Purchasing prediction workspace</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### ℹ️ About the Project")
    st.write(
        "This application uses the trained Decision Tree model "
        "from the project notebook to score online shoppers on their "
        "likelihood of completing a purchase."
    )
    st.divider()
    st.markdown("### ⚙️ Model Settings")
    st.metric("Classification Threshold", "0.35")
    st.caption(
        "Visitors with a predicted purchase probability at or above this "
        "threshold are classified as **likely to purchase**."
    )
    st.divider()
    st.markdown("### 🧭 How to use")
    st.write(
        "1. Fill in visit & browsing details\n"
        "2. Click **Predict Purchase**\n"
        "3. Review the probability & result"
    )


# ============================================================
# Input sections
# ============================================================
st.markdown(
    '<div class="section-head"><div><h2>👤 Customer & Visit</h2><p>Define the visitor profile and session context.</p></div><div class="section-pill">PROFILE</div></div><div class="panel"><div class="panel-title">Visitor context</div><div class="panel-note">These attributes describe who is browsing and when the visit takes place.</div>',
    unsafe_allow_html=True,
)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    visitor_type = st.selectbox(
        "Visitor Type",
        ["Returning_Visitor", "New_Visitor", "Other"],
    )

with info_col2:
    month = st.selectbox(
        "Month",
        ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    )

with info_col3:
    weekend = st.selectbox(
        "Weekend",
        [False, True],
        format_func=lambda x: "Yes" if x else "No",
    )

st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-head"><div><h2>📊 Browsing Behavior</h2><p>Capture engagement, page activity, and acquisition signals.</p></div><div class="section-pill">BEHAVIOR</div></div><div class="panel"><div class="panel-title">Session signals</div><div class="panel-note">Use the visitor’s observed browsing activity to estimate conversion intent.</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    administrative = st.number_input(
        "Administrative",
        min_value=0,
        value=0,
        step=1,
    )

    administrative_duration = st.number_input(
        "Administrative Duration",
        min_value=0.0,
        value=0.0,
        step=1.0,
    )

    informational = st.number_input(
        "Informational",
        min_value=0,
        value=0,
        step=1,
    )

    informational_duration = st.number_input(
        "Informational Duration",
        min_value=0.0,
        value=0.0,
        step=1.0,
    )

    product_related = st.number_input(
        "Product Related",
        min_value=0,
        value=0,
        step=1,
    )

with col2:
    product_related_duration = st.number_input(
        "Product Related Duration",
        min_value=0.0,
        value=0.0,
        step=1.0,
    )

    bounce_rates = st.number_input(
        "Bounce Rate",
        min_value=0.0,
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    exit_rates = st.number_input(
        "Exit Rate",
        min_value=0.0,
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    page_values = st.number_input(
        "Page Values",
        min_value=0.0,
        value=0.0,
        step=1.0,
    )

    special_day = st.number_input(
        "Special Day",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )

with col3:
    operating_systems = st.number_input(
        "Operating Systems",
        min_value=1,
        value=1,
        step=1,
    )

    browser = st.number_input(
        "Browser",
        min_value=1,
        value=1,
        step=1,
    )

    region = st.number_input(
        "Region",
        min_value=1,
        value=1,
        step=1,
    )

    traffic_type = st.number_input(
        "Traffic Type",
        min_value=1,
        value=1,
        step=1,
    )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Prediction
# ============================================================
st.markdown('<div class="cta-note">Ready to score this visitor? The model will compare the predicted probability with the 35% cutoff.</div>', unsafe_allow_html=True)
predict = st.button(
    "🔮 Predict Purchase",
    type="primary",
    use_container_width=True,
)


if predict:

    # --------------------------------------------------------
    # Create one-row input DataFrame
    # --------------------------------------------------------
    input_df = pd.DataFrame(
        {
            "Administrative": [administrative],
            "Administrative_Duration": [administrative_duration],
            "Informational": [informational],
            "Informational_Duration": [informational_duration],
            "ProductRelated": [product_related],
            "ProductRelated_Duration": [product_related_duration],
            "BounceRates": [bounce_rates],
            "ExitRates": [exit_rates],
            "PageValues": [page_values],
            "SpecialDay": [special_day],
            "Month": [month],
            "OperatingSystems": [operating_systems],
            "Browser": [browser],
            "Region": [region],
            "TrafficType": [traffic_type],
            "VisitorType": [visitor_type],
            "Weekend": [weekend],
        }
    )

    # --------------------------------------------------------
    # Encode categorical variables using the SAME fitted
    # encoder that was used during model training
    # --------------------------------------------------------
    categorical_cols = ["VisitorType", "Month"]

    encoded_array = encoder.transform(input_df[categorical_cols])
    encoded_cols = encoder.get_feature_names_out(categorical_cols)

    encoded_df = pd.DataFrame(
        encoded_array,
        columns=encoded_cols,
        index=input_df.index,
    )

    input_df = input_df.drop(columns=categorical_cols)

    input_df = pd.concat(
        [input_df, encoded_df],
        axis=1,
    )

    # --------------------------------------------------------
    # Make sure feature order exactly matches model training
    # --------------------------------------------------------
    if hasattr(model, "feature_names_in_"):
        expected_features = list(model.feature_names_in_)

        missing_features = [
            feature for feature in expected_features
            if feature not in input_df.columns
        ]

        if missing_features:
            st.error(
                "The input features do not match the trained model.\n\n"
                f"Missing features: {missing_features}"
            )
            st.stop()

        input_df = input_df.reindex(columns=expected_features)

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------
    probability = float(model.predict_proba(input_df)[0][1])

    # The project uses 0.35 as the classification threshold.
    threshold = 0.35
    prediction = probability >= threshold

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------
    st.write("")
    st.markdown(
        '<div class="section-head"><div><h2>🎯 Prediction Result</h2><p>Probability, classification, and decision threshold.</p></div><div class="section-pill">MODEL OUTPUT</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
    result_col1, result_col2 = st.columns([1, 1.2])

    with result_col1:
        if prediction:
            st.markdown(
                """
                <div class="result-positive">
                    <h2>🟢 Likely to Purchase</h2>
                    <p>The visitor is predicted to generate revenue.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="result-negative">
                    <h2>🔴 Unlikely to Purchase</h2>
                    <p>The visitor is predicted not to generate revenue.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        badge_col1, badge_col2 = st.columns(2)
        with badge_col1:
            st.metric("Purchase Probability", f"{probability:.2%}")
        with badge_col2:
            st.metric("Threshold", f"{threshold:.0%}")

    with result_col2:
        gauge_color = "#10b981" if prediction else "#f87171"
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                number={"suffix": "%", "font": {"size": 40, "color": "#f1f5f9"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                    "bar": {"color": gauge_color},
                    "bgcolor": "rgba(255,255,255,0.05)",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 35], "color": "rgba(248,113,113,0.25)"},
                        {"range": [35, 100], "color": "rgba(16,185,129,0.20)"},
                    ],
                    "threshold": {
                        "line": {"color": "#f1f5f9", "width": 3},
                        "thickness": 0.8,
                        "value": threshold * 100,
                    },
                },
            )
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#f1f5f9"},
            height=260,
            margin=dict(l=20, r=20, t=30, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Footer
# ============================================================
st.divider()
st.markdown('<div class="footer">PURCHASING CUSTOMER PREDICTION SYSTEM&nbsp;&nbsp;•&nbsp;&nbsp;DECISION TREE&nbsp;&nbsp;•&nbsp;&nbsp;CUSTOMER CONVERSION ANALYTICS</div>', unsafe_allow_html=True)
