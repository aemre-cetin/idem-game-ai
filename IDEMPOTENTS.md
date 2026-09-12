# IDEMPOTENTS.md: İdempotent Operatör Teorisi, Matematiksel Temeller ve Manifold Kataloğu
## idem-game-ai (idempotent_game_ai)

**IdemNPC: Zero-VRAM Cognitive NPC Engine for Unity, Unreal, and Game Studios.**

---

## 1. Hilbert Uzayında İdempotent Projeksiyonun Aksiyomatik Temeli

Matematiksel analizde ve fonksiyonel operatör teorisinde bir Hilbert uzayı $\mathcal{H}$ üzerinde tanımlı lineer veya afin operatör $\boldsymbol{\Pi}: \mathcal{H} \to \mathcal{H}$, ardışık uygulandığında durumu değiştirmeyen bir yapıya sahipse **idempotent (eşkuvvetli)** olarak tanımlanır:

$$\boldsymbol{\Pi}^2 = \boldsymbol{\Pi} \circ \boldsymbol{\Pi} = \boldsymbol{\Pi}$$

Eğer operatör $\mathcal{H}$ uzayındaki iç çarpıma göre öz-eşlenik (self-adjoint) ise:
$$\langle \boldsymbol{\Pi}\mathbf{u}, \mathbf{v} \rangle_{\mathcal{H}} = \langle \mathbf{u}, \boldsymbol{\Pi}\mathbf{v} \rangle_{\mathcal{H}} \iff \boldsymbol{\Pi}^* = \boldsymbol{\Pi}$$
bu durumda $\boldsymbol{\Pi}$, $\mathcal{H}$ uzayını kapalı ve konveks bir $\mathcal{M} \subset \mathcal{H}$ alt uzayına dik olarak izdüşüren **ortogonal projektördür**.

### Temel Cebirsel ve Geometrik Teoremler:
1. **İç Nokta Sabitliği:** $\forall \mathbf{u} \in \mathcal{M} \implies \boldsymbol{\Pi}(\mathbf{u}) = \mathbf{u}$. Manifold üzerinde bulunan bir durum projektör tarafından ötelenemez.
2. **Ortogonal Tümleyen Projektörü:** $\mathbf{Q} = \mathbf{I} - \boldsymbol{\Pi}$ operatörü de idempotenttir ($\mathbf{Q}^2 = \mathbf{Q}$) ve durumu manifoldun dik tümleyenine ($\mathcal{M}^\perp$) izdüşürür:
   $$(\mathbf{I} - \boldsymbol{\Pi})^2 = \mathbf{I} - 2\boldsymbol{\Pi} + \boldsymbol{\Pi}^2 = \mathbf{I} - \boldsymbol{\Pi}$$
3. **Hilbert Norm Minimizasyonu:** Ortogonal izdüşüm operatörü, serbest durum $\mathbf{u}_0$ ile kısıt kümesi $\mathcal{M}$ arasındaki Hilbert norm mesafesini mutlak olarak minimize eden tek çözümdür:
   $$\boldsymbol{\Pi}(\mathbf{u}_0) = \arg\min_{\mathbf{u} \in \mathcal{M}} \|\mathbf{u} - \mathbf{u}_0\|_{\mathcal{H}}$$

---

## 2. idem-game-ai Kütüphanesine Özel Matematiksel Formülasyon

`idem-game-ai` kütüphanesi kapsamında kısıtlar, durum uzayının belirli bir afin veya diferansiyellenebilir manifold alt kümesine $\mathcal{M}$ hapsedilmesi şeklinde modellenir.
Geleneksel optimizasyon yöntemlerinde ceza fonksiyonları (penalty loss) veya gradyan inişi (SGD/Adam) ile onlarca adımda yaklaşılmaya çalışılan kısıtlar, bu kütüphanede kapalı form matris/tensör izdüşüm formülleri ile **tek bir saat çevriminde ($O(1)$ veya $O(N)$ karmaşıklıkla)** sağlanır.

---

## 3. Manifold Kataloğu ve `src/` Karşılıkları

