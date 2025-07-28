# Railway에서 업비트 API IP 설정 가이드

## 문제 상황
Railway는 동적 IP를 사용하므로 업비트 API의 IP 화이트리스트 설정이 어려움

## 해결 방법

### 1. 업비트 API IP 화이트리스트 설정

#### A. Railway IP 범위 확인
Railway는 AWS 인프라를 사용하므로 AWS의 IP 범위를 확인해야 합니다.

**AWS IP 범위 확인 방법:**
```bash
# AWS IP 범위 다운로드
curl -o aws-ip-ranges.json https://ip-ranges.amazonaws.com/ip-ranges.json

# Railway이 사용하는 리전의 IP 범위 추출
# 보통 us-east-1, us-west-2, eu-west-1 등을 사용
```

#### B. 업비트 API 설정
1. 업비트 웹사이트 로그인
2. API 관리 → IP 주소 등록
3. 다음 IP 범위들을 추가:
   - `0.0.0.0/0` (모든 IP 허용 - 보안상 권장하지 않음)
   - 또는 AWS IP 범위들

### 2. 동적 IP 자동 업데이트 스크립트

#### A. IP 확인 스크립트 생성
```python
import requests
import json
import time
import os

def get_current_ip():
    """현재 Railway 인스턴스의 외부 IP 확인"""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except:
        return None

def update_upbit_ip_whitelist(ip):
    """업비트 API IP 화이트리스트 업데이트 (수동)"""
    print(f"현재 IP: {ip}")
    print("업비트 웹사이트에서 다음 IP를 화이트리스트에 추가하세요:")
    print(f"IP: {ip}")
    print("업비트 → API 관리 → IP 주소 등록")

def main():
    while True:
        current_ip = get_current_ip()
        if current_ip:
            update_upbit_ip_whitelist(current_ip)
        
        # 1시간마다 IP 확인
        time.sleep(3600)

if __name__ == "__main__":
    main()
```

#### B. Dockerfile에 IP 확인 스크립트 추가
```dockerfile
# IP 확인 스크립트 추가
COPY ip_checker.py /app/ip_checker.py
RUN chmod +x /app/ip_checker.py

# 시작 시 IP 확인
CMD ["sh", "-c", "python /app/ip_checker.py & python upbit_auto_trading_bot_v5.py"]
```

### 3. 보안 권장사항

#### A. API 키 권한 최소화
- 읽기 권한만 필요한 경우 쓰기 권한 제거
- 거래 금액 제한 설정
- 일일 거래 한도 설정

#### B. 모니터링 설정
- 텔레그램 알림 활성화
- 거래 로그 모니터링
- 비정상 거래 감지

### 4. 대안 플랫폼 고려

#### A. 고정 IP 제공 플랫폼
- **VPS 서비스**: DigitalOcean, Linode, Vultr
- **클라우드 서비스**: AWS EC2, Google Cloud, Azure
- **전용 서버**: 고정 IP 보장

#### B. 프록시 서비스
- **Cloudflare**: 고정 IP 제공
- **AWS API Gateway**: 고정 엔드포인트

### 5. Railway 특화 설정

#### A. 환경변수 설정
```bash
# Railway 대시보드에서 설정
RAILWAY_STATIC_URL=https://your-app.railway.app
ENABLE_IP_CHECK=true
IP_CHECK_INTERVAL=3600
```

#### B. 헬스체크 엔드포인트 추가
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'ip': get_current_ip(),
        'timestamp': datetime.now().isoformat()
    }
```

## 결론

Railway에서 업비트 API를 사용할 때는:
1. **AWS IP 범위를 업비트 화이트리스트에 추가**
2. **동적 IP 모니터링 스크립트 구현**
3. **보안 설정 강화**
4. **필요시 고정 IP 제공 플랫폼으로 마이그레이션 고려**

이 방법들을 통해 Railway에서도 안전하게 업비트 API를 사용할 수 있습니다. 