from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# 네이버 지도 크롤링 코드
def naver_map_crawler(search_query):
    options = set_chrome_options()
    driver = set_chromedriver(options)
    stores = []

    print("naver_map_crawler시작")
    time.sleep(3)
    search(search_query, driver)
    time.sleep(5)
    try:
        for _ in range(5):
            time.sleep(2)
            # store_elements = driver.find_elements(By.CLASS_NAME, "place_bluelink")  # 점포 정보 관련 태그
            store_elements = driver.find_elements(By.CLASS_NAME, "input_search")  # 점포 정보 관련 태그
            print("store_element : ", store_elements)
            for store in store_elements:
                print("store : ", store)
                extract_store_info(store, driver, stores)
            move_next_page(driver)
    except Exception as e:
        print("Crawling error:", e)
    driver.quit()
    create_excel_output(stores)

    return f"총 {len(stores)}개의 데이터를 저장했습니다."


def set_chrome_options():
    """ 크롬 옵션 설정 """
    options = Options()
    options.add_argument('--headless')  # GUI 없이 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    return options


def set_chromedriver(options):
    """ 크롬 드라이버 실행 (Service 객체 활용) """
    chrome_driver_path = r"C:\git\web-scrapping\chrome-driver\win\chromedriver.exe"  # 절대 경로 사용 추천
    service = Service(chrome_driver_path)  # Service 객체 생성
    driver = webdriver.Chrome(service=service, options=options)  # Service 방식 적용
    driver.get("https://map.naver.com/v5/")

    return driver


def search(search_query, driver):
    """ 네이버 지도에서 검색 """
    print("🔎 search() 시작")
    try:
        # ✅ 검색창을 더 정확하게 찾기 위해 CSS 선택자 사용
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.input_search"))
        )
        print("✅ 검색창 로딩 완료!")

        search_box.clear()  # ✅ 기존 검색어 제거
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)
        print(f"🔍 검색어 입력 및 실행: {search_query}")

        # ✅ 검색 결과가 로딩될 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "place_bluelink"))
        )
        print("✅ 검색 완료!")

    except Exception as e:
        print("🚨 Search error:", e)
        print("📌 현재 HTML 내용 일부 출력 (디버깅)")
        print(driver.page_source[:1000])  # HTML 일부 출력하여 현재 페이지 확인




def create_excel_output(stores):
    print("create_excel_output(stores) 시작")
    """ 크롤링된 데이터를 엑셀 파일로 저장 """
    df = pd.DataFrame(stores)
    df.to_excel("./output/results.xlsx", index=False)


def extract_store_info(store, driver, stores):
    """ 점포 상세 정보 추출 """
    print("extract_store_info(store, driver, stores) 시작")
    try:
        name = store.text
        store.click()
        time.sleep(2)

        # ✅ 최신 CSS 선택자 확인 후 적용 (개발자 도구 사용)
        address_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LDg9ec2p"))
        )
        phone_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "xlx7q65"))
        )
        print("address_elem", address_elem)
        print("phone_elem", phone_elem)

        address = address_elem.text if address_elem else "주소 없음"
        phone = phone_elem.text if phone_elem else "전화번호 없음"

        print(f"Store name: {name}")  # ✅ 크롤링 데이터 확인
        print(f"Address: {address}")
        print(f"Phone: {phone}")

        stores.append({
            "상호명": name,
            "주소": address,
            "전화번호": phone
        })
        print("extracted stores info", stores);

        driver.back()
        time.sleep(3)  # ✅ 기존 1초 → 3초로 증가

    except Exception as e:
        print("Error while extracting store info:", e)




def move_next_page(driver):
    """ 다음 페이지로 이동 """
    print("move_next_page() 시작")

    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fvwqf"))
        )
        print("next_button", next_button)
        next_button.click()
    except Exception as e:
        print("No more pages available or error:", e)
