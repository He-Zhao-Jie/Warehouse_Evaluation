# Warehouse Evaluation App

這是一個用於倉庫評估的 Streamlit 應用程式，使用 IDW（反距離加權法）進行空間插值分析。

## 功能特點

- 互動式地圖顯示
- 距離和面積篩選
- IDW 空間插值計算
- 詳細的計算過程展示
- 預測價格與實際價格比較

## 資料格式要求

請準備一個 CSV 檔案 (warehouse_data.csv)，其中需要包含以下欄位：
- Address：地址
- Latitude：緯度
- Longitude：經度
- Total Area (m^2)：總面積
- Price：價格 (€)
- Price per m^2：每平方公尺單價 (€)

## 本地運行

1. 安裝相依套件：
```bash
pip install -r requirements.txt
```

2. 運行應用程式：
```bash
streamlit run app.py
```

## 線上使用

訪問：[Streamlit Cloud 連結]

## 注意事項

- 第一筆資料將被視為勘估標的
- 需要至少 3 個有效的比較標的才能進行 IDW 計算
- 所有金額單位為歐元 (€) 