# 八字與相學時間切片數位模擬系統 (Bazi & Physiognomy Time-Slicing Digital Simulation Engine)

基於 Python 模組化架構與自動化 CI/CD 驗證開發的「八字與相學時間切片數位模擬系統」。本專案旨在建構精確的八字四柱排盤演算、地支藏干權重配比、動態五行能量強弱模型，並結合前端視覺化儀表板進行時間切片（流年/流月/流日）之動態模擬。

---

## 核心功能與架構 (Core Features)

1. **基礎干支與十神演算引擎 (`src/core/bazi.py`)**
   - 自動推算天干與日主之十神關係（比肩、劫財、食神、傷官、偏財、正財、七殺、正官、偏印、正印）。
   - 解析十二地支藏干與對應權重比例（如：辰藏戊 0.6、乙 0.3、癸 0.1）。

2. **時間切片視覺化儀表板 (`index.html`)**
   - **傳統四柱排盤**：符合傳統由右至左（時柱、日柱、月柱、年柱）的視圖呈現與五行色彩對應。
   - **五行動態雷達圖**：透過 Chart.js 即時視覺化原局與切片後的「木、火、土、金、水」能量比重。
   - **時間切片模擬器**：支援流年與流月切片選擇，即時運算地支碰撞效應（合、沖、害、刑）與日主強弱狀態變化。

3. **自動化 CI/CD 工作流 (`.github/workflows/test.yml`)**
   - 整合 Pytest 與 Coverage 測試框架，確保核心排盤演算法每次 Commit 均自動執行單元測試。

---

## 目錄結構 (Project Structure)

```text
bazi-timeline/
├── .github/
│   └── workflows/
│       └── test.yml         # GitHub Actions CI 工作流
├── src/
│   └── core/
│       ├── constants.py     # 天干地支、五行屬性與地支藏干對照表
│       └── bazi.py          # 八字排盤與十神核心演算邏輯
├── tests/
│   └── test_shishen.py      # 十神推算單元測試
├── index.html               # 視覺化動態時間切片儀表板
├── main.py                  # 本地排盤驗證腳本
├── pytest.ini               # Pytest 測試配置
└── requirements.txt         # 專案依賴套件