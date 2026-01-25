# Airflow 공부

## 개요
Apache Airflow는 워크플로우를 프로그래밍 방식으로 작성, 스케줄링 및 모니터링할 수 있는 오픈소스 플랫폼입니다. 복잡한 데이터 파이프라인을 관리하는 데 유용합니다.

## 설치 방법
```bash
pip install apache-airflow
```

## 기본 요소
- **DAG (Directed Acyclic Graph)**: 작업의 의존성과 실행 순서를 정의하는 그래프. 사이클이 없어야 합니다.
- **Task**: DAG 내의 개별 작업 단위. Operator를 사용하여 정의합니다.
- **Operator**: 작업의 유형을 정의하는 클래스. 예를 들어:
  - BashOperator: Bash 명령 실행
  - PythonOperator: Python 함수 실행
  - 다른 Operator들: EmailOperator, HttpOperator 등

## 실행 방법
1. Airflow 데이터베이스 초기화: `airflow db init`
2. 웹 서버 시작: `airflow webserver --port 8080`
3. 스케줄러 시작: `airflow scheduler`
4. 브라우저에서 http://localhost:8080 으로 접속하여 DAG를 확인하고 실행할 수 있습니다.
