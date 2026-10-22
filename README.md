# LazyMate AI 🦥✨
> **The Slow & Steady Local Productivity Assistant**  
> *Submitted for the Hacktoberfest Open-Source AI Challenge — Week 3: Slow and Steady.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39%2B-FF4B4B.svg)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-black.svg)](https://ollama.com)

**LazyMate AI** is a lightweight, privacy-first productivity dashboard that turns unstructured, messy notes, brainstorms, and meeting transcripts into crisp summaries and actionable to-do checklists — running **100% locally on your computer**.

No paid API keys, no recurring subscriptions, and zero telemetry.

---

## 🧭 Why "Slow and Steady"? The Open-Source AI & Privacy Advantage

In an era of hyper-scale cloud AI with continuous data harvesting, vendor lock-in, and unpredictable API fees, **LazyMate AI** embraces the *"Slow and Steady"* philosophy of sustainable, self-reliant personal computing:

- 🔒 **Total Privacy & Zero Data Leakage**: Your sensitive notes, client deliverables, and private thoughts never leave your local machine. No external servers or LLM providers retain your data for model training.
- 💸 **Zero Subscription or Token Cost**: Powered by open weights. Run thousands of queries without paying per-token charges or watching credit balances expire.
- 📴 **100% Offline Capability**: Once your open-weight model is pulled locally, LazyMate AI works seamlessly anywhere — on a flight, in a cafe, or during network outages.
- ⚡ **Lightweight & Accessible**: Designed specifically for small, efficient open-weight models (e.g., `llama3.2:1b` or `qwen2.5:0.5b`) that run smoothly on standard laptops without requiring a high-end dedicated GPU.
- 🛠️ **Full User Ownership**: You own the code, the model weights, and the inference environment.

---

## ✨ Key Features

- 📝 **Messy Notes Summarizer**: Condenses rambling, unformatted notes and meeting transcripts into 2–4 concise bullet points highlighting core decisions and context.
- ✅ **Actionable Checklist Extractor**: Automatically detects tasks, assignments, and deadlines, extracting them into an interactive to-do list.
- 📊 **Live Task Progress Tracking**: Interactive checkboxes with dynamic progress bars calculating completion percentage in real time.
- 🟢 **Real-Time Ollama Health Monitor**: Instant visual connection badges (`🟢 Ollama Online` / `🔴 Ollama Offline`) with automated local model discovery.
- 🎯 **One-Click Test Samples**: Built-in sample buttons ("Team Meeting" and "Project Brain Dump") for immediate testing without typing.
- 💾 **Export to Markdown**: Download your parsed checklist as a clean `.md` file for GitHub Issues, Obsidian, Notion, or personal task managers.
- 🛡️ **Graceful Error Handling**: Helpful, beginner-friendly alerts when input is missing, models are not yet pulled, or Ollama is offline.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend UI** | [Streamlit](https://streamlit.io/) | Fast, responsive, and reactive web dashboard |
| **Local AI Engine** | [Ollama](https://ollama.com/) | High-performance local open-weight model runner |
| **Inference Protocol** | REST (`localhost:11434`) | Direct, asynchronous HTTP communication with Ollama |
| **Programming Language** | Python 3.10+ | Core application logic and text parsing |
| **Recommended Models** | `llama3.2:1b`, `qwen2.5:0.5b`, `llama3.2:3b`, `phi3:mini` | Compact, high-efficiency open weights |

---

## 🪟 Windows Setup Instructions (Step-by-Step)

Follow these steps in **PowerShell** to set up and run LazyMate AI on Windows:

### Step 1: Install Ollama (If not already installed)
1. Download Ollama for Windows from [ollama.com/download/windows](https://ollama.com/download/windows).
2. Run `OllamaSetup.exe`. Once installed, Ollama runs in your Windows system tray.
3. Open a PowerShell terminal and verify:
   ```powershell
   ollama --version
   ```

### Step 2: Pull a Small Open-Weight Model
Pull a fast, lightweight open-weight model (e.g., Llama 3.2 1B):
```powershell
ollama pull llama3.2:1b
```
> **Tip for lower-RAM machines**: You can also use `ollama pull qwen2.5:0.5b` (~400 MB).

### Step 3: Create & Activate a Python Virtual Environment
In the `LazyMate-AI` directory, create and activate an isolated virtual environment:
```powershell
# Create virtual environment
python -m venv venv

# If script execution is restricted in PowerShell, run this once:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```
*(Your command prompt will display `(venv)` once activated).*

### Step 4: Install Dependencies
Install the required packages strictly inside the virtual environment:
```powershell
pip install -r requirements.txt
```

### Step 5: Launch LazyMate AI
Start the application server:
```powershell
streamlit run app.py
```

Your default web browser will automatically open:
```text
http://localhost:8501
```

---

## 🚀 How to Run the App (Quick Reference)

Once initial installation is complete, starting the app takes just two commands:

```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Run Streamlit
streamlit run app.py
```

---

## 💡 How to Use

1. **Verify Connection**: Look at the sidebar status badge. If Ollama is running, it will show **🟢 Ollama Online (Local)**.
2. **Select Model**: Choose `llama3.2:1b` (or your preferred installed model) from the dropdown.
3. **Input Notes**:
   - Paste your meeting notes or raw thoughts into the text area.
   - Or click **📋 Load Sample: Team Meeting** for an instant demo.
4. **Choose an Action**:
   - Click **📝 Generate Summary** for high-level bullet points.
   - Click **✅ Extract Tasks** to generate an interactive checklist.
   - Click **⚡ Generate Both** to run both operations.
5. **Track & Export**: Check off tasks as you finish them, and click **💾 Download Checklist (.md)** to save your tasks.

---

## 📂 Project Structure

```text
LazyMate-AI/
├── .gitignore          # Comprehensive rules excluding venv, caches, and secrets
├── LICENSE             # Open-source MIT License
├── README.md           # Project documentation and Hacktoberfest submission guide
├── requirements.txt    # Python dependencies (Streamlit, Ollama, Requests)
└── app.py              # Main Streamlit dashboard application
```

---

## 🤝 Contributing for Hacktoberfest

Contributions are welcome! If you would like to help improve LazyMate AI:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Commit your changes (`git commit -m 'Add awesome feature'`).
4. Push to the branch (`git push origin feature/awesome-feature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this project.
