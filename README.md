# Data Engineer Project
การ Scraping Web และจัดเก็บข้อมูลลงใน S3 เพื่อสร้าง Data pipline โดยการนำข้อมูล SET100 จาก https://www.set.or.th/th/home นำสร้าง Data pipline เพื่อสามารถให้นำมาใช้ได้ใน Power Bi เพื่อทำการวิเคราะห์ข้อมูล

## Tool 
- Python
- Selenium 
- AWS S3
- AWS EC2
- AWS Crawler
- AWS Glue 
- AWS Athena 
- Power BI 
## Introduction     
โดยผมมีความตั้งใจจะสร้าง Data pipline โดยจะใช้ Service ของ AWS เริ่มจากเขียน code สำหรับ Scraping Web โดยใช้ Python และ Selenium ในการดึงข้อมูลจาก https://www.set.or.th/th/home จากนั้นทำการทดลอง Run บน local เพื่อทดสอบว่าสามารถใช้งานได้หลังจากนั้น ย้าย code ไปไว้บน EC2 (Elastic Compute Cloud) เพื่อสร้างไฟล์ CSV ไปเก็บไว้ที่ S3 (Simple Storage Service) จากนั้นใช้ AWS Crawler ดึงข้อมูลจาก S3 ไปไว้ที่ Database ของ AWS Glue เพื่อทำการ Transform data ให้เป็น  Parquet file เพราะ มีหน่วยความจำในการเก็บไฟล์ที่น้อยกว่า CSV จากนั้นใช้ code Python เขียนเพิ่มในส่วนของ Get Data ของ Power BI เพื่อให้ Data analysis หรือ BI นำจ้อมูลไปใช้ต่อได้
[Web_scraping.py](https://github.com/Naret59/ProjectForDataEngineer_web_scraping_AWS_PowerBI/blob/main/Web_scraping.py)
