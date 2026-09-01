# hotrabbit1016.github.io

個人網站原始碼 — 吳承儒 / Jack Wu，後端工程師。

網址：<https://hotrabbit1016.github.io/resume/>

## 結構

| 檔案 | 說明 |
|---|---|
| `resume/index.html` | 整個網站。內嵌 CSS 與 JS，**零外部請求**，沒有建置步驟 |
| `resume/resume.pdf` | 中文履歷 PDF（公開版） |
| `resume/resume-en.pdf` | English resume PDF (public version) |
| `generate_resume_pdfs.py` | 產生中、英文兩頁 A4 PDF 履歷的 ReportLab 腳本 |
| `resume/og.png` | 分享預覽圖（1200×630） |
| `resume/hintme/index.html` | 面試準備筆記。單檔、內嵌 CSS/JS，練習進度存 `localStorage` |
| `.nojekyll` | 跳過 GitHub 的 Jekyll 處理，部署較快 |

網站放在子目錄是因為這個 repo 是 user site，Pages 只從網域根目錄提供服務，所以 `/resume/` 這個路徑靠的是資料夾結構，不是 Pages 設定。

根目錄**刻意沒有 `index.html`** —— `https://hotrabbit1016.github.io` 直接回 404，不透露 `/resume/` 的存在。不要為了「看起來比較完整」而加回首頁或轉址。

## 面試準備筆記

`/resume/hintme/` 是自己用的面試練習頁，**主站刻意沒有任何連結指向它** —— 加了等於主動把面試官導過去。靠網址直接開。

薪資談判的區間與底線**不在這個 repo 裡**（在本機 `resume_output/薪資談判.md`）。談判前把底線公開等於把牌翻給對方看，這一項不要搬上來。

## 這個網站不對外曝光

用途是**面試前主動把連結給對方**，不是被搜尋到。所以：

- `resume/index.html` 帶 `noindex, nofollow`
- **沒有** `robots.txt`、**沒有** `sitemap.xml` —— 那兩個檔案是公開可讀的，會直接列出 `/resume/`
- 根目錄回 404

要改回「希望被 Google 搜到」的話，這三項要一起回復，只改一項沒有用。

Open Graph 標籤刻意留著 —— 那是給你貼連結時的預覽圖用的，跟搜尋索引無關。

## 怎麼改

直接編輯 `resume/index.html`，推上 `main` 就會自動部署（Pages 從 `main` 分支根目錄讀取），大約一到兩分鐘生效。

PDF 履歷內容與版型由 `generate_resume_pdfs.py` 維護。修改後執行 `python generate_resume_pdfs.py`，會更新 `resume/resume.pdf` 與 `resume/resume-en.pdf`；兩份都應保持兩頁 A4。

改網址時記得同步 `resume/index.html` 裡的 `canonical`、`og:url`、`og:image`、JSON-LD 的 `url`，以及 `sitemap.xml`。

網站是繁中與英文兩份平行內容，用 `class="l-zh"` 與 `class="l-en"` 標記，靠 `<html data-lang>` 切換顯示。**改中文的時候記得同步改英文**，否則切語言會看到舊內容。

深色與淺色主題都要顧到 — 顏色全部走 CSS 變數，定義在 `:root` 與 `html[data-theme="dark"]`。

## 注意

- 頁面與兩份 PDF 都公開顯示 email 與電話，更新聯絡方式時三處要同步修改。
- `resume.pdf` 必須保留為中文版檔名，避免既有公開連結失效；英文版使用 `resume-en.pdf`。
