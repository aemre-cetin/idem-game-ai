# IdemNPC Unreal Engine 5 Test ve Entegrasyon Kılavuzu

> **Unreal Engine 5 C++ Plugin, Blueprint Function Library ve Bellek Doğrulama Prosedürü**  
> *Yazar: Dr. A. Emre ÇETİN | Patent Koruması: U.S. Patent Application No. 64/148,668*

---

## 1. Test Ortamı Gereksinimleri

| Bileşen | Gereksinim | İndirme / Kaynak |
| :--- | :--- | :--- |
| **Epic Games Launcher** | En güncel sürüm | [unrealengine.com](https://www.unrealengine.com/) |
| **Unreal Engine 5** | UE 5.3, 5.4 veya 5.5 | Epic Games Launcher $\to$ Unreal Engine $\to$ Library |
| **Visual Studio 2022** | Community veya Professional | [visualstudio.microsoft.com](https://visualstudio.microsoft.com/)<br>*("Game development with C++" iş yükü seçili olmalıdır)* |

---

## 2. Adım Adım Kurulum ve Projeye Ekleme

### Adım 1: Boş Bir UE5 C++ Projesi Açın
1. Epic Games Launcher'dan Unreal Engine 5'i başlatın.
2. **Games** $\to$ **Blank** şablonunu seçin.
3. Proje tipini **C++** (veya Blueprint) olarak seçin, adını `IdemNPC_Benchmark` yapıp **Create** butonuna tıklayın.

### Adım 2: Eklentiyi Projenin `Plugins/` Dizinine Kopyalayın
1. Projenizin ana dizinine gidin (Örn: `D:\UnrealProjects\IdemNPC_Benchmark\`).
2. Eğer yoksa ana dizinde `Plugins` adında yeni bir klasör oluşturun.
3. Repodaki `packages/idem-game-ai/ue5/` klasörünü bu klasörün içine `IdemNPC` adıyla kopyalayın:
   ```
   IdemNPC_Benchmark/
   └── Plugins/
       └── IdemNPC/
           ├── IdemNPC.uplugin
           ├── Source/
           │   └── IdemNPC/
           │       ├── IdemNPC.Build.cs
           │       ├── Public/
           │       └── Private/
           └── README.md
   ```

### Adım 3: Visual Studio Proje Dosyalarını Yeniden Üretin ve Derleyin
1. Projenin `.uproject` dosyasına sağ tıklayın $\to$ **Generate Visual Studio project files** seçeneğini tıklayın.
2. Oluşan `.sln` dosyasını Visual Studio 2022 ile açın.
3. Solution Explorer'da `IdemNPC_Benchmark` projesine sağ tıklayıp **Build** (veya `Ctrl + Shift + B`) deyin.
4. Derleme tamamlandıktan sonra projeyi başlatın (**F5** veya UE5 Editor'den açın).

---

## 3. Canlı Test: Blueprint ile 10,000 NPC Kıyaslaması

### Adım 1: Test Aktörü (Actor) Oluşturun
1. Unreal Editor'de **Content Drawer** $\to$ sağ tıklayın $\to$ **Blueprint Class** $\to$ **Actor** seçin.
2. Adını `BP_HordeTester` yapın ve çift tıklayarak açın.

### Adım 2: Event Graph'ta Düğümleri Bağlayın
1. **Variables** panelinden `Entities` adında bir değişken oluşturun:
   * **Variable Type:** `Idem Entity State` (Eklenti tarafından sağlanan USTRUCT).
   * Sağındaki düğmeye tıklayarak değişken tipini **Array** (Dizi) yapın.
2. **Event BeginPlay** düğümünden bir döngü (**For Loop**) başlatın:
   * First Index: `1`, Last Index: `10000`.
   * Her döngü adımında `Add` düğümüyle `Entities` dizisine bir eleman ekleyin (Health: 100, IsActive: True, ThreatScore: Random Float).
3. **Event Tick** düğümüne gelin:
   * Graph'ta sağ tıklayın ve **`Compact Active NPCs In Place`** düğümünü arayın.
   * `Entities` dizisini bu düğüme bağlayın.
   * Çıkan `Return Value` (ActiveCount) değerini ekrana yazdırmak için **`Print String`** düğümüne bağlayın.
   * İkinci bir düğüm olarak **`Select Top K Threats In Place`** (K = 50) düğümünü bağlayın.

### Adım 3: Sahneye Yerleştirin ve Çalıştırın
1. `BP_HordeTester` aktörünü sahneye sürükleyip bırakın.
2. Klavyeden **`~`** (Tilde / Konsol) tuşuna basıp `stat fps` ve `stat Unit` komutlarını yazın.
3. **Play** butonuna basın.

---

## 4. Beklenen Sonuçlar ve Metrikler

1. **Bellek Yeniden Tahsisi:** `TArray::RemoveAt()` çağrılmadığı için dizinin ham bellek adresi (`GetData()`) asla değişmez ve yer değiştirme hafıza kopyalamaları sıfırdır.
2. **Kare Hızı:** 10,000 varlıkta karar ve sıkıştırma süresi **< 0.42 ms** seviyesindedir. 60 FPS veya 120 FPS sabit hız korunur.
3. **Log Çıktısı:** Output Log penceresinde şu mesaj doğrulanır:
   ```
   LogTemp: IdemNPC: In-Situ Zero-VRAM Game AI Module Loaded. (U.S. Patent App. 64/148,668)
   ```

