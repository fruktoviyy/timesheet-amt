from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time

url = "http://portal/SiteDirectory/timesheet/default.aspx?CalendarPeriod=week&CalendarDate=24%2E09%2E2024"

try:
    user_dates = input("Напишите дату начала и конца недели, за которую необходимо отправить timesheet (пример ввода: 23.09.2024-27.09.2024)")

    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)

    def select_days():
        list_of_filled_days = browser.find_elements(By.CLASS_NAME, "ms-cal-tweekitem") #получаем список элементов дней с заполненными днями на выбранной неделе
        list_of_filled_date=[] #создаем пустой список, куда будем записывать даты тех дней, которые уже были заполненны
        if len(list_of_filled_days) != 0:
            for i in range(len(list_of_filled_days)):
                list_of_filled_days[i].click()
                date_field = browser.find_element(By.CLASS_NAME, "ms-input") #ищем на страничке дату, за которую был заполненные отчет
                list_of_filled_date.append(date_field.get_attribute("value"))
                browser.get(url)
                list_of_filled_days = browser.find_elements(By.CLASS_NAME, "ms-cal-tweekitem") #получаем список элементов дней с заполненными днями на выбранной неделе
        else:
            print("looser")
        return list_of_filled_date
    time.sleep(5)

    
    print(select_days())
    time.sleep(5)

    def determine_dates():
        





except Exception as e:
    print(f"Возникла ошибка:{e}")