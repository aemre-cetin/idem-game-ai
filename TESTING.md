# IdemNPC Master Test & Verification Guide

> **Unified Multi-Engine Test Suite for Unreal Engine 5, Unity, Roblox (Luau), and PyTorch**  
> *Author: Dr. A. Emre ÇETİN | Protected under U.S. Patent Application No. 64/148,668*

---

## 1. Multi-Engine Test Matrix

This guide provides direct links and quick commands for testing **IdemNPC** across all supported platforms:

| Target Platform | Native Framework | Dedicated Test Guide | Quick Command / Test Location | Verification Metric |
| :--- | :--- | :--- | :--- | :---: |
| **Roblox (Luau)** | Typed Luau (`--!strict`) | [Roblox Testing Guide](./roblox/TESTING.md) | `benchmark.server.luau` | **0.00 KB GC Delta** (0.43 ms @ 5k mobs) |
| **Unity** | C# Burst / DOTS | [Unity Testing Guide](./unity/TESTING.md) | `HordeTestRunner.cs` | **0 B GC Alloc** (120 FPS Profiler) |
| **Unreal Engine 5** | C++20 / Blueprints | [UE5 Testing Guide](./ue5/TESTING.md) | `BP_HordeTester` | **<0.42 ms** @ 10k entities (0 B Aux VRAM) |
| **Python / CUDA** | PyTorch Blackwell (`sm_120`) | Below Section 2 | `test_game_ai.py` | **100% Bit-Exact**, 0 Bytes VRAM leak |

---

## 2. Instant Local Verification (Zero Engine Setup)

You can run comprehensive unit tests and simulations for all algorithms directly from your terminal using Python:

```powershell
# 1. Test Luau Algorithmic Parity & Mathematical Idempotence
python packages/idem-game-ai/tests/test_roblox_luau_logic.py

# 2. Run 5,000-Mob Luau Simulation via CLI
python packages/idem-game-ai/src/idempotent_game_ai/cli.py roblox-demo --entities 5000 --ticks 100

# 3. Test GPU In-Place Compaction & 0-Byte Auxiliary VRAM
.venv\Scripts\python packages/idem-game-ai/tests/test_game_ai.py

# 4. Verify Multi-Engine Export Manifest
python packages/idem-game-ai/src/idempotent_game_ai/cli.py export-all
```

---

## 3. Platform-Specific Integration Links

* **Roblox Studio Integration:** See [`packages/idem-game-ai/roblox/TESTING.md`](./roblox/TESTING.md)
* **Unity UPM Integration:** See [`packages/idem-game-ai/unity/TESTING.md`](./unity/TESTING.md)
* **Unreal Engine 5 Plugin:** See [`packages/idem-game-ai/ue5/TESTING.md`](./ue5/TESTING.md)

