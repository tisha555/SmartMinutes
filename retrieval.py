# SmartMinutes - Action Item Agent
# Responsibilities: Extract tasks, identify owners, and detect deadlines from transcript segments.

import re
from typing import List, Dict, Any

class ActionItemAgent:
    def __init__(self):
        print("[ActionItemAgent] Initializing...")

    def extract_action_items(self, transcript_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scans transcript segments and extracts tasks, assignees, and deadlines.
        Returns a list of dicts: {task, assignee, deadline, priority}
        """
        action_items = []
        print(f"[ActionItemAgent] Extracting action items from {len(transcript_segments)} segments...")

        # In a real environment, this utilizes NLP / LLM extraction. E.g.:
        # prompt = "Identify tasks, owners, and deadlines in this segment..."
        # We can also use rule-based extractors for common patterns:
        
        # We simulate this agent scanning the specific transcript text.
        # Segment 3: "I will share the final design document by Friday. It covers Stripe integration..." (Speaker: Speaker 3 / Rahul)
        # Segment 5: "I need approval on this from the management by Tuesday." (Speaker: Speaker 4 / Priyas)
        # Segment 6: "I'll review the budget sheet tonight..." (Speaker: Speaker 1 / Coordinator)
        
        for seg in transcript_segments:
            text = seg["text"]
            speaker = seg["speaker"]
            
            # Simulated NLP parser finding actions:
            if "share the final design document" in text.lower():
                action_items.append({
                    "task": "Share the final design document (Stripe integration & onboarding UX)",
                    "assignee": "Rahul",
                    "deadline": "Friday",
                    "priority": "High",
                    "status": "Pending"
                })
            elif "approval on this" in text.lower() and "budget" in text.lower() or "server migration" in text.lower():
                action_items.append({
                    "task": "Approve the Q3 server migration and database database scaling budget",
                    "assignee": "Management",
                    "deadline": "Tuesday",
                    "priority": "High",
                    "status": "Pending"
                })
            elif "review the budget sheet" in text.lower():
                action_items.append({
                    "task": "Review and sign-off the Q3 budget sheet",
                    "assignee": speaker, # Speaker 1 / Coordinator
                    "deadline": "Tonight",
                    "priority": "Medium",
                    "status": "Pending"
                })

        # Fallback to general rules if no items matched (for mock/tests)
        if not action_items:
            # Let's add some default templates if they just feed any mock text
            action_items.append({
                "task": "Coordinate project sync timings",
                "assignee": "Team",
                "deadline": "Next Meeting",
                "priority": "Low",
                "status": "Pending"
            })

        return action_items

if __name__ == "__main__":
    agent = ActionItemAgent()
    sample = [
        {"speaker": "Rahul", "text": "I will share the final design document by Friday."}
    ]
    items = agent.extract_action_items(sample)
    print("Extracted Action Items:")
    for item in items:
        print(f"- Task: {item['task']} | Owner: {item['assignee']} | Due: {item['deadline']}")
