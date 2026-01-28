"""
Boto3를 사용하여 S3(MinIO)에서 Parquet 파일을 메모리로 로드하여
학습(train)과 추론(inference)을 수행하는 예제

회사의 get_s3_route(), train(), inference() 함수가 있다고 가정
"""

import boto3
import io
import pandas as pd
from botocore.exceptions import ClientError
from typing import Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3ParquetHandler:
    """S3에서 Parquet 파일을 메모리로 처리하는 클래스"""
    
    def __init__(
        self,
        endpoint_url: str = "http://minio:9000",
        aws_access_key_id: str = "minioadmin",
        aws_secret_access_key: str = "minioadmin",
        bucket_name: str = "ml-data"
    ):
        """
        S3 클라이언트 초기화
        
        Args:
            endpoint_url: MinIO 또는 S3 엔드포인트 URL
            aws_access_key_id: AWS 액세스 키
            aws_secret_access_key: AWS 시크릿 키
            bucket_name: 기본 버킷 이름
        """
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket_name = bucket_name
        logger.info(f"S3 클라이언트 초기화 완료: {endpoint_url}")
    
    def get_parquet_from_s3(self, s3_path: str) -> Optional[pd.DataFrame]:
        """
        S3에서 Parquet 파일을 메모리로 로드하여 DataFrame 반환
        
        Args:
            s3_path: S3 내 파일 경로 (예: "data/file_12345_1.parquet")
            
        Returns:
            pd.DataFrame 또는 None (실패 시)
        """
        try:
            logger.info(f"S3에서 파일 다운로드 시작: {s3_path}")
            
            # S3에서 파일 가져오기
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_path
            )
            
            # 파일 내용을 메모리 버퍼에 읽기
            file_buffer = io.BytesIO(response['Body'].read())
            
            # Parquet 파일을 메모리에서 직접 읽기
            df = pd.read_parquet(file_buffer)
            
            logger.info(f"파일 로드 성공: {s3_path} (행: {len(df)}, 열: {len(df.columns)})")
            return df
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                logger.error(f"파일을 찾을 수 없습니다: {s3_path}")
            elif error_code == 'NoSuchBucket':
                logger.error(f"버킷을 찾을 수 없습니다: {self.bucket_name}")
            else:
                logger.error(f"S3 에러: {error_code}")
            return None
        except Exception as e:
            logger.error(f"파일 로드 중 에러 발생: {str(e)}")
            return None
    
    def get_parquet_chunk(self, s3_path: str, chunk_size: int = 1024 * 1024) -> Optional[pd.DataFrame]:
        """
        대용량 파일을 청크 단위로 읽기 (메모리 효율적)
        
        Args:
            s3_path: S3 내 파일 경로
            chunk_size: 청크 크기 (바이트)
            
        Returns:
            pd.DataFrame 또는 None
        """
        try:
            logger.info(f"S3에서 청크 단위로 파일 다운로드: {s3_path}")
            
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_path
            )
            
            # 청크 단위로 읽기
            chunks = []
            for chunk in iter(lambda: response['Body'].read(chunk_size), b''):
                chunks.append(chunk)
            
            file_buffer = io.BytesIO(b''.join(chunks))
            df = pd.read_parquet(file_buffer)
            
            logger.info(f"청크 읽기 완료: {s3_path}")
            return df
            
        except Exception as e:
            logger.error(f"청크 읽기 중 에러: {str(e)}")
            return None


# ============================================================================
# 회사 함수 (가정: 이미 구현되어 있음)
# ============================================================================

def get_s3_route(file_sno: str, filetype: int) -> str:
    """
    회사의 S3 경로 생성 함수 (실제로는 회사 코드베이스에 있음)
    
    Args:
        file_sno: 파일 시리얼 번호
        filetype: 파일 타입 (1: train, 2: test, etc.)
        
    Returns:
        S3 경로 (예: "data/file_12345_1.parquet")
    """
    file_type_map = {
        1: "train",
        2: "test",
        3: "validation"
    }
    type_name = file_type_map.get(filetype, "unknown")
    return f"data/{type_name}/file_{file_sno}_{filetype}.parquet"


