import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import joblib
import os

# 경로 설정 (컨테이너 내부 마운트 경로 기준)
DATA_PATH = '/app/data'

def main():
    print("[Researcher 1] 데이터 로딩 중...")
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'train.csv'))
    except FileNotFoundError:
        print("Error: train.csv 파일을 찾을 수 없습니다. data 폴더를 확인하세요.")
        return

    # 1. 데이터 전처리
    # 범주형 데이터 변환 (Extracurricular Activities: Yes/No -> 1/0)
    le = LabelEncoder()
    if 'Extracurricular Activities' in df.columns:
        df['Extracurricular Activities'] = le.fit_transform(df['Extracurricular Activities'])

    # X, y 분리
    target = 'Performance Index'
    X = df.drop(columns=[target])
    y = df[target]

    # 학습/검증 데이터 분리
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. 모델링 (선형 회귀)
    print("[Researcher 1] 모델 학습 중...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 3. 성능 평가
    predictions = model.predict(X_val)
    rmse = mean_squared_error(y_val, predictions, squared=False)
    print(f"[Researcher 1] 모델 성능 (RMSE): {rmse:.4f}")

    # 4. 모델 저장 (공유 볼륨인 /app/data 에 저장)
    model_save_path = os.path.join(DATA_PATH, 'model.pkl')
    joblib.dump(model, model_save_path)
    print(f"[Researcher 1] 모델이 저장되었습니다: {model_save_path}")

if __name__ == "__main__":
    main()