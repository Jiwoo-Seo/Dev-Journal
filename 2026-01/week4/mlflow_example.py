import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# MLflow 실험 설정
mlflow.set_experiment("Random Forest Classification Example")

# 샘플 데이터 생성
X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 하이퍼파라미터
n_estimators = 100
max_depth = 10

with mlflow.start_run():
    # 모델 생성 및 학습
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    # 예측 및 평가
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # MLflow에 파라미터 로깅
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # MLflow에 메트릭 로깅
    mlflow.log_metric("accuracy", accuracy)

    # 모델 저장
    mlflow.sklearn.log_model(model, "model")

    # 추가 아티팩트: 분류 리포트
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv("classification_report.csv")
    mlflow.log_artifact("classification_report.csv")

    print(f"Model accuracy: {accuracy}")
    print("Run completed. Check MLflow UI for results.")

# MLflow UI 실행 (터미널에서)
# mlflow ui

# 결과 데이터 확인
# - 실험: Random Forest Classification Example
# - 런: 각 실행에 대한 ID
# - 파라미터: n_estimators, max_depth
# - 메트릭: accuracy
# - 아티팩트: model (모델 파일), classification_report.csv