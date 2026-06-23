🐟 香港釣魚資訊站 — 安裝教學
===================================
by 小婷

📋 安裝步驟：
============

1️⃣ Download 呢個 folder ("fishing-hk") 嘅所有檔案

2️⃣ 放入你部 UGreen NAS

  方法 A — File Manager：
  - 入你部 NAS 嘅管理界面
  - 開 File Manager / 檔案總管
  - 建立一個新 folder，例如 "fishing"
  - Upload 晒啲 file 入去

  方法 B — SMB (網絡磁碟)：
  - 喺你電腦開 \\YOUR_NAS_IP\ 連去 NAS
  - Copy 成個 folder 過去

3️⃣ 開 Web Server

  喺 UGreen NAS 管理界面：
  - 搵 Web Station / Web Server / 網站伺服器
  - 新增一個網站 / Virtual Host
  - Document Root 指向你放 file 嘅 folder
  - Port 可以揀 8080 或者 80
  - 啟動！

4️⃣ 測試：

  喺 browser 打：
  http://YOUR_NAS_IP:PORT/
  （例如 http://192.168.1.100:8080）

✅ 完成！以後每次開網站，天氣會自動更新！


🔧 如果遇到問題：
===============
- 睇下 NAS 有冇開 firewall port
- 確認 Web Server 有開
- Contact 小婷 😊


🌐 For Public Access（街外睇到）：
=============================
如果想由街外都可以睇到：
- 你嘅 NAS 要有 DDNS（動態域名）
- 或者要 set Port Forwarding
- 到時小婷再幫你搞！
