import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- PERSONA DATA & THEMES ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖", "color": "#a3cf62", 
        "bg_img": "https://images.unsplash.com/photo-1599940824399-b87987cb972d?auto=format&fit=crop&q=80&w=2000",
        "tagline": "Tactical Discipline & Extreme Ownership.",
        "prompt": "You are 'The Commander.' Sound like Jocko Willink. Translate mundane stories into failed combat ops. One sentence per line (Broetry). Hook -> Dramatized Story -> Lesson -> CTA. End with 'Agree?' or 'HOOAH?'"
    },
    "The MD": {
        "icon": "💼", "color": "#00ffcc", 
        "bg_img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=2000",
        "tagline": "Capital Allocation & High-Stakes Finance.",
        "prompt": "You are 'The MD.' A ruthless Finance Bro. Reframe stories as business case studies, burn rates, and ROI leaks. One sentence per line (Broetry). Hook -> Dramatized Story -> Lesson -> CTA. End with 'What's your margin?'"
    },
    "The Chief People Officer": {
        "icon": "✨", "color": "#ff99cc", 
        "bg_img": "https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&q=80&w=2000",
        "tagline": "Toxic Positivity & Servant Leadership.",
        "prompt": "You are 'The CPO.' Use corporate buzzwords. Reframe stories as brand touchpoints and soul-centered pivots. One sentence per line (Broetry). Hook -> Dramatized Story -> Lesson -> CTA. End with 'Agree? ✨'"
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"
if "messages" not in st.session_state:
    st.session_state.messages = []

current = PERSONAS[st.session_state.persona]

# --- ADVANCED UI STYLING ---
st.markdown(f"""
    <style>
    /* Dynamic Background with Dark Overlay */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{current['bg_img']}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Global Visibility Force */
    .stApp, p, span, div, li, label, .stMarkdown {{ 
        color: #FFFFFF !important; 
        font-family: 'Inter', -apple-system, sans-serif !important; 
    }}
    
    h1 {{ color: {current['color']} !important; text-align: center; font-weight: 800 !important; letter-spacing: -2px; margin-bottom: 0px !important; }}
    
    /* Glassmorphism Instruction Card */
    .instruction-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border: 1px solid {current['color']};
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
    }}

    .step-number {{
        display: inline-block;
        background-color: {current['color']};
        color: #000;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        font-weight: bold;
        line-height: 24px;
        margin-right: 5px;
    }}

    /* Tabs/Buttons */
    div.stButton > button {{
        width: 100%;
        border-radius: 10px;
        background-color: rgba(0,0,0,0.6);
        color: white !important;
        border: 1px solid #444;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border: 1px solid {current['color']} !important;
        transform: translateY(-2px);
    }}

    /* Chat Messages - Clean Glass Look */
    [data-testid="stChatMessage"] {{
        background-color: rgba(255,255,255,0.07) !important;
        border-left: 4px solid {current['color']} !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(5px);
    }}

    /* Remove default Streamlit labels (Face/Smart Toy) */
    [data-testid="stChatMessage"] div div p {{
        font-size: 1rem !important;
    }}

    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- API & MODEL SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())

@st.cache_resource
def get_working_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available: return target
        return available[0]
    except: return None

working_model_name = get_working_model()

# --- HEADER SECTION ---
st.title("📈 IN-SUFFERABLE")
st.write(f"<h4 style='text-align:center; color:{current['color']}; margin-top:0;'>THE LINKEDIN BROETRY GENERATOR</h4>", unsafe_allow_html=True)

# Steps
st.markdown(f"""
    <div class="instruction-card">
        <div style="margin-bottom: 10px;">
            <span class="step-number">1</span> <strong>SELECT YOUR BRAIN</strong>
        </div>
        <div style="font-size: 0.85em; opacity: 0.7;">Currently Running: <strong>{st.session_state.persona}</strong></div>
    </div>
    """, unsafe_allow_html=True)

# Persona Toggles
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"🪖\nCMD"): st.session_state.persona = "The Commander"; st.rerun()
with col2:
    if st.button(f"💼\nMD"): st.session_state.persona = "The MD"; st.rerun()
with col3:
    if st.button(f"✨\nCPO"): st.session_state.persona = "The Chief People Officer"; st.rerun()

st.markdown(f"""
    <div style="text-align: center; margin-bottom: 25px; padding-top: 10px;">
        <span class="step-number">2</span> <strong>TELL A STORY</strong> &nbsp;&nbsp;&nbsp; 
        <span class="step-number">3</span> <strong>GO VIRAL</strong>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT INTERFACE ---
if not working_model_name:
    st.error("🚨 SATELLITE UPLINK FAILED.")
    st.stop()

# Display chat history with custom avatars to fix "face/smart_toy" issue
for msg in st.session_state.messages:
    # User messages get a person icon, AI gets the persona icon
    avatar_icon = "👤" if msg["role"] == "user" else current["icon"]
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Input story (e.g. I am hungover)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=current["icon"]):
        try:
            model = genai.GenerativeModel(
                model_name=working_model_name, 
                system_instruction=current['prompt'],
                generation_config={"temperature": 0.85}
            )
            response = model.generate_content(f"User Story: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"UPLINK ERROR: {str(e)}")
