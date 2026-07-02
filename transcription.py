# SmartMinutes - Retrieval (RAG) Agent
# Responsibilities: Chunk transcripts, embed segments, store in vector DB, and answer queries with citations.

import numpy as np
from typing import List, Dict, Any

class RetrievalAgent:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", vector_db: str = "chromadb"):
        self.embedding_model = embedding_model
        self.vector_db = vector_db
        self.documents = []  # In-memory storage for simplicity in this code template
        self.embeddings = []
        print(f"[RetrievalAgent] Initializing with Embeddings: {embedding_model} | Vector DB: {vector_db}")

    def chunk_transcript(self, transcript_segments: List[Dict[str, Any]], chunk_size: int = 2) -> List[Dict[str, Any]]:
        """Splits transcript segments into overlapping chunks of sentences/segments"""
        chunks = []
        print(f"[RetrievalAgent] Chunking transcript: {len(transcript_segments)} segments -> chunks (size={chunk_size})")
        
        # Simple segment-based chunking
        for i in range(0, len(transcript_segments), chunk_size - 1):
            group = transcript_segments[i:i + chunk_size]
            if not group:
                break
            combined_text = " ".join([f"{s['speaker']}: {s['text']}" for s in group])
            start_t = group[0]["start_time"]
            end_t = group[-1]["end_time"]
            
            chunks.append({
                "chunk_id": f"chunk_{i}",
                "text": combined_text,
                "start_time": start_t,
                "end_time": end_t,
                "source_speakers": list(set([s["speaker"] for s in group]))
            })
            if i + chunk_size >= len(transcript_segments):
                break
                
        return chunks

    def add_to_vector_db(self, meeting_id: str, transcript_segments: List[Dict[str, Any]]):
        """Generates embeddings and inserts into vector store"""
        chunks = self.chunk_transcript(transcript_segments)
        print(f"[RetrievalAgent] Storing {len(chunks)} chunks in Vector DB for meeting: {meeting_id}")
        
        # Real code uses SentenceTransformers & Qdrant/Chroma client:
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer(self.embedding_model)
        # texts = [c['text'] for c in chunks]
        # embeddings = model.encode(texts)
        # self.db.upsert(collection=meeting_id, embeddings=embeddings, payloads=chunks)
        
        for c in chunks:
            c["meeting_id"] = meeting_id
            self.documents.append(c)
            # Dummy embedding vector (384 dimensional for MiniLM)
            self.embeddings.append(np.random.rand(384).tolist())

    def similarity_search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Queries the vector store and returns matching documents with similarity scores"""
        print(f"[RetrievalAgent] Performing vector similarity search for query: '{query}'")
        
        # In a real app, query is embedded, and cosine-similarity is calculated:
        # query_vector = self.model.encode(query)
        # results = self.db.search(query_vector, limit=top_k)
        
        # Simulating a search matching keyword heuristics
        results = []
        query_words = set(query.lower().split())
        
        for idx, doc in enumerate(self.documents):
            text_lower = doc["text"].lower()
            overlap = sum(1 for w in query_words if w in text_lower)
            score = 0.5 + (overlap / (len(query_words) + 1)) * 0.5
            
            if overlap > 0:
                results.append({
                    "score": round(score, 3),
                    "document": doc
                })
                
        # Sort by score desc
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def answer_query(self, meeting_title: str, query: str) -> Dict[str, Any]:
        """Answers user query by finding relevant chunks (RAG) and generating a response"""
        search_results = self.similarity_search(query)
        
        print(f"[RetrievalAgent] Generating answer with LLM context...")
        
        # Mock answers based on query keywords
        q_lower = query.lower()
        
        if "design" in q_lower or "mobile app" in q_lower or "figma" in q_lower:
            answer = "According to the discussion in the meeting, Rahul has finished the Figma mockups for the mobile app redesign and is polishing UX details. He will share the final design document (covering Stripe integration and onboarding screens) by Friday."
            citations = [r["document"] for r in search_results if "design" in r["document"]["text"].lower() or "figma" in r["document"]["text"].lower()]
        elif "budget" in q_lower or "migration" in q_lower or "cost" in q_lower:
            answer = "Priyas presented the Q3 infrastructure budget: server migrations are estimated at $12,000, and database scaling will cost $5,000. Priyas requested approval on this from management by Tuesday, and the meeting coordinator agreed to review and sign off the budget spreadsheet tonight."
            citations = [r["document"] for r in search_results if "budget" in r["document"]["text"].lower() or "migration" in r["document"]["text"].lower()]
        else:
            answer = f"Based on the meeting: {meeting_title}, the team discussed project timelines, Stripe payment gateways, and infra scaling. Let me know if you need specific details."
            citations = search_results[0]["document"] if search_results else []

        return {
            "answer": answer,
            "citations": citations if isinstance(citations, list) else [citations]
        }

if __name__ == "__main__":
    agent = RetrievalAgent()
    # Mock data injection
    segments = [
        {"start_time": 0, "end_time": 10, "speaker": "Rahul", "text": "I will share the mobile app redesign plans tomorrow."},
        {"start_time": 10, "end_time": 20, "speaker": "Priyas", "text": "We need budget approval of $17,000 for server migration."}
    ]
    agent.add_to_vector_db("meet_1", segments)
    res = agent.answer_query("Project Sync", "What was decided about the budget?")
    print("Answer:", res["answer"])
