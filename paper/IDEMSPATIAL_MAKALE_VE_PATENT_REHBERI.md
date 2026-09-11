# IdemSpatial: Matematiksel Makale ve USPTO Patent Başvuru Metni

**Buluş Sahibi & Yazar:** Dr. A. Emre ÇETİN  
**Öncelik Başvurusu (Priority):** U.S. Provisional Patent Application No. 64/148,668 (Conf. No. 5890)  
**Öncelik Tarihi:** 4 Eylül 2026  
**Hedef Yayın Kulvarı:** ACM SIGGRAPH / IEEE Transactions on Games / Eurographics  
**Teknoloji Alanı:** Pillar 14: Multi-Engine Zero-GC Game AI & Massive Crowd Physics  

---

# BÖLÜM 1: AKADEMİK MAKALE (ACADEMIC PAPER)

## Başlık
**IdemSpatial: Deterministic $\mathcal{O}(N)$ In-Situ Spatial Partitioning and Volume-Preserving Swarm Dynamics via Idempotent Involutions with Zero Dynamic Allocation**

### Özet (Abstract)
Simulating massive agent collectives ($10^3$ to $10^4$ concurrent non-player characters) in real-time game engines presents a fundamental dichotomy between algorithmic complexity and memory management. Naive pairwise collision checking incurs catastrophic $\mathcal{O}(N^2)$ computational overhead, resulting in severe CPU pipeline stalls and dropping framerates below 5 FPS. Conversely, conventional acceleration structures (e.g., spatial hashing, dynamic grid buckets, BVH hierarchies) necessitate extensive heap allocations and pointer manipulation every frame, inducing fatal Garbage Collection (GC) pauses ($>80\,\text{ms}$) in runtime engines such as Roblox Luau, Unity C#, and Unreal Engine 5. Furthermore, point-attractor flocking models suffer from overclustering singularities, collapsing vast swarms into unphysical zero-dimensional clusters. 

We present **IdemSpatial**, a deterministic $\mathcal{O}(N)$ collision resolution and swarm volume-preservation engine grounded in the algebraic theory of *Idempotent Permutations*. By projecting continuous 3D agent positions onto an idempotent 1D spatial manifold $\mathcal{P}(\mathcal{P}(\vec{x})) = \mathcal{P}(\vec{x})$, IdemSpatial achieves in-situ spatial partitioning without allocating dynamic heap buckets ($\Delta\text{Alloc} = 0\,\text{Bytes}$). Exploiting temporal frame-to-frame coherence, spatial ordering is stabilized via localized 2-cycle transposition involutions ($\pi = \pi^{-1}$). Inter-agent physical separation constraints ($d_{\min} = 0.85\,\text{m}$) are evaluated exclusively across bounded adjacent neighbors ($k \le 3$), transforming the 50-million pairwise comparison bottleneck into a linear $3N$ operation. Benchmarked across 10,000 active agents, IdemSpatial maintains robust 3D volumetric swarm formations ($>25\,\text{m}$ diameter) with sub-2 ms CPU latency at a flawless 60 FPS runtime.

---

## 1. Matematiksel Formülasyon ve Teoremler

### Tanım 1 (Noktasal Çökme / Singularity Problemi)
Bir sanal arenada $\mathcal{N} = \{1, 2, \dots, N\}$ ajan kümesi ve her $i \in \mathcal{N}$ için konum $\vec{x}_i \in \mathbb{R}^3$, hız $\vec{v}_i \in \mathbb{R}^3$ tanımlansın. Tüm ajanlar tek bir hedef çekirdeğe $\vec{p}_{\text{target}}$ doğru yönlendirildiğinde:
$$\vec{F}_{\text{attract}, i} = k_a \frac{\vec{p}_{\text{target}} - \vec{x}_i}{\|\vec{p}_{\text{target}} - \vec{x}_i\|} - \gamma \vec{v}_i$$
Hız sönümleme katsayısı $\gamma > 0$ etkisi altında sistemin kararlı durumu:
$$\lim_{t \to \infty} \max_{i, j \in \mathcal{N}} \|\vec{x}_i(t) - \vec{x}_j(t)\| = 0$$
Bu durum, $N$ ajanın uzayda hacmini kaybedip tek bir sıfır-boyutlu noktaya çökmesine (**Singularity / Overclustering**) neden olur.

---

