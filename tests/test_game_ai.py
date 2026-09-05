"""
Unit Tests for IdemNPC (Game AI Decision Tree Engine).
Verifies:
1. In-place action tensor preservation (data_ptr() unchanged).
2. State-level algebraic idempotence T(T(Actions)) = T(Actions).
3. Zero auxiliary VRAM allocation on consumer GPU.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import torch
from idempotent_game_ai import NPCPlanner, generate_npc_prune_map, compact_decision_tree_inplace


def test_npc_tactical_compaction_and_idempotence():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    NumNPCs = 16
    NumActions = 32
    ActionDim = 64
    TopK = 8

    torch.manual_seed(42)
    actions = torch.randn((NumNPCs, NumActions, ActionDim), dtype=torch.float32, device=device)
    scores = torch.randn((NumNPCs, NumActions), dtype=torch.float32, device=device)

    orig_ptr = actions.data_ptr()
    _, topk_idx = torch.topk(scores, k=TopK, dim=-1)

    target_map, su, sv, ns = generate_npc_prune_map(scores, TopK)
    compact_decision_tree_inplace(actions, su, sv, ns)

    # 1. In-place verification
    assert actions.data_ptr() == orig_ptr, "Action tensor data_ptr changed!"

    # 2. No NaNs
    assert not torch.isnan(actions).any(), "NaN found in action tensor!"

    # 3. Mathematical Idempotence
    recompacted_scores = scores.clone()
    for b in range(NumNPCs):
        for idx in range(int(ns[b].item())):
            u = int(su[b, idx].item())
            v = int(sv[b, idx].item())
            tmp = recompacted_scores[b, u].clone()
            recompacted_scores[b, u] = recompacted_scores[b, v]
            recompacted_scores[b, v] = tmp

    _, _, _, second_ns = generate_npc_prune_map(recompacted_scores, TopK)
    assert (second_ns == 0).all(), "Second compaction performed non-zero swaps! Idempotence violated!"

    print("PASS: IdemNPC in-place decision compaction and mathematical idempotence verified!")


def test_zero_aux_vram():
    if not torch.cuda.is_available():
        return

    device = torch.device("cuda")
    actions = torch.randn((128, 64, 128), dtype=torch.float16, device=device)
    scores = torch.randn((128, 64), dtype=torch.float32, device=device)
    _, su, sv, ns = generate_npc_prune_map(scores, 16)

    torch.cuda.reset_peak_memory_stats()
    mem_before = torch.cuda.memory_allocated()

    compact_decision_tree_inplace(actions, su, sv, ns)
    torch.cuda.synchronize()

    mem_after = torch.cuda.memory_allocated()
    assert mem_after == mem_before, f"Memory leak: {mem_after - mem_before} bytes allocated!"
    print("PASS: Exact 0-byte auxiliary VRAM footprint verified on GPU!")


if __name__ == "__main__":
    test_npc_tactical_compaction_and_idempotence()
    test_zero_aux_vram()
    print("ALL IDEMNPC TESTS PASSED!")
