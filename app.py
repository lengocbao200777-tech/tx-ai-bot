import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="V5 T/X AI Simulator", layout="centered")

st.title("🎲 V5 T/X AI Simulator")
st.caption("Mô phỏng Tài/Xỉu + thống kê + quản lý vốn (KHÔNG dự đoán thật)")

# ===== SETTINGS =====
st.sidebar.header("⚙️ Cài đặt")

rounds = st.sidebar.slider("Số ván mô phỏng", 10, 10000, 500)
start_balance = st.sidebar.number_input("Vốn ban đầu", value=1000)
bet_size = st.sidebar.slider("Mức cược mỗi ván (%)", 1, 50, 10)

mode = st.sidebar.selectbox("Chiến thuật", [
    "Random (AI baseline)",
    "Trend follow (giả lập)",
    "Anti-streak (chống chuỗi dài)"
])

# ===== SIMULATION =====
def roll_tx():
    return random.choice(["Tài", "Xỉu"])

balance = start_balance
history = []
streak = 0
last = None

for i in range(rounds):
    result = roll_tx()

    # AI "logic giả lập"
    if mode == "Random (AI baseline)":
        guess = random.choice(["Tài", "Xỉu"])

    elif mode == "Trend follow (giả lập)":
        guess = last if last else random.choice(["Tài", "Xỉu"])

    elif mode == "Anti-streak (chống chuỗi dài)":
        guess = "Xỉu" if streak >= 3 and last == "Tài" else "Tài" if streak >= 3 else random.choice(["Tài", "Xỉu"])

    bet = balance * (bet_size / 100)

    win = (guess == result)

    if win:
        balance += bet
    else:
        balance -= bet

    # streak tracking
    if result == last:
        streak += 1
    else:
        streak = 1

    last = result

    history.append({
        "Ván": i+1,
        "Dự đoán": guess,
        "Kết quả": result,
        "Thắng": win,
        "Số dư": balance
    })

df = pd.DataFrame(history)

# ===== RESULTS =====
st.subheader("📊 Kết quả mô phỏng")

st.write(f"💰 Số dư cuối: **{round(balance,2)}**")
st.write(f"📈 Lợi nhuận: **{round(balance - start_balance,2)}**")

st.line_chart(df["Số dư"])

st.subheader("📋 Log ván gần nhất")
st.dataframe(df.tail(20))

# ===== STATISTICS =====
st.subheader("📊 Thống kê")

win_rate = df["Thắng"].mean() * 100
st.write(f"🎯 Winrate: **{round(win_rate,2)}%**")

tai_count = df[df["Kết quả"] == "Tài"].shape[0]
xiu_count = df[df["Kết quả"] == "Xỉu"].shape[0]

st.write(f"📊 Tài: {tai_count} | Xỉu: {xiu_count}")

st.caption("⚠️ Đây chỉ là mô phỏng xác suất. Không có AI nào dự đoán T/X chính xác 100%.")