def train(file_sno_list: list[str] | str):
    """
    모델 학습 함수 (회사 구현 함수라고 가정)
    
    Args:
        file_sno_list: 파일 시리얼 번호 또는 리스트
    
    실제 구현에서는 머신러닝 모델 학습 로직이 포함됨
    """
    # 단일 문자열을 리스트로 변환
    if isinstance(file_sno_list, str):
        file_sno_list = [file_sno_list]
    
    logger.info(f"[TRAIN] 파일 ID {file_sno_list}로 학습 시작")
    # 실제 학습 로직
    logger.info(f"[TRAIN] 파일 ID {file_sno_list} 학습 완료")


def inference(file_sno_list: list[str] | str):
    """
    모델 추론 함수 (회사 구현 함수라고 가정)
    
    Args:
        file_sno_list: 파일 시리얼 번호 또는 리스트
    
    실제 구현에서는 머신러닝 모델 추론 로직이 포함됨
    """
    # 단일 문자열을 리스트로 변환
    if isinstance(file_sno_list, str):
        file_sno_list = [file_sno_list]
    
    logger.info(f"[INFERENCE] 파일 ID {file_sno_list}로 추론 시작")
    # 실제 추론 로직
    logger.info(f"[INFERENCE] 파일 ID {file_sno_list} 추론 완료")


# ============================================================================
# 통합 함수
# ============================================================================

