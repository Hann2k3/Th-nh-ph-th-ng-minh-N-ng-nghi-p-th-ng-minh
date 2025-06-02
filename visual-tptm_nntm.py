import smtplib
import ssl
import random
import time
import matplotlib.pyplot as plt
from email.message import EmailMessage

# === Cấu hình gửi email ===
EMAIL_SENDER = 'htn20092003@gmail.com'
EMAIL_PASSWORD = 'ghle pyqr dvig jzvm'  # App Password từ Gmail
EMAIL_RECEIVER = 'htn20092003@gmail.com'

# === Cấu hình hệ thống ===
GAS_THRESHOLD = 2000         # Ngưỡng cảnh báo
EMAIL_ALERT_COOLDOWN = 30    # Thời gian giữa 2 lần gửi cảnh báo (giây)

# ✅ Hàm gửi email cảnh báo
def send_gas_alert_email(smoke_value):
    subject = "🔥 CẢNH BÁO RÒ RỈ KHÍ GAS!"
    body = f"⚠️ Phát hiện rò rỉ khí gas vượt ngưỡng ({smoke_value})! Hãy kiểm tra ngay!"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("📧 Email cảnh báo đã được gửi.")
    except Exception as e:
        print("Lỗi khi gửi email:", e)

# Mô phỏng cảm biến khí gas
def simulate_gas_sensor():
    return random.randint(1000, 2500)

# Mô phỏng giám sát và cảnh báo khí gas
def main():
    gas_data = []
    times = []
    last_alert_time = 0  # ✅ thời điểm gửi email gần nhất

    print("=== Bắt đầu mô phỏng giám sát khí gas ===")

    for i in range(60):  # Mô phỏng 60 giây
        smoke = simulate_gas_sensor()
        print(f"[{i+1:02d}s] Mức khí gas: {smoke}")

        gas_data.append(smoke)
        times.append(i)

        current_time = time.time()
        if smoke > GAS_THRESHOLD:
            # ✅ Chỉ gửi email nếu đã qua thời gian cooldown
            if current_time - last_alert_time > EMAIL_ALERT_COOLDOWN:
                send_gas_alert_email(smoke)
                last_alert_time = current_time

        time.sleep(1)

    # Vẽ biểu đồ
    plt.plot(times, gas_data, label='Mức khí gas')
    plt.axhline(y=GAS_THRESHOLD, color='r', linestyle='--', label='Ngưỡng cảnh báo')
    plt.xlabel('Thời gian (s)')
    plt.ylabel('Giá trị khí gas')
    plt.title('Giám sát rò rỉ khí gas (Mô phỏng)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()



