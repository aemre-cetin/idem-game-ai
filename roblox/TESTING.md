# IdemNPC Roblox (Luau) Test ve Doğrulama Kılavuzu

> **Sıfır-GC (0.00 KB GC Churn) ve 5,000+ Varlık Sürü Simülasyonu Test Prosedürü**  
> *Yazar: Dr. A. Emre ÇETİN | Patent Koruması: U.S. Patent Application No. 64/148,668*

---

## 1. Test Ortamı Gereksinimleri

Roblox modüllerini test etmek için **iki farklı yöntem** kullanabilirsiniz:

| Test Yöntemi | Gereken Yazılım | Süre | Açıklama |
| :--- | :--- | :---: | :--- |
| **A. Roblox Studio (Önerilen)** | [Roblox Studio](https://create.roblox.com/) (Ücretsiz) | ~2 Dk | Görsel ortamda, canlı sunucu tick ve GC çıktısını görmek için. |
| **B. Terminal / Python CLI** | Python 3.10+ (Kurulumsuz) | ~5 Sn | Roblox Studio açmadan terminalden doğrudan matematiksel ve algoritmik doğrulama. |

---

## 2. Yöntem A: Roblox Studio ile Canlı Test (Adım Adım)

### Adım 1: Boş Bir Proje Açın
1. Bilgisayarınızda **Roblox Studio**'yu başlatın ve giriş yapın.
2. **New** sekmesinden **Baseplate** şablonunu seçerek boş bir dünya açın.

### Adım 2: Modül Dosyalarını `ReplicatedStorage` İçine Ekleyin
Sağ taraftaki **Explorer** panelinde:
1. `ReplicatedStorage` nesnesine sağ tıklayın $\to$ **Insert Object** $\to$ **Folder** seçin.
2. Bu klasörün adını `IdemNPC` yapın.
3. `IdemNPC` klasörünün içine sağ tıklayarak **4 adet `ModuleScript`** ekleyin ve aşağıdaki gibi adlandırıp ilgili dosya içeriğini yapıştırın:
   * **`init`** $\to$ [`roblox/init.luau`](./init.luau) içeriğini yapıştırın.
   * **`IdemNPC`** $\to$ [`roblox/IdemNPC.luau`](./IdemNPC.luau) içeriğini yapıştırın.
   * **`IdemSwarm`** $\to$ [`roblox/IdemSwarm.luau`](./IdemSwarm.luau) içeriğini yapıştırın.
   * **`IdemSpatialGrid`** $\to$ [`roblox/IdemSpatialGrid.luau`](./IdemSpatialGrid.luau) içeriğini yapıştırın.

> [!TIP]
> Eğer **Rojo** kullanıyorsanız, terminalde `roblox/` dizininde `rojo serve` komutunu çalıştırıp Studio'da Rojo eklentisiyle tek tıkla `Connect` diyebilirsiniz.

### Adım 3: Benchmark Betiğini `ServerScriptService` İçine Ekleyin
1. **Explorer** panelinde `ServerScriptService` nesnesine sağ tıklayın $\to$ **Insert Object** $\to$ **Script** (normal sunucu scripti) seçin.
2. Adını `BenchmarkRunner` yapın.
3. İçine [`roblox/tests/benchmark.server.luau`](./tests/benchmark.server.luau) dosyasındaki kodu yapıştırın.

### Adım 4: Testi Çalıştırın ve Sonuçları İnceleyin
1. Üst menüden **View** $\to$ **Output** penceresini açın.
2. **F5** tuşuna basarak oyunu başlatın (**Play**).
3. `Output` konsolunda aşağıdaki çıktıyı göreceksiniz:

```text
=================================================================
IdemNPC Roblox (Luau) Zero-GC Swarm Benchmark
U.S. Patent App. No. 64/148,668 - Dr. A. Emre ÇETİN
=================================================================
Total Entities:        5000
Ticks Executed:        100
Average Tick Duration: 0.439 ms (Target: < 2.0 ms)
GC Memory Delta:       0.00 KB
VERIFICATION: PASS! Strictly 0.00 KB GC memory growth confirmed!
=================================================================
```

---

## 3. Yöntem B: Terminalden Hızlı Doğrulama (Sıfır Kurulum)

Roblox Studio açmadan, aynı 5,000 varlıklı Luau algoritmasını Python üzerinden test etmek için:

```powershell
# 5,000 varlık ile 100 tick simülasyonu
python packages/idem-game-ai/src/idempotent_game_ai/cli.py roblox-demo --entities 5000 --ticks 100

# Algoritmik eşitlik ve matematiksel idempotens testi
python packages/idem-game-ai/tests/test_roblox_luau_logic.py
```

---

## 4. Başarı Kriterleri

1. **GC Bellek Değişimi:** `collectgarbage("count")` test boyunca `0.00 KB` artış göstermelidir. Hiçbir dinamik tablo (`{}`) veya `table.remove` çağrısı yapılmamalıdır.
2. **Tick Süresi:** 5,000 varlık için ortalama süre **< 1.0 ms** olmalıdır (Roblox sunucu bütçesi olan 16.66 ms'nin ve AI bütçesi olan 2.0 ms'nin çok altındadır).

