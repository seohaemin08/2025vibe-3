import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 남녀 인구 분포", layout="wide")
st.title("👨‍👩‍👧‍👦 서울특별시 연령별 남녀 인구 분포 (2025년 6월 기준)")

uploaded_file = st.file_uploader("남녀 인구 구분 CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 서울특별시 전체 데이터 필터링
    seoul = df[df['행정구역'].str.contains("서울특별시  \(1100000000\)", regex=True)]

    if not seoul.empty:
        # 컬럼 분리
        male_cols = [col for col in df.columns if '남_' in col and '세' in col]
        female_cols = [col for col in df.columns if '여_' in col and '세' in col]

        def extract_age(colname):
            part = colname.split('_')[-1]
            return 100 if '이상' in part else int(part.replace('세', ''))

        ages = [extract_age(col) for col in male_cols]

        def get_population(col_list):
            pops = []
            for col in col_list:
                val = seoul[col].values[0]
                val = int(val.replace(",", "")) if isinstance(val, str) else int(val)
                pops.append(val)
            return pops

        male_pop = get_population(male_cols)
        female_pop = get_population(female_cols)

        # 그래프
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ages, y=male_pop, name="남성", marker_color="blue"))
        fig.add_trace(go.Bar(x=ages, y=female_pop, name="여성", marker_color="pink"))
        fig.update_layout(
            barmode="group",
            title="서울특별시 연령별 남녀 인구 비교",
            xaxis_title="나이",
            yaxis_title="인구 수",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("서울시 전체 데이터를 찾을 수 없습니다.")
else:
    st.info("CSV 파일을 업로드하면 시각화가 시작됩니다.")
