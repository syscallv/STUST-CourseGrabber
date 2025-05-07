# STUST CourseGrabber

這是一個基於 Python 的自動化腳本，使用 Selenium 和 undetected-chromedriver 在南台科技大學（STUST）的選課系統（[course.stust.edu.tw](https://course.stust.edu.tw)）上自動選課。腳本能自動查詢課程、確認空位、填寫驗證碼、選課，並支援退選功能，幫助學生快速搶到目標課程。

## 功能
- 根據課程名稱自動查詢目標課程。
- 即時檢查課程空位（比較當前人數與上限人數）。
- 使用 ddddocr 自動辨識選課系統的驗證碼。
- 自動填寫帳號、密碼並完成登入。
- 支援選課和退選功能（可指定退選課程）。
- 提供帶時間戳的日誌，記錄操作過程並儲存至 `output.txt`。

## 環境需求
- Python 3.8 或更高版本
- 已安裝 Chrome 瀏覽器
- 與 Chrome 版本相容的 ChromeDriver 可執行檔
- 安裝 ddddocr 模型（用於驗證碼辨識）

## 安裝
 1. 安裝所需的 Python 套件：
   所需套件包括：
   - `undetected-chromedriver`
   - `selenium`
   - `ddddocr`
   - `Pillow`
   - `numpy`
   - `onnxruntime`
3. 下載 [ChromeDriver](https://chromedriver.chromium.org/downloads) 並確保其與 Chrome 版本相容，將其放置在系統 PATH 或指定路徑。
4. 確保 ddddocr 的模型檔案（`common_old.onnx`）已正確配置（參考 [ddddocr 文檔](https://github.com/sml2h3/ddddocr)）。

## 使用方法
1. 確保已安裝所有依賴並準備好 ChromeDriver。
2. 運行腳本：
   ```bash
   python STUST-tools.py
   ```
3. 根據提示輸入以下資訊：
   - 學號（帳號）
   - 密碼
   - 目標課程名稱（例如「無障礙生活」）
   - 欲退選的課程名稱（若無則輸入任意值）
4. 腳本將執行以下操作：
   - 檢查目標課程是否有空位。
   - 自動登入選課系統。
   - 查詢並選擇目標課程。
   - 辨識驗證碼並提交選課請求。
   - 若選課失敗（例如重複選課），可自動退選指定課程並重試。
   - 記錄所有操作到 `output.txt`。

## 配置
無需額外的配置文件，但需確保以下項目：
- **帳號與密碼**：運行時手動輸入，確保為有效的 STUST 選課系統學號和密碼。
- **課程名稱**：輸入完整的課程名稱（例如「無障礙生活」），必須與選課系統中的名稱一致。
- **ChromeDriver**：確保 ChromeDriver 可執行檔與 Chrome 版本相容。
- **ddddocr 模型**：確保 `common_old.onnx` 模型檔案已下載並位於正確路徑（參考 ddddocr 安裝指南）。

## 貢獻
歡迎為本專案貢獻！對於任何錯誤或建議，請建立拉取請求或提交問題。

## 授權
本專案採用 MIT 授權，詳情請見 [LICENSE](LICENSE) 文件。

## 免責聲明
本腳本僅供教育用途。使用本腳本時，請確保遵守南台科技大學選課系統的服務條款和相關法律法規。開發者對因使用本腳本而導致的任何問題（包括但不限於帳號封禁或選課失敗）不承擔責任。請謹慎使用，切勿用於非法目的。
