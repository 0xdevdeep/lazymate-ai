import streamlit as st
import requests
import json
import re

# Set page configuration
st.set_page_config(
    page_title="LazyMate AI - Smart Notes & Task Assistant",
    page_icon="🦥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for a clean, modern productivity dashboard
st.markdown("""
<style>
    /* Global accents and fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container card look */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.6;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }
    
    /* Hero Title styling */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .hero-subtitle {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    
    /* Result card styling */
    .result-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.4);
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Status Badge */
    .status-badge-online {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #ecfdf5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid #a7f3d0;
    }
    
    .status-badge-offline {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #fef2f2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid #fecaca;
    }
    
    .task-progress-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        color: #166534;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to check Ollama connection and fetch local models
def get_ollama_status(base_url="http://localhost:11434"):
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            models = [m.get("name") for m in data.get("models", [])]
            return True, models, None
        return False, [], f"Server returned HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, [], "Could not connect to Ollama service (Connection refused at localhost:11434)."
    except requests.exceptions.Timeout:
        return False, [], "Connection to Ollama timed out."
    except Exception as e:
        return False, [], str(e)

# Helper function to query local Ollama model
def query_ollama(model_name: str, prompt: str, base_url="http://localhost:11434", temperature=0.3):
    url = f"{base_url}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=90)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", ""), None
        elif response.status_code == 404:
            return None, f"Model '{model_name}' was not found in your local Ollama library. Run `ollama pull {model_name}` first."
        else:
            return None, f"Ollama error (HTTP {response.status_code}): {response.text}"
    except requests.exceptions.ConnectionError:
        return None, "Connection refused. Please verify Ollama is actively running."
    except requests.exceptions.Timeout:
        return None, "The request timed out. The local model might still be loading or needs more memory."
    except Exception as e:
        return None, f"Unexpected error during generation: {str(e)}"

# Initialize Session State
if "notes_input" not in st.session_state:
    st.session_state["notes_input"] = ""
if "summary_output" not in st.session_state:
    st.session_state["summary_output"] = ""
if "tasks_output" not in st.session_state:
    st.session_state["tasks_output"] = []
if "task_checked_state" not in st.session_state:
    st.session_state["task_checked_state"] = {}

# Check Ollama status
is_online, installed_models, error_detail = get_ollama_status()

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://api.iconify.design/lucide:zap.svg?color=%236366f1", width=36)
    st.title("LazyMate AI")
    st.caption("Slow & Steady Local Productivity")
    
    st.divider()
    
    # Connection Indicator
    st.subheader("System Status")
    if is_online:
        st.markdown('<div class="status-badge-online">🟢 Ollama Online (Local)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-offline">🔴 Ollama Offline</div>', unsafe_allow_html=True)
        st.caption("Start Ollama on your PC: Run `ollama serve` or open the Ollama app.")
    
    st.write("")
    
    # Model Selection
    st.subheader("Model Configuration")
    
    suggested_models = ["llama3.2:1b", "qwen2.5:0.5b", "llama3.2:3b", "phi3:mini", "mistral"]
    combined_model_list = list(dict.fromkeys(installed_models + suggested_models))
    
    if installed_models:
        default_index = 0
    else:
        default_index = 0
        
    selected_model = st.selectbox(
        "Active Open-Weight Model",
        options=combined_model_list,
        index=default_index,
        help="Models running 100% locally on your machine via Ollama."
    )
    
    if is_online and (selected_model not in installed_models):
        st.warning(f"⚠️ `{selected_model}` is not pulled locally yet.\nRun: `ollama pull {selected_model}` in PowerShell.")
    
    temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.2, step=0.05,
                            help="Lower values are more focused and deterministic for summaries & tasks.")
    
    st.divider()
    
    # Quick Instructions
    with st.expander("ℹ️ Quick Setup Guide"):
        st.markdown("""
        **1. Install Ollama:**
        Download and install from [ollama.com](https://ollama.com).
        
        **2. Pull a lightweight model:**
        ```powershell
        ollama pull llama3.2:1b
        ```
        
        **3. Start Ollama:**
        Ensure the Ollama tray app is running or run `ollama serve`.
        """)

# ================= MAIN DASHBOARD =================
st.markdown('<div class="hero-title">LazyMate AI 🦥</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Transform messy notes and brain dumps into clear summaries and actionable checklists — powered by local, private AI.</div>', unsafe_allow_html=True)

# Sample notes loader for quick testing
col_sample_1, col_sample_2, col_clear = st.columns([1.3, 1.3, 3])
with col_sample_1:
    if st.button("📋 Load Sample: Team Meeting", use_container_width=True):
        st.session_state["notes_input"] = (
            "Team sync notes from Thursday 10am.\n"
            "Discussed launch date for v2.0 - we are aiming for next Friday if QA finishes.\n"
            "Sarah mentioned the checkout page has a bug with Safari browsers, she will patch it by Tuesday.\n"
            "Alex needs to update the Stripe API webhooks to prevent duplicate charges.\n"
            "We also need someone to write the release notes and email the beta testers before Thursday.\n"
            "Budget review got postponed until Monday afternoon. Don't forget to send the updated invoices to accounting."
        )
        st.rerun()

with col_sample_2:
    if st.button("💡 Load Sample: Project Brain Dump", use_container_width=True):
        st.session_state["notes_input"] = (
            "Random ideas for the AI assistant project:\n"
            "- Need to build Streamlit frontend with clean tabs\n"
            "- Connect directly to local Ollama localhost:11434 without external APIs\n"
            "- Must add task extraction so people get an interactive checklist\n"
            "- Write solid README with Windows setup steps for beginners\n"
            "- Test error handling when Ollama is offline or model is missing\n"
            "- Add a button to copy summary to clipboard or export markdown"
        )
        st.rerun()

with col_clear:
    if st.button("🗑️ Clear Input", use_container_width=False):
        st.session_state["notes_input"] = ""
        st.session_state["summary_output"] = ""
        st.session_state["tasks_output"] = []
        st.session_state["task_checked_state"] = {}
        st.rerun()

# Text Area for User Notes
notes = st.text_area(
    "Paste your notes, rough ideas, or meeting transcripts here:",
    height=200,
    placeholder="e.g., Met with client today. They want the landing page revised by Friday. John needs to send over the brand assets by Wednesday noon...",
    key="notes_input"
)

# Action Buttons
col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1.5, 3])

with col_btn1:
    btn_summary = st.button("📝 Generate Summary", use_container_width=True, type="primary")

with col_btn2:
    btn_tasks = st.button("✅ Extract Tasks", use_container_width=True)

with col_btn3:
    btn_all = st.button("⚡ Generate Both (Summary & Tasks)", use_container_width=False)

# Validation logic
def validate_inputs():
    if not notes.strip():
        st.warning("⚠️ **Input is empty!** Please paste or type your notes into the text box above.")
        return False
    if not is_online:
        st.error("🔌 **Ollama is offline or unreachable.**\n\n"
                 "Please start the Ollama application or run `ollama serve` in your terminal, then refresh this page.")
        return False
    return True

# Helper: Parse LLM checklist output into clean items
def parse_action_items(raw_text: str):
    items = []
    lines = raw_text.strip().split("\n")
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        # Remove common bullet points, numbers, checkboxes (e.g. - [ ], - [x], 1., -, *)
        cleaned = re.sub(r"^(\d+[\.\)]|\-|\*|\s|\[[\s\*xX]?\])+", "", cleaned).strip()
        # Clean markdown bold headers that are not tasks
        if cleaned.lower().startswith("actionable tasks:") or cleaned.lower().startswith("tasks:") or cleaned.lower().startswith("action items:"):
            continue
        if len(cleaned) > 2:
            items.append(cleaned)
    return items

# Execute Generation
if btn_summary or btn_all:
    if validate_inputs():
        with st.spinner(f"🦥 Thinking... Generating concise summary with `{selected_model}`"):
            summary_prompt = (
                "You are LazyMate AI, an expert productivity assistant.\n"
                "Your task is to provide a concise, clear, and well-structured summary of the following notes.\n"
                "Focus on the core message, decisions made, and key context.\n"
                "Keep it easy to read in 2 to 4 bullet points or a brief paragraph.\n\n"
                f"Notes:\n{notes}\n\nSummary:"
            )
            response, err = query_ollama(selected_model, summary_prompt, temperature=temperature)
            if err:
                st.error(f"❌ {err}")
            else:
                st.session_state["summary_output"] = response

if btn_tasks or btn_all:
    if validate_inputs():
        with st.spinner(f"🦥 Extracting actionable tasks with `{selected_model}`"):
            tasks_prompt = (
                "You are LazyMate AI, an expert productivity assistant.\n"
                "Your task is to extract all actionable tasks, to-dos, and assignments from the notes below.\n"
                "Rules:\n"
                "1. Each task must begin with a strong action verb.\n"
                "2. Include who is responsible or any deadlines mentioned, if available.\n"
                "3. Output strictly one task per line starting with a bullet (- ).\n"
                "4. Do NOT include any conversational preamble or outro.\n\n"
                f"Notes:\n{notes}\n\nTasks:"
            )
            response, err = query_ollama(selected_model, tasks_prompt, temperature=temperature)
            if err:
                st.error(f"❌ {err}")
            else:
                parsed_tasks = parse_action_items(response)
                st.session_state["tasks_output"] = parsed_tasks
                # Reset task completion state for new tasks
                st.session_state["task_checked_state"] = {i: False for i in range(len(parsed_tasks))}

# ================= RESULTS DISPLAY =================
st.divider()

col_summary_display, col_tasks_display = st.columns(2)

with col_summary_display:
    st.subheader("📌 Summary")
    if st.session_state["summary_output"]:
        st.markdown(st.session_state["summary_output"])
    else:
        st.info("Paste your notes and click **Generate Summary** to see key takeaways here.")

with col_tasks_display:
    st.subheader("📋 Actionable Checklist")
    tasks = st.session_state["tasks_output"]
    
    if tasks:
        # Progress counter
        completed_count = sum(1 for val in st.session_state["task_checked_state"].values() if val)
        total_count = len(tasks)
        progress_ratio = completed_count / total_count if total_count > 0 else 0
        
        st.progress(progress_ratio, text=f"Progress: {completed_count} of {total_count} tasks completed")
        
        # Interactive checklist
        for idx, task_text in enumerate(tasks):
            checked = st.checkbox(
                task_text,
                key=f"task_chk_{idx}",
                value=st.session_state["task_checked_state"].get(idx, False)
            )
            st.session_state["task_checked_state"][idx] = checked
            
        # Export options
        st.write("")
        tasks_as_markdown = "\n".join([f"- [{'x' if st.session_state['task_checked_state'].get(i, False) else ' '}] {t}" for i, t in enumerate(tasks)])
        st.download_button(
            label="💾 Download Checklist (.md)",
            data=f"# Action Items\n\n{tasks_as_markdown}",
            file_name="lazymate_tasks.md",
            mime="text/markdown"
        )
    else:
        st.info("Click **Extract Tasks** to turn messy notes into an interactive to-do checklist.")
