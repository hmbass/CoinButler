# 업비트 자동 거래 봇 v1.0.0

업비트 API를 활용한 자동 거래 봇입니다. Docker Compose를 통해 쉽게 배포하고 관리할 수 있으며, GitHub Actions를 통한 자동 배포를 지원합니다.

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/yourusername/upbit-trading-bot)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/upbit-trading-bot)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/upbit-trading-bot)

## 🚀 주요 기능

- **자동 매매**: 상위 10개 마켓 모니터링 및 자동 거래
- **리스크 관리**: 일일 손실 한도 설정 및 자동 정지
- **실시간 대시보드**: 웹 기반 실시간 거래 현황 모니터링
- **텔레그램 알림**: 거래 실행 및 에러 알림
- **시간 제한**: 지정된 시간대에만 거래 실행
- **Docker 지원**: 컨테이너화된 배포

## 📋 요구사항

- Docker & Docker Compose
- 업비트 API 키 (읽기/쓰기 권한)
- 텔레그램 봇 토큰 (선택사항)

## 🚀 빠른 배포

### 원클릭 배포 (권장)
위의 배포 버튼 중 하나를 클릭하여 클라우드에 바로 배포하세요:

- **Railway** (무료 티어 제공)
- **Render** (무료 티어 제공)  
- **Heroku** (무료 티어 제공)

### GitHub Actions 자동 배포
1. 이 저장소를 포크하거나 클론
2. GitHub Secrets에 환경변수 설정
3. main 브랜치에 푸시하면 자동 배포

## 🛠️ 로컬 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/upbit-trading-bot.git
cd upbit-trading-bot
```

### 2. 환경변수 설정
```bash
cp env.example .env
```

`.env` 파일을 편집하여 다음 정보를 입력하세요:

```env
# 업비트 API 설정 (필수)
UPBIT_ACCESS_KEY=your_upbit_access_key_here
UPBIT_SECRET_KEY=your_upbit_secret_key_here

# 텔레그램 알림 설정 (선택사항)
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

### 3. Docker Compose로 실행
```bash
docker-compose up -d
```

### 4. 대시보드 접속
브라우저에서 `http://localhost:5000`으로 접속하여 대시보드를 확인하세요.

## 📊 대시보드 기능

- **실시간 거래 현황**: 총 손익, 거래 횟수, 마지막 업데이트 시간
- **거래 내역**: 최근 10건의 거래 기록
- **계좌 잔고**: 현재 보유 자산 현황
- **자동 새로고침**: 30초마다 자동으로 데이터 업데이트

## ⚙️ 설정 옵션

`upbit_auto_trading_bot_v5.py` 파일에서 다음 설정을 변경할 수 있습니다:

```python
# 거래 설정
TRADE_AMOUNT = 50000        # 거래 금액 (원)
TAKE_PROFIT = 0.03          # 수익률 (3%)
STOP_LOSS = -0.02           # 손실률 (-2%)
DAILY_LOSS_LIMIT = -50000   # 일일 손실 한도 (원)

# 모니터링 시간 (24시간 형식)
MONITORING_HOURS = [(9, 11), (21, 24)]  # 오전 9-11시, 오후 9-12시

# 업데이트 간격 (초)
INTERVAL = 60
```

## ☁️ 클라우드 배포 가이드

### Railway 배포 (무료)
1. [Railway](https://railway.app)에 가입
2. "Deploy from GitHub repo" 선택
3. 이 저장소 연결
4. 환경변수 설정:
   - `UPBIT_ACCESS_KEY`
   - `UPBIT_SECRET_KEY`
   - `TELEGRAM_TOKEN` (선택사항)
   - `TELEGRAM_CHAT_ID` (선택사항)

### Render 배포 (무료)
1. [Render](https://render.com)에 가입
2. "New Web Service" 선택
3. GitHub 저장소 연결
4. 환경변수 설정
5. 자동 배포 활성화

### Heroku 배포 (무료)
1. [Heroku](https://heroku.com)에 가입
2. "Create new app" 선택
3. GitHub 저장소 연결
4. 환경변수 설정
5. 자동 배포 활성화

## 🔧 관리 명령어

### 로컬 Docker 관리
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f trading-bot

# 컨테이너 재시작
docker-compose restart trading-bot

# 컨테이너 중지
docker-compose down
```

### 클라우드 로그 확인
```bash
# Railway
railway logs

# Render
render logs

# Heroku
heroku logs --tail
```

## 📈 거래 전략

현재 구현된 거래 전략:

1. **마켓 선택**: 거래량 기준 상위 10개 KRW 마켓
2. **매수 조건**: 랜덤 확률 기반 (1% 확률)
3. **매도 조건**: 
   - 수익률 3% 이상 시 수익 실현
   - 손실률 -2% 이하 시 손절
4. **리스크 관리**: 일일 손실 한도 도달 시 자동 정지

## ⚠️ 주의사항

- **투자 위험**: 암호화폐 거래는 높은 위험을 수반합니다
- **API 키 보안**: API 키는 절대 공개하지 마세요
- **테스트 환경**: 실제 거래 전 충분한 테스트를 권장합니다
- **모니터링**: 정기적으로 봇 상태를 확인하세요

## 🐛 문제 해결

### 일반적인 문제들

1. **API 키 오류**
   - 업비트 API 키가 올바른지 확인
   - 읽기/쓰기 권한이 있는지 확인

2. **텔레그램 알림이 오지 않는 경우**
   - 봇 토큰과 채팅 ID가 올바른지 확인
   - 봇을 채팅방에 초대했는지 확인

3. **거래가 실행되지 않는 경우**
   - 모니터링 시간인지 확인
   - 계좌 잔고가 충분한지 확인
   - 일일 손실 한도에 도달하지 않았는지 확인

### 로그 확인
```bash
docker-compose logs trading-bot
```

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다. 실제 투자에 사용하기 전에 충분한 검토와 테스트를 거쳐주세요.

## 🔐 GitHub Secrets 설정

GitHub Actions 자동 배포를 위해 다음 Secrets를 설정하세요:

### Railway Secrets
- `RAILWAY_TOKEN`: Railway API 토큰

### Render Secrets  
- `RENDER_TOKEN`: Render API 토큰
- `RENDER_SERVICE_ID`: Render 서비스 ID

### Heroku Secrets
- `HEROKU_API_KEY`: Heroku API 키
- `HEROKU_APP_NAME`: Heroku 앱 이름
- `HEROKU_EMAIL`: Heroku 계정 이메일

### 설정 방법
1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. 위의 Secrets 추가

## 🤝 기여

버그 리포트나 기능 제안은 이슈를 통해 제출해주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**⚠️ 투자 경고**: 암호화폐 거래는 높은 위험을 수반합니다. 투자 결정은 신중하게 하시기 바랍니다. 