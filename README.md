
# 🧠 Text-to-SQL Dashboard with LLMs

An interactive **Streamlit-based Text-to-SQL application** that allows users to ask natural language questions and automatically generate, execute, and visualize SQL queries over a relational healthcare database using Large Language Models (LLMs).

---

## ✨ Features

* 💬 **Natural Language → SQL** using LLMs
* 🧠 **Schema-aware querying** via semantic schema retrieval
* 📊 **Interactive dashboard** built with Streamlit
* 🧾 **Generated SQL preview** for transparency
* 💰 **Token-based cost tracking** per query
* 📌 **Example queries** for better usability
* 👥 **Session-safe visitor counter**
* 🔁 **Retry & error handling** for robust query generation

---

## 🖥️ Demo UI Overview

**Sidebar**

* Visitor count (session-based)
* Context prompt configuration
* View active context instructions

**Main Panel**

* User natural language query input
* Example queries (click-to-fill)
* Query execution button

**Tabs**

* 📊 Results (query output)
* 🧠 Generated SQL
* 💰 Cost & usage metrics


---

## ⚙️ How It Works

1. **User enters a natural language question**
2. Relevant **database schemas are retrieved** using semantic search
3. A **system prompt** is constructed using:

   * Retrieved schemas
   * Optional context prompt
4. The LLM generates a **SQL query**
5. SQL is:

   * validated
   * executed on the SQLite database
6. Results, SQL, and cost metrics are displayed in the dashboard

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone repo
cd rag_txt2sql
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
---

## 🔧 Environment Variables

This project uses a `.env` file in the repository root to configure API keys, model names, and other runtime settings. **Do not commit secrets to version control.**

**Required variables**

- `VECTOR_STORE` — Vector backend (e.g., `pinecone or weaviate`).
- `EMBED_MODEL` — Embedding model name (e.g., `text-embedding-3-small`).
- `GPT_MODEL` — LLM model name (e.g., `gpt-4`).
- `METRIC_FILENAME` — Metrics output file (e.g., `metrics.json`).
- `CONTEXT_PROMPT_FILE_PATH` — Path to context prompt (e.g., `context_prompt.txt`).
- `OPENAI_API_KEY` — Your OpenAI API key (keep secret).
- `PINECONE_API_KEY` — Your Pinecone API key (if using Pinecone).
- `DB_PATH` — Path to the SQLite DB (e.g., `patient_health_data.db`).
- `EMBED_BATCH_SIZE` — Embedding batch size (e.g., `10`).
- `PINECONE_REGION` — Pinecone region (e.g., `us-east-1`).
- `SCHEMAS_FILE_PATH` — Path to schemas file (e.g., `schemas.txt`).
- `SYSTEM_PROMPT_FILE` — Path to system prompt (e.g., `system_prompt.txt`).


### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🧪 Example Queries

* `Show all patients older than 60`
* `List patients with blood pressure above 140`
* `How many patients have diabetes?`

(You can click examples directly inside the UI.)

---

## 🧠 Context Prompt

The **context prompt** allows you to control LLM behavior (tone, constraints, domain rules).

* Loaded from `context_prompt.txt` by default
* Can be overridden from the sidebar
* Useful for:

  * SQL style enforcement
  * Security constraints
  * Domain-specific reasoning

---

## 💰 Cost Tracking

* Token usage is recorded per query
* Cost is calculated using:

  * Prompt tokens
  * Generated tokens
* Cumulative cost is stored in `metrics.json`

> ⚠️ Costs depend on the configured LLM pricing.

---

## 👥 Visitor Counting Logic

Visitor count is **session-based**, not rerun-based.

* Incremented once per browser session
* Uses `st.session_state` to avoid double counting
* Suitable for lightweight analytics

---

## ⚠️ Limitations

* Counts sessions, not unique humans
* SQL execution assumes **trusted LLM output**
* SQLite used (not optimized for large-scale workloads)

---

## 🔮 Future Improvements

* 🔐 Authentication & user accounts
* 📈 Query history & analytics
* 🧪 SQL validation & sandboxing
* 📊 Automatic chart generation
* 🌍 Multi-database support (Postgres, MySQL)
* 🧠 Auto-generated example queries from schema

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* Streamlit
* OpenAI / LLM providers
* SQLite
* Vector embedding frameworks

## 👩‍💻👨‍💻 Authors

| Name        | Student ID |
|-------------|------------|
| Tigist Wondimneh| GSR/5506/17   |
|  Nahom Senay   |GSR/4848/17|
| Michael Shimeles | GSR/6484/17   |


