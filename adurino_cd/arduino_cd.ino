#include <TM1637TinyDisplay.h>
#include "DHT.h"

#define CLK 9
#define DIO 10
#define BUTTON_1 4
#define BUTTON_2 7
#define DHTPIN 2

TM1637TinyDisplay display(CLK, DIO);
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int currentTemperature = 0;
int currentHumidity = 0;
bool showTemperature = true;  // true일 때 온도, false일 때 습도

void setup() {
  Serial.begin(9600);
  display.setBrightness(BRIGHT_7);
  pinMode(BUTTON_1, INPUT);
  pinMode(BUTTON_2, INPUT);
  dht.begin();
}

void loop() {
  if (btn1() == 1) {
    showTemperature = true;  // 버튼 1을 누르면 온도 표시
    sendTemperature();       // 온도 출력
  }

  if (btn2() == 1) {
    showTemperature = false;  // 버튼 2를 누르면 습도 표시
    sendHumidity();           // 습도 출력
  }

  delay(100);  // 버튼 눌림 반응을 위해 약간의 지연 추가
}

int btn1() {
  static int currBtn = 0;
  static int prevBtn = 0;

  currBtn = digitalRead(BUTTON_1);

  if (currBtn != prevBtn) {
    prevBtn = currBtn;
    if (currBtn == 1) {
      return 1;
    }
    delay(50);
  }

  return 0;
}

int btn2() {
  static int currBtn = 0;
  static int prevBtn = 0;

  currBtn = digitalRead(BUTTON_2);

  if (currBtn != prevBtn) {
    prevBtn = currBtn;
    if (currBtn == 1) {
      return 1;
    }
    delay(50);
  }

  return 0;
}

void sendTemperature() {
  float temperature = dht.readTemperature();  // 온도 읽기
  if (!isnan(temperature)) {
    currentTemperature = (int)temperature;
    Serial.print("TEMPERATURE=");
    Serial.println(currentTemperature);

    display.showNumber(currentTemperature);  // FND에 온도 표시
  } else {
    Serial.println("TEMPERATURE=ERROR");
    display.showNumber(-1);  // FND에 오류 표시
  }
}

void sendHumidity() {
  float humidity = dht.readHumidity();  // 습도 읽기
  if (!isnan(humidity)) {
    currentHumidity = (int)humidity;
    Serial.print("HUMIDITY=");
    Serial.println(currentHumidity);

    display.showNumber(currentHumidity);  // FND에 습도 표시
  } else {
    Serial.println("HUMIDITY=ERROR");
    display.showNumber(-1);  // FND에 오류 표시
  }
}
