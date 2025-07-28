#!/usr/bin/env python3
"""
Railway IP Checker for Upbit API
Railway 인스턴스의 현재 IP를 확인하고 업비트 API 설정을 도와주는 스크립트
"""

import requests
import json
import time
import os
import logging
from datetime import datetime
from typing import Optional

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ip_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RailwayIPChecker:
    def __init__(self):
        self.last_ip = None
        self.check_interval = int(os.getenv('IP_CHECK_INTERVAL', 3600))  # 기본 1시간
        self.enable_notifications = os.getenv('ENABLE_IP_CHECK', 'true').lower() == 'true'
        
    def get_current_ip(self) -> Optional[str]:
        """현재 Railway 인스턴스의 외부 IP 확인"""
        try:
            # 여러 IP 확인 서비스 사용 (백업용)
            services = [
                'https://api.ipify.org?format=json',
                'https://httpbin.org/ip',
                'https://ipinfo.io/json'
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if 'ip' in data:
                            return data['ip']
                        elif 'origin' in data:
                            return data['origin']
                except Exception as e:
                    logger.warning(f"IP 확인 서비스 {service} 실패: {e}")
                    continue
            
            logger.error("모든 IP 확인 서비스 실패")
            return None
            
        except Exception as e:
            logger.error(f"IP 확인 중 오류 발생: {e}")
            return None
    
    def get_ip_info(self, ip: str) -> dict:
        """IP 정보 상세 조회"""
        try:
            response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.warning(f"IP 정보 조회 실패: {e}")
        
        return {}
    
    def log_ip_change(self, new_ip: str, ip_info: dict = None):
        """IP 변경 로그 기록"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = {
            'timestamp': timestamp,
            'ip': new_ip,
            'ip_info': ip_info or {},
            'previous_ip': self.last_ip
        }
        
        # 로그 파일에 저장
        with open('ip_changes.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        logger.info(f"IP 변경 감지: {self.last_ip} → {new_ip}")
        if ip_info:
            logger.info(f"IP 정보: {ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}, {ip_info.get('org', 'N/A')}")
    
    def print_upbit_setup_instructions(self, ip: str):
        """업비트 API 설정 안내 출력"""
        print("\n" + "="*60)
        print("🚀 업비트 API IP 화이트리스트 설정 안내")
        print("="*60)
        print(f"현재 Railway IP: {ip}")
        print("\n📋 설정 방법:")
        print("1. 업비트 웹사이트 로그인")
        print("2. 마이페이지 → API 관리")
        print("3. IP 주소 등록에서 다음 IP 추가:")
        print(f"   → {ip}")
        print("\n⚠️  보안 권장사항:")
        print("- API 키 권한을 최소화하세요 (필요한 권한만)")
        print("- 거래 금액 제한을 설정하세요")
        print("- 정기적으로 IP 변경을 모니터링하세요")
        print("="*60)
    
    def send_telegram_notification(self, ip: str, ip_info: dict = None):
        """텔레그램 알림 전송 (선택사항)"""
        telegram_token = os.getenv('TELEGRAM_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not (telegram_token and telegram_chat_id):
            return
        
        try:
            message = f"🚨 Railway IP 변경 알림\n\n"
            message += f"새로운 IP: {ip}\n"
            if ip_info:
                message += f"위치: {ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}\n"
                message += f"ISP: {ip_info.get('org', 'N/A')}\n"
            message += f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            message += "업비트 API 화이트리스트에 추가해주세요!"
            
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            data = {
                'chat_id': telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                logger.info("텔레그램 알림 전송 성공")
            else:
                logger.warning(f"텔레그램 알림 전송 실패: {response.status_code}")
                
        except Exception as e:
            logger.error(f"텔레그램 알림 전송 오류: {e}")
    
    def run(self):
        """메인 실행 함수"""
        logger.info("Railway IP Checker 시작")
        logger.info(f"체크 간격: {self.check_interval}초")
        
        while True:
            try:
                current_ip = self.get_current_ip()
                
                if current_ip:
                    # IP 변경 감지
                    if current_ip != self.last_ip:
                        ip_info = self.get_ip_info(current_ip)
                        self.log_ip_change(current_ip, ip_info)
                        self.print_upbit_setup_instructions(current_ip)
                        
                        if self.enable_notifications:
                            self.send_telegram_notification(current_ip, ip_info)
                        
                        self.last_ip = current_ip
                    else:
                        logger.info(f"IP 변경 없음: {current_ip}")
                else:
                    logger.error("IP 확인 실패")
                
                # 대기
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("IP Checker 종료")
                break
            except Exception as e:
                logger.error(f"예상치 못한 오류: {e}")
                time.sleep(60)  # 오류 시 1분 대기

def main():
    """메인 함수"""
    checker = RailwayIPChecker()
    
    # 즉시 첫 번째 IP 확인
    current_ip = checker.get_current_ip()
    if current_ip:
        ip_info = checker.get_ip_info(current_ip)
        checker.print_upbit_setup_instructions(current_ip)
        checker.last_ip = current_ip
    
    # 지속적인 모니터링 시작
    checker.run()

if __name__ == "__main__":
    main() 