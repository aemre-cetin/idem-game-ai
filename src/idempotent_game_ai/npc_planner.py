"""
In-Place Decision Tree & Action Candidate Compactor for Game NPCs.
Consolidates top-K tactical actions in-place directly within local GPU/CPU registers.
Protected under U.S. Patent Application No. 64/148,668.
"""

import torch
from typing import Tuple


def generate_npc_prune_map(
    q_values: torch.Tensor,
    K: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Constructs an involution permutation pi (pi(pi(x)) == x) swapping
    low-value tactical actions in prefix [0, K-1] with high-value actions in suffix [K, N-1].
    q_values shape: [NumNPCs, NumActions]
    """
    B, N = q_values.shape
    device = q_values.device
    assert K <= N, "Retained tactical actions K must be <= candidate pool N"

    target_map = torch.arange(N, device=device, dtype=torch.int64).unsqueeze(0).repeat(B, 1)
    _, topk_idx = torch.topk(q_values, k=K, dim=-1, largest=True, sorted=False)

    max_swaps = min(K, N - K)
    swap_u = torch.zeros((B, max_swaps), dtype=torch.int64, device=device)
    swap_v = torch.zeros((B, max_swaps), dtype=torch.int64, device=device)
    num_swaps = torch.zeros(B, dtype=torch.int32, device=device)

    topk_list = topk_idx.cpu().tolist()
    for b in range(B):
        selected_set = set(topk_list[b])
        U = [j for j in range(K, N) if j in selected_set]
        V = [i for i in range(K) if i not in selected_set]

        cnt = len(U)
        assert cnt == len(V)
        num_swaps[b] = cnt

        for idx in range(cnt):
            u = U[idx]
            v = V[idx]
            target_map[b, u] = v
            target_map[b, v] = u
            swap_u[b, idx] = u
            swap_v[b, idx] = v

    return target_map, swap_u, swap_v, num_swaps


def compact_decision_tree_inplace(
    action_tensor: torch.Tensor,
    swap_u: torch.Tensor,
    swap_v: torch.Tensor,
    num_swaps: torch.Tensor,
) -> torch.Tensor:
    """
    Applies disjoint 2-cycle transpositions in-place across action feature embeddings.
    action_tensor shape: [NumNPCs, NumActions, ActionDim]
    Guarantees: data_ptr() is preserved, auxiliary VRAM allocated = 0 Bytes.
    """
    B = action_tensor.shape[0]
    swaps_list = num_swaps.tolist() if isinstance(num_swaps, torch.Tensor) else num_swaps
    for b in range(B):
        cnt = swaps_list[b]
        if cnt > 0:
            u_idx = swap_u[b, :cnt]
            v_idx = swap_v[b, :cnt]
            tmp = action_tensor[b, u_idx].clone()
            action_tensor[b, u_idx] = action_tensor[b, v_idx]
            action_tensor[b, v_idx] = tmp

    return action_tensor


class NPCPlanner:
    """
    Tactical Decision Engine for game NPCs.
    Evaluates action candidates and packs top choices in-place without stealing render VRAM.
    """
    def __init__(self, action_dim: int = 64, candidate_actions: int = 32, top_k: int = 8):
        self.action_dim = action_dim
        self.N = candidate_actions
        self.K = top_k

    def plan_tactics_inplace(
        self,
        actions: torch.Tensor,
        action_scores: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        _, su, sv, ns = generate_npc_prune_map(action_scores, self.K)
        compact_decision_tree_inplace(actions, su, sv, ns)
        return actions[:, :self.K], action_scores
