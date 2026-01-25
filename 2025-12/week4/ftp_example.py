import ftplib
import psycopg2
import csv
import io

# FTP 서버에 연결
ftp = ftplib.FTP('ftp.example.com')
ftp.login('username', 'password')

print("FTP 연결 성공")

# FTP에서 CSV 파일 다운로드
remote_file = 'data.csv'
local_file = 'downloaded_data.csv'

with open(local_file, 'wb') as f:
    ftp.retrbinary(f'RETR {remote_file}', f.write)

print(f"FTP에서 {remote_file} 파일 다운로드 완료")

# FTP 연결 종료
ftp.quit()
print("FTP 연결 종료")

# PostgreSQL DB 연결 
conn = psycopg2.connect(
    database="example_db",
    user="username",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

print("PostgreSQL 연결 성공")

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        value INTEGER
    )
""")
conn.commit()

# 다운로드한 CSV 파일 읽기 및 DB에 삽입
with open(local_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # 헤더 스킵 (가정)
    for row in reader:
        if len(row) >= 2:
            name, value = row[0], int(row[1])
            cursor.execute("INSERT INTO data_table (name, value) VALUES (%s, %s)", (name, value))

conn.commit()
print("데이터 DB에 저장 완료")

# DB 연결 종료
cursor.close()
conn.close()
print("PostgreSQL 연결 종료")