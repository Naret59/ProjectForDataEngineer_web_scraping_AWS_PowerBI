# Data Engineer Project
การ Web Scraping และจัดเก็บข้อมูลลงใน S3 เพื่อสร้าง Data pipline โดยการนำข้อมูล SET100 จาก https://www.set.or.th/th/home นำสร้าง Data pipline เพื่อสามารถให้นำมาใช้ได้ใน Power Bi เพื่อทำการวิเคราะห์ข้อมูล

<p align="center">
  <img src="https://github.com/user-attachments/assets/b596e241-47b1-4c5b-8486-1c78a212c155" alt="Image 1" width="200"/>
  <img src="https://github.com/user-attachments/assets/d30af651-6b91-47c2-a9d2-deaf4a0a9bab" alt="Image 2" width="200"/>
  <img src="https://github.com/user-attachments/assets/41f365ed-4d83-4d29-ba0c-106144b6eea6" alt="Image 3" width="200"/>
</p>

## Tool 
- Python
- Selenium
- AWS IAM
- AWS S3
- AWS EC2
- AWS Crawler
- AWS Glue 
- AWS Athena 
- Power BI 
## Introduction     
โดยผมมีความตั้งใจจะสร้าง Data pipline โดยจะใช้ Service ของ AWS เริ่มจากเขียน code สำหรับ Web Scraping โดยใช้ Python และ Selenium ในการดึงข้อมูลจาก https://www.set.or.th/th/home จากนั้นทำการทดลอง Run บน local เพื่อทดสอบว่าสามารถใช้งานได้หลังจากนั้น ย้าย code ไปไว้บน EC2 (Elastic Compute Cloud) เพื่อสร้างไฟล์ CSV ไปเก็บไว้ที่ S3 (Simple Storage Service) จากนั้นใช้ AWS Crawler ดึงข้อมูลจาก S3 ไปไว้ที่ Database ของ AWS Glue เพื่อทำการ Transform data ให้เป็น  Parquet file เพราะ มีหน่วยความจำในการเก็บไฟล์ที่น้อยกว่า CSV จากนั้นใช้ code Python เขียนเพิ่มในส่วนของ Get Data ของ Power BI เพื่อให้ Data analysis หรือ BI นำจ้อมูลไปใช้ต่อได้ 

