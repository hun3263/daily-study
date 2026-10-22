# -*- coding: utf-8 -*-
import os
import json
import re
import urllib.request
import urllib.error
from datetime import datetime

DATA_FILE = "archive_data.json"
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"

def fetch_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://m.stock.naver.com/"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))

def parse_val(text):
    if not text:
        return 0
    return float(str(text).replace(',', '').replace('+', '').replace('-', '').strip())

def auto_collect_today():
    """네이버 금융 공개 API에서 오늘 실시간 지수, 환율, 거래대금 상위, 500억 이상 상승주를 자동 수집"""
    print("[1/3] 네이버 금융에서 오늘 시장 데이터 실시간 자동 수집 시도...")
    try:
        # 1. 지수 데이터 수집
        kospi_data = fetch_json("https://m.stock.naver.com/api/index/KOSPI/basic")
        kosdaq_data = fetch_json("https://m.stock.naver.com/api/index/KOSDAQ/basic")
        
        # 2. 환율 수집
        fx_data = fetch_json("https://m.stock.naver.com/api/marketIndex/exchange/FX_USDKRW")
        
        # 3. 거래대금 상위 종목 수집 (코스피 + 코스닥)
        kospi_tv = fetch_json("https://m.stock.naver.com/api/stocks/tradingValue/KOSPI?page=1&pageSize=15")
        kosdaq_tv = fetch_json("https://m.stock.naver.com/api/stocks/tradingValue/KOSDAQ?page=1&pageSize=15")
        
        # 4. 상승률 상위 종목 수집 (500억 이상 필터링용)
        kospi_rise = fetch_json("https://m.stock.naver.com/api/stocks/rise/KOSPI?page=1&pageSize=30")
        kosdaq_rise = fetch_json("https://m.stock.naver.com/api/stocks/rise/KOSDAQ?page=1&pageSize=30")
    except Exception as e:
        print(f"[안내] 실시간 수집 건너뜀 (네트워크 미연결 또는 휴장일): {e}")
        return None

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    day_str = weekdays[now.weekday()]
    label_str = f"{today_str} ({day_str})"

    # 지수 파싱
    kp_close = kospi_data.get("closePrice", "0")
    kp_diff = kospi_data.get("compareToPreviousClosePrice", "0")
    kp_ratio = kospi_data.get("fluctuationsRatio", "0")
    kp_is_up = float(kp_ratio) >= 0 if kp_ratio else True
    kp_sign = "▲" if kp_is_up else "▼"
    kp_vol = kospi_data.get("accumulatedTradingVolume", "-") + " 천 주"
    kp_val = kospi_data.get("accumulatedTradingValue", "-") + " 백만 원"

    kd_close = kosdaq_data.get("closePrice", "0")
    kd_diff = kosdaq_data.get("compareToPreviousClosePrice", "0")
    kd_ratio = kosdaq_data.get("fluctuationsRatio", "0")
    kd_is_up = float(kd_ratio) >= 0 if kd_ratio else True
    kd_sign = "▲" if kd_is_up else "▼"
    kd_vol = kosdaq_data.get("accumulatedTradingVolume", "-") + " 천 주"
    kd_val = kosdaq_data.get("accumulatedTradingValue", "-") + " 백만 원"

    # 환율
    fx_close = fx_data.get("closePrice", "-")
    fx_diff = fx_data.get("compareToPreviousClosePrice", "-")
    fx_ratio = fx_data.get("fluctuationsRatio", "-")

    # 거래대금 TOP 15 정리
    all_tv = (kospi_tv.get("stocks", []) if isinstance(kospi_tv, dict) else kospi_tv) + \
             (kosdaq_tv.get("stocks", []) if isinstance(kosdaq_tv, dict) else kosdaq_tv)
    
    all_tv.sort(key=lambda x: parse_val(x.get("accumulatedTradingValue", 0)), reverse=True)
    top_tv_list = []
    for rank, item in enumerate(all_tv[:15], 1):
        ratio = item.get("fluctuationsRatio", "0")
        is_up = float(ratio) >= 0 if ratio else True
        sign = "+" if is_up else ""
        top_tv_list.append({
            "rank": rank,
            "name": item.get("stockName", "-"),
            "price": f"{sign}{ratio}%",
            "isUp": is_up,
            "val": f"{item.get('accumulatedTradingValue', '-')} 백만 원",
            "reason": f"장중 거래대금 상위 {rank}위 기록 (실시간 자동 집계)"
        })

    # 500억 이상 & 상승률 상위 종목 필터링 (거래대금 50,000백만원 이상)
    all_rise = (kospi_rise.get("stocks", []) if isinstance(kospi_rise, dict) else kospi_rise) + \
               (kosdaq_rise.get("stocks", []) if isinstance(kosdaq_rise, dict) else kosdaq_rise)
    
    filtered_500 = []
    for item in all_rise:
        tv_val = parse_val(item.get("accumulatedTradingValue", 0))
        if tv_val >= 50000:
            filtered_500.append(item)
    
    filtered_500.sort(key=lambda x: parse_val(x.get("fluctuationsRatio", 0)), reverse=True)
    
    if len(filtered_500) < 10:
        for item in all_tv:
            if float(item.get("fluctuationsRatio", "0")) > 0 and item not in filtered_500:
                filtered_500.append(item)
                if len(filtered_500) >= 15:
                    break
    
    top500_list = []
    for rank, item in enumerate(filtered_500[:15], 1):
        ratio = item.get("fluctuationsRatio", "0")
        top500_list.append({
            "rank": rank,
            "name": item.get("stockName", "-"),
            "price": f"+{ratio}%",
            "val": f"{item.get('accumulatedTradingValue', '-')} 백만 원",
            "reason": f"거래대금 500억 이상 수급 수반 속 상승률 상위 {rank}위"
        })

    # 주요 테마 자동 분류
    auto_themes = [
        {
            "group": "1. 실시간 거래대금 최상위 주도 섹터",
            "badges": ["실시간수급", "메이저집중", "대형주"],
            "stocks": [f"{s['name']} ({s['price']})" for s in top_tv_list[:5]],
            "strategy": "외국인·기관 대량 수급 유입 확인. 지수 방향성 추종 트레이딩"
        },
        {
            "group": "2. 거래대금 500억 이상 탄력 상승 테마",
            "badges": ["500억필터", "거래대금급증", "주도주"],
            "stocks": [f"{s['name']} ({s['price']})" for s in top500_list[:5]],
            "strategy": "실질 수급이 검증된 상승주. 눌림목 지지 여부 확인 후 분할 대응"
        }
    ]

    today_record = {
        "date": today_str,
        "label": label_str,
        "badge": f"코스피 {kp_sign}{kp_ratio}% · 코스닥 {kd_sign}{kd_ratio}%",
        "title": f"{label_str} 국내 증시 실시간 마감 시황 및 거래대금 상위 주도주",
        "indices": [
            {
                "name": "코스피 (KOSPI)",
                "close": kp_close,
                "change": f"{kp_sign} {kp_diff} ({kp_ratio}%)",
                "isUp": kp_is_up,
                "volume": kp_vol,
                "tradingVal": kp_val,
                "investors": "정규장 마감 기준 실시간 집계"
            },
            {
                "name": "코스닥 (KOSDAQ)",
                "close": kd_close,
                "change": f"{kd_sign} {kd_diff} ({kd_ratio}%)",
                "isUp": kd_is_up,
                "volume": kd_vol,
                "tradingVal": kd_val,
                "investors": "정규장 마감 기준 실시간 집계"
            }
        ],
        "macroMetrics": [
            { "label": "원/달러 환율", "val": f"{fx_close}원 ({fx_diff}원)", "note": f"등락률: {fx_ratio}%" },
            { "label": "코스피 거래대금", "val": kp_val, "note": f"거래량: {kp_vol}" },
            { "label": "코스닥 거래대금", "val": kd_val, "note": f"거래량: {kd_vol}" },
            { "label": "500억↑ 상승 종목", "val": f"{len(top500_list)}개 종목", "note": "실질 수급 유입 주도주 선별" }
        ],
        "summaryHtml": f"""
            <p>• {label_str} 코스피는 전일대비 <span class="hl-yellow">{kp_sign} {kp_diff}포인트({kp_ratio}%) 변동한 {kp_close}</span>에 마감했습니다.</p>
            <p>• 코스닥은 <span class="hl-yellow">{kd_sign} {kd_diff}포인트({kd_ratio}%) 변동한 {kd_close}</span>를 기록했습니다.</p>
            <p>• 원/달러 환율은 {fx_close}원({fx_diff}원) 수준을 나타내고 있습니다.</p>
        """,
        "scheduleCheck": [
            { "day": label_str, "event": "정규장 장 마감 시황 집계", "impact": "실시간 거래대금 및 수급 지표 자동 반영" }
        ],
        "top500UpList": top500_list,
        "themes": auto_themes,
        "topTradingValList": top_tv_list,
        "study": {
            "title": "실시간 거래대금 필터와 대형주 수급 집중도 해석 원칙",
            "caseRef": f"실전 사례: {label_str} 거래대금 상위 종목군과 상승률 상위 종목의 수급 일치도",
            "points": [
                "1. 거래대금 상위와 상승률 상위의 교집합 종목이 시장의 진짜 주도주입니다.",
                "2. 단순 테마 급등주는 거래대금이 300억 미만인 경우가 많으므로 500억 원 이상 실린 종목 위주로 대응합니다.",
                "3. 지수 방향성과 무관하게 거래대금이 급증하는 섹터가 다음 거래일의 주도 섹터가 됩니다."
            ]
        }
    }
    print(f"[성공] {today_str} 오늘자 시장 데이터 자동 수집 완료!")
    return today_record

