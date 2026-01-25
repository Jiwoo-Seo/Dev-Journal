# MLflow 공부

## 개요
MLflow는 머신러닝 라이프사이클을 관리하는 오픈소스 플랫폼이다. Databricks에서 개발되었으며, 실험 추적, 재현성, 모델 배포를 지원한다.

## 주요 컴포넌트
- **MLflow Tracking**: 실험, 런, 파라미터, 메트릭, 아티팩트 추적
- **MLflow Projects**: 코드, 데이터, 환경을 패키징하여 재현 가능한 실행
- **MLflow Models**: 다양한 프레임워크의 모델을 표준화된 형식으로 저장 및 서빙
- **MLflow Registry**: 모델 버전 관리 및 라이프사이클 관리

## 설치
```bash
pip install mlflow
```

## 기본 사용법

### 실험 설정
```python
import mlflow
mlflow.set_experiment("Experiment Name")
```

### 런 시작
```python
with mlflow.start_run():
    # 코드 실행
    pass
```

### 로깅
- **파라미터**: `mlflow.log_param(key, value)`
- **메트릭**: `mlflow.log_metric(key, value)`
- **아티팩트**: `mlflow.log_artifact(file_path)`
- **모델**: `mlflow.sklearn.log_model(model, artifact_path)`

## 결과 데이터 구조

MLflow UI (기본적으로 http://localhost:5000)에서 결과를 확인할 수 있다.

### 실험 (Experiment)
- 여러 런을 그룹화하는 컨테이너
- 이름, ID, 설명, 생성 시간 포함

### 런 (Run)
- 단일 실행 단위
- 각 런은 고유 ID, 시작/종료 시간, 상태 포함

### 파라미터 (Parameters)
- 모델 하이퍼파라미터나 설정 값
- 키-값 쌍으로 저장
- 예: `n_estimators: 100`, `max_depth: 10`

### 메트릭 (Metrics)
- 평가 지표나 성능 측정값
- 키-값 쌍으로 저장, 타임스탬프 포함
- 예: `accuracy: 0.95`
- 여러 값 로깅 가능 (학습 곡선 등)

### 아티팩트 (Artifacts)
- 파일이나 디렉토리 (모델, 플롯, 데이터 등)
- S3, Azure Blob 등 클라우드 스토리지 지원
- 예: 모델 pickle 파일, 평가 리포트 CSV, 플롯 이미지

### 태그 (Tags)
- 런에 메타데이터 추가
- 예: `model_type: random_forest`, `dataset: iris`

## UI에서 보는 결과
- **실험 목록**: 모든 실험과 최근 런 표시
- **런 상세**: 파라미터, 메트릭, 아티팩트 탭
- **비교**: 여러 런의 메트릭 비교 차트
- **검색 및 필터링**: 쿼리로 런 필터링

## 고급 기능
- **모델 서빙**: `mlflow models serve`로 REST API로 모델 서빙
- **배치 추론**: `mlflow models predict`로 배치 예측
- **모델 레지스트리**: 프로덕션 모델 버전 관리
- **플러그인**: 커스텀 로깅, 스토리지 백엔드

## 장점
- 프레임워크 독립적 (TensorFlow, PyTorch, scikit-learn 등 지원)
- 로컬 및 분산 환경 지원
- 팀 협업 용이
- 재현성 보장

## 주의사항
- 대용량 아티팩트는 클라우드 스토리지 사용
- 민감한 데이터 로깅 피하기
- 실험 정리 (불필요한 런 삭제)
- 버전 관리와 함께 사용

## 실행 방법
1. `mlflow ui` 명령으로 UI 시작
2. 브라우저에서 http://localhost:5000 접속
3. 예제 코드 실행 후 결과 확인