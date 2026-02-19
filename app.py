import streamlit as st
import numpy as np
import pickle

st.set_page_config(
    page_title="WineIQ — Sommelier AI",
    page_icon="🍷",
    layout="centered"
)

@st.cache_resource
def load_model():
    model   = pickle.load(open('lg_wine.pkl', 'rb'))
    scaler  = pickle.load(open('scaler.pkl',  'rb'))
    columns = pickle.load(open('columns.pkl', 'rb'))
    return model, scaler, columns

model, scaler, columns = load_model()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,700&family=Jost:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --cream:   #F2EBE0;
    --cream2:  #E4D9CC;
    --cream3:  #C8BAA8;
    --burg:    #6B0F2B;
    --burg-dk: #4A0A1E;
    --burg-lt: #8B1535;
    --gold:    #B8923A;
    --gold-lt: #D4AF6A;
    --char:    #1C1C1C;
    --char2:   #2A2A2A;
    --text-dk: #1C0A0A;
    --text-lt: #8A6A6A;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main, .block-container {
    font-family: 'Jost', sans-serif !important;
    background: var(--cream) !important;
    color: var(--text-dk) !important;
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stSidebar"],
[data-testid="stDecoration"] { display: none !important; }

/* centered layout gives us the padding we need */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(160deg, var(--burg) 0%, var(--burg-dk) 100%);
    padding: 5rem 4rem 4.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-radius: 0 0 44px 44px;
    margin-left: -4rem;
    margin-right: -4rem;
    margin-bottom: 3.5rem;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(184,146,58,0.18) 0%, transparent 65%);
    pointer-events: none;
}
.hero-ornament {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.68rem;
    letter-spacing: 0.5rem;
    color: var(--gold-lt);
    text-transform: uppercase;
    opacity: 0.8;
    margin-bottom: 1.4rem;
    position: relative;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 6rem;
    font-weight: 700;
    font-style: italic;
    color: #fff;
    line-height: 1;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    position: relative;
}
.hero-rule {
    width: 60px; height: 1px;
    background: var(--gold);
    margin: 0 auto 1.2rem;
    opacity: 0.65;
    position: relative;
}
.hero-sub {
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 0.3rem;
    text-transform: uppercase;
    color: rgba(255,255,255,0.38);
    position: relative;
}

/* ── SECTION TITLES ── */
.sec-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-dk);
    margin-bottom: 0.4rem;
}
.sec-rule {
    width: 34px; height: 2px;
    background: var(--gold);
    margin-bottom: 2rem;
}

/* ── GROUP LABELS ── */
.glabel {
    font-size: 0.57rem;
    font-weight: 600;
    letter-spacing: 0.35rem;
    text-transform: uppercase;
    color: var(--text-lt);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
}
.glabel::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--cream3);
}

/* ── INPUTS ── */
[data-testid="stNumberInput"] label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.58rem !important;
    font-weight: 500 !important;
    color: var(--text-lt) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.13rem !important;
    margin-bottom: 0.3rem !important;
}
[data-testid="stNumberInput"] input {
    background: var(--char) !important;
    border: 1.5px solid #2E2E2E !important;
    border-radius: 9px !important;
    color: #F0E8DC !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    padding: 0.62rem 0.85rem !important;
    transition: border-color 0.2s !important;
    width: 100% !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(184,146,58,0.12) !important;
    outline: none !important;
}
/* Align the input + stepper button wrapper */
[data-testid="stNumberInput"] > div {
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
}

