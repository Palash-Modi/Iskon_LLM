import json
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from startup_download import download_embeddings

# ====== DOWNLOAD EMBEDDINGS IF NOT PRESENT ======
download_embeddings()

# ====== CONFIG ======
EMBEDDINGS_DIR = Path("embeddings")
EMBEDDINGS_FILE = EMBEDDINGS_DIR / "embeddings.pt"
METADATA_FILE = EMBEDDINGS_DIR / "metadata.json"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

# ====== LOAD PRECOMPUTED EMBEDDINGS ======
print("[INFO] Loading precomputed embeddings...")
if not EMBEDDINGS_FILE.exists():
    raise FileNotFoundError(f"Embeddings file not found at {EMBEDDINGS_FILE}")

corpus_embeddings = torch.load(EMBEDDINGS_FILE, map_location="cpu")

print("[INFO] Loading metadata...")
if not METADATA_FILE.exists():
    raise FileNotFoundError(f"Metadata file not found at {METADATA_FILE}")

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    meta = json.load(f)

device = "cpu"  # CPU because Render free tier has no GPU
corpus_embeddings = corpus_embeddings.to(device)

# Load model for encoding queries
print("[INFO] Loading embedding model for queries...")
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME, device=device)
print(f"[INFO] Using device: {device}")

# ====== SETUP FASTAPI ======
app = FastAPI()

# ====== STATIC FILES (Frontend) ======
STATIC_DIR = Path(__file__).parent / "frontend" / "dist"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# ====== API Endpoints ======
@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        with open(index_file, encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Ask Prabhupada</h1><p>Frontend not found.</p>")

@app.post("/query")
async def query(request: Request):
    body = await request.json()
    query_text = body.get("query", "").strip()

    if not query_text:
        return JSONResponse({"answer": "Please provide a valid question."})

    # Encode query
    query_embedding = embedder.encode([query_text], convert_to_tensor=True).to(device)

    # Compute similarities
    similarities = cosine_similarity(
        query_embedding.cpu().numpy(), corpus_embeddings.cpu().numpy()
    )[0]
    top_indices = similarities.argsort()[-TOP_K:][::-1]

    response_chunks = []
    sources = []

    for idx in top_indices:
        entry_meta = meta[idx]
        title = entry_meta.get("title", "No Title")
        url = entry_meta.get("url", "#")
        response_chunks.append(f"**[{title}]({url})**")
        sources.append({
            "label": title,
            "url": url
        })

    final_answer = "\n\n".join(response_chunks)

    return JSONResponse({
        "answer": final_answer,
        "sources": sources
    })
