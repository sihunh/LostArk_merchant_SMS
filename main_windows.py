# main.py

import json
import time
import schedule
from SolapiAlarmService import SolapiAlarmService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# SolapiAlarmService 초기화
api_key = 'your_api_key'
api_secret = 'your_api_secret'
sender_phone = 'your_sender_phone'
recipient_phone = 'recipient_phone'

solapi_service = SolapiAlarmService(api_key, api_secret, sender_phone)

# 관심 있는 키워드 리스트
keywords = ['바훈투르 카드', '아제나&이난나 카드', '카마인 카드', '웨이 카드', '데런 아만 카드']

def check_website():
    options = Options()
    options.add_argument("--headless")  # 헤드리스 모드 실행
    options.add_argument('--log-level=3') 
    options.add_argument('--disable-loging') 
    options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://kloa.gg/merchant")
        
        # 모든 카단 섹션이 로드될 때까지 기다립니다.
        try:
            kadan_sections = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[text()='카단']"))
            )
        except TimeoutException:
            print("카단 섹션을 찾는 데 시간이 초과되었습니다.")
            return
        
        message_parts = []
        
        for index, kadan_section in enumerate(kadan_sections):
            # 각 카단 섹션의 부모 요소를 찾아 그 아래의 모든 정보를 가져옵니다.
            parent_section = kadan_section.find_element(By.XPATH, "..")
            
            # 카단 섹션 아래의 모든 정보를 가져옵니다.
            info_elements = parent_section.find_elements(By.XPATH, ".//following-sibling::div")
            
            # 정보 수집
            section_info = [info.text.strip() for info in info_elements]
            first_value = section_info[0] if section_info else ""
            
            # 키워드가 포함된 경우 해당 정보를 메시지에 추가
            for keyword in keywords:
                if keyword in " ".join(section_info):
                    message_part = f"카단 섹션 {index + 1} - 위치: {first_value}"
                    # 메시지를 \n으로 나누고 첫 번째 줄만 가져오기
                    message_lines = message_part.split("\n")
                    if message_lines:
                        first_line = message_lines[0] + f" \n키워드: {keyword}"
                        message_parts.append(first_line)
                        print(first_line)  # 찾은 정보의 첫 번째 줄 출력
                    break
        
        if message_parts:
            # 메시지를 합쳐서 SMS 전송
            message = "\n".join(message_parts)
            send_sms(f"{message}")
        else:
            print("관심 있는 카단 정보가 발견되지 않았습니다.")
    
    finally:
        driver.quit()
    
    print("\n" + "-"*50 + "\n")  # 구분선 출력

def send_sms(message):
    data = {
        'messages': [
            {
                'type': 'SMS',
                'to': recipient_phone,
                'from': sender_phone,
                'text': message
            }
        ]
    }
    res = solapi_service.send_many(data)
    print("SMS 전송 결과:")
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))

def job():
    print("웹사이트 확인 중...")
    check_website()

# 매 시간마다 job 함수를 실행합니다.
schedule.every().hour.do(job)
if __name__ == '__main__':
    print("프로그램 시작")
    while True:
        schedule.run_pending()
        time.sleep(1)
