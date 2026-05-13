# AI Assistant Platform for E-commerce

An integrated, multimodal AI suite that empowers sellers with instant, high-converting marketing content and provides customers with an intelligent, agentic support experience.

## 🧭 Architecture Diagram

```mermaid
flowchart TB
    User([👤 User]):::user

    subgraph UI["🖥️ Streamlit UI (app.py)"]
        Page1["📸 Content Generator Page"]
        Page2["🤖 Customer Support Page"]
    end

    subgraph M1["📦 Module 1 — Content Generator"]
        direction TB
        Vision["vision.py<br/>Multimodal Attribute Extraction<br/>(Structured JSON Schema)"]
        TextGen["text_gen.py<br/>SEO + Marketing Copy"]
        Banner["banner.py<br/>Banner Render + PIL Overlay"]
        Parallel{{"concurrent.futures<br/>Parallel Execution"}}
    end

    subgraph M2["🛠️ Module 2 — Customer Support Agent"]
        direction TB
        Agent["agent.py<br/>LangGraph ReAct Loop"]
        Tools["tools.py"]
        T1["🔍 get_order_status"]
        T2["📚 search_knowledge_base"]
        T3["🚨 escalate_to_human"]
    end

    subgraph Shared["⚙️ Shared Layer"]
        LLM["shared/llm_client.py<br/>Gemini Client"]
        Cfg["shared/config.py<br/>Env Loader"]
    end

    subgraph Data["💾 Data & External Services"]
        Gemini[("Google Gemini API")]
        Pollinations[("Pollinations.ai<br/>Image Gen API")]
        SQLite[("SQLite<br/>data/orders.db")]
        Chroma[("ChromaDB<br/>data/chromadb/")]
        Tickets[("tickets.json")]
        HF["HuggingFace<br/>all-MiniLM-L6-v2"]
    end

    User --> Page1 & Page2

    Page1 --> Vision
    Vision --> Parallel
    Parallel --> TextGen
    Parallel --> Banner
    TextGen --> Page1
    Banner --> Page1

    Page2 --> Agent
    Agent <--> Tools
    Tools --> T1 --> SQLite
    Tools --> T2 --> Chroma
    Tools --> T3 --> Tickets
    Chroma -.embeds via.-> HF
    Agent --> Page2

    Vision -.uses.-> LLM
    TextGen -.uses.-> LLM
    Agent -.uses.-> LLM
    LLM --> Gemini
    Banner --> Pollinations
    LLM -.reads.-> Cfg

    classDef user fill:#fef3c7,stroke:#d97706,color:#000
    classDef ui fill:#dbeafe,stroke:#2563eb,color:#000
    classDef mod fill:#dcfce7,stroke:#16a34a,color:#000
    classDef shared fill:#f3e8ff,stroke:#9333ea,color:#000
    classDef data fill:#fee2e2,stroke:#dc2626,color:#000

    class Page1,Page2 ui
    class Vision,TextGen,Banner,Parallel,Agent,Tools,T1,T2,T3 mod
    class LLM,Cfg shared
    class Gemini,Pollinations,SQLite,Chroma,Tickets,HF data
```

**Flow summary:**
- **Module 1:** Image upload → Gemini Vision (structured JSON) → parallel branches: (a) Gemini text generation for SEO copy, (b) Pollinations.ai banner render with PIL overlay.
- **Module 2:** User message → LangGraph ReAct agent (Gemini) reasons over three tools — SQLite order lookup, ChromaDB RAG over policy docs, and escalation ticketing — chaining them as needed before responding.

## ✨ Features

### 📸 Content Generator (Task 2)
* **Multimodal Vision Analysis:** Accurately extracts product materials, colors, and stylistic categories from raw images.
* **SEO & Marketing Copy:** Generates highly targeted titles, bulleted features, and engaging product descriptions.
* **Automated Banner Design:** Programmatically generates 16:9 promotional banners via Pollinations.ai with professional text overlays.
* **Concurrent Generation:** Executes text copywriting and image rendering in parallel, cutting user wait time in half.

