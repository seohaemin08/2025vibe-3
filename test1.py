import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="가위바위보 게임", page_icon="✊")

st.title("✊ ✋ ✌ 가위바위보 게임")

# 세션 상태에 점수 저장
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "rounds" not in st.session_state:
    st.session_state.rounds = 0

# 선택 버튼
st.subheader("무엇을 낼까요?")
cols = st.columns(3)
user_choice = None

with cols[0]:
    if st.button("✌ 가위"):
        user_choice = "가위"
with cols[1]:
    if st.button("✊ 바위"):
        user_choice = "바위"
with cols[2]:
    if st.button("✋ 보"):
        user_choice = "보"

# 컴퓨터 선택
rps_list = ["가위", "바위", "보"]
computer_choice = random.choice(rps_list)

# 결과 계산 함수
def get_result(user, computer):
    if user == computer:
        return "비겼습니다!"
    elif (user == "가위" and computer == "보") or \
         (user == "바위" and computer == "가위") or \
         (user == "보" and computer == "바위"):
        return "🎉 당신이 이겼습니다!"
    else:
        return "😢 당신이 졌습니다..."

# 결과 처리
if user_choice:
    st.markdown("---")
    st.subheader("결과")
    st.write(f"**당신:** {user_choice}")
    st.write(f"**컴퓨터:** {computer_choice}")

    result = get_result(user_choice, computer_choice)
    st.success(result)

    # 점수 반영
    if "이겼습니다" in result:
        st.session_state.user_score += 1
    elif "졌습니다" in result:
        st.session_state.computer_score += 1

    st.session_state.rounds += 1

    # 점수판 출력
    st.markdown("---")
    st.subheader("📊 점수판")
    col_score1, col_score2 = st.columns(2)
    with col_score1:
        st.metric(label="당신의 점수", value=st.session_state.user_score)
    with col_score2:
        st.metric(label="컴퓨터 점수", value=st.session_state.computer_score)

    st.write(f"총 라운드 수: **{st.session_state.rounds}**")

# 초기화 버튼
if st.button("🔄 점수 초기화"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.rounds = 0
    st.success("점수가 초기화되었습니다.")
