# IdemNPC Unity (DOTS & Burst) Test ve Profiling Kılavuzu

> **Unity Package Manager (UPM), Burst Compiler ve Sıfır Managed GC Profiling Prosedürü**  
> *Yazar: Dr. A. Emre ÇETİN | Patent Koruması: U.S. Patent Application No. 64/148,668*

---

## 1. Test Ortamı Gereksinimleri

| Bileşen | Gereksinim | İndirme / Kaynak |
| :--- | :--- | :--- |
| **Unity Hub** | v3.0 veya üzeri | [unity.com/download](https://unity.com/download) |
| **Unity Editor** | 2022.3 LTS, 2023.x veya Unity 6 | Unity Hub üzerinden (Personal Lisansı ücretsizdir) |
| **Gerekli Paketler** | `com.unity.burst` (>=1.8.11)<br>`com.unity.collections` (>=2.2.0)<br>`com.unity.mathematics` (>=1.3.1) | `package.json` üzerinden otomatik yüklenir |

---

## 2. Adım Adım Kurulum ve Test Prosedürü

### Adım 1: Yeni Bir Unity Projesi Oluşturun
1. **Unity Hub** uygulamasını açın.
2. **Projects** $\to$ **New project** butonuna tıklayın.
3. Şablon olarak **3D (Core)** seçin, proje adına `IdemNPC_Test` verip oluşturun.

### Adım 2: IdemNPC Paketini Projeye Ekleyin (UPM)
1. Unity Editor açıldığında üst menüden **Window** $\to$ **Package Manager** penceresini açın.
2. Sol üst köşedeki **`+`** (artı) simgesine tıklayın.
3. **Add package from disk...** seçeneğini seçin.
4. Dosya seçici penceresinde şu dosyayı gösterin:
   ```
   d:/ECETIN/ECETIN/studies/software/idempotent-permutations/packages/idem-game-ai/unity/package.json
   ```
5. Unity, `com.aemrecetin.idemnpc` paketini ve bağımlı olduğu *Burst*, *Collections* ve *Mathematics* kütüphanelerini otomatik olarak indirecek ve derleyecektir.

---

### Adım 3: Test Sahnesi ve Test Betiğini Oluşturun

1. `Assets/Scripts/` adında bir klasör oluşturun.
2. Klasör içine sağ tıklayıp **Create** $\to$ **C# Script** seçin ve adını `HordeTestRunner.cs` yapın.
3. Dosyayı açıp aşağıdaki test kodunu yapıştırın:

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Mathematics;
using IdemNPC.Runtime;

public class HordeTestRunner : MonoBehaviour
{
    [Header("Benchmark Parameters")]
    public int EntityCount = 5000;
    public int TopKThreats = 50;

    private NativeArray<IdemAgentState> agents;

    void Start()
    {
        // 1. 5,000 varlığı yönetilmeyen (unmanaged) yerel bellekte tahsis et
        agents = new NativeArray<IdemAgentState>(EntityCount, Allocator.Persistent);

        for (int i = 0; i < EntityCount; i++)
        {
            agents[i] = new IdemAgentState
            {
                EntityId = i + 1,
                Position = new float3(UnityEngine.Random.insideUnitSphere * 100f),
                Health = 100.0f,
                ThreatScore = UnityEngine.Random.Range(0f, 1000f),
                IsActive = true,
                CustomState = 1
            };
        }

        Debug.Log($"[IdemNPC] {EntityCount} agents initialized in unmanaged memory. Press Play & Open Profiler.");
    }

    void Update()
    {
        // Her 30 karede bir bazı varlıkları rastgele devre dışı bırak
        if (Time.frameCount % 30 == 0)
        {
            for (int i = 0; i < agents.Length; i++)
            {
                if (UnityEngine.Random.value < 0.1f)
                {
                    IdemAgentState s = agents[i];
                    s.Health = 0.0f;
                    s.IsActive = false;
                    agents[i] = s;
                }
            }
        }

        // 2. YERİNDE İDEMPOTENT SIKIŞTIRMA (Strictly 0 Bytes GC Alloc)
        int activeCount = IdemNPC.CompactActiveInPlace(ref agents);

        // 3. EN YÜKSEK TEHDİTLİ TOP-K HEDEF SEÇİMİ (0 B Sıralama Tamponu)
        int selectedK = IdemNPC.SelectTopKThreatsInPlace(ref agents, TopKThreats);
    }

    void OnDestroy()
    {
        if (agents.IsCreated)
        {
            agents.Dispose();
        }
    }
}
```

4. Sahne hiyerarşisinde (**Hierarchy**) sağ tıklayıp **Create Empty** diyerek boş bir GameObject oluşturun (Adını `BenchmarkManager` yapın).
5. Yazdığınız `HordeTestRunner.cs` bileşenini bu objenin üzerine sürükleyip bırakın.

---

### Adım 4: Unity Profiler ile Doğrulama (GC Alloc = 0 B)

1. Üst menüden **Window** $\to$ **Analysis** $\to$ **Profiler** (veya **Ctrl + 7**) penceresini açın.
2. Profiler penceresinde sol taraftan **CPU Usage** satırını seçin.
3. Alt kısımdaki görünümü **Hierarchy** yapın ve sütunları **GC Alloc**'a göre sıralayın.
4. Unity'de **Play** (Oynat) butonuna basın.

#### Doğrulanan Sonuçlar:
* `HordeTestRunner.Update` ve `IdemNPC.CompactActiveInPlace` satırlarında **`GC Alloc: 0 B`** olduğunu göreceksiniz.
* 5,000 varlık için karar döngüsü süresi: **< 0.15 ms** (Burst derleyici optimizasyonu ile).

---

### Adım 5: Burst Compiler Inspector Doğrulaması

1. Üst menüden **Window** $\to$ **Analysis** $\to$ **Burst** $\to$ **Burst Inspector** açın.
2. Arama çubuğuna `IdemNPC` yazın.
3. `CompactActiveInPlace` ve `SelectTopKThreatsInPlace` fonksiyonlarının yeşil onay işaretiyle AVX2/NEON vektörel SIMD makine koduna doğrudan derlendiğini inceleyebilirsiniz.

