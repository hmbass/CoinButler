#!/bin/bash

# GitHub 저장소 설정 스크립트

echo "🚀 GitHub 저장소 설정을 시작합니다..."
echo "================================"

# Git 초기화 확인
if [ ! -d ".git" ]; then
    echo "📦 Git 저장소를 초기화합니다..."
    git init
else
    echo "✅ Git 저장소가 이미 초기화되어 있습니다."
fi

# 사용자 정보 입력
echo ""
echo "Git 사용자 정보를 입력해주세요:"
read -p "GitHub 사용자명: " GITHUB_USERNAME
read -p "GitHub 이메일: " GITHUB_EMAIL

# Git 설정
git config user.name "$GITHUB_USERNAME"
git config user.email "$GITHUB_EMAIL"

echo ""
echo "📝 변경사항을 커밋합니다..."

# 모든 파일 추가
git add .

# 초기 커밋
git commit -m "🎉 Initial commit: Upbit Trading Bot v1.0.0

- 완전한 업비트 자동 거래 봇 기능
- 실시간 웹 대시보드
- 텔레그램 알림 시스템
- Docker 컨테이너화
- GitHub Actions 자동 배포
- 다중 클라우드 플랫폼 지원
- 리스크 관리 시스템"

echo ""
echo "✅ 초기 커밋이 완료되었습니다!"
echo ""
echo "📋 다음 단계:"
echo "1. GitHub에서 새 저장소 생성: https://github.com/new"
echo "2. 저장소 이름: upbit-trading-bot"
echo "3. Public 또는 Private 선택"
echo "4. README, .gitignore, license 추가하지 않음 (이미 있음)"
echo "5. 저장소 생성 후 다음 명령어 실행:"
echo ""
echo "   git remote add origin https://github.com/$GITHUB_USERNAME/upbit-trading-bot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "6. GitHub Secrets 설정 (README 참조)"
echo "7. 클라우드 배포 버튼 사용 또는 GitHub Actions 자동 배포"
echo ""
echo "🎯 완료되면 자동으로 클라우드에 배포됩니다!" 