[data-testid="stNumberInput"] [data-testid="stNumberInputStepperButton"],
[data-testid="stNumberInput"] button {
    background: var(--char2) !important;
    border: 1.5px solid #2E2E2E !important;
    border-radius: 7px !important;
    color: rgba(240,232,220,0.4) !important;
    font-size: 0.9rem !important;
    transition: all 0.15s !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    max-height: 32px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    align-self: center !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    line-height: 1 !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--burg) !important;
    border-color: var(--burg) !important;
    color: white !important;
}
/* ── SEPARATOR between + and - buttons ── */
[data-testid="stNumberInput"] > div > div:last-child {
    display: flex !important;
    flex-direction: column !important;
    gap: 0 !important;
    border: 1.5px solid #2E2E2E !important;
    border-radius: 7px !important;
    overflow: hidden !important;
}
[data-testid="stNumberInput"] > div > div:last-child button {
    border: none !important;
    border-radius: 0 !important;
}
[data-testid="stNumberInput"] > div > div:last-child button:first-child {
    border-bottom: 1px solid #3E3E3E !important;
}

/* ── PREDICT BUTTON ── */
[data-testid="stButton"] > button {
    background: var(--burg) !important;
    color: #F2EBE0 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.32rem !important;
    text-transform: uppercase !important;
    padding: 1.1rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 18px rgba(107,15,43,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--burg-lt) !important;
    box-shadow: 0 8px 26px rgba(107,15,43,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── RESULT ── */
.res-wrap { animation: fadeUp 0.45s ease; margin-top: 1.8rem; }
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.res-good {
    background: linear-gradient(155deg, #0B2516, #0E3020);
    border: 1px solid rgba(82,183,136,0.3);
    border-radius: 14px;
    padding: 2.4rem 2rem;
    text-align: center;
}
.res-avg {
    background: linear-gradient(155deg, var(--burg-dk), var(--burg));
    border: 1px solid rgba(184,146,58,0.3);
    border-radius: 14px;
    padding: 2.4rem 2rem;
    text-align: center;
}
.res-tag {
    font-size: 0.56rem; letter-spacing: 0.38rem;
    text-transform: uppercase; color: rgba(255,255,255,0.28);
    margin-bottom: 1.2rem; font-family: 'Jost', sans-serif;
}
.res-verdict {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.3rem; font-weight: 700; font-style: italic;
    color: white; line-height: 1.2; margin-bottom: 1.3rem;
}
.res-hr { width: 34px; height: 1px; margin: 0 auto 1.3rem; }
.res-score {
    font-family: 'Cormorant Garamond', serif;
    font-size: 4rem; font-weight: 700;
    color: white; line-height: 1; margin-bottom: 0.2rem;
}
.res-slbl {
    font-size: 0.55rem; letter-spacing: 0.3rem;
    text-transform: uppercase; color: rgba(255,255,255,0.28);
    font-family: 'Jost', sans-serif; margin-bottom: 1.5rem;
}
.res-bar {
    height: 2px; background: rgba(255,255,255,0.08);
    border-radius: 100px; overflow: hidden; margin-bottom: 1.5rem;
}
.bar-green { height:100%; background: linear-gradient(90deg,#2D6A4F,#52B788); border-radius:100px; }
.bar-gold  { height:100%; background: linear-gradient(90deg,var(--gold),var(--gold-lt)); border-radius:100px; }
.res-desc {
    font-size: 0.76rem; color: rgba(255,255,255,0.33);
    line-height: 1.75; font-family: 'Jost', sans-serif;
}

/* ── COLUMN DIVIDER ── */
.col-divider {
    width: 1px;
    background: var(--cream2);
    align-self: stretch;
    margin: 0 1rem;
}

/* ── SUGGESTIONS ── */
.sug-wrap {
    margin-top: 2.5rem;
    animation: fadeUp 0.5s ease 0.15s both;
}
.sug-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.sug-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-dk);
}
.sug-rule-h {
    flex: 1;
    height: 1px;
    background: var(--cream2);
}
.sug-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.85rem;
}
.sug-card {
    background: white;
    border: 1px solid var(--cream2);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    transition: box-shadow 0.2s, transform 0.2s;
}
.sug-card:hover {
    box-shadow: 0 6px 24px rgba(107,15,43,0.07);
    transform: translateY(-2px);
}
.sug-card.good {
    border-left: 3px solid #52B788;
}
.sug-card.warn {
    border-left: 3px solid var(--gold);
}
.sug-card.bad {
    border-left: 3px solid var(--burg);
}
.sug-icon {
    font-size: 1.1rem;
    margin-top: 0.05rem;
    flex-shrink: 0;
}
.sug-body {}
.sug-param {
    font-size: 0.55rem;
    font-weight: 600;
    letter-spacing: 0.22rem;
    text-transform: uppercase;
    color: var(--text-lt);
    margin-bottom: 0.2rem;
}
.sug-text {
    font-size: 0.78rem;
    color: var(--text-dk);
    line-height: 1.55;
}
.sug-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--burg);
}
.sug-none {
    text-align: center;
    padding: 2rem;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: var(--text-lt);
    background: white;
    border: 1px solid var(--cream2);
    border-radius: 12px;
    border-left: 3px solid #52B788;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    border-top: 1px solid var(--cream2);
    margin-top: 3rem;
}
.footer-text {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic; font-size: 0.88rem;
    color: var(--text-lt);
}
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-ornament">✦ &nbsp; Sommelier Intelligence &nbsp; ✦</div>
  <div class="hero-title">WineIQ</div>
  <div class="hero-rule"></div>
  <div class="hero-sub">The art of vintage meets the precision of data</div>
