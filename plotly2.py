import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🚨 범죄 유형별 발생 및 검거 현황 (2022년 기준)")

uploaded_file = st.file_uploader("범죄 통계 CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949', skiprows=1)
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8', skiprows=1)

    # 정확한 컬럼명 사용
    df_filtered = df[['죄종별(2)', '발생건수 (건)', '검거건수 (건)']].copy()
    df_filtered.columns = ['범죄유형', '발생건수', '검거건수']

    # 소계/총계 제외
    df_filtered = df_filtered[~df_filtered['범죄유형'].isin(['소계', '총계'])]
    df_filtered[['발생건수', '검거건수']] = df_filtered[['발생건수', '검거건수']].apply(pd.to_numeric, errors='coerce')

    # 상위 10개
    df_top10 = df_filtered.sort_values(by='발생건수', ascending=False).head(10)

    # Plotly 시각화
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_top10['범죄유형'],
        y=df_top10['발생건수'],
        name='발생건수',
        marker_color='crimson'
    ))
    fig.add_trace(go.Bar(
        x=df_top10['범죄유형'],
        y=df_top10['검거건수'],
        name='검거건수',
        marker_color='royalblue'
    ))

    fig.update_layout(
        title='범죄 유형별 발생 및 검거 건수 (2022년, 상위 10개)',
        xaxis_title='범죄 유형',
        yaxis_title='건수 (건)',
        barmode='group',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📁 CSV 파일을 업로드하면 그래프가 표시됩니다.")
