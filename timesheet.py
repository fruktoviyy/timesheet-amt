import time
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta



def is_valide_user_dates(date_range): #проверят, что пользователь ввел даты в правильном формате - ДД.ММ.ГГГГ-ДД.ММ.ГГГГ
     range_pattern = r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$'
     return re.match(range_pattern, date_range) is not None


def choose_type_of_work():
     with open("nazvanie_rabot.txt", "r", encoding="utf-8") as file:
          lines = file.readlines()
     return lines
     

def select_days():
    list_of_filled_days = browser.find_elements(By.CSS_SELECTOR, ".ms-cal-tweekitem b") #получаем список элементов дней с заполненными днями на выбранной неделе
    list_of_filled_date=[] #создаем пустой список, куда будем записывать даты тех дней, которые уже были заполненны
    if len(list_of_filled_days) != 0:
        for i in range(len(list_of_filled_days)):
            list_of_filled_days[i].click()
    #       time.sleep(10)
            date_field = browser.find_element(By.CLASS_NAME, "ms-input") #ищем на страничке дату, за которую был заполненные отчет
            list_of_filled_date.append(date_field.get_attribute("value"))
            browser.get(url)
            list_of_filled_days = browser.find_elements(By.CLASS_NAME, "ms-cal-tweekitem") #получаем список элементов дней с заполненными днями на выбранной неделе
    else:
        print("Заполненных дней не найдено...сейчас заполним!")
    return list_of_filled_date
    

def determine_dates(dates_range, user_date_range):
        start_date_str, end_date_str  = dates_range.split("-")
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

        date_list= []
        current_date = start_date

        while current_date <= end_date:
             date_list.append(current_date.strftime("%d.%m.%Y"))
             current_date += timedelta(days=1) 
        
        for i in user_date_range:
             if i in date_list:
                  date_list.remove(i)

        return date_list

def filling_timesheet(date_list, nazvanie_rabot):
    date_list_str = (", ").join(date_list) 
    print("Будут заполненны отчеты по следующим датам: {}".format(date_list_str))
    for i in date_list:
         browser.get("http://portal/SiteDirectory/timesheet/Lists/timesheet/NewForm.aspx?Source=/SiteDirectory/timesheet")
         # ищем поля, которые нужно заполнить: место, вид работы, время начала, длительность работы, название работы. И заполняем их.
         # обязательное поле "Исполнитель" уже должно быть заполненно автоматически, при прогрузке страницы. Поэтому это поле мы не заполняем.
         place_of_working = browser.find_element(By.ID, place_of_work_selectors[rezhim_raboti])
         place_of_working.click()
         
         type_of_work = Select(browser.find_element(By.ID, "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl06_ctl00_ctl00_ctl04_ctl00_Lookup"))
         type_of_work.select_by_value(("14" if rezhim_raboti == "1" else  "21" if rezhim_raboti == "2" else "51" ))

         start_time_field = browser.find_element(By.ID, "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl07_ctl00_ctl00_ctl04_ctl00_ctl00_DateTimeField_DateTimeFieldDate")
         start_time_field.clear()
         start_time_field.send_keys(i)

         duration_of_work = browser.find_element(By.ID, "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl08_ctl00_ctl00_ctl04_ctl00_ctl00_TextField")
         duration_of_work.clear()
         duration_of_work.send_keys("9")

         name_of_work = browser.find_element(By.ID, "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl09_ctl00_ctl00_ctl04_ctl00_ctl00_TextField")
         name_of_work.clear()
         name_of_work.send_keys((random.choice(nazvanie_rabot)).strip())

         OK_button = browser.find_element(By.ID, "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_toolBarTbl_RightRptControls_ctl01_ctl00_diidIOSaveItem")
         OK_button.click()
         

       

place_of_work_selectors = {
     "1": "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl05_ctl00_ctl00_ctl04_ctl00_ctl00", #"В офисе"
     "2": "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl05_ctl00_ctl00_ctl04_ctl00_ctl01", #"Вне офиса"
     "3": "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl05_ctl00_ctl00_ctl04_ctl00_ctl02", #"Командировка"
     "4": "ctl00_m_g_153a6dd4_f9c7_4190_b75b_e429452b266f_ctl00_ctl05_ctl05_ctl00_ctl00_ctl04_ctl00_ctl03"  #"Дома"
}     


try:
    
    while True:
         user_dates = input("Напишите дату начала и конца недели, за которую необходимо отправить timesheet (пример ввода: 09.09.2024-13.09.2024)\n")
         if is_valide_user_dates(user_dates):
              break
         else:
              print("Вы ввели диапазон дат не в правильном формате. Повторите попытку ввода.")

    rezhim_raboti = input("Выберете, в каком режиме работы вы находились на этой неделе: 1 - В офисе, 2 - Вне офиса, 3 - Командировка, 4 - Дома. Напишите одну цифру, которая соотвествует выбору.\n")

    url_day, url_month, url_year = user_dates[:2], user_dates[3:5], user_dates[6:10]

    url = f"http://portal/SiteDirectory/timesheet/default.aspx?CalendarPeriod=week&CalendarDate={url_day}%2E{url_month}%2E{url_year}"
    
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get(url)
    
    dstes_to_fill = determine_dates(user_dates, select_days())
    
    filling_timesheet(dstes_to_fill, choose_type_of_work())
    browser.get(url)
    time.sleep(12)


except WebDriverException as e:
    print(f"Возникла ошибка:{e}")

else:
     print("Ваш отчет за даты {} заполнен. Вам осталось лишь отправить отчёт".format(user_dates))

finally:
     print("Выполнение работы программы завершено.")