#!/bin/bash

# 업비트 자동 거래 봇 로컬 실행 스크립트

echo "🤖 업비트 자동 거래 봇 v5 (로컬 실행)"
echo "================================"

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되지 않았습니다."
    echo "https://www.python.org/downloads/ 에서 Python을 설치해주세요."
    exit 1
fi

# 가상환경 생성 및 활성화
if [ ! -d "venv" ]; then
    echo "📦 가상환경을 생성합니다..."
    python3 -m venv venv
fi

echo "🔧 가상환경을 활성화합니다..."
source venv/bin/activate

# 의존성 설치
echo "📚 필요한 패키지를 설치합니다..."
pip install -r requirements.txt

# 환경변수 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다."
    echo "env.example을 복사하여 .env 파일을 생성하고 설정을 입력해주세요."
    echo "cp env.example .env"
    exit 1
fi

# 환경변수 로드
export $(cat .env | xargs)

echo "✅ 환경 설정 완료"
echo "🚀 거래 봇을 시작합니다..."
echo "🌐 대시보드: http://localhost:5000"
echo "🛑 중지하려면 Ctrl+C를 누르세요"

# 애플리케이션 실행
python3 upbit_auto_trading_bot_v5.py 