from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

TARGET_DATE = datetime(2026, 9, 11)
EXCLUDE_WORDS = ["사파리", "주키퍼", "동물원", "판다"]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.instagram.com/")
time.sleep(3)

# 인스타그램 로그인
driver.find_element(By.NAME, "username").send_keys("본인_인스타_아이디")
driver.find_element(By.NAME, "password").send_keys("본인_인스타_비밀번호")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(5)

# 해시태그 검색 결과 페이지 이동
driver.get("https://www.instagram.com/explore/tags/블러드시티제로/")
time.sleep(5)

# 첫 번째 게시글 클릭
posts = driver.find_elements(By.CSS_SELECTOR, "div._aagw")
if posts:
    posts[0].click()
    time.sleep(3)

    # 본문 텍스트 추출 및 필터링
    text_elements = driver.find_elements(By.CSS_SELECTOR, "span._aaco")
    if text_elements:
        text = text_elements[0].text
        if not any(w in text for w in EXCLUDE_WORDS):
            print("게시글 내용:", text)

driver.quit()
