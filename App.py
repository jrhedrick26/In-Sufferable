import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- IMPROVED PERSONA PROMPTS ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖", "color": "#a3cf62", "bg": "#0d0f0a",
        "tagline": "Tactical Discipline & Extreme Ownership.",
        "prompt": """
        You are 'The Commander,' a military LinkedIn influencer.
        CRITICAL RULES:
        1. Start with a 1-sentence bold statement (The Hook).
        2. Mention the user's ACTUAL story clearly, but dramatize it as a mission.
        3. Use 'Broetry' (One sentence per line. Double spacing).
        4. End with 'Agree?' or 'HOOAH?'
        EXAMPLE: 
        User: 'I am hungover.'
        Output:
        Pain is a data point. 
        Today, my internal logistics system failed due to suboptimal resource management last night.
        A hangover is just a lapse in operational discipline.
        I didn't call in sick. I hydrated, executed 50 burpees, and took the hill.
        The mission doesn't care how your head feels.
        Standards aren't suggestions.
        Agree?
        #ExtremeOwnership #Discipline #Leadership
        """
    },
    "The MD": {
        "icon": "💼", "color": "#00ffcc", "bg": "#0a0b12",
        "tagline": "Capital Allocation & High-Stakes Finance.",
        "prompt": """
        You are 'The MD,' a ruthless Finance Bro.
        CRITICAL RULES:
        1. Start with a cold statement about money or ROI.
        2. Reframe the user's story as a business case study. 
        3. Use 'Broetry' (One sentence per line).
        4. End with 'What's your margin?'
        EXAMPLE:
        User: 'I am hungover.'
        Output:
        Liquidity is more than just cash. 
        This morning, my cognitive bandwidth is trading at a 40% discount.
        Last night's social capital expenditure had a negative ROI. 
        But real players don't wait for the market to recover.
        I'm arbitrage-ing this headache into high-output grind.
        If you aren't hurting, you aren't scaling.
        What's your margin today?
        #Alpha #VentureCapital #Grindset
        """
    },
    "The Chief People Officer": {
        "icon": "✨", "color": "#ff99cc", "bg": "#0f0d12",
        "tagline": "Toxic Positivity & Servant Leadership.",
        "prompt": """
        You are 'The CPO,' a corporate visionary.
        CRITICAL RULES:
        1. Start with a soft, inspiring statement about growth.
        2. Reframe the user's story as a 'Vulnerability Breakthrough.'
        3. Use 'Broetry' (One sentence per line).
        4. End with 'Agree? ✨'
        EXAMPLE:
        User: 'I am hungover.'
        Output:
        Discomfort is the heartbeat of authenticity. ✨
        Today, I'm leaning into a very 'human' moment of physical misalignment.
        My body is telling a story of connection and synergy from last night.
        I'm not 'hungover.' I'm in a 'Deep-Dive Recovery Phase.'
        By showing up messy, I'm giving my team permission to be their whole selves.
        Let's pivot from 'perfect' to 'purposeful.' 💖
        Agree?
        #ServantLeadership #CultureFirst #Authenticity
        """
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"
if "messages" not in st.session_state:
    st.session_state.messages = []

current = PERSONAS[st.session_state.persona]

# --- UI STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {current['bg']} !important; }}
    .stApp, p, span, div, li, label, .stMarkdown {{ color: #FFFFFF !important; font-family: 'Inter', -apple-system, sans-serif !important; }}
    h1 {{ color: {current['color']} !important; text-align: center; font-weight: 800 !important; letter-spacing: -1px; margin-bottom: 0px !important; }}
    .instruction-card {{ background-color: #1a1d14; padding: 20px; border: 2px solid {current['color']}; border-radius: 12px; margin-bottom: 25px; text-align: center; }}
    .step-number {{ display: inline-block; background-color: {current['color']}; color: #000; border-radius: 50%; width: 25px; height: 25px; font-weight: bold; margin-right: 5px; }}
    div.stButton > button {{ width: 100%; border-radius: 8px; background-color: #1a1d14; color: white !important; border: 1px solid #333; }}
    div.stButton > button:hover {{ border: 1px solid {current['color']} !important; color: {current['color']} !important; }}
    [data-testid="stChatMessage"] {{ background-color: #1a1d14 !important; border-left: 5px solid {current['color']} !important; border-radius: 8px !important; }}
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())

# --- THE "MODEL SCOUT" (The 404 Fix) ---
@st.cache_resource
def get_working_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Check for 1.5-flash, then pro, then anything available
        for target in ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.5-flash-latest"]:
            if target in available: return target
        return available[0]
    except Exception as e:
        return None

working_model_name = get_working_model()

# --- HEADER ---
st.title("📈 IN-SUFFERABLE")
st.write(f"<h4 style='text-align:center; color:{current['color']}'>THE LINKEDIN BROETRY GENERATOR</h4>", unsafe_allow_html=True)

# Step-by-Step
st.markdown(f"""
    <div class="instruction-card">
        <div style="margin-bottom: 10px;">
            <span class="step-number">1</span> <strong>SELECT YOUR BRAIN</strong>
        </div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-bottom: 15px;">Pick a persona to reframe your story.</div>
    </div>
    """, unsafe_allow_html=True)

# Persona Tabs
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"{PERSONAS['The Commander']['icon']}\nCOMMANDER"): 
        st.session_state.persona = "The Commander"; st.rerun()
with col2:
    if st.button(f"{PERSONAS['The MD']['icon']}\nTHE MD"): 
        st.session_state.persona = "The MD"; st.rerun()
with col3:
    if st.button(f"{PERSONAS['The Chief People Officer']['icon']}\nTHE CPO"): 
        st.session_state.persona = "The Chief People Officer"; st.rerun()

st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="step-number">2</span> <strong>TELL A STORY</strong> &nbsp;&nbsp;&nbsp; 
        <span class="step-number">3</span> <strong>GO VIRAL</strong>
    </div>
    <div style="text-align: center; padding: 10px;">
        <p style="font-size: 0.9em; color: {current['color']} !important; font-weight: bold;">ACTIVE: {st.session_state.persona.upper()}</p>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT ---
if not working_model_name:
    st.error("🚨 SATELLITE UPLINK FAILED. Check API Key or Region.")
    st.stop()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Tell me what happened (e.g., I'm hungover)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Re-initialize model with the 'scouted' model name
            model = genai.GenerativeModel(
                model_name=working_model_name, 
                system_instruction=current['prompt'],
                generation_config={"temperature": 0.8}
            )
            response = model.generate_content(f"Story: {prompt}. Transform this into a viral LinkedIn post using the formula: Hook -> Dramatized Story -> Lesson -> CTA.")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"UPLINK ERROR: {str(e)}")
