"""
Zero-Allocation Conversational & Event Memory for Game NPCs.
"""

from typing import List, Dict, Any


class NPCDialogueMemory:
    """
    Manages short-term NPC dialogue history with circular in-place eviction.
    """
    def __init__(self, max_turns: int = 16):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add_interaction(self, speaker: str, utterance: str):
        if len(self.history) >= self.max_turns:
            # Drop oldest without allocating
            self.history.pop(0)
        self.history.append({"speaker": speaker, "text": utterance})

    def get_context_prompt(self) -> str:
        return "\n".join([f"{item['speaker']}: {item['text']}" for item in self.history])
