import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- PERSONA DATA & THEMES ---
PERSONAS = {
    "The Commander": {
        "icon": "🪖", 
        "color": "#a3cf62", 
        "bg_img": "https://images.unsplash.com/photo-1599940824399-b87987cb972d?q=80&w=2000&auto=format&fit=crop",
        "tagline": "Soldier-Scholar & Strategic Thought Leader.",
        "prompt": """You are a 'Military Thought Leader' on LinkedIn. You sound like a Battalion Commander with an MBA.
        Your mission is to take a mundane user story and turn it into a profound lesson on 'Organizational Readiness'.
        
        WRITING RULES:
        1. Start with a profound, high-level statement about leadership or the 'Civilian Battlefield'.
        2. Describe the user's story as a 'Tactical Case Study' or 'Field Observation'. 
        3. Use jargon like: Force Multiplier, Operational Tempo, Human Capital Sustainment, and Situational Awareness.
        4. Dramatize the mundane: (e.g., 'Forgot my keys' = 'A critical failure in equipment accountability protocols').
        5. CRITICAL: Every single sentence MUST be separated by a BLANK LINE (double return). Do not write paragraphs.
        6. End with 'Agree?' or 'Hooah?' and hashtags like #Leadership #MilitaryMindset #ReadyToLead."""
    },
    "The MD": {
        "icon": "💼", 
        "color": "#00ffcc", 
        "bg_img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2000&auto=format&fit=crop",
        "tagline": "Capital Allocation & High-Stakes Finance.",
        "prompt": """You are a high-energy Venture Capitalist or Managing Director in a Patagonia vest. 
        Your mission is to turn a user's story into a lesson about ROI and scaling.
        
        WRITING RULES:
        1. Start with a cold truth about 'Capital', 'Leverage', or 'Alpha'.
        2. Describe the user's story as a 'Value Chain Leak' or 'Underperforming Asset'.
        3. Explain the 'Return on Investment' of the user's actions.
        4. CRITICAL: Every single sentence MUST be separated by a BLANK LINE (double return). Do not write paragraphs.
        5. End with 'What's your margin?' and hashtags like #Alpha #VentureCapital #Grindset."""
    },
    "The Chief People Officer": {
        "icon": "✨", 
        "color": "#ff99cc", 
        "bg_img": "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2000&auto=format&fit=crop",
        "tagline": "Toxic Positivity & Human-Centric Synergy.",
        "prompt": """You are a 'Chief People Officer' who uses words like 'synergy' and 'alignment'. 
        Your mission is to take a user's story and turn it into a lesson about 'Vulnerability' and 'Culture'.
        
        WRITING RULES:
        1. Start with an inspiring quote about 'The Human Spirit' or 'Leading with Heart'.
        2. Describe the user's story as a 'Growth Moment' or a 'Brand Touchpoint'.
        3. Use MANY sparkles and soft emojis. 
        4. CRITICAL: Every single sentence MUST be separated by a BLANK LINE (double return). Do not write paragraphs.
        5. End with 'Agree? ✨' and hashtags like #ServantLeadership #CultureFirst #Blessed."""
    }
}

# --- INITIALIZE STATE ---
if "persona" not in st.session_state:
    st.session_state.persona = "The Commander"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update UI constants based on current persona
current = PERSONAS[st.session_state.persona]

# --- DYNAMIC CSS (THE BULLETPROOF FIX) ---
# We generate a unique ID string for the style tag. 
# This FORCES the browser to delete the old CSS and load the new one every single time.
unique_style_id = f"theme-{st.session_state.persona.replace(' ', '-')}"

st.markdown(f"""
    <style id="{unique_style_id}">
    /* Target the main view container */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{current['bg_img']}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        transition: background 0.4s ease-in-out;
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

# --- API SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())

# --- MODEL SCOUT ---
@st.cache_resource
def get_working_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available: return target
        return available[0]
    except: return None

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
            model = genai.GenerativeModel(
                model_name=model_name, 
                system_instruction=current['prompt'],
                generation_config={"temperature": 0.85}
            )
            
            full_prompt = f"Transform this story into a coherent, cringe-worthy LinkedIn post: '{prompt}'. Remember: Connect the story to a 'leadership' lesson using your persona's jargon."
            
            response = model.generate_content(full_prompt)
            raw_msg = response.text
            
            # Python post-processing to brutally enforce the "Broetry" format.
            clean_lines = [line.strip() for line in raw_msg.split('\n') if line.strip()]
            broetry_msg = '\n\n'.join(clean_lines)
            
            st.write(broetry_msg)
            st.session_state.messages.append({"role": "assistant", "content": broetry_msg})
        except Exception as e:
            st.error(f"UPLINK ERROR: {str(e)}")
