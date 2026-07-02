# SmartMinutes - Meeting Coordinator Agent
# Responsibilities: Orchestrate the entire meeting processing workflow. Route data and log agent communications.

import time
from typing import Dict, Any, List
from transcription import TranscriptionAgent
from summarization import SummarizationAgent
from action_items import ActionItemAgent
from retrieval import RetrievalAgent

class MeetingCoordinatorAgent:
    def __init__(self):
        self.transcriber = TranscriptionAgent()
        self.summarizer = SummarizationAgent()
        self.extractor = ActionItemAgent()
        self.retriever = RetrievalAgent()
        self.logs = []
        print("[MeetingCoordinatorAgent] Swarm Coordinator initialized.")

    def log_agent_message(self, sender: str, recipient: str, action: str, details: str):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "sender": sender,
            "recipient": recipient,
            "action": action,
            "details": details
        }
        self.logs.append(log_entry)
        print(f"[{timestamp}] {sender} -> {recipient}: {action} - {details}")

    def process_meeting(self, meeting_id: str, title: str, audio_path: str) -> Dict[str, Any]:
        """Runs the entire pipeline and returns structured data"""
        self.logs.clear()
        
        self.log_agent_message(
            sender="Coordinator",
            recipient="TranscriptionAgent",
            action="Start Transcription",
            details=f"Processing file {audio_path} for meeting '{title}'."
        )
        
        # 1. Speech-to-Text & Diarization
        segments = self.transcriber.transcribe(audio_path)
        self.log_agent_message(
            sender="TranscriptionAgent",
            recipient="Coordinator",
            action="Transcription Complete",
            details=f"Generated {len(segments)} segments with speaker diarization."
        )
        
        # 2. Summarization
        self.log_agent_message(
            sender="Coordinator",
            recipient="SummarizationAgent",
            action="Extract Summary",
            details="Generating executive summary, topic timeline, and key decisions."
        )
        summary_data = self.summarizer.generate_summary(segments)
        self.log_agent_message(
            sender="SummarizationAgent",
            recipient="Coordinator",
            action="Summary Complete",
            details="Executive summary and topic hierarchy extracted."
        )
        
        # 3. Action Items
        self.log_agent_message(
            sender="Coordinator",
            recipient="ActionItemAgent",
            action="Extract Actions",
            details="Scanning transcript segments for tasks, assignees, and deadlines."
        )
        action_items = self.extractor.extract_action_items(segments)
        self.log_agent_message(
            sender="ActionItemAgent",
            recipient="Coordinator",
            action="Actions Complete",
            details=f"Extracted {len(action_items)} action items."
        )
        
        # 4. RAG Indexing
        self.log_agent_message(
            sender="Coordinator",
            recipient="RetrievalAgent",
            action="Index Transcript",
            details="Splitting transcript into overlapping chunks and generating embeddings."
        )
        self.retriever.add_to_vector_db(meeting_id, segments)
        self.log_agent_message(
            sender="RetrievalAgent",
            recipient="Coordinator",
            action="Indexing Complete",
            details="Vector DB populated. Semantic retrieval is active."
        )
        
        # 5. Follow-up Recommendations
        self.log_agent_message(
            sender="Coordinator",
            recipient="FollowUpAgent",
            action="Draft Follow-up Email",
            details="Generating post-meeting summary email."
        )
        email_body = self.generate_followup_email(title, summary_data, action_items)
        self.log_agent_message(
            sender="FollowUpAgent",
            recipient="Coordinator",
            action="Email Complete",
            details="Follow-up email template ready for distribution."
        )
        
        return {
            "meeting_id": meeting_id,
            "title": title,
            "segments": segments,
            "summary": summary_data,
            "action_items": action_items,
            "followup_email": email_body,
            "agent_logs": self.logs
        }

    def generate_followup_email(self, title: str, summary_data: Dict[str, Any], action_items: List[Dict[str, Any]]) -> str:
        """Formulates the post-meeting follow-up email"""
        exec_sum = summary_data["executive_summary"]
        
        tasks_text = ""
        for idx, item in enumerate(action_items):
            tasks_text += f"{idx + 1}. **{item['task']}** - Assigned to {item['assignee']} (Due: {item['deadline']})\n"
            
        email = (
            f"Subject: Follow-up: {title} - Summary & Action Items\n\n"
            f"Hi Team,\n\n"
            f"Here is a summary of the decisions and follow-up tasks from our recent meeting, **{title}**.\n\n"
            f"### Meeting Summary\n"
            f"{exec_sum}\n\n"
            f"### Action Items\n"
            f"{tasks_text}\n"
            f"Please ensure you update your respective tasks in Jira or reach out if you have any questions.\n\n"
            f"Best regards,\n"
            f"SmartMinutes Follow-up Agent"
        )
        return email

if __name__ == "__main__":
    coordinator = MeetingCoordinatorAgent()
    results = coordinator.process_meeting("meet_101", "Mobile App Redesign Sync", "redesign_audio.wav")
    print("\n--- PROCESS COMPLETE ---")
    print(f"Generated Email:\n{results['followup_email']}")
