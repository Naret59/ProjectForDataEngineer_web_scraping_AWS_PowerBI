import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import boto3
from io import StringIO

# ตั้งค่าให้ Chrome ทำงานในโหมด headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ตั้งค่า WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# โหลดหน้าเว็บ
driver.get("https://www.set.or.th/th/market/index/set100/overview")

# ดึง HTML ของหน้าเว็บ
set_100_str = driver.page_source

# ปิด WebDriver
driver.quit()

# แปลง HTML เป็น DataFrame
df = pd.read_html(set_100_str)[1]

# สร้างไฟล์ CSV ในหน่วยความจำโดยใช้ StringIO
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

# เชื่อมต่อกับ S3 โดยใช้ boto3
s3_client = boto3.client('s3')

# กำหนดชื่อ bucket และชื่อไฟล์ที่ต้องการอัปโหลด
bucket_name = 'set100-naret-input'
file_name = 'Companies.csv'

# อัปโหลดไฟล์ CSV ไปยัง S3
s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())

print(f"Data uploaded to S3 bucket '{bucket_name}' with file name '{file_name}'")