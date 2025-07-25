import streamlit as st
import random
from PIL import Image
import os

# 기본 설정
st.set_page_config(page_title="가위바위보 게임", page_icon="✊")

st.title("✊ ✋ ✌ 가위바위보 게임 - 이미지 버전")

# 이미지 경로
image_dir = "images"
rps_dict = {
    "가위": os.path.join(image_dir, "scissors.png"),
    "바위": os.path.join(image_dir, "rock.png"),
    "보": os.path.join(image_dir, "paper.png"),
}

# 가위바위보 버튼 (이미지로)
col1, col2, col3 = st.columns(3)
user_choice = None

with col1:
    if st.button("✌ 가위"):
        user_choice = "가위"
with col2:
    if st.button("✊ 바위"):
        user_choice = "바위"
with col3:
    if st.button("✋ 보"):
        user_choice = "보"

# 컴퓨터 선택
choices = ["가위", "바위", "보"]
computer_choice = random.choice(choices)

# 결과 계산 함수
def get_result(user, computer):
    if user == computer:
        return "비겼습니다!"
    elif (user == "가위" and computer == "보") or \
         (user == "바위" and computer == "가위") or \
         (user == "보" and computer == "바위"):
        return "당신이 이겼습니다! 🎉"
    else:
        return "당신이 졌습니다... 😢"

# 결과 출력
if user_choice:
    st.subheader("당신의 선택")
    st.image(rps_dict[user_choice], width=150)

    st.subheader("컴퓨터의 선택")
    st.image(rps_dict[computer_choice], width=150)

    st.subheader("게임 결과")
    result = get_result(user_choice, computer_choice)
    st.success(result)
