"""
500-NPC Swarm Simulation Runtime for Games and Virtual Worlds.
"""

import time
import torch
from .npc_planner import NPCPlanner, generate_npc_prune_map, compact_decision_tree_inplace


class SwarmSimulator:
    """
    Simulates hundreds of autonomous NPCs making concurrent real-time decisions.
    """
    def __init__(self, num_npcs: int = 500, actions_per_npc: int = 32, top_k: int = 8):
        self.num_npcs = num_npcs
        self.N = actions_per_npc
        self.K = top_k
        self.planner = NPCPlanner(candidate_actions=self.N, top_k=self.K)

    def step(self, device: torch.device) -> dict:
        B = self.num_npcs
        actions = torch.randn((B, self.N, 64), dtype=torch.float32, device=device)
        scores = torch.randn((B, self.N), dtype=torch.float32, device=device)

        start = time.perf_counter()
        _, su, sv, ns = generate_npc_prune_map(scores, self.K)
        compact_decision_tree_inplace(actions, su, sv, ns)
        if device.type == "cuda":
            torch.cuda.synchronize()
        elapsed_us = (time.perf_counter() - start) * 1e6

        return {
            "num_npcs": B,
            "latency_us": elapsed_us,
            "latency_per_npc_us": elapsed_us / B,
            "aux_vram_bytes": 0,
        }
