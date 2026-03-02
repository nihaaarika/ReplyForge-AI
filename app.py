import streamlit as st
import os
import json
import requests
from typing import Dict, List, Optional, Any
import re
from dotenv import load_dotenv
load_dotenv()


# ---------------------------- CONFIGURATION ----------------------------
st.set_page_config(
    page_title="ReplyForgeAI",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------- THEME DEFINITIONS ----------------------------
THEMES = {
    "Cyber Dark": {
        "bg": "#0a0a0f", "surface": "#111118", "surface2": "#16161f", "border": "#1e1e2e",
        "accent": "#6c63ff", "accent2": "#00d4aa", "accent3": "#ff6b6b",
        "text": "#e2e2f0", "muted": "#5a5a7a", "glow": "rgba(108,99,255,0.15)",
        "btn_p": "linear-gradient(135deg,#6c63ff,#9a63ff)",
        "btn_g": "linear-gradient(135deg,#00d4aa,#00a88a)", "btn_gt": "#0a0a0f",
        "grid": "rgba(108,99,255,0.03)", "font": "'Syne',sans-serif", "mono": "'Space Mono',monospace", "r": "16px"
    },
    "Forest": {
        "bg": "#0d1810", "surface": "#121f14", "surface2": "#162a18", "border": "#1e3b22",
        "accent": "#4ade80", "accent2": "#86efac", "accent3": "#fbbf24",
        "text": "#d1fae5", "muted": "#4a7055", "glow": "rgba(74,222,128,0.12)",
        "btn_p": "linear-gradient(135deg,#16a34a,#4ade80)",
        "btn_g": "linear-gradient(135deg,#4ade80,#86efac)", "btn_gt": "#0d1810",
        "grid": "rgba(74,222,128,0.03)", "font": "'DM Sans',sans-serif", "mono": "'JetBrains Mono',monospace", "r": "12px"
    },
    "Ocean Depth": {
        "bg": "#020b18", "surface": "#051525", "surface2": "#071c30", "border": "#0a2a45",
        "accent": "#00b4d8", "accent2": "#90e0ef", "accent3": "#f77f00",
        "text": "#caf0f8", "muted": "#2a6080", "glow": "rgba(0,180,216,0.15)",
        "btn_p": "linear-gradient(135deg,#0077b6,#00b4d8)",
        "btn_g": "linear-gradient(135deg,#00b4d8,#90e0ef)", "btn_gt": "#020b18",
        "grid": "rgba(0,180,216,0.03)", "font": "'Syne',sans-serif", "mono": "'JetBrains Mono',monospace", "r": "14px"
    },
    "Sunset Gold": {
        "bg": "#0f0800", "surface": "#1a1000", "surface2": "#221500", "border": "#3d2500",
        "accent": "#f59e0b", "accent2": "#fbbf24", "accent3": "#ef4444",
        "text": "#fef3c7", "muted": "#78530a", "glow": "rgba(245,158,11,0.15)",
        "btn_p": "linear-gradient(135deg,#d97706,#f59e0b)",
        "btn_g": "linear-gradient(135deg,#f59e0b,#fbbf24)", "btn_gt": "#0f0800",
        "grid": "rgba(245,158,11,0.04)", "font": "'Syne',sans-serif", "mono": "'Space Mono',monospace", "r": "10px"
    },
    "Neon Noir": {
        "bg": "#050508", "surface": "#0c0c12", "surface2": "#100f18", "border": "#1a0a2e",
        "accent": "#f700ff", "accent2": "#00ffe7", "accent3": "#ff3d3d",
        "text": "#f0e6ff", "muted": "#4a2a6a", "glow": "rgba(247,0,255,0.12)",
        "btn_p": "linear-gradient(135deg,#9b00d3,#f700ff)",
        "btn_g": "linear-gradient(135deg,#00ffe7,#00c9b8)", "btn_gt": "#050508",
        "grid": "rgba(247,0,255,0.03)", "font": "'Syne',sans-serif", "mono": "'JetBrains Mono',monospace", "r": "6px"
    },
    "Ice Nord": {
        "bg": "#1e2030", "surface": "#252740", "surface2": "#2c2f4a", "border": "#373b5c",
        "accent": "#88c0d0", "accent2": "#81a1c1", "accent3": "#bf616a",
        "text": "#eceff4", "muted": "#4c566a", "glow": "rgba(136,192,208,0.12)",
        "btn_p": "linear-gradient(135deg,#5e81ac,#88c0d0)",
        "btn_g": "linear-gradient(135deg,#88c0d0,#8fbcbb)", "btn_gt": "#1e2030",
        "grid": "rgba(136,192,208,0.03)", "font": "'DM Sans',sans-serif", "mono": "'JetBrains Mono',monospace", "r": "14px"
    },
    "Lava": {
        "bg": "#0a0000", "surface": "#160000", "surface2": "#1e0000", "border": "#3d0000",
        "accent": "#ff4444", "accent2": "#ff8c00", "accent3": "#ffdd00",
        "text": "#fff0f0", "muted": "#6a2020", "glow": "rgba(255,68,68,0.15)",
        "btn_p": "linear-gradient(135deg,#cc0000,#ff4444)",
        "btn_g": "linear-gradient(135deg,#ff8c00,#ffdd00)", "btn_gt": "#0a0000",
        "grid": "rgba(255,68,68,0.03)", "font": "'Syne',sans-serif", "mono": "'Space Mono',monospace", "r": "8px"
    },
}

# ---------------------------- SESSION STATE ----------------------------
if "email_content" not in st.session_state:
    st.session_state.email_content = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "generated_response" not in st.session_state:
    st.session_state.generated_response = None
if "reasoning" not in st.session_state:
    st.session_state.reasoning = ""
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = "Accept"
if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "Formal"
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "llama-3.3-70b-versatile"
if "theme" not in st.session_state:
    st.session_state.theme = "Cyber Dark"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edited_response" not in st.session_state:
    st.session_state.edited_response = ""

# ---------------------------- API CONFIG ----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B (Best Quality)",
    "llama-3.1-8b-instant": "Llama 3.1 8B (Fast)",
    "mixtral-8x7b-32768": "Mixtral 8x7B (Good Balance)"
}

