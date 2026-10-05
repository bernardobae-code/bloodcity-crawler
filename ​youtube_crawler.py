from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

TARGET_DATE = datetime(2026, 9, 11)
EXCLUDE_WORDS = ["사파리", "주키퍼", "동물원", "판다"]

def parse_yt_date(date_str):
    now = datetime(2026, 10, 5)
    text = date_str.replace('수정됨', '').strip()
    if any(k in text for k in ['시간', '분', '초', '방금']): return now
    if '일 전' in text: return now - timedelta(days=int(''.join(filter(str.isdigit, text))))
    if '주 전' in text: return now - timedelta(weeks=int(''.join(filter(str.isdigit, text))))
    if '개월 전' in text: return now - timedelta(days=int(''.join(filter(str.isdigit, text))) * 30)
    if '년 전' in text: return now - timedelta(days=int(''.join(filter(str.isdigit, text))) * 365)
    return now

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("유튜브_영상_URL_입력")
time.sleep(3)

# 스크롤 10회 내리기 (댓글 로딩)
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)

comments = driver.find_elements(By.CSS_SELECTOR, "#content-text")
dates = driver.find_elements(By.CSS_SELECTOR, "#published-time-text")

for d, c in zip(dates, comments):
    parsed_date = parse_yt_date(d.text)
    text = c.text
    if parsed_date >= TARGET_DATE and not any(w in text for w in EXCLUDE_WORDS):
        print(f"[{parsed_date.strftime('%Y-%m-%d')}] {text}")

driver.quit()
