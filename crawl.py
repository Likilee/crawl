import time
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup

# SSL 인증서 검증을 비활성화한 컨텍스트 생성
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

url = "https://www.bandtrass.or.kr/customs/total.do?command=CUS001View&viewCode=CUS00101"
html = urlopen(url, context=context) 

bsObject = BeautifulSoup(html, "html.parser") 

# tr 중 id가 1인 태그가 로딩될 때까지 기다리기
loading_tag = bsObject.find("table", {"id": "table_list_1"})
while loading_tag is None:
    time.sleep(1)
    bsObject = BeautifulSoup(html, "html.parser") 
    loading_tag = bsObject.find("table", {"id": "table_list_1"})
    print("로딩중...")

# 결과를 파일로 저장
with open("test.html", "w", encoding="utf-8") as file:
        file.write(str(loading_tag))
