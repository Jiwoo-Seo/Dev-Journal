# Java Optional과 PostgreSQL SQL Functions/Arrays 공부

## Java Optional

### 개요
`Optional`은 Java 8에서 도입된 클래스로, null 값 처리를 위한 컨테이너.
NullPointerException을 방지하고, 코드의 가독성과 안정성을 높인다.

### 기본 개념
- **Optional.empty()**: 빈 Optional 생성
- **Optional.of(value)**: null이 아닌 값으로 Optional 생성
- **Optional.ofNullable(value)**: null일 수 있는 값으로 Optional 생성

### 주요 메서드
- **isPresent()**: 값이 존재하는지 확인
- **isEmpty()**: 값이 비어있는지 확인 (Java 11+)
- **get()**: 값 가져오기 (값이 없으면 예외)
- **orElse(defaultValue)**: 값이 없으면 기본값 반환
- **orElseGet(supplier)**: 값이 없으면 Supplier 실행 결과 반환
- **orElseThrow(exceptionSupplier)**: 값이 없으면 예외 발생
- **map(function)**: 값이 있으면 함수 적용
- **flatMap(function)**: 값이 있으면 함수 적용 (중첩 Optional 평탄화)
- **filter(predicate)**: 조건에 맞는 값만 유지
- **ifPresent(consumer)**: 값이 있으면 Consumer 실행

### 장점
- 명시적 null 처리
- 함수형 프로그래밍 스타일
- 체이닝 가능

### 주의사항
- 필드로 사용하지 말 것 (Serializable하지 않음)
- 매개변수나 반환값으로만 사용
- Optional을 Optional로 감싸지 말 것



## PostgreSQL SQL Functions

### 개요
PostgreSQL은 다양한 내장 SQL 함수를 제공. 문자열, 수학, 날짜, 집계 함수 등

### 주요 함수 카테고리
- **문자열 함수**: UPPER(), LOWER(), LENGTH(), CONCAT(), SUBSTRING()
- **수학 함수**: ABS(), ROUND(), CEIL(), FLOOR(), POWER()
- **날짜/시간 함수**: CURRENT_DATE, CURRENT_TIME, EXTRACT(), DATE_TRUNC()
- **집계 함수**: COUNT(), SUM(), AVG(), MAX(), MIN()
- **윈도우 함수**: ROW_NUMBER(), RANK(), LAG(), LEAD()

### 사용자 정의 함수
PL/pgSQL을 사용하여 사용자 정의 함수를 만들 수 있다.

```sql
CREATE OR REPLACE FUNCTION function_name(params) RETURNS return_type AS $$
BEGIN
    -- 로직
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

## PostgreSQL Arrays

### 소개
PostgreSQL의 배열 타입. 동일한 타입의 여러 값을 하나의 컬럼에 저장할 수 있다.

### 배열 생성
- **ARRAY[1, 2, 3]**: 리터럴로 배열 생성
- **'{1, 2, 3}'**: 문자열로 배열 생성
- **array_append(array, element)**: 요소 추가
- **array_remove(array, element)**: 요소 제거

### 배열 연산
- **array[index]**: 요소 접근 (1-based)
- **ARRAY_LENGTH(array, dimension)**: 배열 길이
- **array[lower:upper]**: 슬라이스
- **ANY(array)**: 배열에 값이 포함되는지 확인
- **&&**: 배열 교집합 확인
- **@>**: 포함 관계 확인

### 집계 함수
- **SUM()**, **AVG()**: 숫자 배열에 적용 가능

### 인덱스
- **GIN 인덱스**: 배열 검색 최적화

### 장점
- 복잡한 데이터 구조를 간단히 저장
- JSON보다 효율적 (특정 시나리오)
- 풍부한 연산자 지원

### 주의사항
- 배열 크기 제한 (1GB)
- 인덱스 생성 시 GIN 사용
- 복잡한 쿼리에서 성능 고려
