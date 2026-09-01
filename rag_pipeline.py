import os

import pymupdf
import faiss

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================================
# 2. Load the PDF
# ============================================================

pdf_path = "data/HR_Employee_Handbook.pdf"

document = pymupdf.open(pdf_path)

print("PDF loaded successfully!")
print("Number of pages:", len(document))


# ============================================================
# 3. Extract text and create policy-based chunks
# ============================================================

chunks = []

for page_number, page in enumerate(document, start=1):

    text = page.get_text()

    # Split the page into individual policies
    policies = text.split("HR-")

    for policy in policies:

        policy = policy.strip()

        # Keep only HR-001 to HR-015
        if policy.startswith((
            "001", "002", "003", "004", "005",
            "006", "007", "008", "009", "010",
            "011", "012", "013", "014", "015"
        )):

            policy_text = "HR-" + policy

            chunks.append({
                "text": policy_text,
                "page": page_number
            })


print("\nTotal chunks:", len(chunks))


# ============================================================
# 4. Load embedding model
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# 5. Create embeddings
# ============================================================

chunk_texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = embedding_model.encode(
    chunk_texts
)

print("\nEmbeddings created successfully!")
print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", embeddings.shape[1])


# ============================================================
# 6. Create FAISS index
# ============================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    embeddings.astype("float32")
)

print("\nFAISS index created successfully!")
print("Number of vectors in FAISS:", index.ntotal)


# ============================================================
# 7. Relevance threshold
# ============================================================

DISTANCE_THRESHOLD = 1.10


# ============================================================
# 8. Generate grounded answer using LLM
# ============================================================

def generate_answer(query, context):

    prompt = f"""
You are an HR Policy Assistant.

Answer the user's question using ONLY the policy context provided below.

Rules:
- Do not use outside knowledge.
- Do not invent or assume any policy.
- If the answer is not available in the provided context, say:
  "The information is unavailable in the HR Policy Handbook."
- Give a clear and concise answer.

Policy Context:
{context}

User Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful HR policy assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ============================================================
# 9. Complete RAG Question Answering
# ============================================================

def ask_hr_assistant(query):

    # Convert question into embedding
    query_embedding = embedding_model.encode(
        [query]
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding.astype("float32"),
        k=1
    )

    # Get best matching policy
    best_index = indices[0][0]

    best_chunk = chunks[best_index]

    distance = distances[0][0]

    # Check relevance
    if distance > DISTANCE_THRESHOLD:

        return {
            "answer": "The information is unavailable in the HR Policy Handbook.",
            "policy_id": None,
            "page": None,
            "distance": distance,
            "context": None
        }

    # Generate grounded answer
    answer = generate_answer(
        query,
        best_chunk["text"]
    )

    # Extract policy ID
    policy_id = best_chunk["text"].split("—")[0].strip()

    return {
        "answer": answer,
        "policy_id": policy_id,
        "page": best_chunk["page"],
        "distance": distance,
        "context": best_chunk["text"]
    }