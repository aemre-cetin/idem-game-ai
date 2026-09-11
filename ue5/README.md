# IdemNPC Unreal Engine 5 Plugin

> **Zero-VRAM In-Place AI Compactor for Unreal Engine 5 (5.3 – 5.5+)**  
> *Author: Dr. A. Emre ÇETİN | Patent Pending: U.S. Patent App. No. 64/148,668*

---

## 1. Overview

In high-density Unreal Engine 5 games (open-world crowd simulations, survival horde shooters, MMORPG battlegrounds, RTS), managing 1,000–10,000 NPCs with traditional `TArray::RemoveAt()` or dynamic actor filtering creates severe CPU overhead and cache pollution:
* `TArray::RemoveAt()` forces an $O(N)$ memory shift of all subsequent elements.
* Creating temporary filtered `TArray` copies causes continuous heap allocation and deallocation, producing GC frame hitches.

**IdemNPC** eliminates this overhead through **in-place 2-cycle involution transpositions ($\pi = \pi^{-1}$)**:
* Active entities are consolidated directly into the prefix `[0, ActiveCount - 1]` with strictly **0 Bytes of auxiliary heap allocation**.
* Preserves contiguous memory layout for maximum cache locality and SIMD vectorization.
* Blueprint callable (`UIdemNPCBlueprintLibrary`) and native C++ template support.

---

## 2. Installation in Your UE5 Project

1. Copy the `ue5/` folder into your Unreal Engine project's `Plugins/` directory:
   ```
   YourProject/
   └── Plugins/
       └── IdemNPC/
           ├── IdemNPC.uplugin
           └── Source/
               └── IdemNPC/
   ```
2. In your project's `.uproject` file, verify that `IdemNPC` is enabled:
   ```json
   {
       "Plugins": [
           {
               "Name": "IdemNPC",
               "Enabled": true
           }
       ]
   }
   ```
3. Re-generate project files and compile in Visual Studio, Rider, or Xcode.

---

## 3. Usage Examples

### C++ Native Usage
```cpp
#include "IdemNPCCompactor.h"

// Array of 5,000 entity states
TArray<FIdemEntityState> HordeEntities;

// In-place compaction: consolidates all alive/active entities to the front
int32 ActiveCount = UIdemNPCBlueprintLibrary::CompactActiveNPCsInPlace(HordeEntities);

// Only tick active entities without modifying array capacity
for (int32 i = 0; i < ActiveCount; ++i)
{
    TickNPC(HordeEntities[i]);
}
```

### Blueprint Usage
Search for **Idem NPC** in any Blueprint graph:
* `Compact Active NPCs In Place`
* `Select Top K Threats In Place`

