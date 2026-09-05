"""
IdemNPC: Zero-VRAM Cognitive NPC Engine for Unity, Unreal, and Game Studios.
Protected under U.S. Patent Application No. 64/148,668.
Author: Dr. A. Emre ÇETİN (aemre.cetin@gmail.com)
"""

__version__ = "0.1.0"
__author__ = "Dr. A. Emre ÇETİN"

from .npc_planner import NPCPlanner, compact_decision_tree_inplace, generate_npc_prune_map
from .dialogue_memory import NPCDialogueMemory
from .swarm_simulator import SwarmSimulator

__all__ = [
    "NPCPlanner",
    "compact_decision_tree_inplace",
    "generate_npc_prune_map",
    "NPCDialogueMemory",
    "SwarmSimulator",
]
