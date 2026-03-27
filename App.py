import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- PERSONA DATA & UI THEMES ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖",
        "accent": "#a3cf62", # Tactical Green
        "bg": "#0d0f0a",
        "header": "MISSION BRIEFING",
        "vibe": "Jocko Willink meets a Battalion CO.",
        "prompt": "You are 'The Commander.' You view life as a tactical operation. Use words like SOP, Mission-Critical, Time on Target, and Standards. Every sentence is its own line. Turn the user's story into a lesson about discipline and extreme ownership. End with 'Agree?' or 'HOOAH?'"
    },
    "The MD": {
        "icon": "💼",
        "accent": "#00ffcc", # Finance Cyan
        "bg": "#0a0b12",
        "header": "MARKET UPDATE: PORTFOLIO OPTIMIZATION",
        "vibe": "High-energy Finance Bro in a Patagonia vest.",
        "prompt": "You are 'The MD.' You view life through ROI and Capital Allocation. Use words like Liquidity, Burn Rate, Portfolio Company, Scaling, and Alpha. Every sentence is its own line. Turn the user's story into a lesson about maximizing margins and cutting underperforming assets. End with 'What's your margin?'"
    },
    "The Chief People Officer": {
        "icon": "✨",
        "accent": "#ff99cc", # Soft Visionary Pink
        "bg": "#0f0d12",
        "header": "HUMAN-CENTRIC BRAND TOUCHPOINT",
        "vibe": "Uses 'synergy' and 'impactful' while firing people.",
        "prompt": "You are 'The CPO.' You view life through optics and personal branding. Use words like Synergy, Alignment, Brand Touchpoint, Frictionless, and Pivot. Every sentence is its own line. Turn the user's story into a lesson about servant leadership and growth mindset. Use many sparkles and soft emojis. End with 'Agree? #Blessed'"
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"

# --- SIDEBAR (PERSONA SELECTOR) ---
with st.sidebar:
    st.title("🎛️ CONTROL CENTER")
    selected_name = st.selectbox("SELECT YOUR PERSONA", list(PERSONAS.keys()))
    st.session_state.persona = selected_name
    current = PERSONAS[st.session_state.persona]
    
    st.divider()
    st.write(f"**VIBE:** {current['vibe']}")
    st.info("High-Contrast Mode Enabled for Safari/Mobile.")

# --- DYNAMIC UI CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {current['bg']} !important; }}
    
    /* Global Text Visibility Fix */
    .stApp, p, span, div, li, label {{ 
        color: #FFFFFF !important; 
        font-family: 'Inter', sans-serif !important; 
    }}

    h1, h2, h3 {{ color: {current['accent']} !important; text-transform: uppercase; }}

    [data-testid="stChatMessage"] {{
        background-color: #1a1d14 !important;
        border-left: 5px solid {current['accent']} !important;
    }}

    .mission-box {{
        background-color: #1a1d14;
        padding: 20px;
        border: 1px solid {current['accent']};
        border-radius: 8px;
        margin-bottom: 25px;
    }}

    .stButton>button {{
        background-color: {current['accent']} !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}
    
    [data-testid="stSidebar"] {{
        border-right: 2px solid {current['accent']};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
else:
    st.error("❌ API KEY MISSING.")
    st.stop()

# --- MODEL SCOUT ---
@st.cache_resource
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available_models: return target
        return available_models[0] if available_models else None
    except: return None

model_name = get_working_model()

# --- MAIN UI ---
st.title(f"{current['icon']} IN-SUFFERABLE")

st.markdown(f"""
    <div class="mission-box">
        <h3 style="margin-top:0;">{current['header']}</h3>
        <p>Input your story below. I will process it through the lens of <strong>{st.session_state.persona}</strong> to generate high-engagement LinkedIn "Broetry."</p>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Tell me what happened..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # We recreate the model per-persona to ensure instructions stick
            model = genai.GenerativeModel(model_name=model_name, system_instruction=current['prompt'])
            response = model.generate_content(prompt)
            
            if response.text:
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.success(f"🫡 {st.session_state.persona.upper()} OUTPUT COMPLETE. POST TO LINKEDIN.")
            else:
                st.warning("REDACTED: Story too spicy for Google's filters.")
        except Exception as e:
            st.error(f"⚠️ UPLINK ERROR: {str(e)}")