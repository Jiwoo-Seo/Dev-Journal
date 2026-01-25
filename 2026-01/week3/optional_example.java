import java.util.Optional;

public class OptionalExample {

    public static void main(String[] args) {
        // Optional 생성
        Optional<String> optionalValue = Optional.of("Hello");
        Optional<String> emptyOptional = Optional.empty();
        Optional<String> nullableOptional = Optional.ofNullable(null);

        // 값 존재 확인
        System.out.println("Is present: " + optionalValue.isPresent());
        System.out.println("Is empty: " + emptyOptional.isEmpty());

        // 값 가져오기
        if (optionalValue.isPresent()) {
            System.out.println("Value: " + optionalValue.get());
        }

        // orElse 사용
        String result1 = optionalValue.orElse("Default");
        String result2 = emptyOptional.orElse("Default");
        System.out.println("Result1: " + result1);
        System.out.println("Result2: " + result2);

        // orElseGet 사용
        String result3 = emptyOptional.orElseGet(() -> "Computed Default");
        System.out.println("Result3: " + result3);

        // orElseThrow 사용
        try {
            String result4 = emptyOptional.orElseThrow(() -> new RuntimeException("Value not present"));
        } catch (RuntimeException e) {
            System.out.println("Exception: " + e.getMessage());
        }

        // map 사용
        Optional<Integer> length = optionalValue.map(String::length);
        System.out.println("Length: " + length.orElse(0));

        // flatMap 사용
        Optional<Optional<String>> nested = Optional.of(Optional.of("Nested"));
        Optional<String> flattened = nested.flatMap(opt -> opt);
        System.out.println("Flattened: " + flattened.orElse("Empty"));

        // filter 사용
        Optional<String> filtered = optionalValue.filter(s -> s.length() > 3);
        System.out.println("Filtered: " + filtered.orElse("Filtered out"));

        // ifPresent 사용
        optionalValue.ifPresent(s -> System.out.println("Present: " + s));
        emptyOptional.ifPresent(s -> System.out.println("This won't print"));
    }

    // 메서드에서 Optional 반환
    public static Optional<String> findUser(String id) {
        if ("123".equals(id)) {
            return Optional.of("John Doe");
        }
        return Optional.empty();
    }
}