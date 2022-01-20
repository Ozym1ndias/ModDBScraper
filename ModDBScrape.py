from pandas import date_range
from selenium import webdriver
#import calendar
from datetime import datetime, timedelta, date
import time
import pyautogui
#from Visitors import Visitors



#################################### Variable init ####################################
Data = {}
driver = webdriver.Chrome('/home/hamza/chromedriver')
driver.get('https://www.moddb.com/mods')
last_page = int(driver.find_element_by_xpath('//*[@id="modsbrowse"]/div[2]/div[2]/div/a[8]').text)
#visitors = {}
pageslinks = []
for i in range(1, last_page + 1):
    pageslinks.append(f'https://www.moddb.com/mods/page/{i}#modsbrowse')
xmlpath2mods = []
for i in range(2, 32):
    xmlpath2mods.append(f'/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div[{i}]/div/h4/a')
########################################################################################

for link in pageslinks:
    driver.get(link)
    for path in xmlpath2mods:
        driver.find_element_by_xpath(path).click()
        driver.get(driver.current_url + '/stats')
        #driver.find_element_by_xpath('//*[@id="chartdiv"]/div/div[2]/div[3]/fieldset/div[2]/input[6]').click()
        driver.find_element_by_xpath('//input[@value="MAX"]').click()
        start_date = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[2]/div/div[2]/div/div/div[2]/div[3]/fieldset/div[1]/input[1]').get_attribute('value')
        end_date = date.today()
        mod_name = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div/div/h2/a').text
        Data[mod_name] = {}
        for day in date_range(start_date, end_date):
            time.sleep(5)
            scrape_day = f'{day.day}-{day.month}-{day.year}'
            driver.find_element_by_css_selector('#chartdiv > div > div.amcharts-center-div > div.amChartsPeriodSelector.amcharts-period-selector-div > fieldset > div:nth-child(2) > input.amChartsInputField.amcharts-end-date-input').click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(2)
            driver.find_element_by_css_selector('#chartdiv > div > div.amcharts-center-div > div.amChartsPeriodSelector.amcharts-period-selector-div > fieldset > div:nth-child(2) > input.amChartsInputField.amcharts-end-date-input').send_keys(scrape_day)
            time.sleep(2)
            driver.find_element_by_css_selector('#chartdiv > div > div.amcharts-center-div > div.amChartsPeriodSelector.amcharts-period-selector-div > fieldset > div:nth-child(2) > input.amChartsInputField.amcharts-start-date-input').click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(2)
            driver.find_element_by_css_selector('#chartdiv > div > div.amcharts-center-div > div.amChartsPeriodSelector.amcharts-period-selector-div > fieldset > div:nth-child(2) > input.amChartsInputField.amcharts-start-date-input').send_keys(scrape_day)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            scraped_data = driver.find_element_by_css_selector('#chartdiv > div > div.amcharts-center-div > div.amcharts-panels-div > div > div > div.amChartsLegend.amcharts-legend-div > svg > g > g > g > text:nth-child(4)').text
            scrape_day_visitors = scraped_data.replace('Total: ', '')
            #print(scrape_day_visitors)
            Data[mod_name][scrape_day] = scrape_day_visitors
            #visitors[f'{str(day.day)}-{str(day.month)}-{str(day.year)}'] = scrape_day_visitors
            driver.refresh()
        driver.execute_script("window.history.go(-1)")