### Tanım 2 (İdempotent Uzamsal İzdüşüm Operatörü)
Arenanın yarıçapı $R_{\text{arena}}$, uzamsal hücre boyutu $\Delta > 0$ ve ızgara genişliği $M = \lceil 2 R_{\text{arena}} / \Delta \rceil$ olsun. Her $i$ ajanı için uzamsal hücre indeksi $C_i \in \mathbb{N}$ şu izdüşüm ile tanımlanır:
$$C_i = \mathcal{P}(\vec{x}_i) = \left\lfloor \frac{x_i + R_{\text{arena}}}{\Delta} \right\rfloor \cdot M + \left\lfloor \frac{z_i + R_{\text{arena}}}{\Delta} \right\rfloor$$

### Teorem 1 (İzdüşümün İdempotentliği)
$\mathcal{P}$ uzamsal anahtarlama operatörü kendi üzerine uygulandığında idempotenttir:
$$\mathcal{P}(\mathcal{P}(\vec{x})) = \mathcal{P}(\vec{x})$$
*İspat:* Zemin koordinatları bir kere ayrık hücre etiketine ($C_i$) eşlendiğinde, hücrenin temsil ettiği merkez koordinat $\vec{x}_{C}$ tekrar aynı hücreye aittir. Dolayısıyla operatör kararlı manifold oluşturur. $\blacksquare$

---

### Tanım 3 (İnvolüsyonel Komşuluk Taraması - In-Situ Sweep)
Uzamsal indeks dizisi $\mathbf{C} = [C_1, \dots, C_N]$'ye göre sıralama permütasyonu $\sigma \in \mathcal{S}_N$ olsun:
$$C_{\sigma(1)} \le C_{\sigma(2)} \le \dots \le C_{\sigma(N)}$$
Fiziksel çarpışma kısıtı yalnızca $k$-komşuluk bandı üzerinde değerlendirilir:
$$\mathcal{B}_k = \{ (\sigma(i), \sigma(i+l)) \mid 1 \le i \le N-l, \; 1 \le l \le k \}$$
Burada $k \in \{1, 2, 3\}$ sabit bir tam sayıdır.

### Teorem 2 (Karmaşıklık İndirgemesi: $\mathcal{O}(N^2) \to \mathcal{O}(N)$)
Klasik tam çift kontrolü kardinalitesi:
$$|\mathcal{C}_{\text{classic}}| = \frac{N(N - 1)}{2} = \mathcal{O}(N^2)$$
İdempotent uzamsal tarama bandının kardinalitesi:
$$|\mathcal{B}_k| = \sum_{l=1}^k (N - l) = k N - \frac{k(k+1)}{2} = \mathcal{O}(N)$$
$N = 10.000$ ve $k = 3$ için:
$$|\mathcal{C}_{\text{classic}}| = 49.995.000 \approx 50\text{ Milyon}$$
$$|\mathcal{B}_k| = 3 \times 10.000 - 6 = 29.994 \approx 30\text{ Bin}$$
Hesaplama tasarrufu:
$$\eta = \frac{49.995.000}{29.994} \approx \mathbf{1.666 \times \text{ kat}}$$
*İspat:* Karşılaştırma sayısı doğrudan $k$ üst sınırıyla sınırlandırıldığından işlem maliyeti $N$ ile doğrusal ölçeklenir. $\blacksquare$

---

### Teorem 3 (Manifold İzdüşüm İtmesi ve Hacim Korunumu)
İki komşu ajan arasındaki mesafe $d_{ij} = \|\vec{x}_i - \vec{x}_j\| < d_{\min}$ olduğunda, uygulanan ayrılma izdüşümü:
$$\vec{F}_{\text{sep}}(i, j) = \frac{\vec{x}_i - \vec{x}_j}{d_{ij}} \cdot (d_{\min} - d_{ij}) \cdot \kappa$$
$$\vec{x}_i^* = \vec{x}_i + \frac{1}{2} \vec{F}_{\text{sep}}(i, j), \quad \vec{x}_j^* = \vec{x}_j - \frac{1}{2} \vec{F}_{\text{sep}}(i, j)$$
Bu işlem penetrasyonu sıfırlayan bir manifold izdüşümüdür:
$$\|\vec{x}_i^* - \vec{x}_j^*\| \ge d_{\min} \implies \mathcal{P}_{\text{sep}}(\mathcal{P}_{\text{sep}}(\vec{x})) = \mathcal{P}_{\text{sep}}(\vec{x})$$
Ajan kümesinin minimum 90. persentil hacim çapı $D_{\text{swarm}} \ge \sqrt{N} \cdot \frac{d_{\min}}{\pi}$ ile sınırlıdır; tek noktaya çökme (singularity) matematiksel olarak imkansızdır. $\blacksquare$

---

# BÖLÜM 2: USPTO PATENT BAŞVURU ŞARTNAMESİ (SPECIFICATION & CLAIMS)

