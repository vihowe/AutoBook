import json
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from aip import AipOcr
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def get_file_content(img_path):
    with open(img_path, 'rb') as fp:
        return fp.read()


def convert_img(img_path):

    APP_ID = '25240182'
    API_KEY = 'eFMcnbgiXsNGwT3OHcYZjOuu'
    SECRET_KEY = 'my5XA70cVDkeBgu08pk4hMBoGwZrWmm7'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content(img_path)
    result = client.basicAccurate(image)
    ret = ''
    with open('./result', 'w') as rf:
        for line in result['words_result']:
            rf.write(line['words'])
            ret += line['words'].replace(' ', '')
    print(ret)
    return ret.rstrip()



def booking(url, user_name, password, type, stadium, date):
    with webdriver.Chrome(executable_path='/opt/WebDriver/chromedriver') as driver:
        # Open URL
        driver.get(url)

        loging_btn = driver.find_element(By.CSS_SELECTOR, '#logoin > div:nth-child(1) > div > div:nth-child(2) > button:nth-child(1) > span')
        loging_btn.click()

        # log in
        while True:
            user_name_input = driver.find_element(By.CSS_SELECTOR, '#user').send_keys(user_name)
            password_input = driver.find_element(By.CSS_SELECTOR, '#pass').send_keys(password)
            verification = driver.find_element(By.CSS_SELECTOR, '#captcha-img')
            veri_img = 'veri.png'
            verification.screenshot(veri_img)
            veri_code = convert_img(veri_img)

            veri_input = driver.find_element(By.CSS_SELECTOR, '#captcha')
            veri_input.send_keys(veri_code)

            submit_btn = driver.find_element(By.CSS_SELECTOR, '#submit-button')
            submit_btn.click()
            try:
                login_error = driver.find_element(By.CSS_SELECTOR, '#div_warn')
            except NoSuchElementException:
                break

        css_addr = {
            'badminton': '#app > div:nth-child(2) > div.w.el-row > div.APPmodule.el-col.el-col-24 > div > div > div.el-carousel__item.is-active.is-animating > ul > li:nth-child(5) > a > img',
            'xinti': '#Venue > div > div:nth-child(5) > div:nth-child(2) > ul > li:nth-child(1) > div > div > div.cardUrl',
            'pingpong': '#app > div:nth-child(2) > div.w.el-row > div.APPmodule.el-col.el-col-24 > div > div > div.el-carousel__item.is-active.is-animating > ul > li:nth-child(6) > a > img',
            'nanti': '#Venue > div > div:nth-child(5) > div:nth-child(2) > ul > li:nth-child(2) > div > div > div.cardUrl'
        }

        badminton = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, css_addr[type])).click()

        badminton = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, css_addr[stadium])).click()

        while True:
            try:
                badminton = WebDriverWait(driver, timeout=0.5).until(lambda d: d.find_element(By.CSS_SELECTOR, f'#tab-2021-{date}'))
                badminton.click()
                break
            except TimeoutException:
                print('refresh')
                driver.refresh()

        while True:
            try:
                a = 15
                b = 16
                num = 0
                while True:
                    eight_nine = WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.CSS_SELECTOR, f'#apointmentDetails > div.lists > div.chart > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > div > div.inner-seat-wrapper.clearfix > div:nth-child({a})')).find_elements(By.CLASS_NAME, 'unselected-seat')

                    nine_ten = WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.CSS_SELECTOR, f'#apointmentDetails > div.lists > div.chart > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > div > div.inner-seat-wrapper.clearfix > div:nth-child({b})')).find_elements(By.CLASS_NAME, 'unselected-seat')

                    for seat in eight_nine:
                        seat.click()
                        num += 1
                        break
                    for seat in nine_ten:
                        seat.click()
                        num += 1
                        break
                    print(a, b, num)
                    if num != 0:
                        break
                    else:
                        a -= 2
                        b -= 2

                book_btn = driver.find_element(By.CSS_SELECTOR, '#apointmentDetails > div.lists > div.chart > div:nth-child(2) > div > div:nth-child(1) > div.drawerStyle > div.butMoney > button')
                book_btn.click()
                confirm_btn = WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.XPATH, '//*[@id="apointmentDetails"]/div[2]/div[2]/div[3]/div/div[3]/div/div[1]/label/span[1]/input'))
                js = 'document.querySelector("#apointmentDetails > div.lists > div.chart > div.el-dialog__wrapper > div > div.el-dialog__footer > div > div.tk > label > span.el-checkbox__input > input").click()'
                driver.execute_script(js)

                WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, '#apointmentDetails > div.lists > div.chart > div.el-dialog__wrapper > div > div.el-dialog__footer > div > div:nth-child(2) > button.el-button.btnStyle.el-button--primary')).click()
            except Exception as e:
                continue
            else:
                break

        time.sleep(30)



if __name__ == '__main__':
    url = 'https://sports.sjtu.edu.cn'
    booking(url, 'jaccount_id', 'jaccount_passwd', 'badminton', 'xinti', '12-05')
    # convert_img('./veri.png')



