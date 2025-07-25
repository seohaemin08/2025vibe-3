import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🌈주요 연령계층별 추계인구")

uploaded_file = st.file_uploader("CSV 파일 업로드 (주요 연령계층별 추계인구)", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 중위 추계 필터
    filtered = df[df['가정별'].str.contains("중위 추계")]
    targets = [
        '생산연령인구(천명): 계(15~64세)',
        '생산연령인구(천명): 15-24세',
        '생산연령인구(천명): 25-49세',
        '생산연령인구(천명): 50-64세'
    ]
    
    # 무지개 색 매핑
    rainbow_colors = {
        '생산연령인구(천명): 계(15~64세)': 'red',
        '생산연령인구(천명): 15-24세': 'orange',
        '생산연령인구(천명): 25-49세': 'green',
        '생산연령인구(천명): 50-64세': 'blue'
    }

    filtered = filtered[filtered['인구종류별'].isin(targets)]
    year_cols = [col for col in filtered.columns if col.isdigit()]
    years = list(map(int, year_cols))

    # 시각화
    fig = go.Figure()
    for _, row in filtered.iterrows():
        group = row['인구종류별']
        values = row[year_cols].astype(float).values
        fig.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            name=group,
            marker_color=rainbow_colors.get(group, 'gray')
        ))

    fig.update_layout(
        title='🌈 생산연령 인구 추이 (무지개 색)',
        xaxis_title='연도',
        yaxis_title='인구 수 (천 명)',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📁 CSV 파일을 업로드하면 무지개 그래프가 표시됩니다.")
