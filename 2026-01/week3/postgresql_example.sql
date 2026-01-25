-- PostgreSQL SQL Functions and Arrays Example

-- 테이블 생성
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    tags TEXT[],
    scores INTEGER[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터 삽입
INSERT INTO users (name, tags, scores) VALUES
('Alice', ARRAY['developer', 'java'], ARRAY[85, 90, 88]),
('Bob', ARRAY['designer', 'ui'], ARRAY[92, 87]),
('Charlie', ARRAY['manager', 'team'], ARRAY[78, 82, 91, 85]);

-- SQL Functions 예제

-- 문자열 함수
SELECT name, UPPER(name) as upper_name, LENGTH(name) as name_length FROM users;

-- 날짜 함수
SELECT name, created_at, EXTRACT(YEAR FROM created_at) as year,
       DATE_TRUNC('month', created_at) as month_start FROM users;

-- 수학 함수
SELECT name, scores, AVG(scores) as avg_score, MAX(scores) as max_score FROM users;

-- 집계 함수
SELECT COUNT(*) as total_users, AVG(ARRAY_LENGTH(scores, 1)) as avg_score_count FROM users;

-- Arrays 예제

-- 배열 요소 접근
SELECT name, tags[1] as first_tag, scores[1] as first_score FROM users;

-- 배열 길이
SELECT name, ARRAY_LENGTH(tags, 1) as tag_count, ARRAY_LENGTH(scores, 1) as score_count FROM users;

-- 배열에 요소 추가
UPDATE users SET tags = array_append(tags, 'new_tag') WHERE name = 'Alice';

-- 배열에서 요소 제거
UPDATE users SET tags = array_remove(tags, 'java') WHERE name = 'Alice';

-- 배열 포함 확인
SELECT name FROM users WHERE 'developer' = ANY(tags);

-- 배열 슬라이스
SELECT name, scores[1:2] as first_two_scores FROM users;

-- 배열 집계
SELECT name, SUM(scores) as total_score, AVG(scores) as avg_score FROM users;

-- JSON 함수 (PostgreSQL 9.3+)
SELECT name, json_build_array(tags) as tags_json FROM users;

-- 사용자 정의 함수 예제
CREATE OR REPLACE FUNCTION calculate_average(arr INTEGER[]) RETURNS FLOAT AS $$
DECLARE
    total INTEGER := 0;
    count INTEGER := 0;
BEGIN
    FOREACH total IN ARRAY arr LOOP
        count := count + 1;
    END LOOP;
    IF count = 0 THEN
        RETURN 0;
    END IF;
    RETURN total::FLOAT / count;
END;
$$ LANGUAGE plpgsql;

-- 사용자 정의 함수 사용
SELECT name, calculate_average(scores) as custom_avg FROM users;

-- 인덱스 생성 (배열 컬럼용)
CREATE INDEX idx_users_tags ON users USING GIN (tags);
CREATE INDEX idx_users_scores ON users USING GIN (scores);

-- 쿼리 예제
SELECT name, tags FROM users WHERE tags && ARRAY['developer', 'manager'];