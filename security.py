# SmartMinutes - Summarization Agent
# Responsibilities: Generate executive summaries, identify key topics, and list decisions.

import json
from typing import List, Dict, Any

class SummarizationAgent:
    def __init__(self, provider: str = "openai", model_name: str = "gpt-4-turbo"):
        self.provider = provider
        self.model_name = model_name
        print(f"[SummarizationAgent] Initializing with LLM: {provider}/{model_name}")

    def generate_summary(self, transcript_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes transcripts to extract summaries.
        Returns a dict: {
            "executive_summary": "...",
            "topic_summary": "JSON String with topics and details",
            "key_decisions": ["...", "..."]
        }
        """
        # Combine transcript segments for the LLM prompt
        full_transcript = "\n".join([f"{seg['speaker']}: {seg['text']}" for seg in transcript_segments])
        print(f"[SummarizationAgent] Summarizing transcript of {len(transcript_segments)} segments...")

        # In a real application, you would invoke an LLM pipeline:
        # response = openai.ChatCompletion.create(
        #     model=self.model_name,
        #     messages=[
        #         {"role": "system", "content": "You are an expert secretary. Summarize the meeting transcript, extract topics, and key decisions."},
        #         {"role": "user", "content": full_transcript}
        #     ]
        # )
        # parsed_result = parse_llm_response(response)

        # Mocked LLM output based on the transcript segments:
        executive_summary = (
            "The team discussed progress on the mobile app redesign, specifically finalizing the Figma mockups "
            "and simplified user flows for the payment gateway. The coordinator requested a review of the Q3 budget "
            "approvals, where server migration was estimated at $12,000, and scaling database instances was estimated "
            "at $5,000. Decisions were made regarding the review timelines, and tasks were assigned to Rahul and Speaker 1."
        )

        topics = [
            {
                "topic": "Mobile App Redesign",
                "summary": "Figma mockups have been completed. The design covers user flows, Stripe integration, and new onboarding screens. UX details are being polished.",
                "importance_score": 0.9,
                "time_range": "00:00 - 00:45"
            },
            {
                "topic": "Q3 Infrastructure Budget",
                "summary": "Priyas presented the server migration cost ($12,000) and database scaling cost ($5,000), totaling $17,000. Needs approval from management.",
                "importance_score": 0.85,
                "time_range": "00:46 - 01:20"
            }
        ]

        key_decisions = [
            "Simplified Stripe integration was chosen as the primary payment gateway for the mobile app.",
            "Meeting coordinator (Speaker 1) agreed to review and sign off the Q3 budget spreadsheet tonight."
        ]

        return {
            "executive_summary": executive_summary,
            "topic_summary": json.dumps(topics),
            "key_decisions": key_decisions
        }

if __name__ == "__main__":
    agent = SummarizationAgent()
    sample_segments = [
        {"speaker": "Speaker 1", "text": "Let's review the budget."},
        {"speaker": "Speaker 2", "text": "It is $17k for migrations."}
    ]
    summary = agent.generate_summary(sample_segments)
    print("Executive Summary:")
    print(summary["executive_summary"])
    print("\nKey Decisions:")
    print(summary["key_decisions"])