### 🤖 Customer Support Agent (Task 1)
* **Agentic Tool Calling:** Uses a LangGraph ReAct loop to autonomously decide when to query databases versus searching policy documents.
* **Real-time Order Tracking:** Directly queries a local SQLite database to retrieve and format complex order statuses and histories.
* **RAG-powered Policy Answers:** Retrieves exact policy details (shipping, returns, warranty) from a persistent ChromaDB vector store.
* **Intelligent Escalation:** Automatically detects legal threats, intense anger, or out-of-scope requests and logs them to a human-review ticket system.

## 🛠️ Tech Stack

* **UI:** Streamlit (`>=1.57.0`)
* **LLM Integration:** Google GenAI SDK (`google-genai>=2.2.0`), Langchain (`>=1.3.0`)
* **Agent Framework:** LangGraph (`>=1.1.10`)
* **Vector Store:** ChromaDB (`>=1.5.9`)
* **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (`>=5.4.1`)
* **Image Processing:** Pillow (`>=12.2.0`)
* **Database:** SQLite (Python standard library)

## 🏗️ Architecture

**Content Generator (Module 1):** The pipeline is triggered by an image upload. We utilize `LLM` with a strict JSON schema to perform a highly factual visual analysis of the product. The resulting JSON attributes are then passed into `LLM` to draft the SEO and marketing copy. Simultaneously, a dynamic prompt is built from those visual attributes and sent to the Pollinations.ai image generation API. We use Python's `concurrent.futures` to run the text generation and image generation in parallel. Finally, Pillow (PIL) is used to composite the generated product title over the banner image.

**Customer Support Agent (Module 2):** This module relies on a LangGraph ReAct (Reasoning and Acting) architecture powered by `LLM`. The agent is given access to three distinct tools: a SQL querying tool (`get_order_status`), a RAG semantic search tool (`search_knowledge_base`), and a ticketing tool (`escalate_to_human`). When a user sends a message, the LLM enters a loop where it reasons about the user's intent, executes the necessary tools (often chaining them together, like looking up an order *then* checking the return policy), and finally synthesizes the tool outputs into a conversational response.

## 🚀 Setup

```bash
# Clone the repository
git clone https://github.com/thepratyushranjan/CommerceTwinAI.git
cd CommerceTwinAI

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Initialize databases
python scripts/seed_orders.py
python scripts/ingest_docs.py

# Run the application
streamlit run app.py
```

## 🎥 Demo

