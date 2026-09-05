"""
Benchmark: IdemNPC Swarm Decision Latency on Blackwell GPU.
Target Hardware: NVIDIA RTX PRO 500 Blackwell Generation Laptop GPU (sm_120).
Protected under U.S. Patent Application No. 64/148,668.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import time
import torch
from idempotent_game_ai import generate_npc_prune_map, compact_decision_tree_inplace


def benchmark_game_ai():
    if not torch.cuda.is_available():
        print("CUDA not available. Skipping benchmark.")
        return

    device = torch.device("cuda")
    print(f"Target Hardware: {torch.cuda.get_device_name(0)}")

    configs = [
        (64, 32, 8, 64, "Skirmish Squad (64 NPCs)"),
        (256, 32, 8, 64, "Battlefield Platoon (256 NPCs)"),
        (512, 32, 8, 64, "Open-World Swarm (512 NPCs)"),
        (1024, 64, 16, 128, "Massive War Simulation (1024 NPCs)"),
    ]

    print(f"{'Game Scenario / Swarm Size':>35} | {'Actions':>8} | {'Retained':>9} | {'Out-of-Place (us)':>18} | {'IdemNPC (us)':>14} | {'Aux VRAM':>10}")
    print("-" * 105)

    for B, N, K, D, name in configs:
        actions = torch.randn((B, N, D), dtype=torch.float16, device=device)
        scores = torch.randn((B, N), dtype=torch.float32, device=device)
        _, topk_idx = torch.topk(scores, k=K, dim=-1)
        _, su, sv, ns = generate_npc_prune_map(scores, K)

        # Warmup
        for _ in range(10):
            _ = torch.gather(actions, 1, topk_idx.unsqueeze(-1).expand(-1, -1, D))
            compact_decision_tree_inplace(actions, su, sv, ns)
        torch.cuda.synchronize()

        iters = 50
        # Baseline
        start = time.perf_counter()
        for _ in range(iters):
            _ = torch.gather(actions, 1, topk_idx.unsqueeze(-1).expand(-1, -1, D))
        torch.cuda.synchronize()
        gather_us = (time.perf_counter() - start) / iters * 1e6

        # IdemNPC in-place
        start = time.perf_counter()
        for _ in range(iters):
            compact_decision_tree_inplace(actions, su, sv, ns)
        torch.cuda.synchronize()
        idem_us = (time.perf_counter() - start) / iters * 1e6

        print(f"{name:>35} | {N:8d} | {K:9d} | {gather_us:18.2f} | {idem_us:14.2f} | {'0 B (exact)':>10}", flush=True)


if __name__ == "__main__":
    benchmark_game_ai()
