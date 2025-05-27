from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Настройки Firefox
opts = FirefoxOptions()
opts.add_argument("--headless")  # Режим без GUI
driver = webdriver.Firefox(options=opts)

# Открываем CSV для записи
with open('divan_lighting_fixed.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Цена', 'Ссылка'])  # Заголовки

    try:
        print("Открываю страницу...")
        driver.get("https://www.divan.ru/category/svet")

        # Ожидание загрузки (явное)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._Ud0k"))
        )
        print("Страница загружена")

        # Прокрутка
        print("Прокручиваю страницу...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Поиск товаров
        products = driver.find_elements(By.CSS_SELECTOR, "div._Ud0k")
        print(f"Найдено товаров: {len(products)}")

        if not products:
            raise Exception("Товары не найдены! Проверьте селекторы.")

        # Парсинг
        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, "div.lsooF span").text.strip()
            except:
                name = "N/A"
                print("Ошибка: не найдено название")

            try:
                price = product.find_element(By.CSS_SELECTOR, "div.pY3d2 span").text.strip()
            except:
                price = "N/A"
                print("Ошибка: не найдена цена")

            try:
                url = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            except:
                url = "N/A"
                print("Ошибка: не найдена ссылка")

            writer.writerow([name, price, url])
            print(f"Добавлен: {name} - {price}")

    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
    finally:
        driver.quit()
        print("Завершено. Проверьте файл divan_lighting_fixed.csv")