[Watch the Demo Video](https://drive.google.com/file/d/17S22EwTDxkrvEb-LRhi-TYOeAVHB3oW2/view?usp=sharing)

## 📂 Project Structure

```text
ai-assistant-platform/
├── app.py                              # Platform landing page
├── pages/
│   ├── 1_Content_Generator.py          # Content Gen UI
│   └── 2_Customer_Support.py           # Customer Support UI
├── modules/
│   ├── content/                        
│   │   ├── banner.py                   # Image generation & PIL overlay
│   │   ├── text_gen.py                 # Marketing copy generation
│   │   └── vision.py                   # Multimodal attribute extraction
│   └── support/                        
│       ├── agent.py                    # LangGraph ReAct setup
│       └── tools.py                    # SQLite, ChromaDB, Escalation tools
├── data/
│   ├── orders.db                       # SQLite Database (generated)
│   ├── docs/                           # FAQ Markdown files
│   └── chromadb/                       # Vector embeddings (generated)
├── scripts/
│   ├── seed_orders.py                  # Database seeder
│   └── ingest_docs.py                  # RAG ingestion script
├── shared/
│   ├── llm_client.py                   # Unified Gemini client config
│   └── config.py                       # Environment loader
└── README.md
```

## 💬 Sample Queries (Customer Support)

Test the agent's reasoning capabilities with these queries:

1. **Order Lookup:** *"Where is my order ORD-1005?"* (Expected: Calls `get_order_status`, returns pending/shipped details).
2. **Policy RAG:** *"What is your return policy?"* (Expected: Calls `search_knowledge_base`, cites the 30-day window).
3. **Multi-Tool Reasoning:** *"I want to return ORD-1003, what's your policy?"* (Expected: Calls BOTH `get_order_status` to check the order, and `search_knowledge_base` to check the rules).
4. **Out of Scope:** *"What is the weather today?"* (Expected: Politely declines, no tools called).
5. **Implicit Escalation:** *"I'm going to sue you, my package never arrived!"* (Expected: Detects threat, calls `escalate_to_human`, returns a TKT ID).

## 🧠 Design Decisions

**Why a single ReAct agent with tools instead of multi-agent?**
For this specific scope (order tracking and FAQ retrieval), a single ReAct loop is significantly faster, easier to debug, and less prone to infinite loops than a multi-agent system (like AutoGen or CrewAI). A single agent with well-defined docstrings on its tools is highly effective at routing basic e-commerce intents without the overhead of inter-agent communication.

**Why ChromaDB over Pinecone for this assessment?**
ChromaDB was chosen to strictly adhere to the "Zero Docker/Zero external infrastructure" requirement. Because it runs embedded in Python via SQLite and Parquet, it allows evaluators to run the setup scripts and immediately test the RAG functionality without needing to sign up for cloud API keys or configure network access policies.

**Why Gemini over OpenAI?**
The Gemini API provides an incredible developer experience for this specific assessment. Gemini 2.5 Pro offers native, high-quality multimodal vision out-of-the-box, which was critical for Task 2. Furthermore, the new `google-genai` SDK allows us to pass Pydantic schemas directly into the generation config, ensuring perfect JSON structured outputs without relying on brittle third-party parsers like LangChain's OutputParsers.

**How structured JSON outputs reduce hallucination in the Vision module.**
By forcing the vision model to adhere to a strict JSON schema (e.g., `primary_color_hex`, `materials` array), we constrain its generation space. It stops the model from hallucinating poetic but useless descriptions (e.g., "A beautiful, ethereal shoe") and forces it into an analytical state ("Material: Leather, Color: #FFFFFF"), which directly improves the quality of the downstream marketing copy.

## 🔮 What I'd Add With More Time

* **Streaming UI for Content Generation:** Instead of spinners, stream the text copy into the UI chunk-by-chunk so the user feels immediate progress while waiting on the image generation API.
* **pgvector Migration:** Move from local SQLite/Chroma to PostgreSQL with `pgvector` so relational order data and vector FAQ data live in the same unified database.
* **Human-in-the-Loop Escalation UI:** Build a third Streamlit page for "Support Managers" to view and resolve the tickets generated in `tickets.json`.
* **Dynamic Tool Selection:** Implement an embedding-based tool retriever for the agent. If the toolset grows to 50+ tools, passing all of them in the prompt becomes too expensive.
* **User Authentication:** Add session state login so users don't have to type their email or Order ID; the agent would automatically know who they are via context.

## 📸 Screenshots

![Screenshot 1](assets/screenshots/1.png)
![Screenshot 2](assets/screenshots/2.png)
![Screenshot 3](assets/screenshots/3.png)
![Screenshot 4](assets/screenshots/4.png)
![Screenshot 5](assets/screenshots/5.png)
![Screenshot 6](assets/screenshots/6.png)
![Screenshot 7](assets/screenshots/7.png)
![Screenshot 8](assets/screenshots/8.png)
![Screenshot 9](assets/screenshots/9.png)
![Screenshot 10](assets/screenshots/10.png)
![Screenshot 11](assets/screenshots/11.png)
![Screenshot 12](assets/screenshots/12.png)
![Screenshot 13](assets/screenshots/13.png)