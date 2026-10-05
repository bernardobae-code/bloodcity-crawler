import time
import pyperclip
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

TARGET_DATE = datetime(2026, 9, 11)
EXCLUDE_WORDS = ["사파리", "주키퍼", "동물원", "판다"]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 네이버 우회 로그인
driver.get("https://nid.naver.com/nidlogin.login")
time.sleep(2)

pyperclip.copy("jwbae1020")
driver.find_element(By.ID, "id").click()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
time.sleep(1)

pyperclip.copy(" dpqpfosem *9")
driver.find_element(By.ID, "pw").click()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
time.sleep(1)

driver.find_element(By.ID, "log.login").click()
time.sleep(3)

# 카페 게시판 이동
driver.get("수집할_네이버_카페_게시판_URL")
time.sleep(3)

# 네이버 카페는 iframe 구조이므로 내부로 포커스 전환 필수
driver.switch_to.frame("cafe_main")

articles = driver.find_elements(By.CSS_SELECTOR, "div.article-board td.td_article")
dates = driver.find_elements(By.CSS_SELECTOR, "div.article-board td.td_date")

for article, d in zip(articles, dates):
    title = article.text
    # 2026.09.12 형식 날짜 파싱
    try:
        post_date = datetime.strptime(d.text.strip(), "%Y.%m.%d.")
        if post_date >= TARGET_DATE and not any(w in title for w in EXCLUDE_WORDS):
            print(f"[{post_date.strftime('%Y-%m-%d')}] {title}")
    except:
        continue

driver.quit()