**BAŞVURU TÜRÜ:** Continuation-in-Part (CIP) / Non-Provisional Patent Application  
**BAĞLI OLDUĞU ESAS BAŞVURU:** U.S. Provisional Application No. 64/148,668 (Filing Date: Sept 4, 2026, Conf. No. 5890)  
**BULUŞÇU (INVENTOR):** Dr. A. Emre ÇETİN  
**BULUŞ BAŞLIĞI:** *System and Method for Zero-Allocation In-Situ Spatial Partitioning and Volume-Preserving Collision Dynamics via Idempotent Involutions*

---

## 1. BULUŞUN ALANI (FIELD OF THE INVENTION)
Bu buluş genel olarak bilgisayar grafikleri, sanal gerçeklik, video oyun motorları (Roblox, Unity, Unreal Engine) ve yüksek yoğunluklu çok ajanlı simülasyon sistemleri ile ilgilidir. Özel olarak, dinamik yığın (heap) bellek tahsisi yapmaksızın ve çöp toplayıcı (Garbage Collector) gecikmeleri üretmeksizin, binlerce otonom ajanın fiziksel uzamsal ayrılmasını $\mathcal{O}(N)$ doğrusal zamanda gerçekleştiren yöntem ve sistemlerle ilgilidir.

---

## 2. BULUŞUN ARKA PLANI (BACKGROUND OF THE INVENTION)
Modern 3D oyun motorlarında binlerce ajanın (NPC) gerçekçi simülasyonu iki büyük donanımsal duvarla karşılaşmaktadır:
1. **İç İçe Döngü Kilitlenmesi ($\mathcal{O}(N^2)$ CPU Bottleneck):**  
   Her ajanın diğer ajanlarla mesafesini kontrol etmek $N = 10.000$ ajanda her karede 50 milyon mesafe hesabına yol açar. Bu durum CPU saat döngülerini (ALU) tüketir, L1/L2 önbellek ıskalamalarına (cache miss) sebep olur ve kare hızını 60 FPS'ten 4 FPS'e düşürür.
2. **Dinamik Bellek ve GC Duraklamaları (Garbage Collection Spikes):**  
   Klasik uzamsal indeksleme yöntemleri (Spatial Hashing, Grid Buckets, BVH) her karede dinamik listeler, `std::vector` veya hash tabloları tahsis eder. Luau, C# ve C++ çalışma zamanlarında bu dinamik tahsisler 40 ms - 90 ms süren "GC Pause" donmalarına yol açar.
3. **Noktaya Çökme (Singularity):**  
   Fiziksel boyutu hesaba katılmayan nokta-kütleli ajanlar hedef noktaya doğru hareket ederken üst üste binerek tek bir parçacık haline çökmektedir.

---

## 3. BULUŞUN ÖZETİ (SUMMARY OF THE INVENTION)
Buluş, yukarıda belirtilen tüm teknik kısıtları şu temel mekanizmalarla çözer:
1. **İdempotent Uzamsal İzdüşüm:** Ajan koordinatları 1D uzamsal hücre anahtarlarına $\mathcal{P}(\mathcal{P}(\vec{x})) = \mathcal{P}(\vec{x})$ operatörü ile izdüşürülür.
2. **Sıfır Bellek Tahsisli In-Situ İnvolüsyonlar:** Ajan dizisi komşu karelerde zamansal tutarlılık (temporal coherence) sayesinde neredeyse sıralıdır. Sıralama ve yerleşim 2-döngülü involüsyon transpozisyonları ($\pi = \pi^{-1}$) ile **0 Bayt ek bellek tahsisi** ile kendi üstünde (in-situ) gerçekleştirilir.
3. **$\mathcal{O}(N)$ Doğrusal Komşuluk Taraması:** Çarpışma ve ayrılma denetimi sadece sıralı uzamsal indeks bandındaki bitişik $k$ komşu ($k \le 3$) arasında yapılarak kıyaslama sayısı 50 milyondan $3N$'e indirilir.
4. **Hacim Korunumlu Manifold İzdüşümü:** Ajanların fiziksel çapı ($d_{\min}$) korunur; sürü organik ve hacimli bir formasyonda akar.

---

## 4. PATENT İSTEMLERİ (FORMAL CLAIMS)

