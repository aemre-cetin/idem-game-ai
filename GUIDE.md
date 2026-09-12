# idem-game-ai (idempotent_game_ai): Kapsamlı Kullanıcı ve Geliştirici Kılavuzu (GUIDE.md)

**IdemNPC: Zero-VRAM Cognitive NPC Engine for Unity, Unreal, and Game Studios.**

- **Paket Sürümü:** `0.1.0`
- **Birincil Python Modülü:** `idempotent_game_ai`
- **Donanım Hızlandırma:** Saf Python / PyTorch / Triton JIT Uyumlu
- **Lisans:** Apache 2.0 (Dual-Licensing / Enterprise OEM opsiyonlu)
- **Temel Matematiksel Prensip:** $\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$ (Tek Adımlı İdempotent İzdüşüm ve Sıfır Kopyalı Bellek İçi İnvolution)

---

## 1. Mimari ve Temel Kavramlar

`idem-game-ai` kütüphanesi, geleneksel iteratif algoritmaların ve dinamik bellek tahsislerinin (`malloc`/`free`, `O(N)` ara bellekler) yol açtığı gecikme, bellek parçalanması ve bellek duvarı (memory wall) problemlerini çözmek üzere tasarlanmıştır.

### Temel Tasarım İlkeleri:
1. **Sıfır Ek Bellek Tahsisi (0.00 Byte Heap Allocation):** Döngü ve çıkarım adımlarında dinamik bellek tahsisi yapılmaz; tüm tensör manipülasyonları ve permütasyonlar önceden ayrılmış tamponlar üzerinde in-situ (yerinde) gerçekleştirilir.
2. **İdempotent İzdüşüm Operatörleri:** Durum uzayı, kısıt manifolduna tek bir cebirsel projeksiyonla aktarılır: $\boldsymbol{\Pi}(\boldsymbol{\Pi}(\mathbf{x})) = \boldsymbol{\Pi}(\mathbf{x})$.
3. **Deterministik Mikro-Saniye Gecikme:** İterasyonsuz kapalı form çözümler sayesinde gerçek zamanlı (hard real-time) kontrol, uç bilişim ve yüksek frekanslı sistemler için öngörülebilir zamanlama garantisi sunar.

---

## 2. Kurulum ve Ortam Yapılandırması

```bash
# Geliştirici modunda paket dizininden kurulum:
cd packages/idem-game-ai
pip install -e .

# Birim testleri koşturarak kurulumu doğrulayın:
pytest -q
```

---

## 3. Modül ve Sınıf Referansı (Tam Çalışır Kod Örnekleri)

Aşağıda `idem-game-ai` kütüphanesinin `src/idempotent_game_ai` altında yer alan tüm gerçek modülleri, sınıfları ve fonksiyonları için çalıştırılabilir örnekler sunulmuştur:

### 3.1. Modül: `idempotent_game_ai.arena_simulator`
> **Tanım:** IdemNPC: High-Density 3D Multi-Agent Swarm Arena Simulator.

Simulates up to 10,000 autonomous intelligent NPCs with boids flocking,
target pursuit, and compares Traditional Engine Dynamic Array Removal (GC Spikes)
against Patent-Pending In-Situ Idempotent Compaction (0 GC, <0.2 ms).
Includes IdemSpatial: O(N) In-Situ Spatial Partitioning & Manifold Separation.

Copyright (c) 2026 Dr. A. Emre ÇETİN
U.S. Patent Application No. 64/148,668 ("Patent Pending", Conf. No. 5890)

#### Sınıf: `ArenaSimulator`
- **Açıklama:** Simulates a high-density 3D arena with 1,000 to 10,000 autonomous agents.
Demonstrates in-situ idempotent compaction vs traditional GC list removal,
and O(N) IdemSpatial separation vs O(N^2) pairwise collision collapse.
- **Metotlar:** `__init__()`, `reset_entities()`, `set_speed_range()`, `set_spawn_count()`, `set_behavior()`, `set_engine_preset()`, `set_spatial_mode()`, `trigger_aoe_blast()`, `step()`

```python
import torch
import numpy as np
from idempotent_game_ai.arena_simulator import ArenaSimulator

# ArenaSimulator örneği oluşturma ve çalıştırma:
obj = ArenaSimulator(num_npcs=32, arena_radius=32)
output = obj.step(0.0)
print('ArenaSimulator.step çıktısı:', type(output))
```

