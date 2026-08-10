# hotrabbit1016.github.io

個人網站原始碼 — 吳承儒 / Jack Wu，後端工程師。

網址：<https://hotrabbit1016.github.io/resume/>

## 結構

| 檔案 | 說明 |
|---|---|
| `resume/index.html` | 整個網站。內嵌 CSS 與 JS，**零外部請求**，沒有建置步驟 |
| `resume/resume.pdf` | 履歷（公開版，不含 email 與電話） |
| `resume/og.png` | 分享預覽圖（1200×630） |
| `robots.txt`、`sitemap.xml` | 搜尋引擎索引用，**必須留在根目錄** |
| `.nojekyll` | 跳過 GitHub 的 Jekyll 處理，部署較快 |

網站放在子目錄是因為這個 repo 是 user site，Pages 只從網域根目錄提供服務，所以 `/resume/` 這個路徑靠的是資料夾結構，不是 Pages 設定。

根目錄**刻意沒有 `index.html`** —— `https://hotrabbit1016.github.io` 直接回 404，不透露 `/resume/` 的存在。不要為了「看起來比較完整」而加回首頁或轉址。

## 怎麼改

直接編輯 `resume/index.html`，推上 `main` 就會自動部署（Pages 從 `main` 分支根目錄讀取），大約一到兩分鐘生效。

改網址時記得同步 `resume/index.html` 裡的 `canonical`、`og:url`、`og:image`、JSON-LD 的 `url`，以及 `sitemap.xml`。

網站是繁中與英文兩份平行內容，用 `class="l-zh"` 與 `class="l-en"` 標記，靠 `<html data-lang>` 切換顯示。**改中文的時候記得同步改英文**，否則切語言會看到舊內容。

深色與淺色主題都要顧到 — 顏色全部走 CSS 變數，定義在 `:root` 與 `html[data-theme="dark"]`。

## 注意

- 頁面上**刻意不放 email 與電話**，聯絡管道只走 GitHub。要加聯絡方式前先想清楚：公開頁面上的信箱會被爬蟲收集。
- `resume.pdf` 是公開版，聯絡資訊已移除、產業用詞改為中性。完整版履歷不在這個 repo 裡。
