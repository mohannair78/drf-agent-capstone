import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Configuration ---
MODEL_NAME = 'all-MiniLM-L6-v2'
PROJECT_DIR = "/home/ubuntu/drf_agent_project"
KB_DIR = os.path.join(PROJECT_DIR, "knowledge_base")
CHUNKS_FILE = os.path.join(KB_DIR, "drf_knowledge_chunks.txt")
FAISS_INDEX_FILE = os.path.join(KB_DIR, "drf_faiss_index.bin")
CHUNKS_LIST_FILE = os.path.join(KB_DIR, "drf_chunks_list.txt")

def load_chunks(file_path):
    """Loads chunks from the file, using '--- CHUNK X ---' as a delimiter."""
    print(f"Loading chunks from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by the delimiter used in the chunking script
    raw_chunks = content.split("--- CHUNK")
    
    # Clean up and filter the chunks
    chunks = []
    for chunk in raw_chunks:
        # Remove the chunk number line (e.g., ' 1 ---') and leading/trailing whitespace
        cleaned_chunk = '\n'.join(chunk.split('\n')[1:]).strip()
        if cleaned_chunk:
            chunks.append(cleaned_chunk)
            
    print(f"Successfully loaded {len(chunks)} clean chunks.")
    return chunks

def create_and_save_index(chunks):
    """Creates embeddings, a FAISS index, and saves both the index and the chunks list."""
    print(f"Initializing SentenceTransformer model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    
    print("Generating embeddings for all chunks...")
    # Encode the chunks to get their embeddings
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
    
    # Check the dimension of the embeddings
    d = embeddings.shape[1]
    print(f"Embeddings generated with dimension: {d}")
    
    # Create a FAISS index (IndexFlatL2 is a simple L2 distance index)
    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(d)
    
    # Add the embeddings to the index
    index.add(embeddings)
    print(f"FAISS index created and populated with {index.ntotal} vectors.")
    
    # Save the FAISS index
    print(f"Saving FAISS index to {FAISS_INDEX_FILE}...")
    faiss.write_index(index, FAISS_INDEX_FILE)
    
    # Save the chunks list (to be able to retrieve the original text later)
    print(f"Saving chunks list to {CHUNKS_LIST_FILE}...")
    with open(CHUNKS_LIST_FILE, 'w', encoding='utf-8') as f:
        f.write('\n---\n'.join(chunks)) # Use a unique delimiter for easy loading
        
    print("Indexing complete.")

if __name__ == "__main__":
    try:
        chunks = load_chunks(CHUNKS_FILE)
        if chunks:
            create_and_save_index(chunks)
        else:
            print("No chunks loaded. Aborting indexing.")
    except Exception as e:
        print(f"An error occurred during indexing: {e}")

# Note: The progress bar for encoding may not display correctly in the terminal.
# The script will still run and complete the task.