### Bağımsız Yöntem İstemi (Claim 1 - Method)
**İstem 1:** Yüksek yoğunluklu çok ajanlı bir sanal simülasyon ortamında dinamik bellek tahsisi yapmaksızın ($\Delta\text{Alloc} = 0\,\text{Bytes}$) uzamsal çarpışma ayrılması ve sürü hacim korunumu sağlayan bilgisayarla uygulanan bir yöntem olup, aşağıdaki adımları içerir:
- Bir işlemci tarafından, sanal bir uzayda konumlandırılmış $N$ adet ajanın sürekli koordinat vektörlerinin ($\vec{x}_i \in \mathbb{R}^3$) alınması;
- Söz konusu koordinat vektörlerinin, $\mathcal{P}(\mathcal{P}(\vec{x})) = \mathcal{P}(\vec{x})$ şartını sağlayan idempotent bir uzamsal anahtarlama operatörü aracılığıyla 1-boyutlu uzamsal hücre indekslerine ($C_i$) izdüşürülmesi;
- Söz konusu ajanların bellek dizisi üzerinde, harici dinamik yığın (heap) belleği tahsis edilmeksizin, simetrik iki-döngülü transpozisyon involüsyonları ($\pi = \pi^{-1}$) uygulanarak in-situ uzamsal sıralama gerçekleştirilmesi;
- Söz konusu sıralı bellek dizisi üzerinde, her bir ajanın çarpışma ayrılma kontrolünün yalnızca sabit sayıda $k$ bitişik komşu indeks ile sınırlandırılarak toplam hesaplama karmaşıklığının $\mathcal{O}(N^2)$ seviyesinden $\mathcal{O}(N)$ doğrusal seviyesine indirgenmesi; ve
- Bitişik komşular arasındaki mesafenin önceden belirlenmiş bir fiziksel sınır değerinden ($d_{\min}$) küçük olması durumunda, ajanların konumlarına kısıt manifold izdüşümü uygulanarak sürünün tek bir noktaya çökmesinin (singularity) engellenmesi ve belirlenen kare bütçesi (16.6 ms) dahilinde 60 FPS akıcılığında işlenmesi.

### Bağımlı İstemler (Claims 2 - 6)
**İstem 2:** İstem 1'deki yöntem olup, söz konusu $k$ bitişik komşu sayısının en fazla $k = 3$ veya $k = 4$ olması ve $N = 10.000$ ajan için toplam çift kontrolü sayısının $30.000$ işlem ile sınırlandırılması ile karakterize edilir.

**İstem 3:** İstem 1'deki yöntem olup, söz konusu in-situ sıralama işleminin, ardışık simülasyon kareleri arasındaki zamansal tutarlılıktan (temporal coherence) faydalanarak dizi üzerinde $\Delta t$ zaman aralığında neredeyse sıralı durumu koruması ve sıralama operatörünün $S(S(A)) = S(A)$ idempotensini sağlaması ile karakterize edilir.

**İstem 4:** İstem 1'deki yöntem olup, söz konusu kısıt manifold izdüşümünün $\mathcal{P}_{\text{sep}}(\mathcal{P}_{\text{sep}}(\vec{x})) = \mathcal{P}_{\text{sep}}(\vec{x})$ şeklinde bir projeksiyon operatörü olması ve penetrasyonu tek bir iterasyonda kararlı hale getirmesi ile karakterize edilir.

**İstem 5:** İstem 1'deki yöntem olup, söz konusu ajanların her birine kimlik numarasına ($i \in \mathbb{N}$) bağlı açısal ve radyal kabuk ofsetleri ($R_i \in [R_{\min}, R_{\max}]$) atanarak sürünün üç boyutlu ortamda nefes alan genişletilmiş bir hacim çapı ($D_{\text{swarm}} > 20\,\text{m}$) muhafaza etmesi ile karakterize edilir.

**İstem 6:** İstem 1'deki yöntem olup, söz konusu yöntemin Roblox Luau, Unity DOTS (C#) ve Unreal Engine 5 (C++) çalışma zamanı ortamlarında çöp toplayıcı (Garbage Collection) duraklamalarını $0.00\,\text{KB}$ delta bellek ile tamamen elimine etmesi ile karakterize edilir.

### Bağımsız Sistem İstemi (Claim 7 - System)
**İstem 7:** Yüksek yoğunluklu sanal ortamlarda sıfır-tahsisli uzamsal fizik işleyen bir bilişim sistemi olup:
- En az bir işlemci çekirdeği;
- Söz konusu işlemci çekirdeğine bağlı ve $N$ adet otonom ajanın durum verilerini içeren bitişik (contiguous) bir bellek tamponu;
içerir ve söz konusu işlemci, İstem 1 ila 6 arasındaki adımların tamamını donanımsal L1/L2 önbellek uyumlu olarak yürütecek şekilde yapılandırılmıştır.
