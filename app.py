import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 앱 제목
st.title("📍 나만의 위치 북마크 지도")

# 세션 상태 초기화
if "places" not in st.session_state:
    st.session_state.places = []

# 사이드바에 입력 폼
with st.sidebar:
    st.header("🔖 장소 추가하기")
    name = st.text_input("장소 이름")
    lat = st.number_input("위도 (예: 37.5665)", format="%.6f")
    lon = st.number_input("경도 (예: 126.9780)", format="%.6f")
    add_button = st.button("추가하기")

    if add_button:
        if name and lat and lon:
            st.session_state.places.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })
            st.success(f"'{name}' 이(가) 북마크에 추가되었습니다.")
        else:
            st.warning("모든 필드를 입력해주세요.")

# 지도 중심 좌표 설정
map_center = [37.5665, 126.9780]  # 서울 기본

# folium 지도 생성
m = folium.Map(location=map_center, zoom_start=12)

# 저장된 장소를 마커로 표시
for place in st.session_state.places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=place["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st.subheader("🗺️ 북마크 지도")
st_data = st_folium(m, width=700, height=500)

# 장소 목록 보기
if st.session_state.places:
    st.subheader("📋 북마크 리스트")
    df = pd.DataFrame(st.session_state.places)
    st.table(df)

    # 저장 버튼
    csv = pd.DataFrame(st.session_state.places).to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 CSV로 저장하기", csv, file_name="my_bookmarks.csv", mime="text/csv")
