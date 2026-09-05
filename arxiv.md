# arXiv & ResearchGate Submission Metadata: Product 4 (idempotent-game-ai)

## 1. arXiv Metadata
- **Title:** Zero-VRAM Cognitive NPC Architectures: In-Place Decision Trees and Memory Compaction for Real-Time Game Engines
- **Authors:** Dr. A. Emre ÇETİN (aemre.cetin@gmail.com)
- **Primary Category:** `cs.AI` (Artificial Intelligence)
- **Secondary Categories:** `cs.GR` (Graphics), `cs.DC` (Distributed, Parallel, and Cluster Computing), `cs.PF` (Performance)
- **Comments:** 3 pages, 2 figures. Reference implementation available at https://github.com/aemre-cetin/idempotent-game-ai. Protected under U.S. Patent Application No. 64/148,668.
- **Archive Package:** `paper/arxiv_package_idempotent_game_ai.tar.gz`

### Abstract:
Embedding autonomous, reasoning Non-Player Characters (NPCs) into modern interactive 3D virtual worlds and video game engines (Unreal Engine 5, Unity) is severely constrained by GPU video memory contention. With visual rendering pipelines (rasterization, geometry shading, ray tracing) consuming upwards of 90% of dedicated VRAM, allocating auxiliary dynamic buffers (`cudaMalloc`, `torch.gather`) to evaluate multi-agent Monte Carlo Tree Search (MCTS) or utility-based behavior trees introduces frame latency jitter and catastrophic frame-rate drops.
Building upon the mathematical foundations of idempotent permutations ($f(f(s)) = f(s)$) established by Cetin (arXiv:1307.3877, arXiv:1301.2046), this paper presents IdemNPC: a zero-VRAM cognitive decision architecture for real-time game engines. IdemNPC maps tactical action candidate pruning into an involution permutation map ($\pi(\pi(x)) = x$) comprising disjoint 2-cycles, executing in-situ vector transpositions directly within GPU scalar registers. Evaluated on an enterprise NVIDIA RTX PRO 500 Blackwell Generation Laptop GPU across swarm scales from 64 to 1,024 concurrent agents, IdemNPC achieves: (1) 100% elimination of auxiliary VRAM allocation (0 bytes allocated); (2) microsecond decision pruning latencies (sub-15 us per agent); (3) bit-exact numerical fidelity ($\Delta = 0.0$, 0 NaN); and (4) mathematical state idempotence ($T(T(	ext{Tree})) = T(	ext{Tree})$), enabling game developers to deploy hundreds of intelligent autonomous NPCs with zero rendering frame-rate degradation.
