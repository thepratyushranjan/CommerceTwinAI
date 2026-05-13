# AI Assistant Platform for E-commerce

An integrated AI-powered suite designed to streamline e-commerce operations. 

**Current Status:** ✅ Phase 1 Complete (Content Generator). Phase 2 (Customer Support Agent) is pending.

## ✨ Features

### 📸 Content Generator (Completed - Task 2)
Transform raw product images into complete, high-converting marketing packages instantly.
* **Multimodal Vision Analysis:** Automatically extracts product categories, materials, colors, and stylistic attributes using `gemini-2.5-pro`.
* **SEO & Marketing Copy:** Generates SEO-optimized titles, engaging descriptions, and feature bullet points using `gemini-2.5-flash`.
* **Social Media Kits:** Creates targeted Instagram and Twitter/X captions with relevant hashtags.
* **Automated Banner Design:** Generates 16:9 promotional banners matching the product's aesthetic, complete with professional text overlays.

### 🤖 Customer Support Agent (Pending - Task 1)
* *Planned:* Agentic chatbot handling customer inquiries using RAG (ChromaDB) and tool calling (SQLite order tracking).

## 🛠️ Tech Stack

* **UI:** Streamlit (Multi-page app with modern layouts)
* **LLM Provider:** Google GenAI SDK (`google-genai`)
* **Vision Model:** Gemini 2.5 Pro (Configured with low temperature for strict factual extraction)
* **Text Model:** Gemini 2.5 Flash
* **Banner Generation:** Pollinations.ai API + Pillow (PIL) for compositing
* **Concurrency:** Python `concurrent.futures` for parallel asset generation

## 🏗️ Architecture (Content Generator)
1. **Upload:** User uploads an image via the Streamlit UI.
2. **Analysis:** The image is sent to Gemini 2.5 Pro with a strict JSON schema to extract product attributes.
3. **Parallel Generation:** 
   * The extracted attributes are sent to Gemini 2.5 Flash to generate marketing text.
   * Simultaneously, a dynamic prompt is built and sent to an image generation API, followed by a Pillow script adding the product title as an overlay.
4. **Presentation:** Results are displayed in a clean, tabbed Streamlit interface with 1-click copy buttons and metric dashboards.

## 🚀 How to Run the Project

Follow these steps to run the application on your local machine:

### 1. Prerequisites
Make sure you have Python 3.11+ installed.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-assistant-platform

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the example environment file and add your Google Gemini API key. You can get a free key from [Google AI Studio](https://aistudio.google.com).
```bash
cp .env.example .env
```
Open `.env` and set your key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```
*The application will open automatically in your default web browser at `http://localhost:8501`.*

## 📂 Project Structure

```text
ai-assistant-platform/
├── app.py                              # Main Streamlit landing page
├── pages/
│   ├── 1_Content_Generator.py          # ✅ Task 2: Content Gen UI
│   └── 2_Customer_Support.py           # ⏳ Task 1: Support UI (Pending)
├── modules/
│   ├── content/                        # Content Generator Backend
│   │   ├── banner.py                   # Image generation & PIL overlay
│   │   ├── text_gen.py                 # Marketing copy generation
│   │   └── vision.py                   # Multimodal attribute extraction
├── prompts/                            # System prompts & strict JSON schemas
│   ├── text_gen_schema.json
│   └── vision_schema.json
├── shared/
│   ├── config.py                       # Environment validation
│   └── llm_client.py                   # Centralized Gemini GenAI client
├── requirements.txt
└── README.md
```

## 🧠 Design Decisions

* **Modern SDK & Strict Typing:** Migrated to the latest `google-genai` SDK to utilize native `response_schema` parameters. This guarantees the LLM outputs strict JSON, eliminating brittle string parsing and formatting errors.
* **Intelligent Fallbacks:** The Vision module is configured with exponential backoffs and automatic model switching (from Pro to Flash) to gracefully handle API rate limits and "503 Deadline Exceeded" errors common with heavy image processing.
* **Parallel Processing:** Text generation and banner generation execute concurrently via `ThreadPoolExecutor`, effectively cutting the user wait time in half.
* **UX/UI Polish:** Implemented `st.tabs`, metrics blocks, and clean code blocks in Streamlit to transform raw data outputs into a professional, dashboard-like experience.