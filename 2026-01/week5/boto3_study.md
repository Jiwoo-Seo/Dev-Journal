# Boto3 스터디: S3 메모리 기반 파일 처리

## Boto3란?
Boto3는 AWS S3, EC2, DynamoDB 등 AWS 서비스와 상호작용하기 위한 Python 라이브러리입니다. 또한 MinIO와 같은 S3 호환 스토리지 서비스에도 사용할 수 있습니다.

## 설치
```bash
pip install boto3
pip install pandas pyarrow  # parquet 파일 처리용
```

## 기본 개념

### 1. S3 클라이언트 생성
```python
import boto3

# AWS S3 연결
s3_client = boto3.client('s3')

# MinIO 연결 (S3 호환 스토리지)
s3_client = boto3.client(
    's3',
    endpoint_url='http://minio-server:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)
```

### 2. 핵심 메서드

#### get_object() - 파일을 메모리에 로드
```python
response = s3_client.get_object(Bucket='bucket-name', Key='path/to/file.parquet')
file_content = response['Body'].read()  # 바이트 형태로 읽음
```

#### get_object()의 반환값 구조
```python
{
    'Body': StreamingBody,        # 파일 내용을 스트리밍하는 객체
    'ContentLength': 1024,         # 파일 크기 (바이트)
    'ContentType': 'application/octet-stream',
    'LastModified': datetime,
    'Metadata': {}
}
```

### 3. 메모리 기반 파일 처리

#### Parquet 파일을 메모리에서 처리
```python
import io
import pandas as pd

# 방법 1: BytesIO를 사용한 메모리 스트림
response = s3_client.get_object(Bucket='bucket', Key='file.parquet')
parquet_buffer = io.BytesIO(response['Body'].read())

# pandas로 직접 읽기
df = pd.read_parquet(parquet_buffer)

# 방법 2: 직접 response의 Body 사용
response = s3_client.get_object(Bucket='bucket', Key='file.parquet')
df = pd.read_parquet(response['Body'])
```

## 주요 장점

### ✅ 메모리 기반 처리의 이점
1. **빠른 속도**: 디스크 I/O 작업 제거
2. **임시 저장소 불필요**: 디스크 공간 절약
3. **스트리밍 처리**: 대용량 파일도 효율적으로 처리 가능
4. **보안**: 임시 파일이 남지 않음

### ✅ MinIO 호환성
- AWS S3와 동일한 API
- 온프레미스 환경에서 S3 호환 스토리지 구축 가능
- 개발/테스트 환경에 용이

## 예제: 머신러닝 파이프라인

```python
import boto3
import io
import pandas as pd

# MinIO 클라이언트 초기화
s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='user',
    aws_secret_access_key='password'
)

def get_s3_route(file_sno: str, filetype: int) -> str:
    """회사 함수라고 가정"""
    return f"data/file_{file_sno}_{filetype}.parquet"

def train(file_sno: str):
    """학습 함수"""
    pass

def inference(file_sno: str):
    """추론 함수"""
    pass

# 파일을 메모리에서 처리
file_sno = "12345"
s3_path = get_s3_route(file_sno, filetype=1)

# S3에서 파일 가져오기
response = s3_client.get_object(Bucket='ml-bucket', Key=s3_path)
parquet_buffer = io.BytesIO(response['Body'].read())

# pandas로 읽기
df = pd.read_parquet(parquet_buffer)

# 학습 및 추론
train(file_sno)
inference(file_sno)
```

## 실제 사용 시 체크사항

### 1. 연결 설정
- Endpoint URL 확인
- 인증 정보 (Access Key, Secret Key)
- Bucket 이름 및 경로

### 2. 에러 처리
```python
from botocore.exceptions import ClientError

try:
    response = s3_client.get_object(Bucket='bucket', Key='key')
except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchKey':
        print("파일이 존재하지 않습니다")
    elif e.response['Error']['Code'] == 'NoSuchBucket':
        print("버킷이 존재하지 않습니다")
```

### 3. 대용량 파일 처리
```python
# 청크 단위로 읽기 (메모리 효율적)
response = s3_client.get_object(Bucket='bucket', Key='large_file.parquet')
chunks = []
for chunk in iter(lambda: response['Body'].read(1024 * 1024), b''):
    chunks.append(chunk)
file_content = b''.join(chunks)
```

## 요약
- **Boto3**: AWS S3 및 S3 호환 스토리지 (MinIO) 접근 라이브러리
- **메모리 처리**: `get_object()`의 응답 Body를 메모리 스트림(BytesIO)으로 변환
- **Pandas 통합**: 메모리의 parquet 파일을 직접 DataFrame으로 변환
- **장점**: 빠른 속도, 보안, 디스크 공간 절약