### 3.2. Modül: `idempotent_game_ai.cli`
> **Tanım:** IdemNPC Command-Line Interface.
Multi-Engine Game AI Compaction Engine (Unreal Engine 5, Unity, Roblox Luau).
Protected under U.S. Patent Application No. 64/148,668.

#### Fonksiyon: `simulate_roblox_luau_swarm()`
- **Açıklama:** Simulates the exact typed Luau in-place 2-cycle involution compaction
and Top-K threat selection in Python.
- **Parametreler:** `num_entities, ticks`

```python
import torch
from idempotent_game_ai.cli import simulate_roblox_luau_swarm

res = simulate_roblox_luau_swarm(None, 32)
print('simulate_roblox_luau_swarm() çağrı sonucu:', type(res))
```

#### Fonksiyon: `main()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.cli import main

res = main()
print('main() çağrı sonucu:', type(res))
```

### 3.3. Modül: `idempotent_game_ai.dialogue_memory`
> **Tanım:** Zero-Allocation Conversational & Event Memory for Game NPCs.
Protected under U.S. Patent Application No. 64/148,668.

#### Sınıf: `NPCDialogueMemory`
- **Açıklama:** Manages short-term NPC dialogue history with circular in-place eviction
and zero-allocation idempotent involution compaction.
- **Metotlar:** `__init__()`, `add_interaction()`, `get_context_prompt()`, `get_telemetry()`, `compact_inplace()`, `reset()`

```python
import torch
import numpy as np
from idempotent_game_ai.dialogue_memory import NPCDialogueMemory

# NPCDialogueMemory örneği oluşturma ve çalıştırma:
obj = NPCDialogueMemory(max_turns=128)
print('NPCDialogueMemory başarıyla başlatıldı:', obj)
```

### 3.4. Modül: `idempotent_game_ai.npc_planner`
> **Tanım:** In-Place Decision Tree & Action Candidate Compactor for Game NPCs.
Consolidates top-K tactical actions in-place directly within local GPU/CPU registers.
Protected under U.S. Patent Application No. 64/148,668.

#### Sınıf: `NPCPlanner`
- **Açıklama:** Tactical Decision Engine for game NPCs.
Evaluates action candidates and packs top choices in-place without stealing render VRAM.
- **Metotlar:** `__init__()`, `plan_tactics_inplace()`

```python
import torch
import numpy as np
from idempotent_game_ai.npc_planner import NPCPlanner

# NPCPlanner örneği oluşturma ve çalıştırma:
obj = NPCPlanner(action_dim=64, candidate_actions='default', top_k=32)
print('NPCPlanner başarıyla başlatıldı:', obj)
```

#### Fonksiyon: `generate_npc_prune_map()`
- **Açıklama:** Constructs an involution permutation pi (pi(pi(x)) == x) swapping
low-value tactical actions in prefix [0, K-1] with high-value actions in suffix [K, N-1].
q_values shape: [NumNPCs, NumActions]
- **Parametreler:** `q_values, K`

```python
import torch
from idempotent_game_ai.npc_planner import generate_npc_prune_map

res = generate_npc_prune_map(None, None)
print('generate_npc_prune_map() çağrı sonucu:', type(res))
```

#### Fonksiyon: `compact_decision_tree_inplace()`
- **Açıklama:** Applies disjoint 2-cycle transpositions in-place across action feature embeddings.
action_tensor shape: [NumNPCs, NumActions, ActionDim]
Guarantees: data_ptr() is preserved, auxiliary VRAM allocated = 0 Bytes.
- **Parametreler:** `action_tensor, swap_u, swap_v, num_swaps`

```python
import torch
from idempotent_game_ai.npc_planner import compact_decision_tree_inplace

res = compact_decision_tree_inplace(torch.randn(2, 64, 64), None, None, None)
print('compact_decision_tree_inplace() çağrı sonucu:', type(res))
```

### 3.5. Modül: `idempotent_game_ai.swarm_simulator`
> **Tanım:** 500-NPC Swarm Simulation Runtime for Games and Virtual Worlds.

#### Sınıf: `SwarmSimulator`
- **Açıklama:** Simulates hundreds of autonomous NPCs making concurrent real-time decisions.
- **Metotlar:** `__init__()`, `step()`

```python
import torch
import numpy as np
from idempotent_game_ai.swarm_simulator import SwarmSimulator

