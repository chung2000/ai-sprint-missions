# Python 버전 고정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY train.py .

# 실행 명령어 (데이터 폴더는 docker-compose에서 마운트하므로 COPY하지 않음)
CMD ["python", "train.py"]