# ---------------------------- API HELPERS ----------------------------
def call_groq(prompt: str, system_prompt: str = "", model: str = "llama-3.3-70b-versatile", temperature: float = 0.3) -> Optional[str]:
    api_key = os.getenv("GROQ_API_KEY") 
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
        return None
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": 1024, "top_p": 0.9}
    try:
        with st.spinner("AI is thinking..."):
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
    return None

def analyze_email_intent(email_content: str, context: str = "") -> Dict[str, Any]:
    system_prompt = """You are an expert email analyst. Analyze the email and return a structured analysis.
    Focus on: email type, action needed, urgency, detected tone, decision needed, and possible paths."""
    prompt = f"""
    Analyze this email and provide a structured response in JSON format:
    Email Content: {email_content}
    Additional Context: {context}
    Return a JSON object with these exact keys:
    - email_type: (e.g., Invitation, Question, Meeting Request, Task, Newsletter, etc.)
    - action_needed: (Yes/No)
    - urgency: (Low/Medium/High)
    - tone_detected: (e.g., Friendly, Formal, Urgent, Professional)
    - decision_needed: (Yes/No)
    - possible_paths: (array of strings, e.g., ["Accept", "Decline", "Delay", "Ask Clarification"])
    - summary: (brief 1-sentence summary)
    - key_points: (array of 2-3 key points)
    """
    result = call_groq(prompt, system_prompt, model=st.session_state.model_choice, temperature=0.2)
    if result:
        try:
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(result)
        except:
            return {
                "email_type": "General", "action_needed": "Yes", "urgency": "Medium",
                "tone_detected": "Neutral", "decision_needed": "Yes",
                "possible_paths": ["Accept", "Decline", "Delay", "Ask Clarification"],
                "summary": "Email analysis completed", "key_points": ["Review email content"]
            }
    return {}

def generate_email_response(email_content: str, reasoning: str, scenario: str, tone: str, context: str = "") -> str:
    system_prompt = f"""You are an expert email writer. Generate a personalized email response with {tone} tone.
    The user has chosen to: {scenario.upper()}
    Their reasoning: {reasoning}
    Write a professional, context-aware response that incorporates their reasoning naturally."""
    prompt = f"""
    Original Email: {email_content}
    Additional Context: {context}
    User's Reasoning for {scenario}: {reasoning}
    Generate a complete email response that:
    1. References the original email appropriately
    2. Incorporates the user's reasoning naturally
    3. Maintains a {tone} tone throughout
    4. Is professional and well-structured
    5. Includes appropriate subject line suggestion
    """
    return call_groq(prompt, system_prompt, model=st.session_state.model_choice, temperature=0.4) or "Error generating response. Please try again."

