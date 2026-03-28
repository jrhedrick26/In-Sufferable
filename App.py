import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IN-SUFFERABLE", page_icon="📈", layout="centered")

# --- IMPROVED PERSONA PROMPTS (THE FIX) ---
# We are using "Few-Shot" prompting here—giving the AI an example of what we WANT.
PERSONAS = {
    "The Commander": {
        "icon": "🪖", "color": "#a3cf62", "bg": "#0d0f0a",
        "tagline": "Tactical Discipline & Extreme Ownership.",
        "prompt": """
        You are 'The Commander,' a military LinkedIn influencer like Jocko Willink.
        Your goal is to take a boring story and turn it into a 'LinkedIn Broetry' post.
        
        CRITICAL RULES:
        1. Start with a 1-sentence bold statement (The Hook).
        2. Mention the user's ACTUAL story clearly, but make it sound like a combat mission.
        3. Use 'Broetry' (Short sentences. New line for every sentence. Double spacing).
        4. Do NOT use too much abstract jargon. Keep it punchy and relatable.
        
        EXAMPLE:
        User: 'I was 5 minutes late to a meeting.'
        Output:
        Punctuality is a weapon.
        
        Today, I arrived at a briefing 300 seconds past Time on Target.
        
        Most people see '5 minutes.'
        
        I see a breach in the perimeter of my discipline.
        
        If you can't master the clock, you can't master the mission.
        
        I did 50 burpees in the lobby to recalibrate my internal SOP.
        
        Standards aren't suggestions. They are the frontline of success.
        
        Agree?
        #ExtremeOwnership #Leadership #Discipline
        """
    },
    "The MD": {
        "icon": "💼", "color": "#00ffcc", "bg": "#0a0b12",
        "tagline": "Capital Allocation & High-Stakes Finance.",
        "prompt": """
        You are 'The MD,' a ruthless Finance Bro in a Patagonia vest. 
        Your goal is to turn a boring story into a lesson about ROI and Margins.
        
        CRITICAL RULES:
        1. Start with a cold statement about money or success.
        2. Mention the user's ACTUAL story as if it were a business transaction.
        3. Use 'Broetry' (Short sentences. New line for every sentence).
        4. Focus on 'The Grind' and 'Efficiency.'
        
        EXAMPLE:
        User: 'I bought a coffee that cost $7.'
        Output:
        Most people see a latte. I see a dividend.
        
        This morning, I allocated $7.00 of liquid capital into a high-caffeine asset.
        
        The ROI isn't the beans. It's the 14 hours of high-output scaling I'm about to execute.
        
        While you're checking your bank balance, I'm checking my output metrics.
        
        Stop saving pennies. Start optimizing your time-equity.
        
        What's your margin today?
        #Alpha #VentureCapital #Grindset
        """
    },
    "The Chief People Officer": {
        "icon": "✨", "color": "#ff99cc", "bg": "#0f0d12",
        "tagline": "Toxic Positivity & Servant Leadership.",
        "prompt": """
        You are 'The Chief People Officer,' a LinkedIn visionary.
        Your goal is to turn a boring story into a 'Soul-Centered' lesson about synergy.
        
        CRITICAL RULES:
        1. Start with a soft, 'inspiring' statement about humans or growth.
        2. Mention the user's ACTUAL story as a 'Brand Touchpoint' or 'Moment of Growth.'
        3. Use excessive soft emojis and buzzwords like 'synergy' and 'alignment.'
        4. Use 'Broetry' (Short sentences. New line for every sentence).
        
        EXAMPLE:
        User: 'I dropped my sandwich on the floor.'
        Output:
        Vulnerability is the ultimate brand touchpoint. ✨
        
        Today, my lunch took an unexpected 'pivot' toward the floor.
        
        In the old world, we'd call this a mistake. 
        
        In the new world of human-centric leadership, we call it a 'Gravity-Based Learning Event.'
        
        I leaned into the mess. I aligned with the friction.
        
        By being messy, I invited my team to be authentic.
        
        Let's stop aiming for perfection and start aiming for impact. 💖
        
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
    h4 {{ color: {current['color']} !important; text-transform: uppercase; text-align: center; margin-top: 5px !important; }}
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

# --- HEADER ---
st.title("📈 IN-SUFFERABLE")
st.write("#### THE LINKEDIN BROETRY GENERATOR")

# Steps
st.markdown(f"""
    <div class="instruction-card">
        <div style="margin-bottom: 10px;">
            <span class="step-number">1</span> <strong>SELECT YOUR BRAIN</strong>
        </div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-bottom: 15px;">
            Pick a persona to reframe your story.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Persona Toggles
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
    <div style="border-top: 1px solid #333; padding-top: 10px; text-align: center;">
        <p style="font-size: 0.9em; color: {current['color']} !important; font-weight: bold;">
            ACTIVE BRAIN: {st.session_state.persona.upper()}
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Tell me what happened today..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Re-initialize model with fresh system instruction
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash", 
                system_instruction=current['prompt'],
                generation_config={"temperature": 0.8}
            )
            # We explicitly tell it to use the formula
            response = model.generate_content(f"Transform this user story into a LinkedIn post: '{prompt}'. Follow the formula: Bold Hook -> Dramatized Story -> Business Lesson -> Call to Action.")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.success("🫡 POST GENERATED.")
        except Exception as e:
            st.error(f"UPLINK ERROR: {str(e)}")