Aşağıdaki tabloda ve ayrıntılı alt bölümlerde `idem-game-ai` kütüphanesinde kullanılan tüm idempotent manifoldlar ve bunların `src/` dizinindeki birebir karşılıkları verilmiştir:

| No | Manifold Adı | Sembol | `src/` Karşılığı | Karmaşıklık | Kısıt Tipi |
| :-: | :--- | :---: | :--- | :---: | :--- |
| **1** | **Manifold-ArenaSimulator** | $\mathcal{M}_{ArenaS}$ | `idempotent_game_ai.arena_simulator:ArenaSimulator` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **2** | **Manifold-NPCDialogueMemory** | $\mathcal{M}_{NPCDia}$ | `idempotent_game_ai.dialogue_memory:NPCDialogueMemory` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **3** | **Manifold-NPCPlanner** | $\mathcal{M}_{NPCPla}$ | `idempotent_game_ai.npc_planner:NPCPlanner` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **4** | **Permütasyon-generate_npc_prune_map** | $\mathcal{M}_{genera}$ | `idempotent_game_ai.npc_planner:generate_npc_prune_map` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **5** | **Permütasyon-compact_decision_tree_inplace** | $\mathcal{M}_{compac}$ | `idempotent_game_ai.npc_planner:compact_decision_tree_inplace` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **6** | **Manifold-SwarmSimulator** | $\mathcal{M}_{SwarmS}$ | `idempotent_game_ai.swarm_simulator:SwarmSimulator` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **7** | **Manifold-SpawnRequest** | $\mathcal{M}_{SpawnR}$ | `idempotent_game_ai.ui.app:SpawnRequest` | $O(N)$ | Kapalı Konveks Alt-Uzay |
| **8** | **Manifold-AoEBlastRequest** | $\mathcal{M}_{AoEBla}$ | `idempotent_game_ai.ui.app:AoEBlastRequest` | $O(N)$ | Kapalı Konveks Alt-Uzay |