# ---------------------------- DYNAMIC CSS ----------------------------
def get_css(t):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Playfair+Display:wght@400;700&family=JetBrains+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');

:root {{
  --bg:{t['bg']};--surface:{t['surface']};--surface2:{t['surface2']};--border:{t['border']};
  --accent:{t['accent']};--accent2:{t['accent2']};--accent3:{t['accent3']};
  --text:{t['text']};--muted:{t['muted']};--glow:{t['glow']};
  --btn-p:{t['btn_p']};--btn-g:{t['btn_g']};--btn-gt:{t['btn_gt']};
  --grid:{t['grid']};--font:{t['font']};--mono:{t['mono']};--r:{t['r']};
}}

html, body, .stApp {{
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
}}

/* Hide streamlit chrome */
#MainMenu, footer, header, .stDeployButton {{ display:none !important; }}
.block-container {{ 
    padding-top: 0rem !important;
    padding-left: 5rem !important; 
    padding-right: 5rem !important; 
    max-width: 100% !important; 
}}

@media (max-width: 768px) {{
    .block-container {{
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }}
}}
section[data-testid="stSidebar"] > div {{ background: var(--surface2) !important; border-right: 1px solid var(--border) !important; }}

/* Background grid */
.stApp::before {{
  content:'';position:fixed;inset:0;
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:40px 40px;z-index:0;pointer-events:none;
}}

/* MAIN WRAPPER */
.ea-wrap {{
  max-width:1300px;margin:0 auto;padding:0 28px 60px;position:relative;z-index:1;
}}

/* HEADER */
.ea-header {{
  display:flex;align-items:center;justify-content:space-between;
  padding:24px 0 26px;border-bottom:1px solid var(--border);margin-bottom:28px;
}}
.ea-logo {{ display:flex;align-items:center;gap:12px; }}
.ea-logo-icon {{
  width:42px;height:42px;background:var(--btn-p);border-radius:var(--r);
  display:flex;align-items:center;justify-content:center;font-size:20px;
  box-shadow:0 0 20px var(--glow);
}}
.ea-logo-text {{
  font-size:1.4rem;font-weight:800;letter-spacing:-.02em;
  background:var(--btn-p);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
}}
.ea-logo-sub {{
  font-family:var(--mono);font-size:.62rem;color:var(--muted);
  letter-spacing:.15em;text-transform:uppercase;
}}
.ea-badge {{
  font-family:var(--mono);font-size:.68rem;color:var(--accent2);
  border:1px solid var(--border);padding:6px 12px;border-radius:20px;
}}
.live-dot {{
  width:6px;height:6px;background:var(--accent2);border-radius:50%;
  display:inline-block;margin-left:6px;animation:pulse 2s infinite;
}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:.4;transform:scale(.7);}}}}

/* Theme selector in header */
.theme-header-selector {{
  font-family:var(--mono);font-size:.8rem;color:var(--text);
  background:var(--surface);border:1px solid var(--border);
  border-radius:20px;padding:4px 12px;cursor:pointer;
  display:flex;align-items:center;gap:6px;
}}

/* PANELS */
.ea-panel {{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);overflow:hidden;margin-bottom:18px;
  transition:border-color .3s;
}}
.ea-panel:hover{{border-color:var(--accent);}}
.ea-panel-hdr {{
  display:flex;align-items:center;gap:10px;padding:14px 20px;
  border-bottom:1px solid var(--border);background:var(--surface2);
}}
.ea-tag {{
  font-family:var(--mono);font-size:.62rem;letter-spacing:.12em;
  text-transform:uppercase;padding:3px 8px;border-radius:4px;font-weight:700;
  border:1px solid var(--border);
}}
.tag-i  {{background:rgba(108,99,255,.12);color:var(--accent);}}
.tag-a1 {{background:rgba(0,212,170,.1); color:var(--accent2);}}
.tag-a2 {{background:rgba(255,107,107,.1);color:var(--accent3);}}
.tag-c  {{background:rgba(255,200,80,.1); color:var(--accent2);}}
.ea-panel-title{{font-weight:700;font-size:.88rem;color:var(--text);}}
.ea-panel-body{{padding:18px 20px;}}

