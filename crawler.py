from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 네이버 지도 크롤링 코드
def naver_map_crawler(search_query):
    # 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 드라이버 설정??? 근데 좀 이상함
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    driver.get("https://map.naver.com/v5/")

    time.sleep(3)

    # 검색창 이동 및 검색어 입력
    search_box = driver.find_element(By.CLASS_NAME, "input_search")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)

    time.sleep(5)

    stores = []
    try:
        for _ in range(5):
            time.sleep(2)
            store_elements = driver.find_elements(By.CLASS_NAME, "place_bluelink")

            for store in store_elements:
                try:
                    name = store.text
                    store.click()
                    time.sleep(2)

                    # 상세 정보 가져오기
                    address = driver.find_element(By.CLASS_NAME, "ldg9ec2p").text
                    phone = driver.find_element(By.CLASS_NAME, "xlx7q65").text

                    stores.append({
                        "상호명" : name,
                        "주소" : address,
                        "전화번호" : phone
                    })

                    driver.back()
                    time.sleep(1)
                except Exception as e:
                    print("Error while extraction store info:", e)
            next_button = driver.find_element(By.CLASS_NAME, "fvwqf")
            next_button.click()
    except Exception as e:
        print("Crawling error: ", e)

    driver.quit()

    df = pd.DataFrame(stores)
    df.to_excel("./output/results.xlsx", index=False)

    return f"총 {len(stores)}개의 데이터를 저장했습니다."



