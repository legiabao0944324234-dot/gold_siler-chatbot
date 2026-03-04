import streamlit as st
import pandas as pd
#import google.generativeai as genai
from groq import 

# Đọc file CSV
df = pd.read_csv("silver_demo.csv")

# Tóm tắt data — chỉ gửi phần quan trọng cho Gemini
summary = f"""
Dữ liệu giá bạc (XAG/USD) gồm {len(df)} phiên giao dịch.
Thời gian: {df['Date'].iloc[0]} đến {df['Date'].iloc[-1]}

Thống kê:
- Giá cao nhất : {df['High'].max():.2f} USD
- Giá thấp nhất: {df['Low'].min():.2f} USD
- Giá TB đóng cửa: {df['Close'].mean():.2f} USD
- Giá đóng cửa gần nhất: {df['Close'].iloc[-1]:.2f} USD

10 phiên gần nhất:
{df.tail(10).to_string(index=False)}
"""

# Lấy API key từ Streamlit Secrets (an toàn hơn hardcode)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
# Giao diện
st.title("📊 Chatbot Dự báo Giá Bạc")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Hỏi về giá bạc...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = f"""Bạn là chuyên gia phân tích giá bạc.
Dưới đây là dữ liệu nghiên cứu:

{summary}

Câu hỏi: {user_input}

Trả lời bằng tiếng Việt, ngắn gọn và rõ ràng."""

    response = model.generate_content(prompt)
    answer = response.text

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
