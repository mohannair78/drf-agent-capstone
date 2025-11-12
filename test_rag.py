import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Configuration ---
MODEL_NAME = 'all-MiniLM-L6-v2'
PROJECT_DIR = "/home/ubuntu/drf_agent_project"
KB_DIR = os.path.join(PROJECT_DIR, "knowledge_base")
FAISS_INDEX_FILE = os.path.join(KB_DIR, "drf_faiss_index.bin")
CHUNKS_LIST_FILE = os.path.join(KB_DIR, "drf_chunks_list.txt")

def load_rag_components():
    """Loads the model, FAISS index, and chunk list."""
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer(MODEL_NAME)
    
    print(f"Loading FAISS index from {FAISS_INDEX_FILE}...")
    index = faiss.read_index(FAISS_INDEX_FILE)
    
    print(f"Loading chunks list from {CHUNKS_LIST_FILE}...")
    with open(CHUNKS_LIST_FILE, 'r', encoding='utf-8') as f:
        chunks = f.read().split('\n---\n')
        
    print(f"RAG components loaded. Index size: {index.ntotal} chunks.")
    return model, index, chunks

def retrieve_context(query, model, index, chunks, k=3):
    """Retrieves the top k most relevant chunks for a given query."""
    # 1. Encode the query
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # 2. Search the FAISS index
    # D is the distance, I is the index of the retrieved vectors
    D, I = index.search(query_embedding, k)
    
    # 3. Retrieve the corresponding chunks
    retrieved_chunks = [chunks[i] for i in I[0]]
    
    return retrieved_chunks

if __name__ == "__main__":
    try:
        model, index, chunks = load_rag_components()
        
        # --- Test Queries ---
        test_queries = [
            "What are the five domains of Digital Emotional Intelligence?",
            "What is the Digital Resonance Framework?",
            "How does Digital Self-Regulation help with digital boundaries?",
            "What is the role of the foreword author, Mohan K Naiyr?"
        ]
        
        print("\n--- Running RAG Test Queries ---")
        for i, query in enumerate(test_queries):
            print(f"\nQUERY {i+1}: {query}")
            context = retrieve_context(query, model, index, chunks, k=3)
            
            print("\nRETRIEVED CONTEXT:")
            for j, chunk in enumerate(context):
                print(f"--- Context Chunk {j+1} ---")
                print(chunk[:300] + "...") # Print first 300 chars for brevity
            print("-" * 50)
            
    except Exception as e:
        print(f"An error occurred during RAG testing: {e}")