def process_ml_pipeline(file_sno_list: list[str] | str, filetype: int = 1, use_chunk: bool = False):
    """
    S3에서 파일들을 가져와 메모리에서 처리하고 학습/추론을 수행하는 메인 파이프라인
    
    Args:
        file_sno_list: 파일 시리얼 번호 또는 리스트
        filetype: 파일 타입 (1: train, 2: test, etc.)
        use_chunk: 청크 단위 읽기 여부 (대용량 파일)
        
    Returns:
        성공 여부 (bool)
    """
    # 단일 문자열을 리스트로 변환
    if isinstance(file_sno_list, str):
        file_sno_list = [file_sno_list]
    
    logger.info("=" * 60)
    logger.info(f"ML 파이프라인 시작: {len(file_sno_list)}개 파일, filetype={filetype}")
    logger.info("=" * 60)
    
    # S3 핸들러 초기화
    handler = S3ParquetHandler()
    
    all_dfs = []
    failed_files = []
    
    # 모든 파일 로드
    for idx, file_sno in enumerate(file_sno_list, 1):
        logger.info(f"\n[{idx}/{len(file_sno_list)}] 파일 로드 시작: {file_sno}")
        
        # S3 경로 획득
        s3_path = get_s3_route(file_sno, filetype)
        logger.info(f"  S3 경로: {s3_path}")
        
        # S3에서 Parquet 파일을 메모리로 로드
        if use_chunk:
            df = handler.get_parquet_chunk(s3_path)
        else:
            df = handler.get_parquet_from_s3(s3_path)
        
        if df is None:
            logger.error(f"  ❌ 파일 로드 실패: {file_sno}")
            failed_files.append(file_sno)
            continue
        
        # 메모리에 로드된 데이터프레임 정보 출력
        logger.info(f"  ✅ 로드 완료 - 형태: {df.shape}, 메모리: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        all_dfs.append((file_sno, df))
    
    if not all_dfs:
        logger.error("모든 파일 로드 실패, 파이프라인 중단")
        return False
    
    logger.info(f"\n총 {len(all_dfs)}개 파일 로드 성공, {len(failed_files)}개 실패")
    
    # 로드된 모든 파일로 학습 수행
    file_sno_success = [file_sno for file_sno, _ in all_dfs]
    train(file_sno_success)
    
    # 로드된 모든 파일로 추론 수행
    inference(file_sno_success)
    
    logger.info("=" * 60)
    logger.info(f"ML 파이프라인 완료: {len(file_sno_success)}개 성공")
    logger.info("=" * 60)
    
    return len(failed_files) == 0


# ============================================================================
# 고급 예제: 데이터 전처리와 함께 처리
# ============================================================================

def process_with_preprocessing(file_sno_list: list[str] | str, filetype: int = 1):
    """
    S3에서 파일들을 로드하고 데이터 전처리를 수행한 후 학습/추론
    
    Args:
        file_sno_list: 파일 시리얼 번호 또는 리스트
        filetype: 파일 타입
    """
    # 단일 문자열을 리스트로 변환
    if isinstance(file_sno_list, str):
        file_sno_list = [file_sno_list]
    
    logger.info(f"데이터 전처리 포함 파이프라인 시작: {len(file_sno_list)}개 파일")
    
    handler = S3ParquetHandler()
    all_processed_dfs = []
    
    for idx, file_sno in enumerate(file_sno_list, 1):
        logger.info(f"\n[{idx}/{len(file_sno_list)}] 파일 처리: {file_sno}")
        
        s3_path = get_s3_route(file_sno, filetype)
        
        # 메모리에서 로드
        df = handler.get_parquet_from_s3(s3_path)
        if df is None:
            logger.error(f"파일 로드 실패: {file_sno}")
            continue
        
        # 데이터 전처리 예제
        logger.info("  데이터 전처리 시작")
        
        # 결측치 처리
        original_len = len(df)
        df = df.dropna()
        logger.info(f"    결측치 제거: {original_len} → {len(df)}")
        
        # 이상치 처리 (예: IQR 방식)
        if 'value' in df.columns:
            Q1 = df['value'].quantile(0.25)
            Q3 = df['value'].quantile(0.75)
            IQR = Q3 - Q1
            original_len = len(df)
            df = df[(df['value'] >= Q1 - 1.5 * IQR) & (df['value'] <= Q3 + 1.5 * IQR)]
            logger.info(f"    이상치 제거: {original_len} → {len(df)}")
        
        # 정규화 예제
        if 'features' in df.columns:
            df['features_normalized'] = (df['features'] - df['features'].mean()) / df['features'].std()
            logger.info("    특성 정규화 완료")
        
        logger.info("  데이터 전처리 완료")
        all_processed_dfs.append((file_sno, df))
    
    if not all_processed_dfs:
        logger.error("전처리할 파일이 없습니다")
        return False
    
    # 전처리된 모든 데이터로 학습/추론
    file_sno_success = [file_sno for file_sno, _ in all_processed_dfs]
    train(file_sno_success)
    inference(file_sno_success)
    
    return True


# ============================================================================
# 배치 처리: 여러 파일을 순차적으로 처리
# ============================================================================

def process_batch_files(file_sno_list: list[str], filetype: int = 1):
    """
    여러 파일을 배치로 처리
    
    Args:
        file_sno_list: 파일 시리얼 번호 리스트
        filetype: 파일 타입
    """
    logger.info(f"배치 처리 시작: {len(file_sno_list)}개 파일")
    
    success_count = 0
    for idx, file_sno in enumerate(file_sno_list, 1):
        logger.info(f"\n[{idx}/{len(file_sno_list)}] 파일 처리")
        if process_ml_pipeline(file_sno, filetype):
            success_count += 1
    
    logger.info(f"\n배치 처리 완료: {success_count}/{len(file_sno_list)} 성공")


# ============================================================================
# 사용 예제
# ============================================================================

if __name__ == "__main__":
    # 예제 1: 단일 파일 처리
    print("\n========== 예제 1: 단일 파일 처리 ==========")
    process_ml_pipeline(file_sno_list="FILE001", filetype=1)
    
    # 예제 2: 여러 파일 처리 (리스트)
    print("\n========== 예제 2: 여러 파일 처리 (리스트) ==========")
    process_ml_pipeline(file_sno_list=["FILE001", "FILE002", "FILE003"], filetype=1)
    
    # 예제 3: 대용량 파일 처리 (청크 단위)
    print("\n========== 예제 3: 대용량 파일 처리 (청크 단위, 리스트) ==========")
    process_ml_pipeline(file_sno_list=["FILE_LARGE_001", "FILE_LARGE_002"], filetype=1, use_chunk=True)
    
    # 예제 4: 데이터 전처리 포함 (리스트)
    print("\n========== 예제 4: 데이터 전처리 포함 (리스트) ==========")
    process_with_preprocessing(file_sno_list=["FILE004", "FILE005", "FILE006"], filetype=1)
    
    # 예제 5: 매우 많은 파일 배치 처리
    print("\n========== 예제 5: 매우 많은 파일 배치 처리 ==========")
    large_file_list = [f"FILE_{i:06d}" for i in range(1, 51)]  # 50개 파일
    process_batch_files(large_file_list, filetype=1)
