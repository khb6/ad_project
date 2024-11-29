import serial
import time
import requests
# Webhook URL 설정
WEBHOOK_URL = "https://hooks.slack.com/services/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"
# 아두이노와 연결된 시리얼 포트 설정
ser = serial.Serial('COM10', 9600, timeout=1)
# 마지막 알림을 보낸 시간 (5분마다 알림을 보낼 때 사용)
last_alert_time = 0
alert_interval = 10  # 5분 (300초)
def send_slack_message(message):
    """Slack으로 메시지를 보내는 함수"""
    payload = {
        "text": message  # Slack으로 보낼 메시지
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()  # 요청이 성공적으로 보내졌는지 확인
        print(f"Message sent to Slack: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Slack: {e}")
def read_temperature_and_humidity():
    """아두이노로부터 온도와 습도를 읽어 조건에 맞으면 Slack 메시지 전송"""
    global last_alert_time  # 마지막 알림 시간 업데이트
    temperature = None  # 초기화
    humidity = None      # 초기화
    while True:
        # 시리얼로부터 한 줄씩 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        if "TEMPERATURE=" in line:
            try:
                # 온도 값 추출
                temperature = int(line.split("=")[1])
                print(f"Temperature: {temperature} °C")
                # 온도가 특정 값 이상이면 알림
                if temperature < 20:
                    send_slack_message(f"Warning! Low Temperature: {temperature}°C. 난방기구 작동을 추천 드립니다.")
                elif 20 <= temperature <= 25:
                    send_slack_message(f"Current Temperature: {temperature}°C. 현재 실내 온도가 적당합니다.")
                elif temperature > 30:
                    send_slack_message(f"Warning! High Temperature: {temperature}°C. 에어컨 작동을 추천 드립니다.")
            except ValueError:
                pass
        elif "HUMIDITY=" in line:
            try:
                # 습도 값 추출
                humidity = int(line.split("=")[1])
                print(f"Humidity: {humidity} %")
                # 습도가 특정 값 이상이면 알림
                if humidity < 40:
                    send_slack_message(f"Warning! Low Humidity: {humidity}%. 가습기 작동을 추천 드립니다.")
                elif 40 <= humidity <= 60:
                    send_slack_message(f"Current Humidity: {humidity}%. 습도가 적당합니다.")
                elif humidity > 70:
                    send_slack_message(f"Warning! High Humidity: {humidity}%. 제습기 작동을 추천 드립니다.")
            except ValueError:
                pass
        # 5분마다 적정 온도 및 습도 상태를 체크
        if temperature is not None and humidity is not None:  # 온도와 습도가 유효할 때만 체크
            current_time = time.time()
            if current_time - last_alert_time >= alert_interval:
                last_alert_time = current_time  # 마지막 알림 시간 갱신
                # 적정 온도 및 습도 범위 확인 후 알림 보내기
                if temperature < 20 or temperature > 30:
                    send_slack_message(f"Reminder: Temperature is still out of range. Current temperature: {temperature}°C.")
                if humidity < 40 or humidity > 70:
                    send_slack_message(f"Reminder: Humidity is still out of range. Current humidity: {humidity}%.")
        time.sleep(1)  # 1초마다 데이터를 읽고 처리
if __name__ == "__main__":
    print("Starting temperature and humidity monitoring...")
    read_temperature_and_humidity()