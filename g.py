import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

# .env faylını yükləyirik
load_dotenv()

# İstifadəçi məlumatlarını götür
USERNAME = os.getenv("KOICA_USERNAME")
PASSWORD = os.getenv("KOICA_PASSWORD")
LOGIN_URL = os.getenv("KOICA_LOGIN_URL")

# Selenium üçün brauzer parametrləri
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Brauzeri görünməz rejimdə işə salır
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Brauzeri işə sal
browser = webdriver.Chrome(options=options)

try:
    # KOICA saytına daxil ol
    browser.get(LOGIN_URL)

    # Gözləmə mexanizmi
    wait = WebDriverWait(browser, 10)

    # İstifadəçi adı və parol sahələrini tap
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = browser.find_element(By.NAME, "password")

    # İstifadəçi məlumatlarını daxil et
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Davamiyyət səhifəsinə yönləndir
    attendance_page_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Python Davamiyyət")))
    attendance_page_link.click()

    # Davamiyyət məlumatlarını götür
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.attendance-table tr")))

    # Məlumatları cədvəl formasında saxla
    attendance_data = []
    for row in rows[1:]:  # Başlıq sətrini keçirik
        cols = row.find_elements(By.TAG_NAME, "td")
        date = cols[0].text
        status = cols[1].text
        attendance_data.append({"Tarix": date, "Davranış": status})

    # Cədvəli fayla yaz
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"attendance_{today}.xlsx"
    df = pd.DataFrame(attendance_data)
    df.to_excel(output_file, index=False)

    print(f"Davamiyyət məlumatları '{output_file}' faylında saxlanıldı.")

except Exception as e:
    print(f"Xəta baş verdi: {e}")

finally:
    # Brauzeri bağla
    browser.quit()