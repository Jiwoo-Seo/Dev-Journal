# Python을 이용한 FTP/DB Connection 공부

## FTP Connection

Python의 `ftplib` 모듈을 사용하여 FTP 서버에 연결하고 파일을 전송할 수 있다. FTP는 File Transfer Protocol의 약자로, 파일 공유에 사용된다.

### 기본 사용법

- **연결**: `ftplib.FTP(host)` - FTP 서버에 연결한다.
- **로그인**: `login(user, passwd)` - 사용자 이름과 비밀번호로 인증한다.
- **목록 조회**: `retrlines('LIST')` - 현재 디렉토리의 파일 목록을 텍스트로 가져온다.
- **파일 다운로드**:
  - 텍스트 모드: `retrlines('RETR filename', callback)`
  - 바이너리 모드: `retrbinary('RETR filename', callback)`
- **파일 업로드**:
  - 텍스트 모드: `storlines('STOR filename', file)`
  - 바이너리 모드: `storbinary('STOR filename', file)`
- **연결 종료**: `quit()` - FTP 연결을 종료한다.

## DB Connection

Python에서 PostgreSQL 데이터베이스에 연결하여 데이터를 쿼리하거나 조작할 수 있습니다. `psycopg2` 라이브러리를 사용합니다.

### 설치

```bash
pip install psycopg2
```

### 기본 사용법

- **연결**: `psycopg2.connect(database='dbname', user='user', password='pass', host='host', port='5432')` - PostgreSQL DB에 연결.
- **커서 생성**: `cursor()` - SQL 실행을 위한 커서 객체.
- **SQL 실행**: `execute(sql, params)` - SQL 쿼리 실행 (params는 튜플로 파라미터화).
- **결과 가져오기**: `fetchone()`, `fetchall()`, `fetchmany(size)` - 쿼리 결과 반환.
- **커밋**: `commit()` - 변경사항 저장 (INSERT, UPDATE, DELETE 시 필요).
- **롤백**: `rollback()` - 변경사항 취소.
- **종료**: `close()` - 커서 및 연결 종료.

### 예제

```python
import psycopg2

# 연결
conn = psycopg2.connect(
    database="example_db",
    user="username",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER
    )
""")

# 데이터 삽입
cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ('John', 30))

# 커밋
conn.commit()

# 조회
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 종료
cursor.close()
conn.close()
```

### 주의사항

- 실제 애플리케이션에서는 SQL 인젝션 방지를 위해 파라미터화된 쿼리를 사용할 것!
- 대용량 데이터 처리 시 ORM (예: SQLAlchemy)을 고려!
- 연결 풀링을 위해 `psycopg2.pool`이나 SQLAlchemy의 엔진을 활용.
- PostgreSQL은 트랜잭션을 지원하므로, 여러 쿼리를 묶어 commit/rollback