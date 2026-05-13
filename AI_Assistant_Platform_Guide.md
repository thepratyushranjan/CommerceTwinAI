# AI Assistant Platform for E-commerce
### 24-Hour Implementation Guide — AI Developer Assessment

A single Streamlit application combining both assessment tasks into one cohesive product. Framed as an **AI Assistant Platform for E-commerce** with two modules:

- **Content Generator** (Task 2) — seller-facing: upload a product image, get complete marketing copy and a promotional banner.
- **Customer Support** (Task 1) — customer-facing: agentic chatbot answering queries using RAG and tool calling.

This framing turns two unrelated tasks into one coherent product story, which scores significantly higher than two disconnected apps.

---

## Table of Contents

1. [Tech Stack](#1-tech-stack-locked-in)
2. [Project Structure](#2-project-structure)
3. [Architecture Overview](#3-architecture-overview)
4. [The 24-Hour Timeline](#4-the-24-hour-timeline)
5. [Phase 0 — Project Setup](#5-phase-0--project-setup-hour-0-1)
6. [Phase 1 — Task 2 Content Generator](#6-phase-1--task-2-content-generator-hour-1-7)
7. [Phase 2 — Task 1 Customer Support](#7-phase-2--task-1-customer-support-hour-10-18)
8. [Phase 3 — Polish & Submission](#8-phase-3--polish--submission-hour-18-22)
9. [Risk Mitigation & Cut List](#9-risk-mitigation--cut-list)
10. [Reference: Prompts & Schemas](#10-reference-prompts--schemas)
11. [Submission Checklist](#11-submission-checklist)

---

## 1. Tech Stack (Locked In)

**Do not deviate from this stack during the 24 hours. Every alternative tool you consider costs you 30 minutes of decision time you don't have.**

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11 | Standard for AI work, all libraries support it |
| UI | Streamlit (multi-page) | Built-in chat, file upload, session state — zero frontend code |
| LLM Provider | Google Gemini API | Generous free tier, native multimodal, native JSON mode, one SDK |
| Vision Model | `gemini-2.5-pro` | Multimodal, structured outputs, best vision quality on free tier |
| Text Generation | `gemini-2.5-flash` | Fast and cheap for non-vision text tasks |
| Agent Framework | LangGraph (`create_react_agent`) | Prebuilt ReAct agent, minimal boilerplate |
| Vector Store | ChromaDB (persistent local) | Zero setup, no Docker needed |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Local, free, fast |
| Mock Database | SQLite | Built into Python, zero install |
| Image Generation | Pollinations.ai (no auth) OR Gemini Imagen | Pollinations is fastest fallback if API access is limited |
| Image Composition | Pillow (PIL) | Standard library for adding text overlay on banner |
| Config | python-dotenv | Standard pattern for API keys |

### `requirements.txt`

```
streamlit>=1.32.0
google-generativeai>=0.5.0
langgraph>=0.2.0
langchain>=0.2.0
langchain-google-genai>=1.0.0
chromadb>=0.4.22
sentence-transformers>=2.5.0
Pillow>=10.0.0
python-dotenv>=1.0.0
requests>=2.31.0
pydantic>=2.5.0
```

### `.env.example`

```
GOOGLE_API_KEY=your_gemini_api_key_here
# Optional fallback for image generation
STABILITY_API_KEY=your_stability_key_if_using
```

Get a free Gemini API key from [https://aistudio.google.com](https://aistudio.google.com). Takes 30 seconds.

---

## 2. Project Structure

```
ai-assistant-platform/
├── app.py                              # Landing page with module cards
├── pages/
│   ├── 1_Content_Generator.py          # Task 2 UI
│   └── 2_Customer_Support.py           # Task 1 UI
├── modules/
│   ├── __init__.py
│   ├── content/
│   │   ├── __init__.py
│   │   ├── vision.py                   # Vision analysis function
│   │   ├── text_gen.py                 # Text content generation
│   │   └── banner.py                   # Banner image generation
│   └── support/
│       ├── __init__.py
│       ├── agent.py                    # LangGraph agent setup
│       ├── tools.py                    # 3 agent tools
│       └── rag.py                      # ChromaDB retrieval
├── shared/
│   ├── __init__.py
│   ├── llm_client.py                   # Gemini client setup
│   └── config.py                       # Loads env vars
├── data/
│   ├── orders.db                       # SQLite (generated)
│   ├── docs/                           # FAQ markdown files
│   │   ├── return_policy.md
│   │   ├── shipping_faq.md
│   │   ├── warranty.md
│   │   └── ... (8-10 files total)
│   ├── chromadb/                       # Persisted vector store
│   └── tickets.json                    # Escalation log
├── scripts/
│   ├── seed_orders.py                  # Populate SQLite with fake orders
│   └── ingest_docs.py                  # Load FAQs into ChromaDB
├── prompts/
│   ├── vision_schema.json              # Product attribute schema
│   ├── text_gen_schema.json            # Marketing content schema
│   └── agent_system.txt                # Customer support agent prompt
├── assets/                             # Screenshots, demo gif
├── .env.example
├── .env                                # Never commit
├── .gitignore
├── requirements.txt
└── README.md
```

### `.gitignore` essentials

```
.env
__pycache__/
*.pyc
data/orders.db
data/chromadb/
data/tickets.json
venv/
.streamlit/secrets.toml
```

---

## 3. Architecture Overview

The application has three layers shared across both modules:

**Shared infrastructure layer.** A single Gemini client in `shared/llm_client.py` is imported by both modules. Configuration loads once from `.env`. This means one place to swap providers if anything goes wrong.

**Module layer.** Each module is self-contained in `modules/`. The content module exposes three functions: `analyze_image()`, `generate_text_content()`, `generate_banner()`. The support module exposes two functions: `get_agent()` and `format_trace()`. Modules don't import from each other.

**UI layer.** Streamlit's `pages/` folder auto-creates sidebar navigation. The landing page (`app.py`) is a short hero section with two cards linking to each module.

### Content Generator flow (Task 2)

```
Image upload → Vision call (returns JSON of attributes)
            → Text generation (one call returns all 6 text fields)
            → Banner generation (image API + PIL overlay)
            → Display in Streamlit with copy/download buttons
```

### Customer Support flow (Task 1)

```
Chat message → LangGraph agent (ReAct loop)
             → Tool selection (search_kb / get_order / escalate)
             → Tool execution against ChromaDB or SQLite
             → Agent composes response
             → Stream to UI + log trace to sidebar
```

The detailed component diagrams for both modules were shared earlier in the design doc. Drop screenshots of those into your README in the Architecture section.

---

## 4. The 24-Hour Timeline

This is a hard plan. Set a timer for each phase.

| Hours | Phase | Deliverable |
|---|---|---|
| 0 – 1 | Setup & scaffolding | Streamlit app runs, Gemini "hello" call works |
| 1 – 7 | Task 2 build | Content Generator fully functional |
| 7 – 10 | **Sleep** | (Non-negotiable. You write better code rested.) |
| 10 – 12 | Task 1 data seed | SQLite seeded, FAQs ingested into ChromaDB |
| 12 – 18 | Task 1 agent build | Agent answers all sample queries correctly |
| 18 – 21 | Polish & README | Screenshots, demo, written README |
| 21 – 23 | Demo video & final test | 60-90 second recording uploaded |
| 23 – 24 | Buffer + submit | Submit and rest |

**The 7-10 sleep block is the highest-leverage decision in this whole plan.** Skipping it produces buggy Task 1 code that takes 50% longer to debug than rested code. Trust this.

---

## 5. Phase 0 — Project Setup (Hour 0-1)

### Step 1: Initialize the repo (10 min)

Create the project folder, set up a virtual environment, install dependencies, and create the directory structure exactly as shown in Section 2. Initialize git on first commit.

### Step 2: Get the Gemini API key working (10 min)

Sign up at aistudio.google.com, copy your API key into `.env`. Write a 5-line test script that imports `google.generativeai`, configures it with the key, and prints the response to "Say hello". Don't move on until this works. If it doesn't work in 10 minutes, your `.env` isn't being loaded — debug with `print(os.getenv("GOOGLE_API_KEY"))`.

### Step 3: Build the shared LLM client (10 min)

In `shared/llm_client.py`, create two functions: one that returns a configured Gemini model for vision (`gemini-2.5-pro`), one for text-only (`gemini-2.5-flash`). Both should accept a `system_instruction` parameter. This is your only LLM abstraction — every other module imports from here.

### Step 4: Streamlit landing page (15 min)

In `app.py`, write a short hero with the project name "AI Assistant Platform for E-commerce", a one-paragraph description, and two cards (use `st.columns(2)` and `st.container(border=True)`) describing each module. Add `st.page_link` to each module page.

Run `streamlit run app.py` and verify the sidebar shows both pages. Stub out `pages/1_Content_Generator.py` and `pages/2_Customer_Support.py` with just an `st.title` for now.

### Step 5: First commit (5 min)

Commit everything so far. From this point forward, commit at the end of every phase.

**Phase 0 checkpoint:** You can run `streamlit run app.py`, see a landing page, navigate to both module pages (empty), and your Gemini key works. Move on.

---

## 6. Phase 1 — Task 2 Content Generator (Hour 1-7)

### Step 1: Streamlit UI for the Content Generator (45 min)

In `pages/1_Content_Generator.py`, build the UI in this order:

1. Title and one-line description at the top.
2. `st.file_uploader` accepting `["jpg", "jpeg", "png"]`.
3. After upload, show the image preview in one column and "Click Generate to produce marketing content" in the other.
4. A `st.button("Generate Marketing Content")` that triggers the pipeline.
5. Below the button, six expandable sections for: Title, Description, Features, SEO Keywords, Hashtags, Social Caption. Each with a copy button. Plus one section for the Banner image with a download button.
6. Use `st.session_state` to cache results so the user doesn't re-run on every interaction.

Run it. Verify upload works and the image preview renders correctly. No backend yet.

### Step 2: Vision analysis function (90 min)

This is the highest-leverage step in Task 2. Bad attributes ruin everything downstream.

In `modules/content/vision.py`, write `analyze_image(image_bytes) -> dict`. The function:

1. Loads the strict JSON schema from `prompts/vision_schema.json` (see Section 10 for the schema).
2. Calls Gemini 2.5 Pro with the image and a prompt requesting JSON output matching the schema.
3. Parses the JSON response and returns a Python dict.

Use Gemini's `response_schema` parameter to enforce the schema — this dramatically reduces parse errors.

**Test it on 5 wildly different products** before moving on: a sneaker, a candle, a phone case, a coffee mug, a t-shirt. Print the JSON output for each. If the outputs look generic or wrong, iterate on the system prompt. The system prompt should make the model think like a product analyst, not a poet — be specific about wanting concrete materials, hex color codes, and distinguishing features.

### Step 3: Text content generation (90 min)

In `modules/content/text_gen.py`, write `generate_text_content(attributes: dict) -> dict`. The function:

1. Takes the attribute dict from Step 2.
2. Loads the text-gen schema from `prompts/text_gen_schema.json` (see Section 10).
3. Calls Gemini 2.5 Flash with the attributes serialized into the user message and a system instruction explaining the brand voice and constraints.
4. Returns a dict with keys: `title`, `description`, `features`, `seo_keywords`, `hashtags`, `instagram_caption`, `twitter_caption`.

Constraints to bake into the prompt:
- Title under 70 characters
- Description 150-250 words
- Features exactly 5 bullet points
- SEO keywords: 5 head terms + 5 long-tail
- Hashtags: 10, no spaces, lowercase
- Instagram caption: 150-300 chars with hashtags at end
- Twitter caption: under 280 chars total

Test on the same 5 products. Read the outputs critically. Iterate the prompt until it sounds like a real product page, not AI slop.

### Step 4: Banner generation (90 min)

In `modules/content/banner.py`, write `generate_banner(attributes: dict, product_title: str) -> bytes`. Two paths:

**Path A (preferred): Pollinations.ai.** Build a prompt programmatically from attributes like: `"A clean minimalist promotional banner for a {category}. Style: {style_adjectives}. Color palette: {primary_color} and {secondary_color}. Soft studio lighting, copy space on the right, professional product photography aesthetic, 16:9 aspect ratio."` Hit `https://image.pollinations.ai/prompt/{url-encoded-prompt}?width=1024&height=576&nologo=true` and download the resulting image. No auth needed.

**Path B (fallback): Stability AI free tier or Gemini Imagen** if Pollinations is too slow or low quality.

After the image comes back, use Pillow to overlay the `product_title` in a clean sans-serif font with a semi-transparent background rectangle for readability. Place it in the bottom-left or center based on your design choice. Return the final image bytes.

### Step 5: Wire it all together (30 min)

In `pages/1_Content_Generator.py`, on button click:

1. Show a `st.spinner("Analyzing product image...")` while calling `analyze_image()`.
2. Show `st.spinner("Writing marketing copy...")` and `st.spinner("Designing banner...")` for the next two steps. Run text generation and banner generation in parallel using `concurrent.futures.ThreadPoolExecutor` to halve wait time.
3. Store all results in `st.session_state`.
4. Render each output in its expandable section with copy buttons (use `st.code` for copyable text).
5. Display the banner with `st.image` and a download button via `st.download_button`.

### Step 6: Test end-to-end (45 min)

Test on at least 5 different products. For each, verify:
- Vision call returns sensible attributes
- Text outputs are on-topic and well-written
- Banner reflects the product's style
- UI looks clean

Fix anything obviously broken. **Don't polish further at this stage** — move on to sleep.

**Phase 1 checkpoint:** Content Generator works end-to-end on 5 sample products. Commit, then sleep.

---

## 7. Phase 2 — Task 1 Customer Support (Hour 10-18)

### Step 1: Seed mock orders in SQLite (45 min)

In `scripts/seed_orders.py`, create a table `orders` with columns: `order_id` (TEXT PK, format `ORD-XXXX`), `customer_email` (TEXT), `status` (TEXT — pending/shipped/delivered/cancelled), `items` (TEXT — JSON list), `total` (REAL), `order_date` (TEXT), `ship_date` (TEXT, nullable), `tracking_number` (TEXT, nullable).

Seed 30 orders spanning all statuses and varied items. Make sure at least 5 customer emails appear multiple times so the agent can handle "show all my orders".

Run the script. Verify with `sqlite3 data/orders.db "SELECT * FROM orders LIMIT 5"`.

### Step 2: Write FAQ markdown files (45 min)

In `data/docs/`, create 8-10 short markdown files covering: return policy, shipping FAQ, warranty terms, refund process, account management, payment methods, contact info, common technical troubleshooting, loyalty program, gift cards.

Each file should be 200-400 words with clear section headings. Cover the questions your agent will be asked. This is what determines retrieval quality — write it like a real e-commerce help center.

### Step 3: Ingest docs into ChromaDB (30 min)

In `scripts/ingest_docs.py`:

1. Read every `.md` file in `data/docs/`.
2. Chunk each file into ~200-word chunks with 30-word overlap.
3. Embed each chunk with `sentence-transformers/all-MiniLM-L6-v2`.
4. Store in a persistent ChromaDB collection at `data/chromadb/` with metadata `{source: filename, chunk_id: N}`.

Run the script. Verify with a test query: load the collection and run `collection.query(query_texts=["how do I return an item"], n_results=3)`. The top result should be from `return_policy.md`.

### Step 4: Define the three tools (60 min)

In `modules/support/tools.py`, define three functions decorated for LangGraph:

**Tool 1: `search_knowledge_base(query: str) -> str`**
Docstring: "Searches the company knowledge base for policies, FAQs, return/refund procedures, shipping info, warranty terms, and how-to guides. Use this for any general policy or how-to question. Returns the most relevant policy text."

Implementation: queries ChromaDB, returns top 3 chunks concatenated with source citations.

**Tool 2: `get_order_status(order_id: str) -> str`**
Docstring: "Retrieves the current status of a specific customer order. Requires the order ID in format ORD-XXXX. Returns order status, items, tracking number if available, and ship date."

Implementation: SQL query against SQLite, returns formatted string or "Order not found" if missing.

**Tool 3: `escalate_to_human(customer_message: str, reason: str) -> str`**
Docstring: "Escalates the conversation to a human support agent. Use this when: the customer explicitly asks for a human, the issue involves legal threats or chargebacks, or you have attempted multiple tools without resolving the issue. Returns a confirmation message for the customer."

Implementation: appends a record to `data/tickets.json` with timestamp, customer message, and reason. Returns: "I've escalated your request to our human support team. A representative will contact you within 24 hours. Your ticket ID is TKT-XXX."

**The docstrings are critical** — the LLM reads them to decide when to call each tool. Be specific.

### Step 5: Build the LangGraph agent (90 min)

In `modules/support/agent.py`, use `create_react_agent` from `langgraph.prebuilt`. Pass:

- A Gemini 2.5 Flash model wrapped with `ChatGoogleGenerativeAI` from `langchain_google_genai`.
- The three tools from `tools.py`.
- A system prompt loaded from `prompts/agent_system.txt` (see Section 10).

Wrap the agent in a `get_agent()` function. Add a thin wrapper `run_agent(message: str, history: list) -> dict` that:

1. Invokes the agent with the message and chat history.
2. Extracts the trace of tool calls from the agent's intermediate steps.
3. Returns `{response: str, trace: list, tool_calls: list}`.

The trace extraction is what powers the sidebar — it's worth getting right.

### Step 6: Streamlit chat UI (60 min)

In `pages/2_Customer_Support.py`:

1. Set up `st.session_state.messages` as a list of chat messages.
2. Render history with `st.chat_message` for each message.
3. `st.chat_input` for the user's next message.
4. On submit, call `run_agent()` with the message and history.
5. Stream or display the response inside an `st.chat_message("assistant")` block.
6. Append both user and assistant messages to session state.

### Step 7: Trace sidebar (45 min)

This is what sells the "agentic" framing during evaluation.

In the sidebar (`st.sidebar`):

1. Header: "Agent Trace (Last Query)".
2. For each tool call in the last response: show tool name, arguments (formatted JSON), and a preview of the result (first 200 chars).
3. Use `st.expander` for each step so it's collapsible.
4. Add a colored badge showing whether the query was resolved by the agent or escalated.

When an evaluator opens the support page and sees the trace updating with each query — showing thinking steps, tool selection, arguments — that's the strongest signal possible for an AI Developer assessment.

### Step 8: Test conversations (45 min)

Run through these test queries in order:

1. "Where is my order ORD-1003?" → should call `get_order_status`
2. "How do I return something?" → should call `search_knowledge_base`
3. "I want to return ORD-1003, what's your policy?" → should call both tools in sequence
4. "What's the weather today?" → should refuse politely, no tool call
5. "I want to speak to a human" → should call `escalate_to_human`
6. "I'm going to sue you, my package never arrived!" → should escalate
7. Multi-turn: "I have an issue" → "It's about ORD-1005" → agent should remember context
8. "Show me orders for customer@example.com" → should call `get_order_status` adaptation or escalate

Fix any obvious failures. Don't chase perfection — chase "evaluator sees coherent agent behavior."

**Phase 2 checkpoint:** Customer Support module handles all 8 test queries reasonably. Commit.

---

## 8. Phase 3 — Polish & Submission (Hour 18-22)

### Step 1: README.md (60 min)

Write the README in this exact structure. The README is what 90% of evaluators read first.

```markdown
# AI Assistant Platform for E-commerce

[One-sentence elevator pitch]

[Architecture diagram screenshot — embed one of the two from the design doc]

## Features

### Content Generator
[3-4 bullet points]

### Customer Support Agent
[3-4 bullet points]

## Tech Stack
[Bullet list with versions]

## Architecture
[Two paragraphs explaining the design — one per module]

## Setup

\`\`\`bash
git clone ...
cd ai-assistant-platform
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
python scripts/seed_orders.py
python scripts/ingest_docs.py
streamlit run app.py
\`\`\`

## Demo

[Embedded 60-90 second video link or GIF]

## Project Structure
[Tree from Section 2]

## Sample Queries

[5-6 example queries for Customer Support with expected behavior]

## Design Decisions

[3-4 paragraphs explaining WHY you made key choices:
- Why a single agent with tools instead of multi-agent
- Why ChromaDB over Pinecone for this assessment
- Why Gemini over OpenAI
- How structured JSON outputs reduce hallucination]

## What I'd Add With More Time

[5-7 bullets — this signals product thinking]
```

The "Design Decisions" section is where you score points. Most candidates skip it. Evaluators love it.

### Step 2: Screenshots (30 min)

Capture clean screenshots:
- Landing page
- Content Generator with a complete output (use a nice product image)
- Customer Support mid-conversation
- Customer Support trace sidebar showing tool calls
- Architecture diagrams (paste from the design doc)

Save them in `assets/` and embed in the README.

### Step 3: Demo video (60 min)

Record a 60-90 second screen recording. Loom is free and easy. Show:

1. (0:00-0:10) Landing page, briefly describe the platform.
2. (0:10-0:35) Content Generator: upload an image, walk through the generated outputs.
3. (0:35-1:15) Customer Support: ask 3 different queries showing different tools being used. Point at the trace sidebar.
4. (1:15-1:30) Quick architecture overview from the README.

Upload as unlisted on YouTube or use Loom's share link. Embed in the README.

### Step 4: Final test pass (30 min)

Wipe the database, re-run setup scripts from scratch, test both modules with fresh sample inputs. Catch any bugs that only appear in a clean environment.

### Step 5: Final commit and submit (20 min)

```
git add .
git commit -m "Final submission"
git push origin main
```

Check the submission instructions one more time. Submit.

**Phase 3 checkpoint:** README is complete, screenshots embedded, demo video linked, submission sent. Done.

---

## 9. Risk Mitigation & Cut List

If you fall behind, cut from the end of this list, not the start.

| If behind at... | Cut this |
|---|---|
| Hour 6 (Task 2 not done) | Skip parallel execution — run text and banner sequentially. Cut the copy buttons, just show plain text. |
| Hour 12 (still seeding data) | Reduce to 15 orders and 5 FAQ files. Cover the most common categories only. |
| Hour 15 (agent not working) | Drop `escalate_to_human` tool. Two working tools demos just as well. |
| Hour 17 (still debugging agent) | Use a simpler `AgentExecutor` from LangChain instead of LangGraph — it's less powerful but faster to wire up. |
| Hour 19 (no time for polish) | Skip the demo video. Skip screenshots. Just write a good README. |
| Hour 21 (still broken) | Submit Task 2 working alone with a note that Task 1 is partially complete. Better than a broken submission of both. |

### Common pitfalls to avoid

- **Don't switch LLM providers mid-build.** If Gemini misbehaves, fix your prompt, don't switch to OpenAI.
- **Don't try LangChain Expression Language (LCEL) chains.** They're elegant but debugging them under time pressure is brutal. Use plain Python functions wherever possible.
- **Don't optimize prompts past "good enough."** Diminishing returns hit fast. If 4 of 5 test cases pass, move on.
- **Don't add features beyond the brief.** Streaming responses, dark mode, fancy CSS — all great in week 2, terrible in hour 14.
- **Don't skip the README.** A working app with no README scores below a half-working app with great documentation.

---

## 10. Reference: Prompts & Schemas

### `prompts/vision_schema.json`

```json
{
  "type": "object",
  "required": ["category", "subcategory", "primary_color_hex", "materials", "style_adjectives", "target_audience", "distinctive_features", "use_cases"],
  "properties": {
    "category": {
      "type": "string",
      "description": "Top-level product category (e.g., footwear, home decor, electronics)"
    },
    "subcategory": {
      "type": "string",
      "description": "More specific category (e.g., running shoes, scented candles, wireless earbuds)"
    },
    "primary_color_hex": {
      "type": "string",
      "description": "Dominant color in hex format like #FF5733"
    },
    "secondary_color_hex": {
      "type": "string",
      "description": "Second most prominent color in hex format"
    },
    "materials": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Visible materials e.g. leather, cotton, brushed aluminum"
    },
    "style_adjectives": {
      "type": "array",
      "items": {"type": "string"},
      "description": "3-5 style descriptors e.g. minimalist, rustic, modern, vintage"
    },
    "target_audience": {
      "type": "string",
      "description": "Likely target demographic in one phrase"
    },
    "distinctive_features": {
      "type": "array",
      "items": {"type": "string"},
      "description": "3-5 visible distinguishing features"
    },
    "use_cases": {
      "type": "array",
      "items": {"type": "string"},
      "description": "3-4 typical use cases for this product"
    }
  }
}
```

### Vision system prompt

```
You are a product analyst extracting structured attributes from product images for an e-commerce catalog. Be specific and concrete. Avoid generic adjectives like "nice" or "good quality". Focus on visually-verifiable attributes only. If you cannot determine a field with confidence, make a best estimate based on visible evidence rather than leaving it blank.

Return ONLY valid JSON matching the provided schema.
```

### `prompts/text_gen_schema.json`

```json
{
  "type": "object",
  "required": ["title", "description", "features", "seo_keywords", "hashtags", "instagram_caption", "twitter_caption"],
  "properties": {
    "title": {
      "type": "string",
      "description": "Product title under 70 characters, SEO-friendly"
    },
    "description": {
      "type": "string",
      "description": "Product description 150-250 words, engaging and benefit-focused"
    },
    "features": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 5,
      "maxItems": 5,
      "description": "Exactly 5 feature bullet points"
    },
    "seo_keywords": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 10,
      "maxItems": 10,
      "description": "10 SEO keywords: 5 head terms and 5 long-tail variations"
    },
    "hashtags": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 10,
      "maxItems": 10,
      "description": "10 hashtags without # symbol, lowercase, no spaces"
    },
    "instagram_caption": {
      "type": "string",
      "description": "Instagram caption 150-300 chars with hashtags at the end"
    },
    "twitter_caption": {
      "type": "string",
      "description": "Twitter/X caption under 280 characters total including hashtags"
    }
  }
}
```

### Text generation system prompt

```
You write high-converting e-commerce marketing copy. You are given a JSON object of product attributes and must produce a complete content package.

Voice: confident, benefit-focused, specific. Avoid superlatives like "best" or "amazing" — describe what makes the product useful instead. Avoid AI tells like "elevate your experience" or "in today's fast-paced world".

Constraints are strict — adhere to character limits and item counts exactly.

Return ONLY valid JSON matching the provided schema.
```

### `prompts/agent_system.txt`

```
You are an AI customer support agent for an e-commerce company. You help customers with order inquiries, returns, refunds, shipping questions, and product information.

You have access to three tools:

1. search_knowledge_base — use for policy questions, returns, shipping, warranty, and how-to guides
2. get_order_status — use when a customer asks about a specific order (requires order ID format ORD-XXXX)
3. escalate_to_human — use when:
   - The customer explicitly requests a human agent
   - The customer mentions legal action, chargebacks, or threats
   - You've attempted multiple tools without resolving the issue
   - The query is outside your knowledge or capability

Guidelines:
- Be concise and helpful. Don't pad your responses.
- Always cite which policy you're referencing when answering FAQ questions.
- If a customer asks about an order but doesn't provide an ID, ask for it.
- Never make up order information or policy details.
- If you don't know, escalate rather than guess.
- Match the customer's tone — formal if they're formal, friendly if they're casual.

When a query is ambiguous, prefer asking a clarifying question over guessing.
```

### Banner prompt template (built programmatically from attributes)

```
A clean minimalist promotional banner for a {category} product. The product is a {subcategory}, with primary color {primary_color_hex} and secondary color {secondary_color_hex}. Style: {style_adjectives}. The composition should feel {target_audience}-appropriate. Soft studio lighting, professional product photography aesthetic, with copy space on the right side for text overlay. 16:9 aspect ratio. No text in the image.
```

---

## 11. Submission Checklist

Before clicking submit, verify every item below.

**Functionality**
- [ ] `streamlit run app.py` starts the app cleanly with no errors
- [ ] Landing page renders both module cards
- [ ] Content Generator: upload → vision → text → banner all work
- [ ] Content Generator tested on at least 3 different product types
- [ ] Customer Support: chat input works
- [ ] Customer Support: all 3 tools fire on appropriate queries
- [ ] Customer Support: trace sidebar shows tool calls
- [ ] Customer Support: escalation triggers correctly
- [ ] No hardcoded API keys anywhere in the code

**Code quality**
- [ ] Modules are organized in `modules/content/` and `modules/support/`
- [ ] No file over 300 lines
- [ ] No commented-out blocks of code
- [ ] `.env` is in `.gitignore`
- [ ] `requirements.txt` is complete and pinned

**Documentation**
- [ ] README has all sections from Phase 3 Step 1
- [ ] Architecture diagram(s) embedded
- [ ] At least 3 screenshots embedded
- [ ] Demo video link works (test in incognito)
- [ ] Setup instructions work on a fresh machine (test them yourself)
- [ ] Sample queries listed for Customer Support
- [ ] Design Decisions section is written

**Submission**
- [ ] Repository is public (or shared with the evaluator email)
- [ ] Latest commit pushed to main
- [ ] Submission form filled out correctly
- [ ] Email confirming submission saved

---

## Final note

You will be tempted to over-engineer at every step. Resist it. The goal is a working, complete, well-documented submission that demonstrates the core AI concepts (multimodal vision, prompt engineering, structured outputs, agentic AI, RAG, tool calling, escalation logic). A polished simple thing beats an ambitious broken thing every time.

Set timers. Take the sleep break. Commit often. Submit on time.

Good luck.
