import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="IN-SUFFERABLE", 
    page_icon="📈", 
    layout="centered"
)

# --- PERSONA DATA & UI THEMES ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖",
        "accent": "#a3cf62", # Tactical Green
        "bg": "#0d0f0a",
        "header": "MISSION BRIEFING",
        "desc": "Jocko Willink meets a Battalion CO.",
        "prompt": "You are 'The Commander.' You view life as a tactical operation. Use words like SOP, Mission-Critical, Time on Target, and Standards. Every sentence is its own line. Turn the user's story into a lesson about discipline and extreme ownership. End with 'Agree?' or 'HOOAH?'"
    },
    "The MD": {
        "icon": "💼",
        "accent": "#00ffcc", # Finance Cyan
        "bg": "#0a0b12",
        "header": "MARKET UPDATE: PORTFOLIO OPTIMIZATION",
        "desc": "High-energy Finance Bro in a Patagonia vest.",
        "prompt": "You are 'The MD.' You view life through ROI and Capital Allocation. Use words like Liquidity, Burn Rate, Portfolio Company, Scaling, and Alpha. Every sentence is its own line. Turn the user's story into a lesson about maximizing margins and cutting underperforming assets. End with 'What's your margin?'"
    },
    "The Chief People Officer": {
        "icon": "✨",
        "accent": "#ff99cc", # Soft Visionary Pink
        "bg": "#0f0d12",
        "header": "HUMAN-CENTRIC BRAND TOUCHPOINT",
        "desc": "Uses 'synergy' and 'impactful' while firing people.",
        "prompt": "You are 'The CPO.' You view life through optics and personal branding. Use words like Synergy, Alignment, Brand Touchpoint, Frictionless, and Pivot. Every sentence is its own line. Turn the user's story into a lesson about servant leadership and growth mindset. Use many sparkles. End with 'Agree? #Blessed'"
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"

current = PERSONAS[st.session_state.persona]

# --- DYNAMIC MOBILE-FIRST CSS ---
st.markdown(f"""
    <style>
    /* Global visibility fixes */
    .stApp {{ background-color: {current['bg']} !important; }}
    
    .stApp, p, span, div, li, label, .stMarkdown {{ 
        color: #FFFFFF !important; 
        font-family: 'Inter', -apple-system, sans-serif !important; 
    }}

    h1, h2, h3 {{ 
        color: {current['accent']} !important; 
        text-transform: uppercase; 
        text-align: center;
    }}

    /* The Persona Switcher Buttons */
    div.stButton > button {{
        width: 100%;
        border-radius: 4px;
        height: 3em;
        background-color: #1a1d14;
        color: white !important;
        border: 1px solid #333;
        font-size: 12px !important;
    }}

    /* Highlight the selected button */
    div.stButton > button:active, div.stButton > button:focus {{
        border: 2px solid {current['accent']} !important;
        color: {current['accent']} !important;
    }}

    /* Mission Box Styling */
    .mission-box {{
        background-color: #1a1d14;
        padding: 15px;
        border: 1px solid {current['accent']};
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    /* Chat Styling */
    [data-testid="stChatMessage"] {{
        background-color: #1a1d14 !important;
        border-left: 5px solid {current['accent']} !important;
    }}

    /* Hide the sidebar completely on mobile to avoid confusion */
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
else:
    st.error("❌ API KEY MISSING IN SECRETS.")
    st.stop()

# --- MAIN UI ---
st.title(f"{current['icon']} IN-SUFFERABLE")

# --- PERSONA TABS (The Mobile Fix) ---
st.write("### CHOOSE YOUR FLAVOR OF CRINGE:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪖 COMMANDER"):
        st.session_state.persona = "The Commander"
        st.rerun()
with col2:
    if st.button("💼 THE MD"):
        st.session_state.persona = "The MD"
        st.rerun()
with col3:
    if st.button("✨ THE CPO"):
        st.session_state.persona = "The Chief People Officer"
        st.rerun()

# --- MISSION BRIEFING ---
st.markdown(f"""
    <div class="mission-box">
        <h4 style="margin-top:0; color:{current['accent']} !important;">{current['header']}</h4>
        <p style="font-size: 0.9em; opacity: 0.8;">{current['desc']}</p>
        <p style="margin-bottom:0;">Turn your story into a {st.session_state.persona} post below.</p>
    </div>
    """, unsafe_allow_html=True)

# --- MODEL LOADING ---
@st.cache_resource
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available_models: return target
        return available_models[0]
    except: return None

model_name = get_working_model()

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Tell me your story..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_name=model_name, system_instruction=current['prompt'])
            response = model.generate_content(prompt)
            if response.text:
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.success(f"🫡 {st.session_state.persona.upper()} OUTPUT READY.")
            else:
                st.warning("REDACTED: Story blocked by safety filters.")
        except Exception as e:
            st.error(f"⚠️ COMMS ERROR: {str(e)}")
