#include <Servo.h>

// Khai báo chân kết nối (tối ưu bằng byte)
const byte mq5Pin      = A0;  // Cảm biến MQ5 nối vào A0
const byte relay1Pin   = 7;   // Relay 1 (ví dụ: quạt)
const byte relay2Pin   = 8;   // Relay 2 (ví dụ: đèn, van điện)
const byte buzzerPin   = 9;   // Còi báo động
const byte servo1Pin   = 5;   // Servo điều khiển 1
const byte servo2Pin   = 6;   // Servo điều khiển 2

// Giá trị ngưỡng phát hiện gas (có thể điều chỉnh sau khi hiệu chuẩn)
uint16_t gasThreshold  = 300;

// Giá trị đọc từ MQ5
uint16_t gasValue = 0;

// Tạo đối tượng servo
Servo servo1;
Servo servo2;

void setup() {
  // Khởi tạo Serial để kiểm tra giá trị MQ5
  Serial.begin(9600);

  // Cấu hình các chân xuất
  pinMode(relay1Pin, OUTPUT);
  pinMode(relay2Pin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  // Tắt thiết bị ban đầu
  digitalWrite(relay1Pin, LOW);
  digitalWrite(relay2Pin, LOW);
  digitalWrite(buzzerPin, LOW);

  // Gắn servo vào chân điều khiển
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);

  // Đặt servo về vị trí ban đầu
  servo1.write(0);
  servo2.write(0);
}

void loop() {
  // Đọc giá trị khí gas từ MQ5
  gasValue = analogRead(mq5Pin);
  Serial.print(F("MQ5 Gas Value: "));
  Serial.println(gasValue);

  // Nếu phát hiện khí gas vượt ngưỡng
  if (gasValue > gasThreshold) {
    // Bật thiết bị cảnh báo
    digitalWrite(relay1Pin, HIGH);  // Bật quạt
    digitalWrite(relay2Pin, HIGH);  // Bật thiết bị khác
    digitalWrite(buzzerPin, HIGH);  // Bật còi

    // Xoay servo để đóng/mở van hoặc cửa
    servo1.write(90);
    servo2.write(90);
  } else {
    // Không phát hiện khí gas – trở về trạng thái an toàn
    digitalWrite(relay1Pin, LOW);
    digitalWrite(relay2Pin, LOW);
    digitalWrite(buzzerPin, LOW);

    // Trả servo về vị trí ban đầu
    servo1.write(0);
    servo2.write(0);
  }

  delay(500); // Đợi 0.5 giây trước lần kiểm tra tiếp theo
}

