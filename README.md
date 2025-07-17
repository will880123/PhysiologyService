# 🐍 Physiology Service

## 📖 專案簡介

**PhysiologyService** 是一個以 **Python** 開發的微服務（Microservice）專案，遵循三層架構設計，主要功能為記錄與管理生理機能資料（如血壓、血糖等），並透過 **Google Sheets API** 實現雲端資料儲存。

### 核心功能

- 提供 RESTful API 接口（CRUD 操作）
- 整合 Google Sheets 作為資料儲存後端
- 採用三層架構（Controller / Service / Repository）
- 支援 OAuth 2.0 驗證機制（Google Sheets 使用）

---

## 🚀 專案啟動流程

### 1️⃣ 建立虛擬環境

```bash
python -m venv .venv
```

### 2️⃣ 啟動虛擬環境

- Windows：

```bash
.venv\Scripts\activate
```

- macOS / Linux：

```bash
source .venv/bin/activate
```

### 3️⃣ 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4️⃣ 設定 Google Sheets API 認證資訊

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立專案並啟用 Google Sheets API
3. 建立 OAuth 2.0 憑證，下載 `credentials.json`
4. 將 `credentials.json` 放置於 `./credentials` 資料夾內

### 5️⃣ 用 uvicorn 啟動應用程式

```bash
python main.py
```


### 6️⃣ 測試 API

- 開啟瀏覽器並前往自動產生的 Swagger UI：
    ```nginx
    http://127.0.0.1:8000/docs
    ```

- 也可以用 curl 或 Postman 測試：
    ```nginx
    curl http://127.0.0.1:8000/records
    ```

### 7️⃣ 結束與退出虛擬環境

```bash
deactivate
```

---

## 專案結構

```
PhysiologyService/
├── controllers/             # 路由與 API 實作
├── credentials/             # 憑證資料夾
│   └── credentials.json     # Google API 憑證
├── models/                  # 資料模型
├── repositories/            # 資料存取與處理
├── services/                # 商業邏輯
├── main.py                  # 主程式入口，啟動 FastAPI app
└── requirements.txt         # 套件清單
```

---

## API 功能概述

| 方法     | 路由            | 說明     |
| ------ | ------------- | ------ |
| GET    | /records      | 取得所有記錄 |
| GET    | /records/\:id | 取得指定記錄 |
| POST   | /records      | 新增一筆記錄 |
| PUT    | /records/\:id | 更新指定記錄 |
| DELETE | /records/\:id | 刪除指定記錄 |