</div>
""", unsafe_allow_html=True)

# ── TWO COLUMNS ───────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="sec-title">Chemical Analysis</div><div class="sec-rule"></div>', unsafe_allow_html=True)

    st.markdown('<div class="glabel">Acidity</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: fixed_acidity    = st.number_input("Fixed Acidity",    min_value=0.0, max_value=20.0,  value=7.4,   step=0.1)
    with c2: volatile_acidity = st.number_input("Volatile Acidity", min_value=0.0, max_value=2.0,   value=0.50,  step=0.01)
    with c3: citric_acid      = st.number_input("Citric Acid",      min_value=0.0, max_value=2.0,   value=0.27,  step=0.01)

    st.markdown('<br><div class="glabel">Composition</div>', unsafe_allow_html=True)
    c4, c5, c6, c7 = st.columns(4)
    with c4: residual_sugar       = st.number_input("Residual Sugar", min_value=0.0, max_value=20.0,  value=2.1,   step=0.1)
    with c5: chlorides            = st.number_input("Chlorides",       min_value=0.0, max_value=1.0,   value=0.080, step=0.001, format="%.3f")
    with c6: free_sulfur_dioxide  = st.number_input("Free SO₂",       min_value=0.0, max_value=100.0, value=17.0,  step=1.0)
    with c7: total_sulfur_dioxide = st.number_input("Total SO₂",      min_value=0.0, max_value=400.0, value=34.0,  step=1.0)

    st.markdown('<br><div class="glabel">Properties</div>', unsafe_allow_html=True)
    c8, c9, c10, c11 = st.columns(4)
    with c8:  density   = st.number_input("Density",   min_value=0.990, max_value=1.010, value=0.9978, step=0.0001, format="%.4f")
    with c9:  pH        = st.number_input("pH",         min_value=2.0,   max_value=5.0,   value=3.50,   step=0.01)
    with c10: sulphates = st.number_input("Sulphates",  min_value=0.0,   max_value=2.0,   value=0.56,   step=0.01)
    with c11: alcohol   = st.number_input("Alcohol %",  min_value=8.0,   max_value=15.0,  value=9.4,    step=0.1)

with right:
    st.markdown('<div class="sec-title">Prediction Verdict</div><div class="sec-rule"></div>', unsafe_allow_html=True)

    predict = st.button("Analyse Vintage", use_container_width=True)

    if predict:
        features = np.array([[
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
            chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
            density, pH, sulphates, alcohol
        ]])
        fs    = scaler.transform(features)
        pred  = model.predict(fs)[0]
        proba = model.predict_proba(fs)[0]
        gp    = round(proba[1] * 100, 1)
        ap    = round(proba[0] * 100, 1)

        # Store results in session state so suggestions section can access them
        st.session_state["result"] = {
            "pred": pred, "gp": gp, "ap": ap,
            "volatile_acidity": volatile_acidity,
            "alcohol": alcohol, "sulphates": sulphates,
            "citric_acid": citric_acid,
            "total_sulfur_dioxide": total_sulfur_dioxide,
            "pH": pH,
        }

    if "result" in st.session_state:
        r = st.session_state["result"]
        if r["pred"] == 1:
            st.markdown(f"""
            <div class="res-wrap">
              <div class="res-good">
                <div class="res-tag">✦ &nbsp; Quality Assessment &nbsp; ✦</div>
                <div class="res-verdict">Good Quality<br>Wine</div>
                <div class="res-hr" style="background:rgba(82,183,136,0.4);"></div>
                <div class="res-score">{r["gp"]}%</div>
                <div class="res-slbl">Confidence</div>
                <div class="res-bar"><div class="bar-green" style="width:{r["gp"]}%"></div></div>
                <div class="res-desc">A balanced profile — strong alcohol, refined acidity and optimal sulphates reflect a premium vintage.</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="res-wrap">
              <div class="res-avg">
                <div class="res-tag">✦ &nbsp; Quality Assessment &nbsp; ✦</div>
                <div class="res-verdict">Average Quality<br>Wine</div>
                <div class="res-hr" style="background:rgba(184,146,58,0.4);"></div>
                <div class="res-score">{r["ap"]}%</div>
                <div class="res-slbl">Confidence</div>
                <div class="res-bar"><div class="bar-gold" style="width:{r["ap"]}%"></div></div>
                <div class="res-desc">Consider reducing volatile acidity and elevating alcohol content to improve this wine's quality profile.</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── SUGGESTIONS ──────────────────────────────────────────────────────────────
