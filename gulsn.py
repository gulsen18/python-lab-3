
import re
from dotenv import load_dotenv
import os
import pandas as pd

# KOICA platformasına daxil olun
login_url = "https://sso.aztu.edu.az/"
attendance_url = "https://sap.aztu.edu.az/studies/lecture_attend.php?lec_open_idx=60456&lecture_code=4138&sem_code=20242"

session = requests.Session()
login_payload = {
    "username":load_dotenv.username,
    "password": load_dotenv.password,
}

session.post(login_url, data=login_payload)

# Davamiyyət məlumatlarını əldə edin
response = session.get(attendance_url)
html_content = response.content.decode('utf-8')

# Müvafiq məlumatları toplamaq üçün regular expressions istifadə edin
pattern = re.compile(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>')
matches = pattern.findall(html_content)

# Məlumatları cədvəl faylında saxlayın
attendance_data = []

for match in matches:
    date, attendance = match
    attendance_data.append([date, attendance])

attendance_df = pd.DataFrame(attendance_data, columns=["Tarix", "Davamiyyət"])
attendance_df.to_excel("attendance.xlsx", index=False)

print("Davamiyyət məlumatlari uğurla cədvəl faylinda saxlanildi.")

