#!/bin/bash

echo "🚀 Upbit Trading Bot v5 시작 중..."

# 환경변수 확인
echo "📋 환경변수 확인:"
echo "- UPBIT_ACCESS_KEY: ${UPBIT_ACCESS_KEY:+설정됨}"
echo "- UPBIT_SECRET_KEY: ${UPBIT_SECRET_KEY:+설정됨}"
echo "- TELEGRAM_TOKEN: ${TELEGRAM_TOKEN:+설정됨}"
echo "- TELEGRAM_CHAT_ID: ${TELEGRAM_CHAT_ID:+설정됨}"

# IP Checker 시작 (백그라운드)
echo "🔍 IP Checker 시작..."
python ip_checker.py &
IP_CHECKER_PID=$!

# 메인 애플리케이션 시작
echo "🤖 Trading Bot 시작..."
python upbit_auto_trading_bot_v5.py

# 프로세스 종료 시 IP Checker도 함께 종료
echo "🛑 프로세스 종료 중..."
kill $IP_CHECKER_PID 2>/dev/null || true 