/* STAT CHIPS */
.stat-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;}}
.stat-chip{{
  background:var(--bg);border:1px solid var(--border);
  border-radius:calc(var(--r) * .5);padding:11px 13px;
}}
.stat-chip:hover{{border-color:var(--accent);}}
.stat-lbl{{font-family:var(--mono);font-size:.58rem;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:3px;}}
.stat-val{{font-weight:700;font-size:.88rem;color:var(--text);}}
.u-h{{color:var(--accent3);}}.u-m{{color:var(--accent2);}}.u-l{{color:var(--accent);}}

/* PATH PILLS */
.paths-lbl{{font-family:var(--mono);font-size:.58rem;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;margin-top:12px;}}
.paths-row{{display:flex;flex-wrap:wrap;gap:7px;}}
.path-pill{{
  padding:5px 13px;border-radius:20px;font-size:.76rem;font-weight:600;
  border:1px solid var(--border);background:var(--surface2);color:var(--text);
  transition:all .2s;
}}
.path-pill:hover{{border-color:var(--accent);color:var(--accent);background:var(--glow);}}

/* SUMMARY */
.summary-box{{
  background:var(--bg);border:1px solid var(--border);
  border-radius:calc(var(--r)*.5);padding:11px 13px;margin-top:12px;
  font-size:.83rem;line-height:1.6;color:var(--muted);font-style:italic;
}}

/* RESPONSE BOX */
.resp-box{{
  background:var(--bg);border:1px solid var(--border);
  border-radius:calc(var(--r)*.5);padding:18px;
  font-family:var(--mono);font-size:.8rem;line-height:1.8;
  color:var(--text);white-space:pre-wrap;margin:16px;
}}
.resp-actions{{
  padding:14px 18px;display:flex;gap:8px;align-items:center;
  border-top:1px solid var(--border);
}}

/* STREAMLIT OVERRIDES */
.stTextArea textarea, .stTextInput input, .stSelectbox select {{
  background:var(--bg) !important;border:1px solid var(--border) !important;
  border-radius:calc(var(--r)*.6) !important;color:var(--text) !important;
  font-family:var(--font) !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
  border-color:var(--accent) !important;box-shadow:0 0 0 3px var(--glow) !important;
}}
.stButton>button {{
  background:var(--btn-p) !important;color:#fff !important;
  border:none !important;border-radius:calc(var(--r)*.6) !important;
  font-family:var(--font) !important;font-weight:700 !important;
  transition:transform .2s,box-shadow .2s,filter .2s !important;
}}
.stButton>button:hover {{
  transform:translateY(-2px) !important;
  box-shadow:0 8px 24px var(--glow) !important;filter:brightness(1.1) !important;
}}
label, .stSelectbox label, .stTextArea label, .stTextInput label {{
  font-family:var(--mono) !important;font-size:.62rem !important;
  color:var(--muted) !important;letter-spacing:.1em !important;text-transform:uppercase !important;
}}
.stSelectbox>div>div {{
  background:var(--bg) !important;border:1px solid var(--border) !important;
  color:var(--text) !important;border-radius:calc(var(--r)*.6) !important;
}}
.stAlert{{background:var(--surface) !important;border:1px solid var(--border) !important;}}

/* DIVIDER */
hr{{border-color:var(--border) !important;}}

/* Custom styled selectbox for scenario and tone */
.custom-select-container {{
  display:flex;flex-direction:column;gap:4px;
}}
.custom-select-label {{
  font-family:var(--mono);font-size:.62rem;color:var(--muted);
  letter-spacing:.1em;text-transform:uppercase;margin-left:4px;
}}

/* Action row layout */
.action-row {{
  display:grid;grid-template-columns:auto 1fr 1fr auto;gap:12px;align-items:end;margin-top:16px;
}}
.action-box {{
  display:flex;flex-direction:column;gap:4px;width:100%;
}}

/* FOOTER */
.ea-footer{{
  text-align:center;padding-top:28px;border-top:1px solid var(--border);
  font-family:var(--mono);font-size:.63rem;color:var(--muted);letter-spacing:.1em;
}}
.ea-footer span{{color:var(--accent2);}}

