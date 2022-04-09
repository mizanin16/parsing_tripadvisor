import csv
import os.path
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


def driver_init() -> webdriver:
    """
    Определение параметров драйвера
    :return: web driver файл
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    driver.set_window_size(2400, 2400)
    return driver


def open_csv_city():
    """
    Открытие спарсинного файла из main.py
    Переход по ссылке из файла и парсинг определенных полей
    :return:
    """

    # Открытие спарсинного файла из main.py
    file = open('sochi.csv', 'r', encoding='utf-16')
    data = file.readlines()
    file.close()
    # Инициализация драйвера
    driver = driver_init()

    # Проходим построчно по каждому значению из файла
    for general_info_hotel in data:
        # Проверка на наличие данных в файле
        if len(general_info_hotel) < 5:
            continue
        # Разделяем данные в массив для правильной работы
        info_hotel = general_info_hotel.rsplit('\t')
        # В случае некоректной записи в файл присваиваем параметру url 3 значение
        url = info_hotel[1]
        if 'http' not in url:
            url = info_hotel[2]
        # Выполняем replace заголовка для удаления лишних символов, для исключения ошибок при записи в файл
        name_hotel = info_hotel[0].strip('\"').replace('\"', '').strip('/').replace('*', '')
        # Необходимо реализовать через wait для правильного ожидания
        time.sleep(0.3)
        # Переходим по ссылке, которую спарсили раннее
        driver.get(url)
        # Нажимаем кнопку ESCAPE для закрытия всплывшего окна
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        # Считываем расположение
        destinations_city = driver.find_elements_by_xpath(".//li[@class='breadcrumb']/a")
        # Определяем полный путь к файлу с помощью расположения конкретной гостиницы из объявления
        name_path = [name_path.text for name_path in destinations_city]
        full_path = os.path.join(*name_path)
        # Сохраняем изображения страницы для анализа парсинга
        path_to_png = os.path.join(full_path, f'{name_hotel}.png')
        # Если изображения существует, то подразумеваем что сайт уже прочитан раннее
        if os.path.exists(path_to_png):
            continue
        driver.save_screenshot(path_to_png)
        # Сохраняем папку, как полный путь ао адрессу
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        try:
            # Определям расположение
            destination_current = driver.find_element_by_xpath(".//span[@class='ceIOZ yYjkv']").text
        except Exception as ex:
            destination_current = 'Destination is not find'
        try:
            # Определяем телефон
            tel = driver.find_element_by_xpath(".//a[@class='bIWzQ']").text
        except Exception:
            try:
                # Определяем телефон из другого места на сайте
                tel = driver.find_element_by_xpath(
                    ".//div[@class='ApqWZ S4 H3 f u eEkxn' and @data-blcontact='PHONE ']").text
            except Exception:
                tel = 'Tel not find'
        if 'Задать вопрос' in tel:
            tel = 'Tel not find'
        try:
            # Считываем описание отеля
            description_info = driver.find_element_by_xpath(
                ".//div[@class='pIRBV _T' and @style='max-height: 242px; line-break: normal; cursor: auto;']").text
        except Exception:
            description_info = 'Описание не найдено'
        # Считывем Услуги отеля
        services = driver.find_elements_by_xpath(
            ".//div[@class='exmBD K']/div[@class='bUmsU f ME H3 _c' and @data-test-target='amenity_text']")
        name_services = [name_service.text for name_service in services]
        try:
            # Выполняем поиск ссылки на официальный сайт
            site_general = driver.find_element_by_xpath(
                ".//div[@class='ApqWZ S4 H3 f u eEkxn' and @data-blcontact='URL_HOTEL ']/a").get_attribute('href')
            if len(site_general) > 5:
                driver.get(site_general)
                time.sleep(0.5)
                site_general = driver.current_url
            else:
                site_general = 'General site not find'
        except Exception:
            site_general = 'General site not find'

        # Записываем в файл
        csvFile = open(os.path.join(full_path, fr'{name_hotel}.csv'), 'w', encoding="utf-16")
        csvFile.write(f'Наименование;{name_hotel}\n')
        csvFile.write(f'Телефон;{tel}\n')
        csvFile.write(f'Почтовый адрес;{destination_current}\n')
        csvFile.write(f'Официальный сайт\Сайт партнера;{site_general}\n')
        csvFile.write('Услуги;')
        print(*name_services, file=csvFile)
        csvFile.write(f'\nОписание;{description_info}\n')
        csvFile.close()
    driver.close()
