import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import period_select


def choose_class(driver):
    driver.get("https://www.mvdis.gov.tw/m3-emv-trn/applyCourse")
    driver.find_element(By.LINK_TEXT, "新增預約").click()
    dropdown = driver.find_element(By.ID, "trainingYear")
    dropdown.find_element(By.XPATH, "//option[. = '111']").click()
    dropdown = driver.find_element(By.ID, "dmvId")
    dropdown.find_element(By.XPATH, "//option[. = '公路人員訓練所南部訓練中心']").click()
    driver.find_element(By.LINK_TEXT, "查詢").click()
    row = 1
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({row}) > td:nth-child(3)")
            row += 1
        except NoSuchElementException:
            break
    # print(f"There are {row} rows.")
    for i in range(1, row):
        period = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({i}) > td:nth-child(3)").text
        if period == period_select.period or period == period_select.period_2 or period == period_select.period_3 or period == period_select.period_4:
            print(f"Found period {period_select.period}.")
            try:
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({i}) .std_btn").click()
            except NoSuchElementException:
                print(f"Error, The period {period_select.period} can't be selected.", file=sys.stderr)
                return False
            return True
        else:
            continue

    print(f"Error, can't find period {period_select.period}.", file=sys.stderr)
    return False


def information(driver):
    driver.find_element(By.LINK_TEXT, "我已充分知悉相關約定並願接受").click()
    driver.find_element(By.ID, "idNo").send_keys(period_select.ID)
    driver.find_element(By.ID, "birthdayStr").send_keys(period_select.birth)
    driver.find_element(By.ID, "stuName").send_keys(period_select.name)
    dropdown = driver.find_element(By.NAME, "county")
    dropdown.find_element(By.XPATH, f"//option[. = '{period_select.county}']").click()
    dropdown = driver.find_element(By.NAME, "district")
    dropdown.find_element(By.XPATH, f"//option[. = '{period_select.district}']").click()
    driver.find_element(By.ID, "contactAddr").send_keys(period_select.contactAddr)
    driver.find_element(By.ID, "cellPhone").send_keys(period_select.phone)
    driver.find_element(By.ID, "eMail").send_keys(period_select.e_mail)
    if period_select.choose:
        driver.find_element(By.LINK_TEXT, "送出").click()
        print(driver.find_element(By.ID, "headerMessage").text)


def main():
    # 隱藏自動化測試標籤
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome("./chromedriver", options=option)

    # driver.execute_script('navigator.webdriver = null;')

    find = choose_class(driver)
    if find:
        information(driver)

    print("Press Enter to end process.", file=sys.stderr)
    input()


if __name__ == "__main__":
    main()
