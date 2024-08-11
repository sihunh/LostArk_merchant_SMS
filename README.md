# LostArk_Merchant_SMS

이 프로젝트는 Kloa.gg 웹사이트에서 특정 키워드에 해당하는 카단 서버에 대한 정보를 주기적으로 확인하고, 관심 있는 정보가 발견되면 SMS로 알림을 보내는 자동화 서비스입니다.

## 기능

- Kloa.gg 웹사이트의 카단 정보를 주기적으로 스크래핑
- 설정된 키워드에 해당하는 정보 감지
- 관심 정보 발견 시 SMS 알림 전송

## 필요 조건

- Python 3.6+
- Chrome 브라우저
- ChromeDriver (자동으로 설치됨)

## 설치

1. 필요한 라이브러리 설치:

```bash
pip install selenium webdriver_manager schedule requests
```

1. 프로젝트 클론:

```bash
git clone https://github.com/sihunh/LostArk_merchant_SMS.git
```

## 설정

1. `main.py` 파일에서 다음 변수들을 설정하세요:

```python
api_key = 'your_api_key'
api_secret = 'your_api_secret'
sender_phone = 'your_sender_phone'
recipient_phone = 'recipient_phone'
```

1. Chrome 브라우저 경로 설정 (필요한 경우):

```python
options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
```

1. 관심 키워드 설정:

```python
keywords = ['바훈투르 카드', '아제나&이난나 카드', '카마인 카드', '웨이 카드', '데런 아만 카드']

```

## 사용 방법

다음 명령어로 프로그램을 실행하세요:

```bash
python main_windows.py
```

프로그램은 매 시간마다 Kloa.gg 웹사이트를 확인하고, 설정된 키워드에 해당하는 정보가 발견되면 SMS로 알림을 보냅니다.

## 주요 구성 요소

### SolapiAlarmServic

SMS 전송을 위한 Solapi API 래퍼 클래스입니다. 자세한 내용은 [SolapiAlarmService 문서](https://github.com/solapi/solapi-python)를 참조하세요.

### 웹 스크래핑

Selenium을 사용하여 Kloa.gg 웹사이트의 카단 정보를 스크래핑합니다.

### 스케줄링

`schedule` 라이브러리를 사용하여 매 시간마다 웹사이트 확인 작업을 스케줄링합니다.

## 주의사항

- 이 프로그램은 개인 용도로 제작되었습니다. 웹사이트의 이용 약관을 준수하세요.
- API 키와 전화번호 등의 민감한 정보는 안전하게 관리하세요.
- 과도한 요청으로 서버에 부담을 주지 않도록 주의하세요.

## 기여

버그 리포트나 기능 개선 제안은 이슈를 통해 제출해 주세요.
