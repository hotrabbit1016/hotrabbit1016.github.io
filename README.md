# hotrabbit1016.github.io

個人網站原始碼 — 吳承儒 / Jack Wu，後端工程師。

網址：<https://hotrabbit1016.github.io>

## 結構

| 檔案 | 說明 |
|---|---|
| `index.html` | 整個網站。內嵌 CSS 與 JS，**零外部請求**，沒有建置步驟 |
| `resume.pdf` | 履歷（公開版，不含 email 與電話） |
| `og.png` | 分享預覽圖（1200×630） |
| `robots.txt`、`sitemap.xml` | 搜尋引擎索引用 |
| `.nojekyll` | 跳過 GitHub 的 Jekyll 處理，部署較快 |

## 怎麼改

直接編輯 `index.html`，推上 `main` 就會自動部署（Pages 從 `main` 分支根目錄讀取），大約一到兩分鐘生效。

網站是繁中與英文兩份平行內容，用 `class="l-zh"` 與 `class="l-en"` 標記，靠 `<html data-lang>` 切換顯示。**改中文的時候記得同步改英文**，否則切語言會看到舊內容。

深色與淺色主題都要顧到 — 顏色全部走 CSS 變數，定義在 `:root` 與 `html[data-theme="dark"]`。

## 注意

- 頁面上**刻意不放 email 與電話**，聯絡管道只走 GitHub。要加聯絡方式前先想清楚：公開頁面上的信箱會被爬蟲收集。
- `resume.pdf` 是公開版，聯絡資訊已移除、產業用詞改為中性。完整版履歷不在這個 repo 裡。
