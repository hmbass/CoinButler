FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# curl 설치 (healthcheck용)
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pip 업그레이드 및 SSL 문제 해결
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# 애플리케이션 파일 복사
COPY upbit_auto_trading_bot_v5.py .
COPY templates/ templates/

# 포트 노출
EXPOSE 5000

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 애플리케이션 실행
CMD ["python", "upbit_auto_trading_bot_v5.py"] 