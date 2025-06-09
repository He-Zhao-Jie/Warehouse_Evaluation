import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
from folium.plugins import Fullscreen
from folium.features import IFrame
import plotly.graph_objects as go

# 設置頁面標題
st.title('Soria Natural Warehouse Evaluation')

# 讀取CSV檔案
@st.cache_data
def load_data():
    df = pd.read_csv('warehouse_data.csv')
    # 清理 Price 欄位：移除 € 符號、空格和千位分隔符，並轉換為浮點數
    df['Price'] = df['Price'].str.replace('€', '').str.replace(',', '').str.strip().astype(float)
    # 清理 Price per m^2 欄位
    df['Price per m^2'] = df['Price per m^2'].str.replace('€', '').str.replace(',', '').str.strip().astype(float)
    return df

df = load_data()

# 在側邊欄添加篩選條件
st.sidebar.header('篩選條件')

# 距離篩選
max_distance = st.sidebar.slider(
    '最大距離 (km)',
    min_value=0.0,
    max_value=50.0,
    value=50.0,
    step=0.5
)

# 修改面積篩選方式
target_area = df.iloc[0]['Total Area (m^2)']  # 勘估標的面積
area_difference = st.sidebar.slider(
    '面積誤差範圍 (±m²)',
    min_value=0.0,
    max_value=2000.0,
    value=1000.0,
    step=100.0
)

# 計算面積範圍
min_area = target_area - area_difference
max_area = target_area + area_difference

# 在側邊欄顯示實際的面積範圍
st.sidebar.write(f'搜尋面積範圍：')
st.sidebar.write(f'{min_area:,.0f} ~ {max_area:,.0f} m²')

# 建立地圖
def create_map(df, max_distance, min_area, max_area):
    # 以勘估標的為中心點
    center_lat = df.iloc[0]['Latitude']
    center_lon = df.iloc[0]['Longitude']
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    # 添加全螢幕控制
    Fullscreen(
        position='topleft',
        title='全螢幕切換',
        title_cancel='退出全螢幕',
        force_separate_button=True
    ).add_to(m)
    
    # 添加勘估標的（紅色標記）
    html = f"""
        <div style="font-size: 14px; font-family: Arial;">
            <b>勘估標的：</b>{df.iloc[0]['Address']}<br>
            <b>總面積：</b>{df.iloc[0]['Total Area (m^2)']}m²<br>
            <b>售價：</b>€{df.iloc[0]['Price']:,.2f}<br>
            <b>單價：</b>€{df.iloc[0]['Price per m^2']:,.2f}/m²
        </div>
    """
    iframe = IFrame(html=html, width=300, height=120)
    popup = folium.Popup(iframe, max_width=300)
    
    folium.Marker(
        [df.iloc[0]['Latitude'], df.iloc[0]['Longitude']],
        popup=popup,
        icon=folium.Icon(color='red'),
    ).add_to(m)
    
    # 添加比較標的（藍色標記）
    for idx, row in df.iloc[1:].iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            # 計算與勘估標的的距離
            distance = geodesic(
                (df.iloc[0]['Latitude'], df.iloc[0]['Longitude']),
                (row['Latitude'], row['Longitude'])
            ).kilometers
            
            # 根據篩選條件決定是否顯示此標的
            if (distance <= max_distance and 
                min_area <= row['Total Area (m^2)'] <= max_area):
                
                html = f"""
                    <div style="font-size: 14px; font-family: Arial;">
                        <b>比較標的：</b>{row['Address']}<br>
                        <b>總面積：</b>{row['Total Area (m^2)']}m²<br>
                        <b>售價：</b>€{row['Price']:,.2f}<br>
                        <b>單價：</b>€{row['Price per m^2']:,.2f}/m²<br>
                        <b>距離勘估標的：</b>{distance:.2f}km
                    </div>
                """
                iframe = IFrame(html=html, width=300, height=140)
                popup = folium.Popup(iframe, max_width=300)
                
                folium.Marker(
                    [row['Latitude'], row['Longitude']],
                    popup=popup,
                    icon=folium.Icon(color='blue'),
                ).add_to(m)
    
    return m