/* TRANSITIONS */
*{{transition:background-color .35s ease,border-color .35s ease,color .2s ease;}}
button,.path-pill{{transition:transform .2s,box-shadow .2s,filter .2s,background .35s,border-color .35s,color .2s !important;}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(12px);}}to{{opacity:1;transform:translateY(0);}}}}
</style>
"""

# ---------------------------- SIDEBAR (EMPTY) ----------------------------
with st.sidebar:
    pass  # Completely empty sidebar as requested

# ---------------------------- INJECT CSS ----------------------------
t = THEMES[st.session_state.theme]
st.markdown(get_css(t), unsafe_allow_html=True)



# ---------------------------- MAIN APP ----------------------------
st.markdown('<div class="ea-wrap">', unsafe_allow_html=True)

# Header with theme selector and model indicator
theme_names = list(THEMES.keys())
col_logo, col_theme, col_model = st.columns([2, 2, 1])

with col_logo:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:42px;height:42px;background:var(--btn-p);border-radius:var(--r);display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 0 20px var(--glow);">📧</div>
        <div>
            <div style="font-size:1.4rem;font-weight:800;letter-spacing:-.02em;background:var(--btn-p);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">ReplyForgeAI</div>
            <div style="font-family:var(--mono);font-size:.62rem;color:var(--muted);letter-spacing:.15em;text-transform:uppercase;">AI-Powered Response Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_theme:
    selected_theme = st.selectbox(
        "Theme",
        options=theme_names,
        index=theme_names.index(st.session_state.theme),
        label_visibility="collapsed",
        key="theme_selector_header",
        format_func=lambda x: f"{x}" if not x.startswith(('🌌','🌸','🌲','🌊','🌅','📄','🔮','❄️','🌋','🍃')) else x
    )
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

with col_model:
    st.markdown(f"""
    <div style="font-family:var(--mono);font-size:.68rem;color:var(--accent2);border:1px solid var(--border);padding:6px 12px;border-radius:20px;text-align:center;white-space:nowrap;">
        ⚡ {MODELS.get(st.session_state.model_choice,'Llama 3.3 70B')}<span class="live-dot"></span>
    </div>
    """, unsafe_allow_html=True)

# Add a small spacer
st.markdown("<br>", unsafe_allow_html=True)

# ---------- TWO COLUMN GRID ----------
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("""
    <div class="ea-panel">
      <div class="ea-panel-hdr">
        <span class="ea-tag tag-i">INPUT</span>
        <span class="ea-panel-title">Paste Your Email</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    email_input = st.text_area(
        "Email Content",
        height=140,
        placeholder="Paste the email content here...",
        key="email_input_area",
        label_visibility="collapsed"
    )

    context_input = st.text_input(
        "One-Line Context",
        placeholder="Brief context about this email...",
        key="context_input_field",
        label_visibility="collapsed"
    )

    col_tone, col_role = st.columns(2)
    with col_tone:
        selected_tone_input = st.selectbox("Tone", ["Formal","Friendly","Professional","Assertive","Neutral"], key="tone_input", label_visibility="collapsed")
    with col_role:
        selected_role = st.selectbox("Role", ["Client","Colleague","Manager","Team Lead","Vendor","Partner"], key="role_input", label_visibility="collapsed")

    if st.button("Analyze Email", use_container_width=True, key="analyze_btn"):
        if email_input or context_input:
            combined = email_input if email_input else context_input
            result = analyze_email_intent(combined, context_input)
            if result:
                st.session_state.analysis_result = result
                st.session_state.email_content = combined
                st.success("✓ Analysis complete!")
        else:
            st.warning("Please paste an email or provide context.")