def main():
    # 1. 기존 누적 아카이브 로드
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            archive = json.load(f)
    else:
        archive = []

    # 2. 오늘 날짜 실시간 자동 수집
    today_data = auto_collect_today()
    if today_data:
        today_date = today_data["date"]
        existing_idx = next((i for i, item in enumerate(archive) if item["date"] == today_date), None)
        if existing_idx is not None:
            archive[existing_idx] = today_data
            print(f"[업데이트] 기존 {today_date} 데이터를 최신 장 마감 데이터로 갱신했습니다.")
        else:
            archive.insert(0, today_data)
            print(f"[추가] 새 날짜({today_date}) 데이터가 아카이브 최상단에 자동 추가되었습니다.")

        # archive_data.json 자동 저장 (다음 실행 때 누적 보관됨)
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(archive, f, ensure_ascii=False, indent=2)
            print(f"[성공] {DATA_FILE} 누적 저장 완료 (총 {len(archive)}일 치)")
        except Exception as e:
            print(f"[주의] {DATA_FILE} 저장 실패: {e}")

    # 3. template.html 로드
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"'{TEMPLATE_FILE}' 파일이 없습니다. 최상위 폴더에 {TEMPLATE_FILE}이 있는지 확인해주세요.")
    
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    # 4. 데이터 주입 (최신 누적 아카이브 전체 삽입)
    json_str = json.dumps(archive, ensure_ascii=False)
    placeholder = "/* __ARCHIVE_DATA__ */ []"

    if placeholder in template:
        html_out = template.replace(placeholder, json_str)
    else:
        start_marker = "const ARCHIVE_DATA = ["
        end_marker = "];"
        s_idx = template.find(start_marker)
        if s_idx != -1:
            e_idx = template.find(end_marker, s_idx) + 2
            html_out = template[:s_idx] + f"const ARCHIVE_DATA = {json_str};" + template[e_idx:]
        else:
            raise ValueError("템플릿에서 ARCHIVE_DATA 위치를 찾을 수 없습니다.")

    # 5. index.html 출력 (홈페이지 파일 생성)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"[최종 성공] {OUTPUT_FILE} 배포 파일 생성 완료! (기준: {len(archive)}일 치 아카이브, 최신일: {archive[0]['date'] if archive else '없음'})")

if __name__ == "__main__":
    main()
