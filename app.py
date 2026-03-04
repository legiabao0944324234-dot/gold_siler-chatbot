import streamlit as st
import pandas as pd
from groq import Groq

# Đọc file CSV
df = pd.read_csv("silver_demo.csv")

# Tóm tắt data — chỉ gửi phần quan trọng
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

# Kết nối Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Giao diện
st.title("📊 Chatbot Dự báo Giá Bạc")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiện lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Ô nhập câu hỏi
user_input = st.chat_input("Hỏi về giá bạc...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gửi cho Groq
    response = client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""Bạn là chuyên gia phân tích giá bạc.
Dưới đây là dữ liệu nghiên cứu:
{summary}
Trả lời bằng tiếng Việt, ngắn gọn và rõ ràng."""
            },
            *[{"role": m["role"], "content": m["content"]}
              for m in st.session_state.messages]
        ]
    )

    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
