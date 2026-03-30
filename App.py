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
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update UI constants based on current persona
current = PERSONAS[st.session_state.persona]

# --- DYNAMIC CSS (THE TIMESTAMP HACK) ---
css_id = int(time.time() * 1000)

st.markdown(f"""
    <style id="theme-{css_id}">
    /* Base Fallback Color */
    [data-testid="stAppViewContainer"] {{
        background-color: #121212 !important; 
    }}
    
    /* The Actual Image & Overlay */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{current['bg_img']}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        z-index: -1;
    }}

    /* Make the default Streamlit header transparent */
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* Global Text Visibility */
    p, span, div, li, label, .stMarkdown {{ 
        color: #FFFFFF !important; 
        font-family: 'Inter', -apple-system, sans-serif !important; 
    }}
    
    h1 {{ color: {current['color']} !important; text-align: center; font-weight: 800 !important; letter-spacing: -2px; margin-bottom: 0px !important; }}
    h4 {{ color: {current['color']} !important; text-align: center; text-transform: uppercase; margin-top: 5px !important; margin-bottom: 20px; }}

    /* Instruction Card */
    .instruction-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        padding: 15px;
        border: 1px solid {current['color']};
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }}

    /* Persona Buttons */
    div.stButton > button {{
        width: 100%;
        border-radius: 10px;
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
        border: 1px solid #444 !important;
        font-weight: bold !important;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border: 1px solid {current['color']} !important;
        color: {current['color']} !important;
    }}

    /* Chat Messages */
    [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-left: 5px solid {current['color']} !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
    }}

    /* Hide Sidebar */
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP (NEW SDK) ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"].strip())

# --- MODEL SCOUT ---
@st.cache_resource
def get_working_model():
    try:
        models = client.models.list()
        available = [m.name for m in models]
        for target in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            if target in available or f"models/{target}" in available:
                return target
        return "gemini-1.5-flash"
    except: 
        return "gemini-1.5-flash"

model_name = get_working_model()

# --- MAIN UI ---
st.title("📈 IN-SUFFERABLE")
st.write(f"<h4>{current['tagline']}</h4>", unsafe_allow_html=True)

# Step Instructions
st.markdown(f"""
    <div class="instruction-card">
        <strong>1. CHOOSE A BRAIN &nbsp; | &nbsp; 2. TELL A STORY &nbsp; | &nbsp; 3. GO VIRAL</strong>
    </div>
    """, unsafe_allow_html=True)

# Persona Tabs
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"🪖\nCOMMANDER"): 
        st.session_state.persona = "The Commander"
        st.rerun()
with col2:
    if st.button(f"💼\nTHE MD"): 
        st.session_state.persona = "The MD"
        st.rerun()
with col3:
    if st.button(f"✨\nTHE CPO"): 
        st.session_state.persona = "The Chief People Officer"
        st.rerun()

# --- CHAT INTERFACE ---
if not model_name:
    st.error("🚨 SATELLITE UPLINK FAILED.")
    st.stop()

# Display history
for msg in st.session_state.messages:
    icon = "👤" if msg["role"] == "user" else current["icon"]
    with st.chat_message(msg["role"], avatar=icon):
        st.write(msg["content"])

if prompt := st.chat_input("Tell me what happened today..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=current["icon"]):
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
            
            # Python post-processing to brutally enforce the "Broetry" format.
            clean_lines = [line.strip() for line in raw_msg.split('\n') if line.strip()]
            broetry_msg = '\n\n'.join(clean_lines)
            
            st.write(broetry_msg)
            st.session_state.messages.append({"role": "assistant", "content": broetry_msg})
        except Exception as e:
            st.error(f"UPLINK ERROR: {str(e)}")
