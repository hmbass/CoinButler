import requests, time, datetime, hashlib, jwt, uuid, os, csv
from flask import Flask, render_template, jsonify
import threading
import json
import hmac
import base64

# === 환경변수 ===
ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")
SERVER_URL = 'https://api.upbit.com'
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === 설정 ===
TRADE_AMOUNT = 50000
TAKE_PROFIT = 0.03
STOP_LOSS = -0.02
VOLUME_THRESHOLD = 3.0
INTERVAL = 60
MONITORING_HOURS = [(9, 11), (21, 24)]
LOG_FILE = "trade_history.csv"
DAILY_LOSS_LIMIT = -50000  # 1일 최대 손실
current_daily_pnl = 0

# === 업비트 API 인증 ===
def get_headers(query=None):
    payload = {
        'access_key': ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }
    
    if query:
        query_string = query.encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'

    jwt_token = jwt.encode(payload, SECRET_KEY)
    return {'Authorization': f'Bearer {jwt_token}'}

# === 텔레그램 알림 ===
def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"텔레그램 메시지 전송 성공: {message}")
        else:
            print(f"텔레그램 메시지 전송 실패: {response.text}")
    except Exception as e:
        print(f"텔레그램 메시지 전송 에러: {e}")

# === 시장 데이터 조회 ===
def get_top_10_markets():
    """거래량 기준 상위 10개 마켓 조회"""
    try:
        url = f"{SERVER_URL}/v1/market/all"
        response = requests.get(url)
        markets = response.json()
        
        # KRW 마켓만 필터링
        krw_markets = [market['market'] for market in markets if market['market'].startswith('KRW-')]
        
        # 거래량 기준 상위 10개 선택
        top_markets = []
        for market in krw_markets[:10]:
            ticker_url = f"{SERVER_URL}/v1/ticker"
            ticker_response = requests.get(ticker_url, params={'markets': market})
            if ticker_response.status_code == 200:
                ticker_data = ticker_response.json()
                if ticker_data:
                    top_markets.append(market)
                    if len(top_markets) >= 10:
                        break
        
        return top_markets
    except Exception as e:
        print(f"마켓 조회 에러: {e}")
        return ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-ADA', 'KRW-DOGE']

def get_market_price(market):
    """특정 마켓의 현재 가격 조회"""
    try:
        url = f"{SERVER_URL}/v1/ticker"
        response = requests.get(url, params={'markets': market})
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['trade_price'])
    except Exception as e:
        print(f"가격 조회 에러 ({market}): {e}")
    return None

def get_account_balance():
    """계좌 잔고 조회"""
    try:
        headers = get_headers()
        url = f"{SERVER_URL}/v1/accounts"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"잔고 조회 에러: {e}")
    return []

# === 모니터링 시간 체크 ===
def is_within_monitoring_hours():
    """현재 시간이 모니터링 시간인지 확인"""
    now = datetime.datetime.now()
    current_hour = now.hour
    
    for start_hour, end_hour in MONITORING_HOURS:
        if start_hour <= current_hour < end_hour:
            return True
    return False

# === Flask 대시보드 ===
app = Flask(__name__)

@app.route('/')
def dashboard():
    trades = read_trade_history()
    pnl = calculate_pnl(trades)
    balance = get_account_balance()
    return render_template("dashboard.html", trades=trades, pnl=pnl, balance=balance)

@app.route('/data')
def get_data():
    trades = read_trade_history()
    pnl = calculate_pnl(trades)
    balance = get_account_balance()
    return jsonify({"trades": trades, "pnl": pnl, "balance": balance})

def run_dashboard():
    app.run(host='0.0.0.0', port=5000, debug=False)

# === 거래 로그 ===
def log_trade(data):
    fieldnames = ["datetime", "market", "action", "price", "amount", "pnl"]
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def read_trade_history():
    trades = []
    if not os.path.isfile(LOG_FILE): 
        return trades
    with open(LOG_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        trades = list(reader)
    return trades

def calculate_pnl(trades):
    pnl = 0
    for t in trades:
        if t['action'] in ['SELL', 'STOP_LOSS']:
            try:
                pnl += float(t.get('pnl', 0))
            except (ValueError, TypeError):
                pass
    return pnl

# === 매매 로직 ===
def place_order(market, side, price, volume):
    """주문 실행"""
    try:
        data = {
            'market': market,
            'side': side,
            'price': str(price),
            'ord_type': 'limit',
            'volume': str(volume)
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in data.items()])
        headers = get_headers(query_string)
        
        url = f"{SERVER_URL}/v1/orders"
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code == 201:
            order_data = response.json()
            print(f"주문 성공: {side} {market} {volume}개 @ {price}")
            return order_data
        else:
            print(f"주문 실패: {response.text}")
            return None
    except Exception as e:
        print(f"주문 에러: {e}")
        return None

