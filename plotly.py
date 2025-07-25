import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울 인구 시각화", layout="wide")
st.title("🧑‍🤝‍🧑 서울특별시 연령별 인구 시각화 (2025년 6월)")

# 파일 업로드
col1, col2 = st.columns(2)
with col1:
    total_file = st.file_uploader("📂 [1] 월간 합계 파일", type="csv", key="total")
with col2:
    gender_file = st.file_uploader("📂 [2] 남녀 구분 파일", type="csv", key="gender")

# 모드 선택
mode = st.radio("⚙️ 시각화 모드 선택", ["전체 인구", "남녀 구분"], horizontal=True)

# 전처리 함수
def get_age_and_pop(df, prefix):
    seoul = df[df['행정구역'].str.contains("서울특별시  \(1100000000\)", regex=True)]
    cols = [col for col in df.columns if prefix in col and '세' in col]

    def age_label(colname):
        label = colname.split('_')[-1]
        return 100 if '이상' in label else int(label.replace('세', ''))

    ages = [age_label(c) for c in cols]

    pops = []
    for col in cols:
        val = seoul[col].values[0]
        val = int(val.replace(',', '')) if isinstance(val, str) else int(val)
        pops.append(val)

    return ages, pops

# 전체 인구 모드
if mode == "전체 인구" and total_file:
    df_total = pd.read_csv(total_file, encoding='cp949')
    ages, pops = get_age_and_pop(df_total, "계_")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=ages, y=pops, name="전체 인구"))
    fig.update_layout(
        title="서울특별시 연령별 전체 인구",
        xaxis_title="나이",
        yaxis_title="인구 수",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# 남녀 구분 모드
elif mode == "남녀 구분" and gender_file:
    df_gender = pd.read_csv(gender_file, encoding='cp949')
    ages_m, pops_m = get_age_and_pop(df_gender, "남_")
    ages_f, pops_f = get_age_and_pop(df_gender, "여_")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=ages_m, y=pops_m, name="남성", marker_color='blue'))
    fig.add_trace(go.Bar(x=ages_f, y=pops_f, name="여성", marker_color='pink'))
    fig.update_layout(
        barmode="group",
        title="서울특별시 연령별 남녀 인구 비교",
        xaxis_title="나이",
        yaxis_title="인구 수",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# 안내
elif not total_file or not gender_file:
    st.info("좌측에서 두 개의 CSV 파일을 업로드하고 모드를 선택하세요.")
