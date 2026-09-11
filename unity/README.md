# IdemNPC Unity Package (Burst & DOTS Compatible)

> **Zero-Allocation In-Place AI Compactor for Unity (2022.3 LTS – 2024+)**  
> *Author: Dr. A. Emre ÇETİN | Patent Pending: U.S. Patent App. No. 64/148,668*

---

## 1. Overview

In Unity, simulating thousands of NPCs (Tower Defense enemies, zombie hordes, strategy units) typically causes severe **Garbage Collection (GC) pauses**:
* Standard lists (`List<T>.RemoveAt()`) shift entire memory buffers ($O(N)$) and trigger memory reallocations.
* Filtering active entities into new collections spawns managed heap garbage, causing stuttering frame drops.

**IdemNPC** provides **strictly 0 Bytes of managed heap allocation**:
* Uses `Unity.Collections.NativeArray<T>` and `Unity.Burst` compilation.
* Implements in-place 2-cycle involution transpositions ($\pi = \pi^{-1}$).
* Consolidates active entities into `[0, ActiveCount - 1]` in sub-millisecond execution times.

---

## 2. Installation

### Via Unity Package Manager (UPM)
1. Open Unity $\to$ **Window** $\to$ **Package Manager**.
2. Click **+** $\to$ **Add package from disk...**
3. Select `packages/idem-game-ai/unity/package.json`.

---

## 3. Quick Start Example

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Mathematics;
using IdemNPC.Runtime;

public class HordeManager : MonoBehaviour
{
    private NativeArray<IdemAgentState> agents;

    void Start()
    {
        // Allocate 5,000 agents in native unmanaged memory
        agents = new NativeArray<IdemAgentState>(5000, Allocator.Persistent);
        for (int i = 0; i < agents.Length; i++)
        {
            agents[i] = new IdemAgentState
            {
                EntityId = i,
                Position = new float3(UnityEngine.Random.insideUnitSphere * 50f),
                Health = 100f,
                ThreatScore = UnityEngine.Random.Range(0f, 100f),
                IsActive = true
            };
        }
    }

    void Update()
    {
        // 1. In-place compaction: Consolidates active NPCs to the front
        // Strictly 0.00 Bytes GC allocated!
        int activeCount = IdemNPC.CompactActiveInPlace(ref agents);

        // 2. Select top 50 highest threats for tower targeting
        int topK = IdemNPC.SelectTopKThreatsInPlace(ref agents, 50);

        Debug.Log($"Active Agents: {activeCount} | Top Threats Partitioned: {topK}");
    }

    void OnDestroy()
    {
        if (agents.IsCreated) agents.Dispose();
    }
}
```

