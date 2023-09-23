import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않음

# ChromeDriver 실행
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

# 웹 페이지 로드
url = "https://www.bandtrass.or.kr/customs/total.do?command=CUS001View&viewCode=CUS00101"
driver.get(url)

# 웹 페이지 로딩을 위한 대기 시간 설정 (최대 대기 시간: 10초)
wait = WebDriverWait(driver, 10)

# tr 태그의 id가 1인 요소가 나타날 때까지 대기
loading_tag = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, 'tr[role="row"][id="1"]')))

# 대기가 완료되면 해당 tr 태그를 가져오기
table = driver.find_element(By.CSS_SELECTOR, 'table[id="table_list_1"]')

# tr 태그의 내용 출력
table_data = table.get_attribute('outerHTML')
# content = table.get_attribute("innerHTML")
print(table_data)


# 데이터 가공
soup = BeautifulSoup(table_data, 'html.parser')

# 테이블 데이터 추출
table = soup.find('tbody')
rows = table.find_all('tr')

# 데이터 가공을 위한 리스트 초기화
data = []

# 각 행에서 데이터 추출
for row in rows:
    # 행의 모든 셀을 선택
    cells = row.find_all('td')

    # 셀 데이터 추출
    year = cells[0].text.strip().replace('년', '')
    month = cells[0].find_next('td').text.strip().replace('월', '')
    ex_val = cells[1].text.strip().replace(',', '')
    ex_incre_ratio = cells[2].text.strip()
    mon_ex_incre_ratio = cells[3].text.strip()
    im_val = cells[4].text.strip().replace(',', '')
    im_incre_ratio = cells[5].text.strip()
    mon_im_incre_ratio = cells[6].text.strip()
    trade_val = cells[7].text.strip().replace(',', '')

    # 추출한 데이터를 리스트에 추가
    data.append([year, month, ex_val, ex_incre_ratio, mon_ex_incre_ratio,
                im_val, im_incre_ratio, mon_im_incre_ratio, trade_val])

# 데이터프레임 생성
df = pd.DataFrame(data, columns=['Year', 'Month', 'Export Value', 'Export Increase Ratio',
                                 'Monthly Export Increase Ratio', 'Import Value', 'Import Increase Ratio',
                                 'Monthly Import Increase Ratio', 'Trade Value'])

# 데이터프레임을 엑셀 파일로 저장
df.to_excel('test.xlsx', index=False)
# 결과를 파일로 저장
with open("test.html", "w", encoding="utf-8") as file:
    file.write(str(table_data))

# WebDriver 종료
driver.quit()

# 생성된 엑셀 파일 출력
df = pd.read_excel('test.xlsx')
print(df)
