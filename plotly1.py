import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📈 생산연령 인구 추이 시각화 (2022 ~ 2072)")

uploaded_file = st.file_uploader("CSV 파일 업로드 (예: 주요 연령계층별 추계인구)", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 필터링
    filtered = df[df['가정별'].str.contains("중위 추계")]
    targets = [
        '생산연령인구(천명): 계(15~64세)',
        '생산연령인구(천명): 15-24세',
        '생산연령인구(천명): 25-49세',
        '생산연령인구(천명): 50-64세'
    ]
    filtered = filtered[filtered['인구종류별'].isin(targets)]

    # 연도별 컬럼
    year_cols = [col for col in filtered.columns if col.isdigit()]
    years = list(map(int, year_cols))

    # 그래프
    fig = go.Figure()
    for _, row in filtered.iterrows():
        values = row[year_cols].astype(float).values
        fig.add_trace(go.Scatter(x=years, y=values, mode='lines+markers', name=row['인구종류별']))

    fig.update_layout(
        title=