# 在距離表格之前，先顯示勘估標的和比較標的的基本資訊
st.subheader('勘估標的資訊')
target_info = {
    '地址': df.iloc[0]['Address'],
    '總面積(m²)': f"{df.iloc[0]['Total Area (m^2)']:,.0f}",
    '售價(€)': f"€{df.iloc[0]['Price']:,.2f}",
    '單價(€/m²)': f"€{df.iloc[0]['Price per m^2']:,.2f}"
}
target_df = pd.DataFrame([target_info])
st.dataframe(target_df, hide_index=True)

st.subheader('比較標的資訊')
comp_data = []
for idx, row in df.iloc[1:].iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        distance = geodesic(
            (df.iloc[0]['Latitude'], df.iloc[0]['Longitude']),
            (row['Latitude'], row['Longitude'])
        ).kilometers
        
        # 根據篩選條件決定是否加入表格
        if (distance <= max_distance and 
            min_area <= row['Total Area (m^2)'] <= max_area):
            comp_data.append({
                '地址': row['Address'],
                '總面積(m²)': f"{row['Total Area (m^2)']:,.0f}",
                '售價(€)': f"€{row['Price']:,.2f}",
                '單價(€/m²)': f"€{row['Price per m^2']:,.2f}",
                '距離(km)': f"{distance:.2f}"
            })

comp_df = pd.DataFrame(comp_data)
st.dataframe(comp_df, hide_index=True)

# 先顯示地圖
st.subheader('倉庫位置地圖')
m = create_map(df, max_distance, min_area, max_area)
folium_static(m)

# 在IDW計算之前添加箱型圖
st.subheader('單價分布箱型圖分析')

# 準備箱型圖數據
filtered_prices = []
for idx, row in df.iloc[1:].iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        distance = geodesic(
            (df.iloc[0]['Latitude'], df.iloc[0]['Longitude']),
            (row['Latitude'], row['Longitude'])
        ).kilometers
        
        # 根據篩選條件決定是否納入計算
        if (distance <= max_distance and 
            min_area <= row['Total Area (m^2)'] <= max_area):
            filtered_prices.append(row['Price per m^2'])

if filtered_prices:
    # 創建箱型圖
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=filtered_prices,
        name='比較標的',
        boxpoints='all',  # 顯示所有數據點
        jitter=0.3,  # 數據點的分散程度
        pointpos=-1.8,  # 數據點的位置
        marker_color='blue',
        marker_size=8,
        line_color='blue'
    ))

    # 添加勘估標的的單價作為參考線
    target_price = df.iloc[0]['Price per m^2']
    fig.add_hline(
        y=target_price,
        line_dash="dash",
        line_color="red",
        annotation_text="勘估標的單價",
        annotation_position="top right"
    )

    # 更新圖表布局
    fig.update_layout(
        title='比較標的單價分布',
        yaxis_title='單價 (€/m²)',
        showlegend=True,
        height=500,
        yaxis=dict(
            gridcolor='lightgrey',
            zeroline=False
        ),
        plot_bgcolor='white'
    )

    # 顯示箱型圖
    st.plotly_chart(fig, use_container_width=True)

    # 顯示統計摘要
    st.write('單價統計摘要：')
    summary_stats = pd.Series(filtered_prices).describe()
    summary_df = pd.DataFrame({
        '統計量': ['數量', '平均值', '標準差', '最小值', '25%分位數', '中位數', '75%分位數', '最大值'],
        '數值': [
            f"{summary_stats['count']:.0f}",
            f"€{summary_stats['mean']:,.2f}",
            f"€{summary_stats['std']:,.2f}",
            f"€{summary_stats['min']:,.2f}",
            f"€{summary_stats['25%']:,.2f}",
            f"€{summary_stats['50%']:,.2f}",
            f"€{summary_stats['75%']:,.2f}",
            f"€{summary_stats['max']:,.2f}"
        ]
    })
    st.dataframe(summary_df, hide_index=True)
else:
    st.warning('沒有符合篩選條件的比較標的，無法生成箱型圖')

# 再進行IDW計算
st.subheader('IDW空間插值計算')

