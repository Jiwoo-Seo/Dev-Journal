import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.http.MediaType;
import java.util.List;
import java.util.Arrays;
import com.fasterxml.jackson.databind.JsonNode;

@RestController
@RequestMapping("/api")
public class WebFluxExampleController {

    private final WebClient webClient;

    public WebFluxExampleController() {
        this.webClient = WebClient.create("http://localhost:8000"); // FastAPI 서버 주소
    }

    // 간단한 Mono 예제
    @GetMapping("/hello")
    public Mono<String> hello() {
        return Mono.just("Hello, Spring WebFlux!");
    }

    // Flux 예제
    @GetMapping("/numbers")
    public Flux<Integer> getNumbers() {
        return Flux.fromIterable(Arrays.asList(1, 2, 3, 4, 5));
    }

    // 경로 변수와 Mono
    @GetMapping("/user/{id}")
    public Mono<String> getUser(@PathVariable String id) {
        return Mono.just("User ID: " + id);
    }

    // 쿼리 파라미터
    @GetMapping("/search")
    public Flux<String> search(@RequestParam String query) {
        List<String> results = Arrays.asList("Result1 for " + query, "Result2 for " + query);
        return Flux.fromIterable(results);
    }

    // POST 예제
    @PostMapping("/create")
    public Mono<String> createItem(@RequestBody Mono<String> item) {
        return item.map(i -> "Created: " + i);
    }

    // 비동기 처리 예제
    @GetMapping("/async")
    public Mono<String> asyncOperation() {
        return Mono.fromCallable(() -> {
            // 시뮬레이션: 비동기 작업
            Thread.sleep(1000);
            return "Async result";
        });
    }

    // 외부 API 호출 예제: FastAPI의 /items/ 엔드포인트 호출
    @GetMapping("/external/items")
    public Flux<JsonNode> getExternalItems() {
        return webClient.get()
                .uri("/items/")
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToFlux(JsonNode.class)
                .doOnNext(item -> System.out.println("Received item: " + item));
    }

    // 외부 API 호출 예제: 특정 아이템 조회
    @GetMapping("/external/items/{itemId}")
    public Mono<JsonNode> getExternalItem(@PathVariable int itemId) {
        return webClient.get()
                .uri("/items/{itemId}", itemId)
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .map(item -> {
                    // 파싱 예제: JSON에서 특정 필드 추출
                    String name = item.get("name").asText();
                    double price = item.get("price").asDouble();
                    return item; // 실제로는 가공된 데이터 반환
                });
    }

    // 외부 API에 POST 요청 예제
    @PostMapping("/external/create")
    public Mono<JsonNode> createExternalItem(@RequestBody JsonNode newItem) {
        return webClient.post()
                .uri("/items/")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(newItem)
                .retrieve()
                .bodyToMono(JsonNode.class);
    }
}