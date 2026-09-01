# 🤖 AI HR Policy Assistant

An AI-powered HR Policy Assistant that uses **Retrieval-Augmented Generation (RAG)** to answer employee questions from an HR Policy Handbook.

The application retrieves the most relevant HR policy using **FAISS vector search** and **Sentence Transformers**, then generates a grounded answer using **OpenAI**. A **Streamlit** interface provides an interactive chat experience.

## 🚀 Features

* 📄 Extracts HR policies from a PDF handbook
* ✂️ Creates policy-based text chunks
* 🧠 Generates embeddings using Sentence Transformers
* 🔍 Performs semantic search using FAISS
* 🎯 Uses a relevance threshold to avoid unsupported answers
* 🤖 Generates grounded answers using OpenAI
* 📚 Displays the retrieved policy and source page
* 💬 Interactive Streamlit chat interface
* 🛡️ Handles questions outside the knowledge base

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – User interface
* **PyMuPDF** – PDF text extraction
* **Sentence Transformers** – Text embeddings
* **FAISS** – Vector similarity search
* **OpenAI API** – Answer generation
* **python-dotenv** – Environment variable management

## 🔄 How It Works

```text
HR Policy PDF
      ↓
PDF Text Extraction
      ↓
Policy-based Chunking
      ↓
Sentence Transformer Embeddings
      ↓
FAISS Vector Index
      ↓
User Question
      ↓
Question Embedding
      ↓
Similarity Search
      ↓
Relevant HR Policy
      ↓
OpenAI LLM
      ↓
Grounded Answer
      ↓
Streamlit UI
```

## 📁 Project Structure

```text
AI-HR-Policy-Assistant/
│
├── data/
│   └── HR_Employee_Handbook.pdf
│
├── app.py
├── rag_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd AI-HR-Policy-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

**Never upload the `.env` file to GitHub.**

The `.gitignore` file contains:

```text
.env
```

to prevent the API key from being committed.

## ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 💡 Example Questions

You can ask questions such as:

* **How many annual leave days do I get?**
* **Can I work from home 10 days every month?**
* **What is the meal allowance?**
* **What should I do about phishing?**
* **Can I transfer internally after 4 months?**

The assistant retrieves the relevant policy and provides an answer based only on the HR Policy Handbook.

## 🛡️ Knowledge Base Grounding

The application uses a similarity-distance threshold to identify whether a question is sufficiently related to the HR knowledge base.

For example, if a user asks:

> What is the maternity leave policy?

and the information is not present in the handbook, the application responds:

```text
The information is unavailable in the HR Policy Handbook.
```

This helps reduce unsupported or hallucinated answers.

## 📌 Project Status

**Completed**

The project currently includes:

* PDF processing
* Policy chunking
* Embedding generation
* FAISS retrieval
* Relevance threshold
* OpenAI-based grounded responses
* Streamlit chat interface
* Source policy display
* Out-of-knowledge-base handling

## 🔮 Future Improvements

* Support multiple HR documents
* Add document upload functionality
* Improve retrieval using Top-K results
* Add conversation memory
* Add authentication
* Deploy the application to the cloud
* Add evaluation metrics for RAG performance

## 👩‍💻 Author

**Shwetha B**

BE – Artificial Intelligence & Machine Learning
