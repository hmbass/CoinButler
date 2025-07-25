#!/bin/bash

# 업비트 자동 거래 봇 실행 스크립트

echo "🤖 업비트 자동 거래 봇 v5"
echo "================================"

# 환경변수 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다."
    echo "env.example을 복사하여 .env 파일을 생성하고 설정을 입력해주세요."
    echo "cp env.example .env"
    exit 1
fi

# Docker 설치 확인
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되지 않았습니다."
    echo "https://docs.docker.com/get-docker/ 에서 Docker를 설치해주세요."
    exit 1
fi

# Docker Compose 설치 확인
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되지 않았습니다."
    echo "https://docs.docker.com/compose/install/ 에서 Docker Compose를 설치해주세요."
    exit 1
fi

echo "✅ 환경 확인 완료"

# 명령어 파라미터 처리
case "$1" in
    "start")
        echo "🚀 거래 봇을 시작합니다..."
        docker-compose up -d
        echo "✅ 거래 봇이 시작되었습니다."
        echo "🌐 대시보드: http://localhost:5000"
        echo "📊 로그 확인: docker-compose logs -f trading-bot"
        ;;
    "stop")
        echo "🛑 거래 봇을 중지합니다..."
        docker-compose down
        echo "✅ 거래 봇이 중지되었습니다."
        ;;
    "restart")
        echo "🔄 거래 봇을 재시작합니다..."
        docker-compose restart
        echo "✅ 거래 봇이 재시작되었습니다."
        ;;
    "logs")
        echo "📋 거래 봇 로그를 확인합니다..."
        docker-compose logs -f trading-bot
        ;;
    "status")
        echo "📊 거래 봇 상태를 확인합니다..."
        docker-compose ps
        ;;
    "build")
        echo "🔨 Docker 이미지를 빌드합니다..."
        docker-compose build --no-cache
        echo "✅ 빌드가 완료되었습니다."
        ;;
    "clean")
        echo "🧹 컨테이너와 이미지를 정리합니다..."
        docker-compose down --rmi all --volumes --remove-orphans
        echo "✅ 정리가 완료되었습니다."
        ;;
    *)
        echo "사용법: $0 {start|stop|restart|logs|status|build|clean}"
        echo ""
        echo "명령어:"
        echo "  start   - 거래 봇 시작"
        echo "  stop    - 거래 봇 중지"
        echo "  restart - 거래 봇 재시작"
        echo "  logs    - 로그 확인"
        echo "  status  - 상태 확인"
        echo "  build   - 이미지 빌드"
        echo "  clean   - 정리"
        echo ""
        echo "예시:"
        echo "  $0 start"
        echo "  $0 logs"
        ;;
esac 