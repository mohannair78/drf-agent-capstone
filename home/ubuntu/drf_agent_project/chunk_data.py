import re

def chunk_by_section(file_path):
    """
    Reads a text file and chunks the content based on major section headers.
    Major sections are assumed to start with a capitalized title followed by a newline.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex to find major sections (e.g., "Chapter 1: Title" or "Section Title")
    # This is a heuristic and may need adjustment. We'll use a simpler split for now.
    # Split by two or more newlines to separate paragraphs/sections
    sections = re.split(r'\n\n+', text)
    
    # Filter out empty strings and very short strings (like page numbers or single words)
    chunks = [s.strip() for s in sections if s.strip() and len(s.strip()) > 50]
    
    # Further refinement: combine small chunks that are logically related
    final_chunks = []
    current_chunk = ""
    max_chunk_size = 1000 # Max characters per chunk
    
    for chunk in chunks:
        if len(current_chunk) + len(chunk) < max_chunk_size:
            current_chunk += "\n\n" + chunk
        else:
            if current_chunk:
                final_chunks.append(current_chunk.strip())
            current_chunk = chunk
    
    if current_chunk:
        final_chunks.append(current_chunk.strip())

    return final_chunks

def save_chunks(chunks, output_path):
    """Saves the list of chunks to a single file, separated by a clear delimiter."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- CHUNK {i+1} ---\n")
            f.write(chunk)
            f.write("\n\n")

if __name__ == "__main__":
    input_file = "/home/ubuntu/drf_agent_project/knowledge_base/drf_manuscript.txt"
    output_file = "/home/ubuntu/drf_agent_project/knowledge_base/drf_knowledge_chunks.txt"
    
    print(f"Starting chunking process for {input_file}...")
    chunks = chunk_by_section(input_file)
    save_chunks(chunks, output_file)
    print(f"Chunking complete. {len(chunks)} chunks saved to {output_file}")