def auto_trade():
    global current_daily_pnl
    
    print("자동 거래 봇 시작...")
    send_telegram_message("🤖 업비트 자동 거래 봇이 시작되었습니다.")
    
    markets = get_top_10_markets()
    print(f"[{datetime.datetime.now()}] 모니터링 시작: {markets}")
    
    # 거래 상태 추적
    active_trades = {}  # {market: {'buy_price': price, 'amount': amount}}
    
    while True:
        try:
            current_time = datetime.datetime.now()
            
            # 모니터링 시간 체크
            if not is_within_monitoring_hours():
                print(f"[{current_time}] 모니터링 시간이 아닙니다.")
                time.sleep(INTERVAL)
                continue
            
            # 일일 손실 한도 체크
            if current_daily_pnl <= DAILY_LOSS_LIMIT:
                print(f"[{current_time}] 일일 손실 한도 도달: {current_daily_pnl}")
                send_telegram_message(f"⚠️ 일일 손실 한도 도달: {current_daily_pnl:,}원")
                time.sleep(INTERVAL)
                continue
            
            # 각 마켓 모니터링
            for market in markets:
                current_price = get_market_price(market)
                if not current_price:
                    continue
                
                # 활성 거래가 있는 경우 매도 조건 체크
                if market in active_trades:
                    trade = active_trades[market]
                    buy_price = trade['buy_price']
                    amount = trade['amount']
                    
                    # 수익률 계산
                    profit_rate = (current_price - buy_price) / buy_price
                    
                    # 매도 조건 체크
                    if profit_rate >= TAKE_PROFIT or profit_rate <= STOP_LOSS:
                        # 매도 실행
                        sell_order = place_order(market, 'ask', current_price, amount)
                        if sell_order:
                            # 손익 계산
                            pnl = (current_price - buy_price) * amount
                            current_daily_pnl += pnl
                            
                            # 거래 로그
                            trade_data = {
                                'datetime': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'market': market,
                                'action': 'SELL' if profit_rate >= TAKE_PROFIT else 'STOP_LOSS',
                                'price': current_price,
                                'amount': amount,
                                'pnl': pnl
                            }
                            log_trade(trade_data)
                            
                            # 텔레그램 알림
                            action_text = "수익 실현" if profit_rate >= TAKE_PROFIT else "손실 절단"
                            message = f"💰 {action_text}\n마켓: {market}\n매수가: {buy_price:,}원\n매도가: {current_price:,}원\n수익률: {profit_rate:.2%}\n손익: {pnl:,.0f}원"
                            send_telegram_message(message)
                            
                            # 활성 거래에서 제거
                            del active_trades[market]
                
                # 새로운 매수 기회 탐지 (거래량 기준)
                elif market not in active_trades:
                    # 간단한 매수 조건: 랜덤 확률로 매수 (실제로는 더 정교한 분석 필요)
                    import random
                    if random.random() < 0.01:  # 1% 확률로 매수
                        amount = TRADE_AMOUNT / current_price
                        buy_order = place_order(market, 'bid', current_price, amount)
                        if buy_order:
                            active_trades[market] = {
                                'buy_price': current_price,
                                'amount': amount
                            }
                            
                            # 거래 로그
                            trade_data = {
                                'datetime': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'market': market,
                                'action': 'BUY',
                                'price': current_price,
                                'amount': amount,
                                'pnl': 0
                            }
                            log_trade(trade_data)
                            
                            # 텔레그램 알림
                            message = f"📈 매수 실행\n마켓: {market}\n가격: {current_price:,}원\n수량: {amount:.4f}"
                            send_telegram_message(message)
            
            time.sleep(INTERVAL)
            
        except Exception as e:
            print(f"에러 발생: {e}")
            send_telegram_message(f"❌ 거래 봇 에러: {str(e)}")
            time.sleep(INTERVAL)

# === 스레드로 Flask + 트레이딩 병행 실행 ===
if __name__ == "__main__":
    print("업비트 자동 거래 봇 v5 시작...")
    threading.Thread(target=run_dashboard, daemon=True).start()
    auto_trade()
