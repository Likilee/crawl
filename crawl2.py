from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver 경로 설정
webdriver_service = Service('/path/to/chromedriver')

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않음

# ChromeDriver 실행
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# 웹 페이지 로드
url = "https://www.bandtrass.or.kr/customs/total.do?command=CUS001View&viewCode=CUS00101"
driver.get(url)

# 웹 페이지 로딩을 위한 대기 시간 설정 (최대 대기 시간: 10초)
wait = WebDriverWait(driver, 10)

# tr 태그의 id가 1인 요소가 나타날 때까지 대기
loading_tag = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tr[role="row"][id="1"]')))

# 대기가 완료되면 해당 tr 태그를 가져오기
table = driver.find_element(By.CSS_SELECTOR, 'table[id="table_list_1"]')

# tr 태그의 내용 출력
content = table.get_attribute("innerHTML")
print(content)
# 크롤링을 위한 코드 추가 작성
# # ...

# 결과를 파일로 저장
with open("test.html", "w", encoding="utf-8") as file:
    file.write(str(content))

# WebDriver 종료
driver.quit()