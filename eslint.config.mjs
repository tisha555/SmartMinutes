# SmartMinutes - FastAPI Backend Application
# Responsibilities: Define REST APIs and handle service coordination.

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Import from security and coordinator (relative path resolution assumed in run context)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ai_services")))
from coordinator import MeetingCoordinatorAgent
from security import verify_password, get_password_hash, create_access_token

app = FastAPI(title="SmartMinutes API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents coordinator
coordinator = MeetingCoordinatorAgent()

# Dummy database dictionaries to simulate database transactions
users_db = {}
meetings_db = {}

# Pydantic schemas for request validation
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RAGQuery(BaseModel):
    query: str


# Authentication endpoints
@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(user.password)
    user_id = f"user_{len(users_db) + 1}"
    users_db[user.email] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "password": hashed_pwd
    }
    return {"id": user_id, "name": user.name, "email": user.email, "message": "User registered successfully"}

@app.post("/api/auth/login", response_model=Token)
def login(user: UserLogin):
    db_user = users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": db_user["id"]})
    return {"access_token": token, "token_type": "bearer"}


# Meeting capturing & processing endpoints
@app.post("/api/meetings/upload")
async def upload_meeting(title: str, file: UploadFile = File(...)):
    """
    Receives audio/video file and queues background task for AI pipeline processing.
    In production, this uploads to S3, and delegates processing to Celery workers.
    """
    meeting_id = f"meet_{len(meetings_db) + 1}"
    
    # Save the file locally during development
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    print(f"[FastAPI] File saved to {file_path}. Initiating multi-agent coordination...")
    
    # Execute the coordinator pipeline (simulated synchronously or via task queue)
    result = coordinator.process_meeting(meeting_id, title, file_path)
    
    # Save results to the database dictionary
    meetings_db[meeting_id] = result
    
    return {
        "meeting_id": meeting_id,
        "title": title,
        "status": "Processed",
        "result": {
            "summary": result["summary"]["executive_summary"],
            "action_items_count": len(result["action_items"])
        }
    }

@app.get("/api/meetings")
def list_meetings():
    """Returns lists of all meetings"""
    return [
        {
            "meeting_id": mid,
            "title": m["title"],
            "date": m.get("date", "2026-06-17"),
            "duration": len(m["segments"]) * 10, # Mock duration
            "executive_summary_preview": m["summary"]["executive_summary"][:100] + "..."
        }
        for mid, m in meetings_db.items()
    ]

@app.get("/api/meetings/{meeting_id}")
def get_meeting(meeting_id: str):
    """Retrieves full details of a specific processed meeting"""
    meeting = meetings_db.get(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


# Retrieval and Chat endpoints (RAG)
@app.post("/api/meetings/{meeting_id}/chat")
def chat_with_meeting(meeting_id: str, query_data: RAGQuery):
    """Semantic question-answering with citation matching (RAG) on a single meeting"""
    meeting = meetings_db.get(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
        
    # Delegate query answering to Retrieval Agent
    answer_payload = coordinator.retriever.answer_query(meeting["title"], query_data.query)
    return answer_payload

@app.get("/api/analytics/overview")
def get_analytics():
    """Generates user engagement and model analytics"""
    total_meetings = len(meetings_db)
    total_duration = sum([len(m["segments"]) * 10 for m in meetings_db.values()])
    
    # Simple defaults for dashboard visualizations
    return {
        "total_meetings_processed": total_meetings,
        "total_speaking_time_sec": total_duration,
        "average_duration_sec": total_duration / max(total_meetings, 1),
        "speaking_time_distribution": {
            "Speaker 1": 45.2,
            "Speaker 2": 25.8,
            "Speaker 3": 18.0,
            "Speaker 4": 11.0
        },
        "action_item_completion_rate": 68.5,
        "frequently_discussed_topics": [
            {"name": "Mobile App Redesign", "count": 12},
            {"name": "Server Migration", "count": 7},
            {"name": "Stripe Integration", "count": 5},
            {"name": "Budget Approval", "count": 3}
        ],
        "estimated_api_cost_usd": total_meetings * 0.12 # Mocked token cost calculation
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
