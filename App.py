import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- PERSONA DATA ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖", "color": "#a3cf62", "bg": "#0d0f0a",
        "tagline": "Tactical Discipline & Extreme Ownership.",
        "header": "SITREP: MISSION READINESS",
        "prompt": "You are 'The Commander.' You sound like Jocko Willink. Translate mundane stories into failed combat ops and SOP failures. One sentence per line. End with 'Agree?' or 'HOOAH?' #Discipline #ExtremeOwnership"
    },
    "The MD": {
        "icon": "💼", "color": "#00ffcc", "bg": "#0a0b12",
        "tagline": "Capital Allocation & High-Stakes Finance.",
        "header": "QUARTERLY REPORT: PORTFOLIO OPTIMIZATION",
        "prompt": "You are 'The MD.' A ruthless Finance Bro. Reframe stories as business case studies, burn rates, and ROI leaks. One sentence per line. End with 'What's your margin?' #Alpha #VentureCapital"
    },
    "The Chief People Officer": {
        "icon": "✨", "color": "#ff99cc", "bg": "#0f0d12",
        "tagline": "Toxic Positivity & Servant Leadership.",
        "header": "CULTURE CHECK: HUMAN-CENTRIC SYNERGY",
        "prompt": "You are 'The CPO.' Use massive amounts of corporate buzzwords. Reframe stories as brand touchpoints and soul-centered pivots. One sentence per line. End with 'Agree? ✨' #CultureFirst #Blessed"
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"
if "messages" not in st.session_state:
    st.session_state.messages = []

current = PERSONAS[st.session_state.persona]

# --- UI STYLING (NUCLEAR VISIBILITY) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {current['bg']} !important; }}
    .stApp, p, span, div, li, label, .stMarkdown {{ color: #FFFFFF !important; font-family: 'Inter', -apple-system, sans-serif !important; }}
    
    /* Title & Header Colors */
    h1 {{ color: {current['color']} !important; text-align: center; font-weight: 800 !important; letter-spacing: -1px; margin-bottom: 0px !important; }}
    h3, h4 {{ color: {current['color']} !important; text-transform: uppercase; text-align: center; margin-top: 5px !important; }}

    /* Instruction Box */
    .instruction-card {{
        background-color: #1a1d14;
        padding: 20px;
        border: 2px solid {current['color']};
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }}
    .step-number {{
        display: inline-block;
        background-color: {current['color']};
        color: #000;
        border-radius: 50%;
        width: 25px;
        height: 25px;
        font-weight: bold;
        margin-right: 5px;
    }}

    /* Persona Buttons Styling */
    div.stButton > button {{
        width: 100%;
        border-radius: 8px;
        background-color: #1a1d14;
        color: white !important;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    
    /* Highlight Active Persona Button */
    div.stButton > button:hover {{
        border: 1px solid {current['color']} !important;
        color: {current['color']} !important;
    }}

    /* Chat Messages */
    [data-testid="stChatMessage"] {{
        background-color: #1a1d14 !important;
        border-left: 5px solid {current['color']} !important;
        border-radius: 8px !important;
    }}

    /* Hide sidebar on mobile */
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- SECURE API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
else:
    st.error("API KEY MISSING.")
    st.stop()

# --- HEADER SECTION ---
st.title("📈 IN-SUFFERABLE")
st.write("#### THE LINKEDIN BROETRY GENERATOR")

# Onboarding / Step-by-Step UI
st.markdown(f"""
    <div class="instruction-card">
        <div style="margin-bottom: 10px;">
            <span class="step-number">1</span> <strong>SELECT YOUR BRAIN</strong>
        </div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-bottom: 15px;">
            Choose a persona to reframe your story.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PERSONA SELECTOR ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"{PERSONAS['The Commander']['icon']}\nCOMMANDER"): 
        st.session_state.persona = "The Commander"
        st.rerun()
with col2:
    if st.button(f"{PERSONAS['The MD']['icon']}\nTHE MD"): 
        st.session_state.persona = "The MD"
        st.rerun()
with col3:
    if st.button(f"{PERSONAS['The Chief People Officer']['icon']}\nTHE CPO"): 
        st.session_state.persona = "The Chief People Officer"
        st.rerun()

# --- STEP 2 & 3 INSTRUCTIONS ---
st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="step-number">2</span> <strong>TELL A STORY</strong> &nbsp;&nbsp;&nbsp; 
        <span class="step-number">3</span> <strong>GO VIRAL</strong>
    </div>
    <div style="border-top: 1px solid #333; padding-top: 10px; text-align: center;">
        <p style="font-size: 0.9em; color: {current['color']} !important; font-weight: bold;">
            ACTIVE PERSONA: {st.session_state.persona.upper()}
        </p>
        <p style="font-size: 0.8em; opacity: 0.7;">VIBE: {current['tagline']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- MODEL LOGIC ---
@st.cache_resource
def get_model(p_name):
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    m_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    return genai.GenerativeModel(
        model_name=m_name, 
        system_instruction=PERSONAS[p_name]['prompt'],
        generation_config={"temperature": 0.9} 
    )

# --- CHAT DISPLAY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- INPUT SECTION ---
if prompt := st.chat_input("Tell me a boring story (e.g., I bought coffee)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            model = get_model(st.session_state.persona)
            enhanced_prompt = f"Take this mundane story and re-imagine it as a high-stakes, cringe-worthy LinkedIn post using your specific persona: '{prompt}'. Do not be literal. Use heavy jargon and 'Broetry' formatting."
            
            response = model.generate_content(enhanced_prompt)
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
            st.success("🫡 POST GENERATED. Copy to LinkedIn and wait for the engagement.")
        except Exception as e:
            st.error(f"UPLINK ERROR: {str(e)}")
