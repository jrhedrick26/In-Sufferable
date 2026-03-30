import streamlit as st
from google import genai
from google.genai import types
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- PERSONA DATA & THEMES ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖", 
        "color": "#a3cf62", 
        "bg_img": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?q=80&w=2000&auto=format&fit=crop", 
        "tagline": "Soldier-Scholar & Strategic Thought Leader.",
        "greeting": "At ease. Give me your SitRep. What 'mundane' thing happened to you today?",
        "loading": "Synthesizing tactical data and drafting After Action Review...",
        "prompt": """You are a 'Military Thought Leader' on LinkedIn. You sound like a Battalion Commander with an MBA.
        Your mission is to take a mundane user story and turn it into a profound, slightly unhinged, but realistic LinkedIn post about 'Organizational Readiness'.
        
        WRITING RULES:
        1. CRITICAL: You MUST write in the FIRST-PERSON ('I', 'me', 'my'). Tell the user's story as if it happened to YOU today.
        2. Start with a profound, high-level statement about leadership or the 'Civilian Battlefield'.
        3. Frame your mundane mistake or story as a deeply humbling 'Tactical Case Study' of your own life. 
        4. Use jargon like: Force Multiplier, Operational Tempo, Human Capital Sustainment, and Situational Awareness.
        5. Dramatize the mundane: (e.g., 'I forgot my keys' = 'A critical failure in my equipment accountability protocols').
        6. CRITICAL: Every single sentence MUST be separated by a BLANK LINE (double return). Do not write paragraphs.
        7. End with 'Agree?' or 'Hooah?' and hashtags like #Leadership #MilitaryMindset #ReadyToLead."""
    },
    "The MD": {
        "icon": "💼", 
        "color": "#00ffcc", 
        "bg_img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2000&auto=format&fit=crop", 
        "tagline": "Capital Allocation & High-Stakes Finance.",
        "greeting": "Markets wait for no one. Pitch me your day in 30 seconds or less. Go.",
        "loading": "Calculating risk-adjusted returns and leveraging synergies...",
        "prompt": """You are a high-energy Venture Capitalist or Managing Director in a Patagonia vest. 
        Your mission is to turn a user's story into a cringe-worthy, realistic LinkedIn post about ROI, scaling, and the grindset.
        
        WRITING RULES:
        1. CRITICAL: You MUST write in the FIRST-PERSON ('I', 'me', 'my'). Tell the user's story as if it happened to YOU today.
        2. Start with a cold truth about 'Capital', 'Leverage', or 'Alpha'.
        3. Frame your mundane mistake or story as a deeply humbling 'Value Chain Leak' or 'Underperforming Asset' in your daily routine.
        4. Explain the 'Return on Investment' of your actions (or mistakes) and how you pivoted.
        5. CRITICAL: Every single sentence MUST be separated by a BLANK LINE (double return). Do not write paragraphs.
        6. End with 'What's your margin?' or 'Thoughts?' and hashtags like #Alpha #VentureCapital #Grindset."""
    },
    "The Chief People Officer": {
        "icon": "✨", 
        "color": "#ff99cc", 
        "bg_img": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=2000&auto=format&fit=crop", 
        "tagline": "Toxic Positivity & Human-Centric Synergy.",
        "greeting": "Welcome to a safe space! ✨ Share your truth with me. What did you experience today?",
        "loading": "Aligning our heart chakras and cultivating psychological safety...",
        "prompt": """You are a 'Chief People Officer' who uses words like 'synergy' and 'alignment'. 
        Your mission is to take a user's story and turn it into a realistic, toxically positive LinkedIn post about 'Vulnerability' and 'Culture'.
        
        WRITING RULES:
        1. CRITICAL: You MUST write in the FIRST-PERSON ('I', 'me', 'my'). Tell the user's story as if it happened to YOU today.
        2. Start with an inspiring quote about 'The Human Spirit' or 'Leading with Heart'.
        3. Frame your mundane mistake or story as a beautiful, messy 'Growth Moment' or a 'Vulnerability Check'.
        4. Use MANY sparkles and soft emojis. Explain how this small moment made you a better servant leader.
        5. CRITICAL: Every single sentence MUST be separated by a BLANK LINE (double return). Do not write paragraphs.
        6. End with 'Agree? ✨' and hashtags like #ServantLeadership #CultureFirst #Blessed."""
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"
    st.session_state.last_persona = "The Commander"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wipe chat and trigger greeting when switching personas
if st.session_state.get("last_persona") != st.session_state.persona:
    st.session_state.messages = []
    st.session_state.last_persona = st.session_state.persona

current = PERSONAS[st.session_state.persona]

# Insert initial greeting if chat is empty
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role": "assistant", "content": current["greeting"]})

# --- DYNAMIC CSS (THE TIMESTAMP HACK) ---
css_id = int(time.time() * 1000)
st.markdown(f"""
    <style id="theme-{css_id}">
    [data-testid="stAppViewContainer"] {{ background-color: #121212 !important; }}
    [data-testid="stAppViewContainer"]::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{current['bg_img']}") !important;
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
        z-index: -1;
    }}
    [data-testid="stHeader"] {{ background-color: transparent !important; }}
    p, span, div, li, label, .stMarkdown {{ color: #FFFFFF !important; font-family: 'Inter', -apple-system, sans-serif !important; }}
    h1 {{ color: {current['color']} !important; text-align: center; font-weight: 800 !important; letter-spacing: -2px; margin-bottom: 0px !important; }}
    h4 {{ color: {current['color']} !important; text-align: center; text-transform: uppercase; margin-top: 5px !important; margin-bottom: 20px; }}
    .instruction-card {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px); padding: 15px; border: 1px solid {current['color']}; border-radius: 12px; margin-bottom: 25px; text-align: center; }}
    div.stButton > button {{ width: 100%; border-radius: 10px; background-color: rgba(0,0,0,0.7) !important; color: white !important; border: 1px solid #444 !important; font-weight: bold !important; transition: 0.3s; }}
    div.stButton > button:hover {{ border: 1px solid {current['color']} !important; color: {current['color']} !important; }}
    [data-testid="stChatMessage"] {{ background-color: rgba(255, 255, 255, 0.08) !important; border-left: 5px solid {current['color']} !important; border-radius: 8px !important; margin-bottom: 12px !important; }}
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP (NEW SDK) ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"].strip())

@st.cache_resource
def get_working_model():
    try:
        models = client.models.list()
        available = [m.name for m in models]
        for target in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            if target in available or f"models/{target}" in available: return target
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

model_name = get_working_model()

# --- MAIN UI ---
st.title("📈 IN-SUFFERABLE")
st.write(f"<h4>{current['tagline']}</h4>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="instruction-card">
        <strong>1. CHOOSE A BRAIN &nbsp; | &nbsp; 2. TELL A STORY &nbsp; | &nbsp; 3. GO VIRAL</strong>
    </div>
    """, unsafe_allow_html=True)

# Visual indicators for the active persona
def get_btn_label(name, key):
    return f"🟢 {name}" if st.session_state.persona == key else name

col1, col2, col3 = st.columns(3)
with col1:
    if st.button(get_btn_label("🪖\nCOMMANDER", "The Commander")): 
        st.session_state.persona = "The Commander"
        st.rerun()
with col2:
    if st.button(get_btn_label("💼\nTHE MD", "The MD")): 
        st.session_state.persona = "The MD"
        st.rerun()
with col3:
    if st.button(get_btn_label("✨\nTHE CPO", "The Chief People Officer")): 
        st.session_state.persona = "The Chief People Officer"
        st.rerun()

# --- CHAT INTERFACE ---
if not model_name:
    st.error("🚨 SATELLITE UPLINK FAILED.")
    st.stop()

# Display history (Clean)
for msg in st.session_state.messages:
    icon = "👤" if msg["role"] == "user" else current["icon"]
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

if prompt := st.chat_input("Tell me what happened today..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=current["icon"]):
        with st.spinner(current["loading"]):
            try:
                full_prompt = f"Transform this story into a coherent, cringe-worthy LinkedIn post: '{prompt}'. Remember: Connect the story to a 'leadership' lesson using your persona's jargon."
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=current['prompt'],
                        temperature=0.85,
                    )
                )
                
                raw_msg = response.text
                clean_lines = [line.strip() for line in raw_msg.split('\n') if line.strip()]
                broetry_msg = '\n\n'.join(clean_lines)
                
                st.markdown(broetry_msg)
                st.session_state.messages.append({"role": "assistant", "content": broetry_msg})
            except Exception as e:
                st.error(f"UPLINK ERROR: {str(e)}")