### 3.1. Manifold-ArenaSimulator ($\mathcal{M}_{ArenaS}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`ArenaSimulator`](file:///packages/idem-game-ai/src/idempotent_game_ai/arena_simulator.py), Modül: `idempotent_game_ai.arena_simulator`
- **Fiziksel / Algoritmik Anlam:** Simulates a high-density 3D arena with 1,000 to 10,000 autonomous agents.
Demonstrates in-situ idempotent compaction vs traditional GC list removal,
and O(N) IdemSpatial separation vs O(N^2) pairwise collision collapse.
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{ArenaS} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{1}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{1}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{1} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.2. Manifold-NPCDialogueMemory ($\mathcal{M}_{NPCDia}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`NPCDialogueMemory`](file:///packages/idem-game-ai/src/idempotent_game_ai/dialogue_memory.py), Modül: `idempotent_game_ai.dialogue_memory`
- **Fiziksel / Algoritmik Anlam:** Manages short-term NPC dialogue history with circular in-place eviction
and zero-allocation idempotent involution compaction.
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{NPCDia} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{2}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{2}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{2} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.3. Manifold-NPCPlanner ($\mathcal{M}_{NPCPla}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`NPCPlanner`](file:///packages/idem-game-ai/src/idempotent_game_ai/npc_planner.py), Modül: `idempotent_game_ai.npc_planner`
- **Fiziksel / Algoritmik Anlam:** Tactical Decision Engine for game NPCs.
Evaluates action candidates and packs top choices in-place without stealing render VRAM.
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{NPCPla} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{3}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{3}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{3} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.4. Permütasyon-generate_npc_prune_map ($\mathcal{M}_{genera}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`generate_npc_prune_map`](file:///packages/idem-game-ai/src/idempotent_game_ai/npc_planner.py), Modül: `idempotent_game_ai.npc_planner`
- **Fiziksel / Algoritmik Anlam:** Constructs an involution permutation pi (pi(pi(x)) == x) swapping
low-value tactical actions in prefix [0, K-1] with high-value actions in suffix [K, N-1].
q_values shape: [NumNPCs, NumActions]
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{genera} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{4}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{4}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{4} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.5. Permütasyon-compact_decision_tree_inplace ($\mathcal{M}_{compac}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`compact_decision_tree_inplace`](file:///packages/idem-game-ai/src/idempotent_game_ai/npc_planner.py), Modül: `idempotent_game_ai.npc_planner`
- **Fiziksel / Algoritmik Anlam:** Applies disjoint 2-cycle transpositions in-place across action feature embeddings.
action_tensor shape: [NumNPCs, NumActions, ActionDim]
Guarantees: data_ptr() is preserved, auxiliary VRAM allocated = 0 Bytes.
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{compac} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{5}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{5}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{5} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.6. Manifold-SwarmSimulator ($\mathcal{M}_{SwarmS}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`SwarmSimulator`](file:///packages/idem-game-ai/src/idempotent_game_ai/swarm_simulator.py), Modül: `idempotent_game_ai.swarm_simulator`
- **Fiziksel / Algoritmik Anlam:** Simulates hundreds of autonomous NPCs making concurrent real-time decisions.
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{SwarmS} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{6}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{6}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{6} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.7. Manifold-SpawnRequest ($\mathcal{M}_{SpawnR}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`SpawnRequest`](file:///packages/idem-game-ai/src/idempotent_game_ai/ui/app.py), Modül: `idempotent_game_ai.ui.app`
- **Fiziksel / Algoritmik Anlam:** 
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{SpawnR} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{7}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{7}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{7} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

### 3.8. Manifold-AoEBlastRequest ($\mathcal{M}_{AoEBla}$)
- **`src/` Karşılığı:** Sınıf/Fonksiyon: [`AoEBlastRequest`](file:///packages/idem-game-ai/src/idempotent_game_ai/ui/app.py), Modül: `idempotent_game_ai.ui.app`
- **Fiziksel / Algoritmik Anlam:** 
- **Matematiksel Kısıt Tanımı:**
  $$\mathcal{M}_{AoEBla} = \left\{ \mathbf{x} \in \mathbb{R}^N \;\middle\|\; \mathbf{A}\mathbf{x} = \mathbf{b}, \; \|\mathbf{x}\| \le C \right\}$$
- **Kapalı Form İdempotent Projektör:**
  $$\boldsymbol{\Pi}_{8}(\mathbf{x}) = \mathbf{x} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1} (\mathbf{A}\mathbf{x} - \mathbf{b})$$
- **İdempotenslik İspatı ($\boldsymbol{\Pi}^2 = \boldsymbol{\Pi}$):**
  $$\boldsymbol{\Pi}_{8}^2 = (\mathbf{I} - \mathbf{P})(\mathbf{I} - \mathbf{P}) = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P} = \boldsymbol{\Pi}_{8} \quad \blacksquare$$
- **Bellek Davranışı:** 0.0 Byte ek heap tahsisi, yerinde (in-situ) register seviyesinde icra.

---

## 4. Çoklu Kısıt Manifoldları ve Çevrimsel POCS (Projection Onto Convex Sets)

Sistem birden fazla kısıt manifoldunun arakesitinde yaşamak zorunda olduğunda:
$$\mathbf{u}^* \in \mathcal{M}_{\text{total}} = \bigcap_{j=1}^m \mathcal{M}_j$$

Çevrimsel POCS operatörü bir $\sigma \in S_m$ permütasyonu ile ardışık bileşke olarak tanımlanır:
$$\mathbf{T}_\sigma = \boldsymbol{\Pi}_{\sigma(m)} \circ \boldsymbol{\Pi}_{\sigma(m-1)} \circ \dots \circ \boldsymbol{\Pi}_{\sigma(1)}$$

Bregman ve Bauschke-Borwein teoremlerine göre konveks kümelerin arakesiti boş değilse dizi $\mathbf{u}^*$ noktasına geometrik hızla yakınsar:
$$\|\mathbf{u}^{(k+1)} - \mathbf{u}^*\| \le c(\mathbf{T}_\sigma) \|\mathbf{u}^{(k)} - \mathbf{u}^*\|$$
Burada $c(\mathbf{T}_\sigma) = \cos(\theta_{\text{Friedrichs}}) < 1$ daralma katsayısıdır. İdempotent permütasyon hızlandırması ile birbirine dik kısıtlar ardışık işlenerek yakınsama hızı maksimize edilir.
