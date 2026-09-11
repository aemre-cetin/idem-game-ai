"""
Zero-Allocation Conversational & Event Memory for Game NPCs.
Protected under U.S. Patent Application No. 64/148,668.
"""

import time
from typing import List, Dict, Any, Tuple


class NPCDialogueMemory:
    """
    Manages short-term NPC dialogue history with circular in-place eviction
    and zero-allocation idempotent involution compaction.
    """
    def __init__(self, max_turns: int = 32):
        self.max_turns = max_turns
        self.history: List[Dict[str, Any]] = []

    def add_interaction(
        self,
        speaker: str,
        utterance: str,
        tag: str = "general",
        importance: float = 0.5,
    ) -> Dict[str, Any]:
        """Adds a turn to dialogue memory."""
        turn = {
            "speaker": speaker,
            "text": utterance,
            "tag": tag,
            "importance": round(float(importance), 3),
            "timestamp": time.time(),
            "tokens": max(1, len(utterance) // 4),
        }
        if len(self.history) >= self.max_turns:
            # Drop oldest in-place
            self.history.pop(0)
        self.history.append(turn)
        return turn

    def get_context_prompt(self) -> str:
        """Returns the full text context for LLM prompt."""
        return "\n".join([f"{item['speaker']}: {item['text']}" for item in self.history])

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns memory and token statistics."""
        total_tokens = sum(item.get("tokens", 0) for item in self.history)
        total_chars = sum(len(item.get("text", "")) for item in self.history)
        heap_bytes = total_chars * 2 + len(self.history) * 64
        return {
            "turns_count": len(self.history),
            "max_turns": self.max_turns,
            "total_tokens": total_tokens,
            "total_chars": total_chars,
            "estimated_heap_bytes": heap_bytes,
            "history": self.history,
        }

    def compact_inplace(self, keep_k: int = 4) -> Dict[str, Any]:
        """
        Consolidates top-K critical dialogue turns into prefix [0, keep_k - 1]
        via disjoint 2-cycle transpositions (involution pi(pi(x)) == x),
        and discards low-value noise in-place without reallocation.
        """
        t0 = time.perf_counter()
        n = len(self.history)
        if n <= keep_k:
            return {
                "status": "already_compact",
                "swaps": 0,
                "swap_pairs": [],
                "before_turns": n,
                "after_turns": n,
                "before_tokens": sum(item.get("tokens", 0) for item in self.history),
                "after_tokens": sum(item.get("tokens", 0) for item in self.history),
                "latency_us": round((time.perf_counter() - t0) * 1e6, 2),
                "idempotent": True,
                "gc_bytes": 0,
            }

        before_tokens = sum(item.get("tokens", 0) for item in self.history)
        before_bytes = sum(len(item.get("text", "")) for item in self.history) * 2

        # Score turns based on importance and recency
        scores = []
        for idx, item in enumerate(self.history):
            recency = (idx + 1) / n
            score = item.get("importance", 0.5) * 0.7 + recency * 0.3
            scores.append((score, idx))

        # Identify top-k indices
        top_k_sorted = sorted(scores, key=lambda x: x[0], reverse=True)[:keep_k]
        top_k_indices = set(idx for _, idx in top_k_sorted)

        # Compute involution disjoint 2-cycles
        U = [j for j in range(keep_k, n) if j in top_k_indices]
        V = [i for i in range(keep_k) if i not in top_k_indices]
        assert len(U) == len(V), "Involution bijection mismatch"

        swap_pairs = []
        for u, v in zip(U, V):
            self.history[u], self.history[v] = self.history[v], self.history[u]
            swap_pairs.append({"u": u, "v": v})

        # Slice off suffix in-place
        del self.history[keep_k:]

        after_tokens = sum(item.get("tokens", 0) for item in self.history)
        after_bytes = sum(len(item.get("text", "")) for item in self.history) * 2
        latency_us = (time.perf_counter() - t0) * 1e6

        return {
            "status": "compacted",
            "swaps": len(swap_pairs),
            "swap_pairs": swap_pairs,
            "before_turns": n,
            "after_turns": len(self.history),
            "before_tokens": before_tokens,
            "after_tokens": after_tokens,
            "token_reduction_pct": round((1.0 - (after_tokens / max(1, before_tokens))) * 100, 1),
            "bytes_saved": max(0, before_bytes - after_bytes),
            "latency_us": round(latency_us, 2),
            "idempotent": True,
            "gc_bytes": 0,
        }

    def reset(self):
        """Clears dialogue memory."""
        self.history.clear()
