import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

url = "https://ev.delhi.gov.in/charging_station"
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.get(url)
time.sleep(2)

list_of_broad_areas = driver.find_elements(By.CSS_SELECTOR, value='div.ch-name')
list_of_charging_station = driver.find_elements(By.CSS_SELECTOR, value='div.ch-st')

for broad in list_of_broad_areas:
    ActionChains(driver).click(broad).perform()
    time.sleep(1)

record = []
count = 1
for station in list_of_charging_station:
    try:
        # ele = station.find_element(By.CSS_SELECTOR, value='div.ch-st-name')
        ele = WebDriverWait(station, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.ch-st-name')))
        # print(ele.get_attribute('innerHTML'))
        # button = station.find_element(By.CSS_SELECTOR, value='div.dir')
        # --------------------
        # print(ele.get_attribute('outerHTML'))
        ActionChains(driver).click(ele).perform()
        # print(ele.get_attribute('outerHTML'))
        # time.sleep(1)
        button = WebDriverWait(station, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dir')))
        # print(button.get_attribute('data-lat'))
        ActionChains(driver).click(button).perform()
        time.sleep(1)
        # --------------------
        brand_name = ele.get_attribute('innerHTML').split('<span')[0].strip()
        xpath = '/html/body/section[4]/div[1]/div/div[2]/div[3]/div[1]/div[6]/div/div[1]'
        popup = WebDriverWait(station, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # css_selector = "div.leaflet-pane.leaflet-popup-pane div.leaflet-popup.leaflet-zoom-animated div.leaflet-popup-content-wrapper"
        # popup = driver.find_element(By.XPATH, xpath)
        # popup = driver.find_elements(By.CSS_SELECTOR, value='div.leaflet-popup div.leaflet-popup-content-wrapper')
        # ---------------------
        location = popup.find_element(By.CSS_SELECTOR, value='.station-info-window div').get_attribute(
            "innerHTML").strip()
        lat_long_link = popup.find_element(By.CSS_SELECTOR, value='.station-info-window a').get_attribute('href')
        lat = lat_long_link.split('@')[1].split(',')[0].strip()
        long = lat_long_link.split('@')[1].split(',')[1].strip()
        details = popup.find_elements(By.CSS_SELECTOR, value='div.station-info-window div div')
        # print(len(details))
        # for i in details:
        #     print(i.get_attribute('outerHTML'))
        charging_points = details[1].get_attribute('innerHTML').split('span>')[2].split(' (')[0].strip()
        cost_of_charging = details[2].get_attribute('innerHTML').split('span>')[-1].strip()
        charging_type = details[3].get_attribute('innerHTML').split('span>')[-1].strip()
        payment_options = details[4].get_attribute('innerHTML').split('span>')[-1].strip()
        # -------------------------------
        print(f"Brand Name : {brand_name}")
        print(f'latitude {lat}')
        print(f'longitude {long}')
        print(f'Address {location}')
        print(f'charging type : {charging_type}')
        print(f'charging port : {charging_points}')
        print(f'cost per unit : {cost_of_charging}')
        print(f'payment type : {payment_options}')
        print('-------------------------------')
        record.append(
            (brand_name, location, lat, long, charging_type, charging_points, cost_of_charging, payment_options))
    except:
        try:
            ele = WebDriverWait(station, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.ch-st-name')))
            button = WebDriverWait(station, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dir')))
            brand_name = ele.get_attribute('innerHTML').split('<span')[0].strip()
            location = button.get_attribute("data-address").strip()
            lat = button.get_attribute('data-lat').strip()
            long = button.get_attribute('data-lng').strip()
            charging_type = ''
            cost_of_charging = ''
            charging_points = station.find_element(By.CSS_SELECTOR, value='div.ch-st-pts div').get_attribute('innerHTML').split('</span>')[1].strip()
            payment_options = station.find_element(By.CSS_SELECTOR, value='div.ch-st-pay').get_attribute('innerHTML').split(':')[1].strip()
            # -------------------------------
            print(f"Brand Name : {brand_name}")
            print(f'latitude {lat}')
            print(f'longitude {long}')
            print(f'Address {location}')
            print(f'charging type : {charging_type}')
            print(f'charging port : {charging_points}')
            print(f'cost per unit : {cost_of_charging}')
            print(f'payment type : {payment_options}')
            print('-------------------------------')
            record.append((brand_name, location, lat, long, charging_type, charging_points, cost_of_charging, payment_options))
        except:
            continue

df = pd.DataFrame(record, columns=['Brand Name', 'Address', 'latitude', 'longitude', 'charging type', 'charging port', 'cost per unit', 'payment type'])
df.to_csv('EV_Charging_Swapping_Database.csv', index=False, encoding='utf-8')

driver.quit()