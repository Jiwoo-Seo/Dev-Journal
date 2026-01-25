# Spring WebFlux 공부

## 개요
Spring WebFlux는 Spring Framework 5에서 도입된 반응형 웹 프레임워크이다. 비차단, 이벤트 기반의 프로그래밍 모델을 제공하며, Reactor 라이브러리를 기반으로 한다. 전통적인 서블릿 기반 Spring MVC와 달리, Netty나 Undertow 같은 비차단 서버를 사용한다.

## 주요 개념
- **반응형 프로그래밍 (Reactive Programming)**: 데이터 스트림과 변경 전파에 중점을 둔 프로그래밍 패러다임
- **Mono와 Flux**: Reactor의 핵심 타입
  - **Mono**: 0 또는 1개의 요소를 방출하는 Publisher
  - **Flux**: 0개 이상의 요소를 방출하는 Publisher
- **비차단 (Non-blocking)**: 스레드를 블로킹하지 않고 I/O 작업 처리
- **백프레셔 (Backpressure)**: 생산자와 소비자 간의 데이터 흐름 제어

## 기본 사용법
- **의존성**: Spring Boot에서 `spring-boot-starter-webflux` 추가
- **컨트롤러**: `@RestController`와 `@RequestMapping` 사용
- **반응형 타입**: Mono와 Flux를 반환 타입으로 사용
- **연산자**: map, flatMap, filter 등으로 데이터 변환

### 주요 패턴
- **Mono.just()**: 단일 값 생성
- **Flux.fromIterable()**: 컬렉션에서 Flux 생성
- **map()**: 요소 변환
- **flatMap()**: 비동기 변환
- **subscribe()**: 구독하여 실행

## 장점
- 높은 동시성 처리
- 낮은 메모리 사용량
- 마이크로서비스 아키텍처에 적합
- 함수형 프로그래밍 스타일

## 단점
- 학습 곡선이 가파름
- 디버깅이 어려움
- 모든 라이브러리가 반응형을 지원하지 않음

## Spring MVC vs WebFlux
- **Spring MVC**: 서블릿 기반, 블로킹 I/O, 스레드 풀 사용
- **WebFlux**: 반응형 기반, 비차단 I/O, 이벤트 루프 사용

## 외부 API 호출
WebFlux에서 외부 API를 호출할 때는 `WebClient`를 사용한다. 이는 비차단 HTTP 클라이언트로, Mono/Flux와 자연스럽게 통합된다.

### WebClient 기본 사용법
- **생성**: `WebClient.create(baseUrl)` 또는 `WebClient.builder().build()`
- **요청**: `webClient.get().uri(uri).retrieve().bodyToMono(Class.class)`
- **응답 처리**: Mono/Flux로 비동기 처리

### 장점
- 비차단 I/O로 효율적
- Reactor 연산자와 결합 가능
- 에러 처리와 재시도 로직 쉽게 추가

### 주의사항
- WebClient는 Spring 5부터 제공되며, 별도 의존성 필요 없음
- 타임아웃, 헤더 설정 등 다양한 옵션 지원
- 마이크로서비스 간 통신에 유용