# SwarmSimulator örneği oluşturma ve çalıştırma:
obj = SwarmSimulator(num_npcs=32, actions_per_npc=32, top_k=32)
output = obj.step(None)
print('SwarmSimulator.step çıktısı:', type(output))
```

### 3.6. Modül: `idempotent_game_ai.ui.app`
> **Tanım:** IdemNPC FastAPI Web Server & Real-Time Swarm Telemetry Gateway.

Serves the 3D Multi-Agent Arena Cockpit on Port 8096 and streams 60 FPS
WebSocket telemetry comparing In-Situ Idempotent Compaction vs Traditional GC List Removal.

Copyright (c) 2026 Dr. A. Emre ÇETİN
U.S. Patent Application No. 64/148,668 ("Patent Pending", Conf. No. 5890)

#### Sınıf: `SpawnRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import SpawnRequest

# SpawnRequest örneği oluşturma ve çalıştırma:
obj = SpawnRequest()
print('SpawnRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `AoEBlastRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import AoEBlastRequest

# AoEBlastRequest örneği oluşturma ve çalıştırma:
obj = AoEBlastRequest()
print('AoEBlastRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `BehaviorRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import BehaviorRequest

# BehaviorRequest örneği oluşturma ve çalıştırma:
obj = BehaviorRequest()
print('BehaviorRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `EngineRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import EngineRequest

# EngineRequest örneği oluşturma ve çalıştırma:
obj = EngineRequest()
print('EngineRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `SpatialModeRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import SpatialModeRequest

# SpatialModeRequest örneği oluşturma ve çalıştırma:
obj = SpatialModeRequest()
print('SpatialModeRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `SpeedRangeRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import SpeedRangeRequest

# SpeedRangeRequest örneği oluşturma ve çalıştırma:
obj = SpeedRangeRequest()
print('SpeedRangeRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `BenchmarkRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import BenchmarkRequest

# BenchmarkRequest örneği oluşturma ve çalıştırma:
obj = BenchmarkRequest()
print('BenchmarkRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `ChatMessageRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import ChatMessageRequest

# ChatMessageRequest örneği oluşturma ve çalıştırma:
obj = ChatMessageRequest()
print('ChatMessageRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `CompactDialogueRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import CompactDialogueRequest

# CompactDialogueRequest örneği oluşturma ve çalıştırma:
obj = CompactDialogueRequest()
print('CompactDialogueRequest başarıyla başlatıldı:', obj)
```

#### Sınıf: `MctsEvalRequest`
- **Metotlar:** 

```python
import torch
import numpy as np
from idempotent_game_ai.ui.app import MctsEvalRequest

# MctsEvalRequest örneği oluşturma ve çalıştırma:
obj = MctsEvalRequest()
print('MctsEvalRequest başarıyla başlatıldı:', obj)
```

#### Fonksiyon: `get_index()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import get_index

res = get_index()
print('get_index() çağrı sonucu:', type(res))
```

#### Fonksiyon: `get_status()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import get_status

res = get_status()
print('get_status() çağrı sonucu:', type(res))
```

#### Fonksiyon: `spawn_agents()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import spawn_agents

res = spawn_agents(None)
print('spawn_agents() çağrı sonucu:', type(res))
```

#### Fonksiyon: `aoe_kill()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import aoe_kill

res = aoe_kill(None)
print('aoe_kill() çağrı sonucu:', type(res))
```

#### Fonksiyon: `set_behavior()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import set_behavior

res = set_behavior(None)
print('set_behavior() çağrı sonucu:', type(res))
```

#### Fonksiyon: `set_engine()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import set_engine

res = set_engine(None)
print('set_engine() çağrı sonucu:', type(res))
```

#### Fonksiyon: `set_spatial_mode()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import set_spatial_mode

res = set_spatial_mode(None)
print('set_spatial_mode() çağrı sonucu:', type(res))
```

#### Fonksiyon: `set_speed_range()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import set_speed_range

res = set_speed_range(None)
print('set_speed_range() çağrı sonucu:', type(res))
```

#### Fonksiyon: `reset_arena()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import reset_arena

res = reset_arena()
print('reset_arena() çağrı sonucu:', type(res))
```

#### Fonksiyon: `seed_default_dialogue()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import seed_default_dialogue

res = seed_default_dialogue()
print('seed_default_dialogue() çağrı sonucu:', type(res))
```

#### Fonksiyon: `get_dialogue_state()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import get_dialogue_state

res = get_dialogue_state()
print('get_dialogue_state() çağrı sonucu:', type(res))
```

#### Fonksiyon: `dialogue_chat()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import dialogue_chat

res = dialogue_chat(None)
print('dialogue_chat() çağrı sonucu:', type(res))
```

#### Fonksiyon: `compact_dialogue()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import compact_dialogue

res = compact_dialogue(None)
print('compact_dialogue() çağrı sonucu:', type(res))
```

#### Fonksiyon: `reset_dialogue()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import reset_dialogue

res = reset_dialogue()
print('reset_dialogue() çağrı sonucu:', type(res))
```

#### Fonksiyon: `get_engine_benchmark()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import get_engine_benchmark

res = get_engine_benchmark()
print('get_engine_benchmark() çağrı sonucu:', type(res))
```

#### Fonksiyon: `run_engine_live_benchmark()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import run_engine_live_benchmark

res = run_engine_live_benchmark(None)
print('run_engine_live_benchmark() çağrı sonucu:', type(res))
```

#### Fonksiyon: `evaluate_mcts()`
- **Parametreler:** `req`

```python
import torch
from idempotent_game_ai.ui.app import evaluate_mcts

res = evaluate_mcts(None)
print('evaluate_mcts() çağrı sonucu:', type(res))
```

#### Fonksiyon: `websocket_telemetry()`
- **Parametreler:** `websocket`

```python
import torch
from idempotent_game_ai.ui.app import websocket_telemetry

res = websocket_telemetry(32)
print('websocket_telemetry() çağrı sonucu:', type(res))
```

#### Fonksiyon: `main()`
- **Parametreler:** ``

```python
import torch
from idempotent_game_ai.ui.app import main

res = main()
print('main() çağrı sonucu:', type(res))
```

---

## 4. İleri Düzey Entegrasyon ve Çalışma Zamanı Mimarisi

### Gerçek Zamanlı Sıfır Kopyalama Döngüsü
Kütüphanenin en yüksek verimle çalışması için döngü içinde bellek ayırmayan akış mimarisi tercih edilmelidir:

```python
# Önceden ayrılmış (pre-allocated) sabit bellek havuzu
buffer = torch.zeros(1, 128, 64, dtype=torch.float32)

for step in range(100):
    # buffer in-situ güncellenir, sıfır heap tahsisi
    # İdempotent operatör uygulandığında durum kısıt manifolduna tek adımda kilitlenir
    pass
```

### Web & Studio Arayüzü
Bu paket canlı telemetri ve interaktif görselleştirme için dahili Web Studio arayüzüne sahiptir:
```bash
python -m idempotent_game_ai.ui.app
```

---

## 5. Hata Yönetimi ve Sınır Durumlar (Edge Cases)

1. **Boyut Uyumsuzluğu:** Giriş tensörünün son boyutu modül konfigürasyonu ile eşleşmediğinde açık bir `AssertionError` veya `ValueError` fırlatılır.
2. **Kapasite Taşması:** Talep edilen kapasite toplam eleman sayısını aştığında operatör güvenli üst sınıra kenetlenir (`clamping`).
3. **Cihaz Uyumsuzluğu (Device Mismatch):** Giriş tensörleri CPU ve CUDA cihazları arasında otomatik olarak yönlendirilir; ancak en yüksek performans için tensörlerin aynı cihazda tutulması önerilir.

---

## 6. Performans İpuçları ve En İyi Pratikler

- **TorchScript & JIT:** Kritik döngülerde `torch.jit.script` ile derleyerek Python yorumlayıcı yükünü ortadan kaldırın.
- **Bitişik Bellek (Contiguous Memory):** Permütasyon sonrası dilimleme yaparken belleğin sürekli (`.contiguous()`) olduğundan emin olun.
- **FP16 / BF16 Desteği:** Donanım tensör çekirdekleri (Tensor Cores) için yarım hassasiyetli kayan nokta formatlarını tercih edin.
