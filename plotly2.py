import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🚨 범죄 유형별 발생 및 검거 현황 (2022년 기준)")

uploaded_file = st.file_uploader("범죄 통계 CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 실제 컬럼명 자동 탐색 (유사한 이름 포함)
    col_names = df.columns.tolist()
    crime_col = next((c for c in col_names if '죄종별' in c and '(2)' in c), None)
    occur_col = next((c for c in col_names if '발생건수' in c), None)
    arrest_col = next((c for c in col_names if '검거건수' in c), None)

    if not all([crime_col, occur_col, arrest_col]):
        st.error("필요한 열(죄종별, 발생건수, 검거건수)을 찾을 수 없습니다. CSV 파일 구조를 확인하세요.")
    else:
        df_filtered = df[[crime_col, occur_col, arrest_col]].copy()
        df_filtered.columns = ['범죄유형', '발생건수', '검거건수']

        # '총계', '소계' 제거 및 숫자 변환
        df_filtered = df_filtered[~df_filtered['범죄유형'].isin(['소계', '총계'])]
        df_filtered[['발생건수', '검거건수']] = df_filtered[['발생건수', '검거건수']].apply(pd.to_numeric, errors='coerce')

        # 상위 10개
        df_top10 = df_filtered.sort_values(by='발생건수', ascending=False).head(10)

        # Plotly 그래프
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
