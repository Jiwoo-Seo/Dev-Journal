# FastAPI 공부

## 개요
FastAPI는 Python으로 빠르고 현대적인 웹 API를 구축하기 위한 프레임워크이다. 자동 API 문서화, 타입 힌팅 지원, 비동기 처리 등으로 유명함. Starlette과 Pydantic 라이브러리를 기반으로 작동.

## 설치
```bash
pip install fastapi uvicorn
```

## 실행
```bash
uvicorn main:app --reload
```
- `main`은 파일 이름 (fastapi_example.py라면 `fastapi_example:app`)
- `--reload`는 개발 시 코드 변경 시 자동 재시작

## 기본 개념
- **FastAPI 인스턴스**: `app = FastAPI()` - 애플리케이션 객체 생성
- **경로 연산자 (Path Operations)**: `@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()` 등으로 HTTP 메서드 정의
- **경로 매개변수 (Path Parameters)**: URL 경로의 동적 부분, 예: `/items/{item_id}`
- **쿼리 매개변수 (Query Parameters)**: URL의 ? 뒤에 오는 파라미터, 함수 파라미터로 정의
- **요청 본문 (Request Body)**: POST 등에서 JSON 데이터를 받을 때 Pydantic 모델 사용
- **응답 모델**: 함수의 return 타입 힌팅으로 자동 검증

## 예제
`app/` 
- `models/`: Pydantic 모델 (데이터 구조 정의)
- `services/`: 비즈니스 로직 (데이터 처리)
- `routers/`: API 엔드포인트 (컨트롤러 역할)
- `main.py`: FastAPI 앱 인스턴스 및 라우터 등록

실행: `uvicorn app.main:app --reload`

## 추가 기능
- **자동 문서화**: `/docs` (Swagger UI), `/redoc` (ReDoc)
- **비동기 지원**: `async def`로 비동기 함수 정의
- **의존성 주입**: `Depends()`로 재사용 가능한 로직
- **보안**: OAuth2, JWT 등 지원
- **테스트**: `TestClient`로 API 테스트

## 주의사항
- Pydantic 모델을 사용하여 데이터 검증 및 직렬화
- 타입 힌팅을 적극 활용하여 자동 문서화 및 검증
- 프로덕션 배포 시 Gunicorn + Uvicorn 사용 고려