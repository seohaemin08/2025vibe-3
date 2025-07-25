import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 연령별 인구 분포", layout="wide")

st.title("📊 서울특별시 연령별 인구 분포 (2025년 6월 기준)")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (예: '연령별인구현황_월간 합계')", type="csv")

if uploaded_file is not None:
    # CSV 읽기
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 서울시 전체 데이터 필터링
    seoul = df[df['행정구역'].str.contains("서울특별시  \(1100000000\)", regex=True)]

    if not seoul.empty:
        # 연령별 컬럼 필터링
        age_cols = [col for col in seoul.columns if '계_' in col and '세' in col]

        ages = []
        populations = []

        for col in age_cols:
            age_label = col.split('_')[-1]
            age = 100 if '이상' in age_label else int(age_label.replace('세', ''))
            value = seoul[col].values[0]
            value = int(value.replace(',', '')) if isinstance(value, str) else int(value)
            ages.append(age)
            populations.append(value)

        # 시각화
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ages, y=populations, name="연령별 인구"))
        fig.update_layout(
            title='서울특별시 연령별 인구 분포 (2025년 6월)',
            xaxis_title='나이',
            yaxis_title='인구 수',
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("서울특별시 전체 데이터가 포함된 행이 없습니다.")
else:
    st.info("좌측 사이드바에서 CSV 파일을 업로드해주세요.")
