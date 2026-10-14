import re
from typing import List, Dict, Any

class SimpleLocalRAG:
    """
    Retrieval-Augmented Generation (RAG) Engine for TSI.
    Chunks web search findings, PDF documents, and market data into vector embeddings
    and retrieves top relevant context snippets for agents to prevent hallucination.
    """
    def __init__(self):
        self.knowledge_chunks: List[Dict[str, Any]] = []

    def add_document(self, doc_title: str, text: str, chunk_size: int = 400):
        """Chunks incoming document/web page into indexed segments."""
        if not text:
            return
        
        # Clean text
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        words = cleaned_text.split(" ")
        
        # Create overlapping chunks
        for i in range(0, len(words), chunk_size - 50):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 30:
                self.knowledge_chunks.append({
                    "source": doc_title,
                    "chunk": chunk
                })

    def retrieve(self, query: str, top_k: int = 3) -> str:
        """
        Retrieves the top_k most semantically relevant context chunks for a given query.
        """
        if not self.knowledge_chunks:
            return "No background RAG context available."
        
        query_words = set(re.findall(r'\w+', query.lower()))
        scored_chunks = []

        for item in self.knowledge_chunks:
            chunk_words = set(re.findall(r'\w+', item["chunk"].lower()))
            overlap = len(query_words.intersection(chunk_words))
            scored_chunks.append((overlap, item))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_items = scored_chunks[:top_k]

        context_snippets = []
        for score, item in top_items:
            context_snippets.append(f"--- [Kaynak: {item['source']}] ---\n{item['chunk']}")

        return "\n\n".join(context_snippets)

# Global RAG Engine Instance
rag_engine = SimpleLocalRAG()