with col2:
    st.markdown("""
    <div class="ea-panel">
      <div class="ea-panel-hdr">
        <span class="ea-tag tag-a1">SUMMARY</span>
        <span class="ea-panel-title">Intent Analysis</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analysis_result:
        a = st.session_state.analysis_result
        urgency_class = {"High":"u-h","Medium":"u-m","Low":"u-l"}.get(a.get("urgency","Medium"),"u-m")
        paths = a.get("possible_paths", [])
        pills_html = "".join([f'<span class="path-pill">{p}</span>' for p in paths])
        st.markdown(f"""
        <div style="padding:16px 0;">
          <div class="stat-grid">
            <div class="stat-chip"><div class="stat-lbl">Email Type</div><div class="stat-val">{a.get('email_type','N/A')}</div></div>
            <div class="stat-chip"><div class="stat-lbl">Urgency</div><div class="stat-val {urgency_class}">{a.get('urgency','N/A')}</div></div>
            <div class="stat-chip"><div class="stat-lbl">Tone Detected</div><div class="stat-val">{a.get('tone_detected','N/A')}</div></div>
            <div class="stat-chip"><div class="stat-lbl">Decision Needed</div><div class="stat-val">{a.get('decision_needed','N/A')}</div></div>
          </div>
          <div class="paths-lbl">Possible Paths</div>
          <div class="paths-row">{pills_html}</div>
          <div class="summary-box">"{a.get('summary','')}"</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click 'Analyze Email' to see intent analysis")

# ---------- CONTEXT + ACTIONS ----------
st.markdown("""
<div class="ea-panel">
  <div class="ea-panel-hdr">
    <span class="ea-tag tag-c">CONTEXT</span>
    <span class="ea-panel-title">Provide your context here</span>
  </div>
</div>
""", unsafe_allow_html=True)

reasoning = st.text_area(
    "Your Reasoning",
    height=90,
    placeholder="e.g. I need to accept because this is a key client opportunity, but I need to clarify timeline...",
    value=st.session_state.reasoning,
    key="reasoning_input",
    label_visibility="collapsed"
)
if reasoning:
    st.session_state.reasoning = reasoning

possible_paths = ["Accept","Decline","Delay","Ask Clarification"]
if st.session_state.analysis_result:
    possible_paths = st.session_state.analysis_result.get("possible_paths", possible_paths)

# Action row with proper layout
st.markdown('<div class="action-row">', unsafe_allow_html=True)

col_save, col_scenario, col_tone_override, col_generate = st.columns([0.5, 1.5, 1.5, 0.8])

with col_save:
    if st.button("SAVE", key="save_btn", use_container_width=True):
        if reasoning:
            st.success("Saved!")
        else:
            st.warning("Enter reasoning first")


with col_scenario:
    st.session_state.selected_scenario = st.selectbox(
        "Scenario", possible_paths, key="scenario_sel",
        index=0 if "Accept" in possible_paths else 0,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_tone_override:
    st.session_state.selected_tone = st.selectbox(
        "Tone Override", ["Formal","Friendly","Professional","Assertive","Neutral"], key="tone_gen_sel",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_generate:
    if st.button("GENERATE", key="generate_btn", use_container_width=True):
        if st.session_state.email_content and st.session_state.reasoning:
            resp = generate_email_response(
                email_content=st.session_state.email_content,
                reasoning=st.session_state.reasoning,
                scenario=st.session_state.selected_scenario,
                tone=st.session_state.selected_tone,
                context=context_input if context_input else ""
            )
            st.session_state.generated_response = resp
            st.session_state.edit_mode = False
        else:
            st.warning("Analyze an email and provide reasoning first.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- AGENT 2 OUTPUT ----------
st.markdown("""
<div class="ea-panel">
  <div class="ea-panel-hdr">
    <span class="ea-tag tag-a2">GENERATED RESPONSE</span>
    <span class="ea-panel-title">SUGGESTED MESSAGE</span>
  </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.generated_response:
    if st.session_state.edit_mode:
        edited = st.text_area(
            "Edit Response",
            value=st.session_state.generated_response,
            height=220,
            key="edit_area",
            label_visibility="collapsed"
        )
        e1, e2 = st.columns(2)
        with e1:
            if st.button("Save Changes", key="save_edit"):
                st.session_state.generated_response = edited
                st.session_state.edit_mode = False
                st.rerun()
        with e2:
            if st.button("Cancel", key="cancel_edit"):
                st.session_state.edit_mode = False
                st.rerun()
    else:
        st.markdown(f'<div class="resp-box">{st.session_state.generated_response}</div>', unsafe_allow_html=True)

        r1, r2, r3, _ = st.columns([1, 1, 1, 3])
        with r1:
            if st.button("Regenerate", use_container_width=True, key="regen_btn"):
                resp = generate_email_response(
                    email_content=st.session_state.email_content,
                    reasoning=st.session_state.reasoning,
                    scenario=st.session_state.selected_scenario,
                    tone=st.session_state.selected_tone,
                    context=context_input if context_input else ""
                )
                st.session_state.generated_response = resp
                st.rerun()
        with r2:
            if st.button("Edit", use_container_width=True, key="edit_btn"):
                st.session_state.edit_mode = True
                st.rerun()
        with r3:
            if st.button("Copy", use_container_width=True, key="copy_btn"):
                st.markdown(
                    f"""<script>navigator.clipboard.writeText(`{st.session_state.generated_response}`);</script>""",
                    unsafe_allow_html=True
                )
                st.success("Copied!")
else:
    st.info("Configure context and click 'Generate' to create a personalized email response.")

# Footer
st.markdown("""
<div class="ea-footer">
  POWERED BY <span>GROQ</span> &nbsp;•&nbsp; <span>LLAMA 3.3 70B</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)