def val(v, decimals=2):
    """Format a float value for display."""
    return f"{v:.{decimals}f}".rstrip('0').rstrip('.')

def sug_card(status, icon, param, text):
    return (
        f'<div class="sug-card {status}">'
        f'<div class="sug-icon">{icon}</div>'
        f'<div class="sug-body">'
        f'<div class="sug-param">{param}</div>'
        f'<div class="sug-text">{text}</div>'
        f'</div></div>'
    )

def highlight(v):
    return f'<span class="sug-value">{v}</span>'

if "result" in st.session_state:
    r   = st.session_state["result"]
    va  = r["volatile_acidity"]
    alc = r["alcohol"]
    sul = r["sulphates"]
    ca  = r["citric_acid"]
    so2 = r["total_sulfur_dioxide"]
    ph  = r["pH"]

    cards = []

    # Volatile Acidity
    if va > 0.6:
        cards.append(sug_card("bad", "⚗️", "Volatile Acidity",
            f"At {highlight(val(va))}, this is high. Reduce below {highlight('0.4')} "
            "to eliminate vinegary notes and sharpen the palate."))
    elif va > 0.4:
        cards.append(sug_card("warn", "⚗️", "Volatile Acidity",
            f"At {highlight(val(va))}, this is slightly elevated. "
            f"Aim below {highlight('0.4')} for a cleaner, more refined finish."))
    else:
        cards.append(sug_card("good", "⚗️", "Volatile Acidity",
            f"Excellent at {highlight(val(va))}. "
            "Well within the premium range — no intervention needed."))

    # Alcohol
    if alc < 9.5:
        cards.append(sug_card("bad", "🍾", "Alcohol %",
            f"At {highlight(val(alc) + '%')}, alcohol is too low. "
            f"Target above {highlight('10.5%')} for better body, warmth, and quality."))
    elif alc < 10.5:
        cards.append(sug_card("warn", "🍾", "Alcohol %",
            f"At {highlight(val(alc) + '%')}, alcohol is slightly low. "
            f"Increasing toward {highlight('11–13%')} would improve structure and mouthfeel."))
    else:
        cards.append(sug_card("good", "🍾", "Alcohol %",
            f"At {highlight(val(alc) + '%')}, alcohol is in the premium zone. "
            "This contributes positively to body and complexity."))

    # Sulphates
    if sul < 0.5:
        cards.append(sug_card("bad", "🧪", "Sulphates",
            f"Value of {highlight(val(sul))} is low. "
            f"Increase to {highlight('0.6–0.9')} to enhance antimicrobial stability and fruitiness."))
    elif sul > 1.0:
        cards.append(sug_card("warn", "🧪", "Sulphates",
            f"At {highlight(val(sul))}, sulphates are slightly high. "
            f"Keep below {highlight('1.0')} to avoid harsh, bitter aftertastes."))
    else:
        cards.append(sug_card("good", "🧪", "Sulphates",
            f"Sulphate level of {highlight(val(sul))} is optimal. "
            "This supports freshness and antimicrobial balance perfectly."))

    # Citric Acid
    if ca < 0.2:
        cards.append(sug_card("warn", "🍋", "Citric Acid",
            f"At {highlight(val(ca))}, citric acid is low. "
            f"Increase to {highlight('0.25–0.5')} to add freshness and brightness."))
    elif ca > 0.6:
        cards.append(sug_card("warn", "🍋", "Citric Acid",
            f"At {highlight(val(ca))}, citric acid is slightly high. "
            f"Reduce toward {highlight('0.5')} to avoid an overly tart profile."))
    else:
        cards.append(sug_card("good", "🍋", "Citric Acid",
            f"Citric acid at {highlight(val(ca))} adds ideal freshness. "
            "Bright, clean notes characteristic of premium wines."))

    # Total SO2
    if so2 > 200:
        cards.append(sug_card("bad", "💨", "Total SO₂",
            f"At {highlight(str(int(so2)) + ' mg/L')}, SO₂ is very high. "
            f"Reduce below {highlight('150 mg/L')} to prevent sulphur off-aromas."))
    elif so2 > 150:
        cards.append(sug_card("warn", "💨", "Total SO₂",
            f"At {highlight(str(int(so2)) + ' mg/L')}, SO₂ is slightly elevated. "
            f"Target below {highlight('150 mg/L')} to improve aromatic purity."))
    else:
        cards.append(sug_card("good", "💨", "Total SO₂",
            f"Total SO₂ of {highlight(str(int(so2)) + ' mg/L')} is well-managed. "
            "Freshness is preserved without compromising aromatics."))

    # pH
    if ph < 3.1:
        cards.append(sug_card("warn", "⚖️", "pH Balance",
            f"pH of {highlight(val(ph))} is too low (overly acidic). "
            f"Aim for {highlight('3.2–3.5')} for a more balanced, approachable palate."))
    elif ph > 3.7:
        cards.append(sug_card("warn", "⚖️", "pH Balance",
            f"pH of {highlight(val(ph))} is too high. "
            f"Lower toward {highlight('3.2–3.5')} to improve microbial stability."))
    else:
        cards.append(sug_card("good", "⚖️", "pH Balance",
            f"pH of {highlight(val(ph))} is in the ideal range. "
            "Proper microbial stability and a well-balanced acid profile."))

    cards_html = "\n".join(cards)

    st.markdown(
        f'<div class="sug-wrap">'
        f'<div class="sug-header">'
        f'<div class="sug-title">Winemaker\'s Suggestions</div>'
        f'<div class="sug-rule-h"></div>'
        f'</div>'
        f'<div class="sug-grid">{cards_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-text">WineIQ &nbsp;·&nbsp; Extra Trees Classifier &nbsp;·&nbsp; 78.60% Accuracy</div>
</div>
""", unsafe_allow_html=True)