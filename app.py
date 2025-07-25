import streamlit as st
import pandas as pd

st.title("📍 나만의 위치 북마크 지도")

# 세션 상태에 장소 목록이 없으면 초기화
if "places" not in st.session_state:
    st.session_state.places = []

# 사이드바에서 장소 입력
with st.sidebar:
    st.header("🔖 장소 추가하기")
    name = st.text_input("장소 이름")
    lat = st.number_input("위도 (예: 37.5665)", format="%.6f")
    lon = st.number_input("경도 (예: 126.9780)", format="%.6f")
    add_button = st.button("장소 추가")

    if add_button:
        if name and lat and lon:
            st.session_state.places.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })
            st.success(f"✅ '{name}' 북마크 완료!")
        else:
            st.warning("⚠️ 모든 값을 입력해 주세요.")

# 북마크가 있을 경우 지도와 목록 표시
if st.session_state.places:
    df = pd.DataFrame(st.session_state.places)

    st.subheader("🗺️ 북마크 지도")
    st.map(df[["lat", "lon"]])  # Streamlit 내장 지도

    st.subheader("📋 북마크 목록")
    st.dataframe(df[["name", "lat", "lon"]])

    # CSV 다운로드 기능
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 CSV로 저장", csv, "bookmarks.csv", "text/csv")
else:
    st.info("아직 북마크한 장소가 없어요. 사이드바에서 추가해보세요!")