def idw_interpolation(target_point, comp_points, comp_values, power=2):
    """
    執行IDW插值
    target_point: 目標點的座標 [lat, lon]
    comp_points: 比較標的的座標列表 [[lat1, lon1], [lat2, lon2], ...]
    comp_values: 比較標的的單價列表
    power: 距離權重指數，預設為2
    """
    weights = []
    total_weight = 0
    
    # 計算每個比較標的的權重
    for point in comp_points:
        distance = geodesic(target_point, point).kilometers
        if distance == 0:  # 如果距離為0，直接返回該點的值
            return comp_values[comp_points.index(point)]
        
        # 計算權重 (1/d^p)
        weight = 1 / (distance ** power)
        weights.append(weight)
        total_weight += weight
    
    # 正規化權重並計算加權平均
    weights = [w/total_weight for w in weights]
    predicted_value = sum(w * v for w, v in zip(weights, comp_values))
    
    return predicted_value

# 準備IDW分析所需的資料
comp_data = []
comp_points = []
comp_values = []

for idx, row in df.iloc[1:].iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        distance = geodesic(
            (df.iloc[0]['Latitude'], df.iloc[0]['Longitude']),
            (row['Latitude'], row['Longitude'])
        ).kilometers
        
        # 根據篩選條件決定是否納入計算
        if (distance <= max_distance and 
            min_area <= row['Total Area (m^2)'] <= max_area):
            comp_points.append([row['Latitude'], row['Longitude']])
            comp_values.append(row['Price per m^2'])
            comp_data.append({
                '地址': row['Address'],
                '單價(€/m²)': row['Price per m^2'],
                '距離(km)': distance,
                '權重(1/d²)': 1/(distance**2)
            })

if len(comp_points) >= 3:  # 確保有足夠的比較標的
    # 先顯示計算過程的詳細資訊
    st.write('IDW計算過程詳細資訊：')
    process_df = pd.DataFrame(comp_data)
    # 計算權重佔比
    total_weight = process_df['權重(1/d²)'].sum()
    process_df['權重佔比(%)'] = (process_df['權重(1/d²)'] / total_weight * 100).round(2)
    process_df['加權單價(€/m²)'] = (process_df['單價(€/m²)'] * process_df['權重佔比(%)'] / 100).round(2)
    
    # 格式化顯示
    process_df['單價(€/m²)'] = process_df['單價(€/m²)'].apply(lambda x: f'€{x:,.2f}')
    process_df['權重(1/d²)'] = process_df['權重(1/d²)'].round(4)
    process_df['權重佔比(%)'] = process_df['權重佔比(%)'].apply(lambda x: f'{x:.2f}%')
    process_df['加權單價(€/m²)'] = process_df['加權單價(€/m²)'].apply(lambda x: f'€{x:,.2f}')
    
    st.dataframe(process_df, hide_index=True)

    # 再顯示計算結果
    target_point = [df.iloc[0]['Latitude'], df.iloc[0]['Longitude']]
    predicted_price = idw_interpolation(target_point, comp_points, comp_values)
    
    # 計算所有需要的值
    actual_price = df.iloc[0]['Price per m^2']
    target_area = df.iloc[0]['Total Area (m^2)']
    predicted_total_price = predicted_price * target_area
    actual_total_price = actual_price * target_area
    
    # 使用CSS來設置樣式
    st.markdown("""
        <style>
        .result-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .result-header {
            color: #0e1117;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .result-item {
            margin-left: 10px;
            color: #0e1117;
            font-size: 1.2em;
            line-height: 2;
        }
        .result-value {
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # 使用設置好的CSS類別來顯示結果
    st.markdown("""
        <div class="result-container">
            <div class="result-header">計算結果</div>
            <div class="result-item">
                • 勘估標的預測單價：<span class="result-value">€{:,.2f}/m²</span><br>
                • 勘估標的實際單價：<span class="result-value">€{:,.2f}/m²</span><br>
                • 勘估標的預測售價：<span class="result-value">€{:,.2f}</span><br>
                • 勘估標的實際售價：<span class="result-value">€{:,.2f}</span>
            </div>
        </div>
    """.format(
        predicted_price,
        actual_price,
        predicted_total_price,
        actual_total_price
    ), unsafe_allow_html=True)
    
    # 計算差異百分比
    price_diff_pct = ((predicted_price - actual_price) / actual_price) * 100
    
else:
    st.error('執行IDW計算需要至少3個有效的比較標的') 