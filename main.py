"""
Скрипт реализует парсинг сайта tripadvisor на поиск отелей по указанным ссылкам и запись в указанный файл
"""

import csv
from selenium import webdriver

import time


def find_page_hotel(container, csvWriter):
    """
    Поиск атрибутов наименования и ссылки на страницу и запись в файл
    :param container: Атрибут со списком отелей
    :param csvWriter: Объект для записи в файл
    """
    for j in range(len(container)):
        href = container[j].get_attribute("href")
        title = container[j].get_attribute("text").strip()

        csvWriter.writerow([title, href])


def main():
    """
    Парсинг определенного города
    :return:
    """
    # Путь к файлу с данными статистики
    path_to_file = "sochi.csv"

    # url адрес к конкретному городу
    url = "https://www.tripadvisor.ru/Hotels-g298536-Sochi_Greater_Sochi_Krasnodar_Krai_Southern_District-Hotels.html"

    # Инициализируем web driver от Chrome
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    # Переходим по ссылке
    driver.get(url)

    # Открытие файла для записи
    csvFile = open(path_to_file, 'w', encoding="utf-16")
    csvWriter = csv.writer(csvFile)
    time.sleep(2)
    # Условие будет работать пока будут поля
    while True:
        # Находим поле с списком отелей
        container = driver.find_elements_by_xpath(".//div[@class='listing_title']/a")
        find_page_hotel(container, csvWriter)
        try:
            # Обнаруживаем кнопку включения
            next_page = driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]')
            # Нажимаем на кнопку включения
            next_page.click()
            # Необходимо реализовать через wait для правильного ожидания
            time.sleep(2)
        except Exception as ex:
            # Вывод ошибки и закрытие приложения
            print(ex)
            driver.close()
            exit()
        continue


if __name__ == '__main__':
    main()
