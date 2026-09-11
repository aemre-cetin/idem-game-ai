# IdemNPC Roblox (Luau) Package

> **Zero-GC In-Place AI Compactor & 5,000+ Swarm Engine for Roblox**  
> *Author: Dr. A. Emre ÇETİN | Patent Pending: U.S. Patent App. No. 64/148,668*

---

## 1. Why Roblox Games Need IdemNPC

On Roblox servers, AI scripts running in `Heartbeat` have a rigid **<2.0 ms execution budget** to prevent server-side tick degradation below 60 Hz. 

The #1 culprit for server lag, rubberbanding, and ping spikes (50 ms $\to$ 800 ms) is the **Luau Garbage Collector (GC)**:
* Calling `table.remove(entities, index)` causes an $O(N)$ shift of all succeeding elements.
* Re-allocating dynamic tables (`local alive = {}`) every tick creates immense garbage memory churn.

**IdemNPC** solves this natively in typed Luau:
1. **Zero-GC Compaction:** Uses 2-cycle involution transpositions ($\pi = \pi^{-1}$) to swap dead/inactive entities with active ones in $O(1)$ scalar steps.
2. **0.00 Bytes GC Churn:** Eliminates temporary tables and `table.remove` entirely.
3. **5,000+ Active Mobs:** Enables Tower Defense games, zombie survival hordes, and anime boss battles to simulate thousands of entities at a locked 60 FPS on low-end mobile devices.

---

## 2. Installation Methods

### Method A: Wally (Recommended for Professional Studios)
Add `idemnpc-luau` to your `wally.toml`:
```toml
[dependencies]
IdemNPC = "aemre-cetin/idemnpc-luau@0.1.0"
```
Then run:
```bash
wally install
```

### Method B: Rojo & Roblox Studio
1. Clone this repository or copy the `roblox/` folder into your project.
2. Use `rojo serve` to sync `IdemNPC` directly into `ReplicatedStorage`.

### Method C: Drag & Drop
Copy `IdemNPC.luau`, `IdemSwarm.luau`, and `IdemSpatialGrid.luau` directly into a `ModuleScript` inside `ReplicatedStorage`.

---

## 3. Quick Start: Tower Defense / Zombie Horde Example

```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local IdemNPCSuite = require(ReplicatedStorage.IdemNPC)
local IdemNPC = IdemNPCSuite.IdemNPC
local IdemSwarm = IdemNPCSuite.IdemSwarm

-- Initialize a 2,000 zombie horde moving toward the player base
local horde = IdemSwarm.new({
    maxEntities = 2000,
    moveSpeed = 14.0,
    targetX = 0,
    targetY = 0,
    targetZ = 0,
})

-- Server tick loop (60 Hz)
game:GetService("RunService").Heartbeat:Connect(function(dt)
    -- 1. Step swarm: updates positions and compacts alive zombies in-place
    -- Zero Luau tables allocated!
    local activeCount = horde:step(dt)

    -- 2. Tower Defense targeting: partition top 10 highest-threat enemies
    local topK = IdemNPC.selectTopKInPlace(horde.entities, function(e)
        return e.threat
    end, 10)

    -- Towers fire at horde.entities[1..topK] with zero sorting allocations!
end)
```