## Step 1 Web Scraping
โดยในที่นี้จะใช้ Selenium เพราะ ผมเคยได้ทดลองใช้ Beautiful Soup แล้วผลคือไม่สามารถทำได้ครับ Website SET100 เป็น dynamic website ซึ่งใช้ Javascript เขียน ทำให้จึงเลือกใช้ Selenium แทน 
จากนั้นทดสอบการทำงานของ code บน local 
ตัวอย่างหน้าเว็บต้องการจะทำ Web Scraping 
![image](https://github.com/user-attachments/assets/2248ee6e-a014-49b7-8591-78c76ae0f2a3)

```python
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO
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

# บันทึก DataFrame ลงไฟล์ CSV
df.to_csv('Companies.csv', index=False)

print("Data saved to Companies.csv")
```
พบว่าระบบสามารถทำงานได้บน Local โดยได้ผลลัพธ์ดังนี้ 
![image](https://github.com/user-attachments/assets/f494df2f-de4c-4079-bb54-bbc18edaeae2)
จากนั้นย้าย code ไปไว้บน Cloud โดยครั้งแรกผมตั้งใจจะใช้ AWS Lambda เพราะเป็น Severless จะได้ช่วยในเรื่องของการลด Cost ในการใช้จ่ายแต่ด้วยความที่ Lambda ไม่เหมาะแก่การใช้ Selenium เพราะต้องทำการติดตั้ง chromedriver ด้วยและอีกทั้งเรายังใช้ library ที่เยอะด้วยทำให้ติดปัญหาของ Lambda Layer ที่พบว่า library Selenium มีขนาดที่ใหญ่เกินกว่าที่กำหนด ผมเลยเลือกใช้เป็น EC2 แทนเพราะสะดวกและง่ายกว่าสำหรับการทำงานขอ code ชุดนี้ 
จากนั้นผมก็เพิ่ม Code ส่วนที่เป็น Headless ของ chromedriver เข้าไปเพราะ ตอนที่ Run บนเครื่องจะพบว่าต้องมีการเปิด Google Chrome ทุกครั้งที่ Run code ซึ่งบน Cloud ไม่สามารถทำได้โดยใช้ code ส่วนนี้ครับ 
```python
# ตั้งค่าให้ Chrome ทำงานในโหมด headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```
เพื่อเปิดการใช้งาน Chrome แบบไม่ต้องใช้หน้าจอ จากนั้นทำการเปิดใช้ EC2 instance โดยในที่นี้ผมเลือกใช้เป็น OS แบบ Linux ครับจากนั้นทำการติดตั้ง library ตามไฟล์นี้ได้เลยครับ [requirements.txt](https://github.com/Naret59/ProjectForDataEngineer_web_scraping_AWS_PowerBI/blob/main/requirements.txt)  จากนั้นทำการติดตั้ง AWS CLI เพื่อที่จะสามาใช้ library boto3 เพื่อทำการเขียน configure ของ AWS CLI ให้ลิงค์กับ EC2 จากนั้นทำการลง chromedriver สำหรับ Linux ซึ่งสามารถ Download ได้จากลิงค์นี้ได้เลยครับ [เว็บสำหรับดาวโหลด](https://googlechromelabs.github.io/chrome-for-testing/) 
![image](https://github.com/user-attachments/assets/fc258927-7c65-4450-af33-8bf304141ce7)

จากนั้นเมื่อทำการเตรียม Environment เรียบร้อยแล้วทำการสร้าง User ที่ AWS IAM (AWS Identity and Access Management) เพื่อที่จะนำ Access key และ Secret access key มากกรอกใน aws configure

```bash
AWS Access Key ID : your Access key 
AWS Secret Access Key [None]: your Secret access key 
Default region name [None]: ap-southeast-1
Default output format [None]: json
```
โดย Permissions policies ผมจะเลือกใช้เป็นดังนี้ครับ
![image](https://github.com/user-attachments/assets/5cdca4e6-5ef6-4b49-b404-ebe4fe6b2503)
จากนั้นทำการ Create User 
![image](https://github.com/user-attachments/assets/b13201b0-881d-4ff3-aafc-0e06832b11b8)
จากนั้นนำ Access key และ Secret access key มากกรอกใน aws configure ตอนนี้เราสามารถนำ Code ต่อไปนี้ในการ Run เพื่อทำงาน Web Scraping ได้เลยครับ โดยจะเพิ่มในในส่วนของ bucket ของ S3 ที่เราต้องการจัดเก็บ [Web_scraping.py](https://github.com/Naret59/ProjectForDataEngineer_web_scraping_AWS_PowerBI/blob/main/Web_scraping.py) 
เมื่อทำการ Run Code เรียบร้อยจะได้ไฟล์ CSV ไปเก็บไว้ที่ S3 ดังรูปด้านล่าง
![image](https://github.com/user-attachments/assets/e1041581-e6fd-47f5-9ed4-e291e65b4b4e)

## Step 2 แปลงไฟล์ CSV เป็น Parquet file โดยใช้ AWS Glue 
โดยขั้นตอนนี้เราจะใช้ AWS Crawlers ดึงข้อมูลตจา่ก S3 ไปไว้ที่ Database ของ AWS Glue โดยใช้ Visual ETL ซึ่งเป็นเครื่องมือสำหรับการวร้าง ETL job บน AWS โดยสามาร Run ทั้งแบบ Visual , Notebook และ Script แต่ใน Project นี้เราจะใช้ Visual ETL
![image](https://github.com/user-attachments/assets/ed00f891-9431-4b40-8632-0079c707bc5f)
1.Box แรกจะเป็นการนำเข้าข้อมูลจาก Database ที่อยู่บน AWS Glue 
2.Box ที่สองจะเป็น Box สำหรับ Transform ข้อมูล 
3.Box ที่สามจะเป็น Box สำหรับแปลงไฟล์เป็น Parquet file แล้วส่งไปที่ S3 
ผลลัพธ์ 
![image](https://github.com/user-attachments/assets/1e785673-8831-44a2-ba56-2dccb2d1aac1)

## Step 3 Get Data จาก S3 ไปใช้ต่อที่ Power BI 
โดยในที่นี้เราจะใช้ Code [python_srcipt_get_s3.py](https://github.com/Naret59/ProjectForDataEngineer_web_scraping_AWS_PowerBI/blob/main/python_srcipt_get_s3.py) โดยใช้ User เดียวกันกับที่ใช้ configure ที่สร้างจาก IAM โดยเราจะทำการกรอก Access key และ Secret access key 
```python
import boto3, os, io
import pandas as pd 

my_key= '' 
my_secret= '' 

my_bucket_name = 'set100-naret-input' 
my_file_path = 'CSV_set100/Companies (1).csv' 

session = boto3.Session(aws_access_key_id=my_key,aws_secret_access_key=my_secret) 
s3Client = session.client('s3') 
f = s3Client.get_object(Bucket=my_bucket_name, Key=my_file_path) 
heart_disease_data = pd.read_csv(io.BytesIO(f['Body'].read()), header=0)

```
จากนั้นดูผลลัพธ์ 
![image](https://github.com/user-attachments/assets/32d5c003-d604-4924-be87-b9fa75fb5148)
จะเห็นว่า เราสามารถโหลด Data จาก S3 มาได้แล้ว เป็นอันจบกระบวนการทำงาน หากต้องการตั้งเวลาสำหรับการดึงข้อมูลทุกๆเช้าเวลา 10.00 ก็สามารถใช้ Service EventBridge ในการทำ Job scheduler ได้ 🙌








 


