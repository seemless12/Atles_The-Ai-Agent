# Atlas | Crypto Intelligence Agent

Atlas is a professional-grade AI-driven crypto analyst platform. This project integrates LangChain, OpenRouter, and a modern Flask-based web interface to provide real-time market data analysis and conversational insights.

## 🚀 Project Evolution Summary

### 1. Environment & Backend Setup
- **Dependency Management**: Updated `requirements.txt` to include essential libraries: `flask`, `flask-cors`, `requests`, `langchain`, and `langchain-openai`.
- **API Integration**: Configured OpenRouter for LLM access (LLama 3.1) and FreeCrypto API for real-time market conversions.
- **Context Layering**: Integrated a multi-stage system prompt and a markdown-based crypto knowledge base for specialized domain awareness.

### 2. Premium Frontend Redesign
- **Aesthetic Overhaul**: Implemented a "Premium Dark" theme with **Glassmorphism**, neon glow effects, and modern typography (Outfit & Inter fonts).
- **Floating Chat Widget**: Replaced the static chat panel with a floating interactive bubble in the bottom right corner.
- **Interactive UI**: Added micro-animations, pulse effects for the chat bubble, and smooth panel transitions.
- **Favicon**: Integrated a custom-generated AI icon for browser tab branding.

### 3. Feature Enhancements
- **Atlas v3 Engine**: Upgraded the system prompt to enforce strict data integrity, source consistency, and **Confidence Scoring** (0.00 - 1.00) for all AI responses.
- **Mobile Responsiveness**: Optimized the layout for mobile devices, ensuring the chat widget stays within the viewport.
- **Clearing Terminal**: Added functionality to clear the chat history and reset the AI session.

### 4. Verification & Testing
- **Automated Browser Testing**: Used agentic browser tools to verify landing page elements, responsive positioning, and interactive states.
- **End-to-End Chat Flow**: Verified the connection between the frontend UI, Flask backend, and the LangChain executor.

## 🛠️ Project Structure

- `app.py`: Flask server and API endpoints.
- `chatbot.py`: LangChain logic, tool definitions, and agent executor.
- `index.html`: The modern landing page.
- `style.css`: Premium glassmorphism design system.
- `script.js`: Frontend logic for chat interactions and UI state.
- `systemprompt.txt`: The "brains" of the agent, defining behavioral rules (Atlas v3).
- `requirements.txt`: Python package dependencies.

## 🚦 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Ensure `.env` contains:
   - `OPENROUTER_API_KEY`
   - `FREECRYPTO_API_KEY`

3. **Start the Agent**:
   ```bash
   python app.py
   ```

4. **Access UI**:
   Open [http://localhost:5000](http://localhost:5000) in your browser.

---
*Created and refined by Antigravity AI.*
