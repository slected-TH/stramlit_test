from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

# 다나와 사이트 검색
options=Options()
options.add_argument('headless') # headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드

# webdirver 설정(Chrome, Firefox 등)
driver=webdriver.Chrome(options=options) # 브라우저 창 안보이기
# driver=webdriver.Chrome() # 브라우저 창 보이기

# 크롬 브라우저 내부 대기 (암묵적 대기)
driver.implicitly_wait(5)

# 브라우저 사이즈
# driver.set_window_size(1920,1280)

# 페이지 이동(열고 싶은 URL)
url = "http://www.danawa.com"
driver.get(url)
elem = driver.find_element(By.ID, "AKCSearch")
elem.send_keys('세탁기')
elem.send_keys(Keys.RETURN)

# 검색 결과가 렌더링 될 때까지 잠시 대기
time.sleep(2)

# 크롤링할 전체 페이지수
totalPage = 2

prod_data_total = []
for i in range(1,totalPage+1):

    # 페이지 내용
    print(f'{i} Page Crawling >>>>>>>>>>> ')
    
    # 페이지 이동
    driver.find_element(By.LINK_TEXT,str(i)).click()
    time.sleep(2)
    # break
    #bs4 초기화
    soup=BeautifulSoup(driver.page_source,'html.parser')
    # 상품 리스트 선택
    goods_list=soup.select('li.prod_item>div.prod_main_info')
    prod_data = []
    for v in goods_list:
        try:
            # 상품 모델명, 가격, 이미지
            name=v.select_one('p.prod_name>a').text.strip()
            spec_list = v.select_one('div.spec_list').text.replace('\t','').replace('\n','')
            price=v.select_one('p.price_sect>a').text.strip().replace(",","").replace("원","")
            # img_link=v.select_one('div.thumb_image>a>img').get('src')
            img_link=v.select_one('div.thumb_image>a>img')['src']

            # print(name,spec_list, price,img_link)
            prod_data.append([name,spec_list,price,'http:'+img_link])
        except:
            pass

    prod_data_total = prod_data_total + prod_data
    time.sleep(2)
    
    # BeautifulSoup 인스턴스 삭제
    del soup

    # 3초간 대기
    time.sleep(3)

# 데이터 저장
data = pd.DataFrame(prod_data_total)
data.columns = ['상품명', '스펙 목록', '가격','링크주소']
data.to_excel('3_danawa_crawling_result.xlsx', index = False)
print('Crawling succeed!')
driver.close()
