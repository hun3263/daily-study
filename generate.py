# -*- coding: utf-8 -*-
import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

DATA_FILE = "archive_data.json"
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://finance.naver.com/"
}

# 주요 시장 주도주 기본 코드 풀 (실시간 크롤링 종목과 자동 병합되어 일별 시세 추정에 사용)
CORE_STOCKS = [
    ("005930", "삼성전자", "반도체·메가캡"),
    ("000660", "SK하이닉스", "AI반도체·HBM"),
    ("042700", "한미반도체", "AI반도체·HBM"),
    ("036930", "주성엔지니어링", "반도체장비"),
    ("131970", "두산테스나", "시스템반도체"),
    ("373220", "LG에너지솔루션", "2차전지·ESS"),
    ("006400", "삼성SDI", "2차전지·전고체"),
    ("003670", "포스코퓨처엠", "2차전지소재"),
    ("247540", "에코프로비엠", "2차전지소재"),
    ("096770", "SK이노베이션", "정유·에너지"),
    ("010950", "S-Oil", "정유·에너지"),
    ("012450", "한화에어로스페이스", "K-방산·우주"),
    ("064350", "현대로템", "K-방산·철도"),
    ("079550", "LIG넥스원", "K-방산·유도무기"),
    ("267260", "HD현대일렉트릭", "전력설비·변압기"),
    ("010120", "LS ELECTRIC", "전력설비·배전"),
    ("298040", "효성중공업", "전력설비·변압기"),
    ("034020", "두산에너빌리티", "원전·가스터빈"),
    ("329180", "HD현대중공업", "조선·LNG선"),
    ("011200", "HMM", "해운·컨테이너"),
    ("028670", "팬오션", "해운·벌크·LNG"),
    ("452280", "한선엔지니어링", "LNG·수소피팅"),
    ("039610", "화성밸브", "LNG·가스밸브"),
    ("207940", "삼성바이오로직스", "바이오·CDMO"),
    ("068270", "셀트리온", "바이오·신약"),
    ("196170", "알테오젠", "바이오플랫폼"),
    ("278470", "에이피알", "K-뷰티·디바이스"),
    ("003230", "삼양식품", "K-푸드·수출"),
    ("005380", "현대차", "자동차·모빌리티"),
    ("000270", "기아", "자동차·모빌리티"),
    ("105560", "KB금융", "금융·밸류업"),
    ("055550", "신한지주", "금융·밸류업"),
    ("000720", "현대건설", "건설·원전"),
    ("033780", "KT&G", "고배당·방어주"),
    ("053800", "안랩", "사이버보안·AI"),
    ("402340", "SK스퀘어", "반도체지주")
]


def safe_fetch_json(url, timeout=8):
    """개별 URL JSON 요청 (실패 시 전체 중단 없이 None 반환)"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"  [참고] JSON 호출 건너뜀 ({url}): {e}")
        return None


def safe_fetch_text(url, encoding="euc-kr", timeout=8):
    """개별 URL 텍스트/HTML/XML 요청 (실패 시 None 반환)"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            try:
                return raw.decode(encoding)
            except UnicodeDecodeError:
                return raw.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [참고] 텍스트 호출 건너뜀 ({url}): {e}")
        return None


def parse_num(val):
    if val is None:
        return 0.0
    s = re.sub(r"[^0-9.\-]", "", str(val))
    if not s or s in ("-", ".", "-."):
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def format_eok(eok_val):
    """억 원 단위 숫자를 'X조 Y,YYY억 원' 또는 'X,XXX억 원'으로 포맷팅"""
    eok = int(round(eok_val))
    if eok >= 10000:
        jo = eok // 10000
        rem = eok % 10000
        return f"{jo}조 {rem:,}억 원" if rem > 0 else f"{jo}조 원"
    return f"{max(eok, 1):,}억 원"


def get_weekday_kr(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
    except Exception:
        return ""


class SiseTableParser(HTMLParser):
    """네이버 금융 시세 테이블(sise_market_sum, sise_quant, sise_rise) 파서 (표준 라이브러리만 사용)"""
    def __init__(self):
        super().__init__()
        self.in_tr = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = []
        self.row_code = ""
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "tr":
            self.in_tr = True
            self.current_row = []
            self.row_code = ""
        elif self.in_tr and tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = []
        elif self.in_tr and tag == "a":
            href = attrs_dict.get("href", "")
            m = re.search(r"code=(\d{6})", href)
            if m and not self.row_code:
                self.row_code = m.group(1)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            text = re.sub(r"\s+", " ", "".join(self.current_cell)).strip()
            self.current_row.append(text)
        elif tag == "tr" and self.in_tr:
            self.in_tr = False
            if len(self.current_row) >= 6:
                self.rows.append((self.row_code, self.current_row))

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)


def fetch_fchart_series(symbol, count=20):
    """네이버 차트 XML API(fchart)에서 일봉 시계열 수집: { 'YYYY-MM-DD': {close, diff, ratio, volume} }"""
    url = f"https://fchart.stock.naver.com/sise.nhn?symbol={symbol}&timeframe=day&count={count}&requestType=0"
    xml_text = safe_fetch_text(url, encoding="euc-kr")
    if not xml_text:
        return {}
    items = re.findall(r'data="(\d{8})\|([^"|]+)\|([^"|]+)\|([^"|]+)\|([^"|]+)\|([^"|]+)"', xml_text)
    series = {}
    prev_close = None
    for raw_date, open_p, high_p, low_p, close_p, vol in items:
        d_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
        c_val = parse_num(close_p)
        v_val = parse_num(vol)
        if prev_close and prev_close > 0:
            diff_val = c_val - prev_close
            ratio_val = (diff_val / prev_close) * 100.0
        else:
            diff_val = 0.0
            ratio_val = 0.0
        series[d_str] = {
            "close": c_val,
            "diff": diff_val,
            "ratio": ratio_val,
            "volume": v_val
        }
        prev_close = c_val
    return series


def fetch_index_history(code="KOSPI", count=20):
    """지수 일별 시세 수집 (fchart XML + 모바일 JSON API 교차 보완)"""
    history = fetch_fchart_series(code, count=count + 5)

    # 모바일 JSON API로 정확한 전일비/등락률 보완
    api_url = f"https://m.stock.naver.com/api/index/{code}/price?pageSize={count}&page=1"
    data = safe_fetch_json(api_url)
    items = data if isinstance(data, list) else (data.get("priceInfos") or data.get("datas") or [] if isinstance(data, dict) else [])
    for item in items:
        if not isinstance(item, dict):
            continue
        d_str = str(item.get("localTradedAt", ""))[:10]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", d_str):
            continue
        c_val = parse_num(item.get("closePrice"))
        diff_val = parse_num(item.get("compareToPreviousClosePrice"))
        ratio_val = parse_num(item.get("fluctuationsRatio"))
        price_info = item.get("compareToPreviousPrice")
        if isinstance(price_info, dict) and price_info.get("name") in ("FALLING", "LOWER_LIMIT"):
            diff_val = -abs(diff_val)
            ratio_val = -abs(ratio_val)
        elif ratio_val < 0:
            diff_val = -abs(diff_val)

        prev = history.get(d_str, {})
        history[d_str] = {
            "close": c_val if c_val > 0 else prev.get("close", 0.0),
            "diff": diff_val if diff_val != 0 else prev.get("diff", 0.0),
            "ratio": ratio_val if ratio_val != 0 else prev.get("ratio", 0.0),
            "volume": prev.get("volume", 0.0),
            "tradingValStr": None
        }

    # 당일 basic API에서 거래대금/거래량 보완
    basic = safe_fetch_json(f"https://m.stock.naver.com/api/index/{code}/basic")
    if isinstance(basic, dict) and history:
        latest_d = sorted(history.keys())[-1]
        acc_val = parse_num(basic.get("accumulatedTradingValue"))
        acc_vol = parse_num(basic.get("accumulatedTradingVolume"))
        if acc_val > 0:
            # 네이버 지수 basic의 accumulatedTradingValue 단위는 백만원 (100백만원 = 1억원)
            history[latest_d]["tradingValStr"] = format_eok(acc_val / 100.0)
        if acc_vol > 0:
            history[latest_d]["volume"] = acc_vol

    return history


def fetch_fx_history(count=20):
    """원/달러 환율 일별 시세 수집"""
    fx_map = {}
    url = f"https://api.stock.naver.com/marketindex/exchange/FX_USDKRW/prices?page=1&pageSize={count}"
    data = safe_fetch_json(url)
    items = data if isinstance(data, list) else (data.get("result") or data.get("prices") or [] if isinstance(data, dict) else [])
    for item in items:
        if not isinstance(item, dict):
            continue
        d_str = str(item.get("localTradedAt", ""))[:10]
        if re.match(r"^\d{4}-\d{2}-\d{2}$", d_str):
            c_val = parse_num(item.get("closePrice"))
            diff_val = parse_num(item.get("fluctuations") or item.get("compareToPreviousClosePrice"))
            ratio_val = parse_num(item.get("fluctuationsRatio"))
            if ratio_val < 0:
                diff_val = -abs(diff_val)
            fx_map[d_str] = {
                "close": c_val,
                "diff": diff_val,
                "ratio": ratio_val
            }
    return fx_map


def scrape_naver_sise_stocks():
    """네이버 금융 거래량상위(sise_quant), 상승률상위(sise_rise), 시가총액상위(sise_market_sum)에서 실시간 종목 수집"""
    urls = [
        "https://finance.naver.com/sise/sise_quant.naver?sosok=0",
        "https://finance.naver.com/sise/sise_quant.naver?sosok=1",
        "https://finance.naver.com/sise/sise_rise.naver?sosok=0",
        "https://finance.naver.com/sise/sise_rise.naver?sosok=1",
        "https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page=1",
        "https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page=1"
    ]
    stocks_by_code = {}

    for url in urls:
        html_text = safe_fetch_text(url, encoding="euc-kr")
        if not html_text:
            continue
        parser = SiseTableParser()
        try:
            parser.feed(html_text)
        except Exception:
            continue

        headers = []
        for code, row in parser.rows:
            if not code and ("종목명" in row and "현재가" in row):
                headers = row
                continue
            if not code or len(row) < 6:
                continue

            try:
                name_idx = headers.index("종목명") if "종목명" in headers else 1
                price_idx = headers.index("현재가") if "현재가" in headers else 2
                ratio_idx = headers.index("등락률") if "등락률" in headers else 4
                vol_idx = headers.index("거래량") if "거래량" in headers else 5
                val_idx = headers.index("거래대금") if "거래대금" in headers else -1
            except ValueError:
                name_idx, price_idx, ratio_idx, vol_idx, val_idx = 1, 2, 4, 5, -1

            if max(name_idx, price_idx, ratio_idx) >= len(row):
                continue

            name = row[name_idx].strip()
            if not name or any(skip in name for skip in ("KODEX", "TIGER", "KBSTAR", "RISE", "ACE", "SOL", "HANARO", "ETN", "스팩")):
                continue

            price = parse_num(row[price_idx])
            ratio_raw = row[ratio_idx].strip()
            ratio = parse_num(ratio_raw)
            if "-" in ratio_raw and ratio > 0:
                ratio = -ratio

            vol = parse_num(row[vol_idx]) if vol_idx < len(row) else 0.0
            if val_idx != -1 and val_idx < len(row):
                val_eok = parse_num(row[val_idx]) / 100.0
            else:
                val_eok = (price * vol) / 100000000.0

            if price > 0 and val_eok > 0:
                stocks_by_code[code] = {
                    "code": code,
                    "name": name,
                    "close": price,
                    "ratio": ratio,
                    "val_eok": val_eok
                }

    return stocks_by_code


def collect_multi_day_stock_bars(extra_stocks_map, count=18):
    """주요 종목들의 일별 시세(종가, 등락률, 거래대금)를 fchart에서 병렬 수집하여 날짜별로 매핑"""
    pool = {code: (name, theme) for code, name, theme in CORE_STOCKS}
    for code, info in extra_stocks_map.items():
        if code not in pool and len(pool) < 55:
            pool[code] = (info["name"], "수급주도주")

    daily_stocks = {}

    def worker(item):
        code, (name, theme) = item
        return code, name, theme, fetch_fchart_series(code, count=count)

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(worker, pool.items()))

    for code, name, theme, series in results:
        for d_str, bar in series.items():
            val_eok = (bar["close"] * bar["volume"]) / 100000000.0
            daily_stocks.setdefault(d_str, {})[code] = {
                "code": code,
                "name": name,
                "theme": theme,
                "close": bar["close"],
                "ratio": bar["ratio"],
                "val_eok": val_eok
            }

    return daily_stocks


def build_daily_record(date_str, kp_info, kd_info, fx_info, day_stocks_map):
    """특정 거래일(date_str)의 리포트 객체를 자동 생성"""
    wd = get_weekday_kr(date_str)
    label_str = f"{date_str} ({wd})" if wd else date_str

    kp_close = f"{kp_info['close']:,.2f}" if kp_info["close"] else "-"
    kp_ratio = kp_info["ratio"]
    kp_diff = abs(kp_info["diff"])
    kp_is_up = kp_ratio >= 0
    kp_sign = "▲" if kp_is_up else "▼"
    kp_ratio_str = f"+{kp_ratio:.2f}%" if kp_is_up else f"{kp_ratio:.2f}%"
    kp_vol_str = f"{int(kp_info['volume']):,} 천 주" if kp_info["volume"] else "집계중"
    kp_val_str = kp_info.get("tradingValStr") or (format_eok(kp_info["volume"] * 65000 / 100000) if kp_info["volume"] else "정규장 마감 기준")

    kd_close = f"{kd_info['close']:,.2f}" if kd_info["close"] else "-"
    kd_ratio = kd_info["ratio"]
    kd_diff = abs(kd_info["diff"])
    kd_is_up = kd_ratio >= 0
    kd_sign = "▲" if kd_is_up else "▼"
    kd_ratio_str = f"+{kd_ratio:.2f}%" if kd_is_up else f"{kd_ratio:.2f}%"
    kd_vol_str = f"{int(kd_info['volume']):,} 천 주" if kd_info["volume"] else "집계중"
    kd_val_str = kd_info.get("tradingValStr") or (format_eok(kd_info["volume"] * 13500 / 100000) if kd_info["volume"] else "정규장 마감 기준")

    if fx_info and fx_info.get("close"):
        fx_sign = "+" if fx_info["diff"] >= 0 else "-"
        fx_val_str = f"{fx_info['close']:,.1f}원 ({fx_sign}{abs(fx_info['diff']):.1f}원)"
        fx_note = f"전일대비 등락률 {fx_info['ratio']:+.2f}%"
    else:
        fx_val_str = "외환시장 마감 기준"
        fx_note = "원/달러 장중 수급 연동"

    stocks_list = list(day_stocks_map.values())
    stocks_by_val = sorted(stocks_list, key=lambda x: x["val_eok"], reverse=True)

    # 거래대금 상위 TOP 15
    top_tv_list = []
    for rank, st in enumerate(stocks_by_val[:15], 1):
        r = st["ratio"]
        is_up = r >= 0
        r_str = f"+{r:.2f}%" if is_up else f"{r:.2f}%"
        p_str = f"{int(st['close']):,}원 ({r_str})"
        top_tv_list.append({
            "rank": rank,
            "name": st["name"],
            "price": p_str,
            "isUp": is_up,
            "val": format_eok(st["val_eok"]),
            "reason": f"{st.get('theme', '주도섹터')} 내 거래대금 상위 {rank}위 ({format_eok(st['val_eok'])}) 기록하며 시장 유동성 집중"
        })

    # 거래대금 500억 이상 & 상승률 상위 TOP 15
    up_500 = [st for st in stocks_list if st["val_eok"] >= 500.0 and st["ratio"] > 0]
    up_500.sort(key=lambda x: x["ratio"], reverse=True)
    if len(up_500) < 5:
        fallback_up = [st for st in stocks_by_val if st["ratio"] > 0 and st not in up_500]
        up_500.extend(fallback_up[:10 - len(up_500)])

    top500_list = []
    for rank, st in enumerate(up_500[:15], 1):
        r = st["ratio"]
        sang_mark = " 상" if r >= 29.0 else ""
        p_str = f"{int(st['close']):,}원 (+{r:.2f}%){sang_mark}"
        top500_list.append({
            "rank": rank,
            "name": st["name"],
            "price": p_str,
            "val": format_eok(st["val_eok"]),
            "reason": f"거래대금 {format_eok(st['val_eok'])} 수반하며 {st.get('theme', '핵심 테마')} 강세 주도"
        })

    theme_buckets = {}
    for st in stocks_by_val:
        t_name = st.get("theme", "수급주도주")
        theme_buckets.setdefault(t_name, []).append(st)

    sorted_themes = sorted(
        theme_buckets.items(),
        key=lambda kv: sum(x["val_eok"] for x in kv[1]),
        reverse=True
    )
    auto_themes = []
    for idx, (t_name, t_stocks) in enumerate(sorted_themes[:4], 1):
        t_stocks_sorted = sorted(t_stocks, key=lambda x: x["ratio"], reverse=True)
        stock_pills = []
        for s in t_stocks_sorted[:5]:
            r = s["ratio"]
            r_str = f"+{r:.2f}%" if r >= 0 else f"{r:.2f}%"
            stock_pills.append(f"{s['name']} ({r_str})")
        avg_r = sum(x["ratio"] for x in t_stocks) / len(t_stocks)
        strategy_txt = (
            "대량 거래대금 수반 상승 구간. 장중 5일선 및 시초가 지지 확인하며 분할 대응"
            if avg_r >= 0 else
            "차익실현 및 수급 숨고르기 구간. 거래대금 바닥 확인 후 눌림목 분할 접근"
        )
        auto_themes.append({
            "group": f"{idx}. {t_name} 핵심 섹터",
            "badges": [t_name.split("·")[0], "대량수급", "주도섹터"],
            "stocks": stock_pills,
            "strategy": strategy_txt
        })

    if kp_ratio >= 2.0:
        market_tone = "강력한 매수 수급 유입 속 지수 급반등"
        hl_class = "hl-yellow"
    elif kp_ratio <= -2.0:
        market_tone = "대외 변동성 확대 및 차익실현 매물 출회 속 조정"
        hl_class = "hl-red"
    elif kp_ratio >= 0:
        market_tone = "업종별 순환매 속 견조한 상승 마감"
        hl_class = "hl-yellow"
    else:
        market_tone = "숨고르기 장세 속 거래대금 상위 주도주 차별화"
        hl_class = "hl-yellow"

    lead_stocks_str = ", ".join(f"{s['name']}({s['price'].split(' ')[1] if ' ' in s['price'] else s['price']})" for s in top500_list[:3]) if top500_list else "대형 주도주"

    summary_html = f"""
        <p>• {label_str} 국내 증시는 <span class="{hl_class}">코스피 {kp_close}({kp_sign} {kp_diff:.2f}pt, {kp_ratio_str}), 코스닥 {kd_close}({kd_sign} {kd_diff:.2f}pt, {kd_ratio_str})</span>로 마감하며 {market_tone} 흐름을 보였습니다.</p>
        <p>• 거래대금 500억 원 이상 실린 실질 주도주 중에서는 <span class="hl-yellow">{lead_stocks_str}</span> 등이 상위를 기록하며 시장 매기를 이끌었습니다.</p>
        <p>• 합산 거래대금 최상위권에서는 {top_tv_list[0]['name'] if top_tv_list else '반도체 메가캡'}({top_tv_list[0]['val'] if top_tv_list else '-'})을 중심으로 메이저 수급 공방이 전개되었습니다.</p>
    """

    return {
        "date": date_str,
        "label": label_str,
        "badge": f"코스피 {kp_ratio_str} · 코스닥 {kd_ratio_str}",
        "title": f"{label_str} 마감 시황 — {market_tone} ({top500_list[0]['name'] if top500_list else '대형주'} 등 강세)",
        "indices": [
            {
                "name": "코스피 (KOSPI)",
                "close": kp_close,
                "change": f"{kp_sign} {kp_diff:.2f} ({kp_ratio_str})",
                "isUp": kp_is_up,
                "volume": kp_vol_str,
                "tradingVal": kp_val_str,
                "investors": "기관·외인 수급 연동 (장 마감 기준)"
            },
            {
                "name": "코스닥 (KOSDAQ)",
                "close": kd_close,
                "change": f"{kd_sign} {kd_diff:.2f} ({kd_ratio_str})",
                "isUp": kd_is_up,
                "volume": kd_vol_str,
                "tradingVal": kd_val_str,
                "investors": "수급 상위 종목 차별화 (장 마감 기준)"
            }
        ],
        "macroMetrics": [
            {"label": "원/달러 환율", "val": fx_val_str, "note": fx_note},
            {"label": "코스피 등락폭", "val": f"{kp_sign} {kp_diff:.2f} pt ({kp_ratio_str})", "note": f"마감 종가 {kp_close}"},
            {"label": "코스닥 등락폭", "val": f"{kd_sign} {kd_diff:.2f} pt ({kd_ratio_str})", "note": f"마감 종가 {kd_close}"},
            {"label": "500억↑ 상승 주도주", "val": f"{len(up_500)}개 주요 종목", "note": f"1위: {top500_list[0]['name'] if top500_list else '-'}"}
        ],
        "summaryHtml": summary_html,
        "scheduleCheck": [
            {"day": label_str, "event": "국내 증시 정규장 마감 시황 및 거래대금 상위 수급 자동 집계", "impact": f"코스피 {kp_ratio_str} / 코스닥 {kd_ratio_str}"}
        ],
        "top500UpList": top500_list,
        "themes": auto_themes,
        "topTradingValList": top_tv_list,
        "study": {
            "title": "거래대금 500억 이상 주도주 필터링과 시장 변동성 국면별 대응 원칙",
            "caseRef": f"실전 데이터: {label_str} 거래대금 1위 {top_tv_list[0]['name'] if top_tv_list else '-'} ({top_tv_list[0]['val'] if top_tv_list else '-'}) 및 상승 주도주 비교",
            "points": [
                "1. 거래대금 500억 원 기준의 중요성: 소액 품절주 급등을 배제하고 기관·외인·메이저 수급이 실제로 유입된 주도주만 선별하는 핵심 기준입니다.",
                "2. 거래대금 상위(섹션 4)와 상승률 상위(섹션 2)의 교집합에 속한 종목이 당일 시장의 실질 대장주 역할을 수행합니다.",
                "3. 지수 변동성이 커질수록 당일 급등 추격 매수보다 익일 시초가 눌림목 지지 여부를 확인한 뒤 분할 접근하는 전략이 유리합니다."
            ]
        }
    }


def collect_missing_and_today_records(existing_dates):
    """네이버 금융에서 최근 거래일 데이터를 자동 수집하여 누락된 날짜 및 오늘 리포트를 생성"""
    print("[1/3] 네이버 금융에서 최근 거래일 지수·환율·종목 시세 자동 수집 중...")
    kospi_hist = fetch_index_history("KOSPI", count=18)
    kosdaq_hist = fetch_index_history("KOSDAQ", count=18)
    fx_hist = fetch_fx_history(count=18)

    if not kospi_hist:
        print("  [안내] 실시간 지수 데이터를 가져오지 못했습니다 (오프라인 환경 또는 응답 지연).")
        return []

    live_stocks = scrape_naver_sise_stocks()
    daily_stocks = collect_multi_day_stock_bars(live_stocks, count=18)

    all_trading_dates = sorted(kospi_hist.keys(), reverse=True)
    if all_trading_dates and live_stocks:
        latest_date = all_trading_dates[0]
        merged = daily_stocks.get(latest_date, {}).copy()
        for code, info in live_stocks.items():
            if code in merged:
                merged[code]["close"] = info["close"]
                merged[code]["ratio"] = info["ratio"]
                merged[code]["val_eok"] = max(merged[code]["val_eok"], info["val_eok"])
            else:
                merged[code] = {
                    "code": code,
                    "name": info["name"],
                    "theme": "실시간수급상위",
                    "close": info["close"],
                    "ratio": info["ratio"],
                    "val_eok": info["val_eok"]
                }
        daily_stocks[latest_date] = merged

    new_records = []
    for d_str in all_trading_dates:
        if d_str in existing_dates:
            continue
        if d_str < "2026-10-14":
            continue

        kp_info = kospi_hist.get(d_str)
        kd_info = kosdaq_hist.get(d_str, {"close": 0, "diff": 0, "ratio": 0, "volume": 0})
        fx_info = fx_hist.get(d_str)
        day_st = daily_stocks.get(d_str, {})
        if kp_info and kp_info.get("close", 0) > 0:
            rec = build_daily_record(d_str, kp_info, kd_info, fx_info, day_st)
            new_records.append(rec)
            print(f"  [자동 생성] {d_str} 리포트 데이터 생성 완료")

    return new_records


def main():
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"'{TEMPLATE_FILE}' 파일이 없습니다. 저장소에 {TEMPLATE_FILE}이 있는지 확인해주세요.")

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    # 1. archive_data.json 또는 template.html 내부의 기존 데이터 확인 (절대 빈 배열로 초기화하지 않음!)
    archive_json_list = None
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list) and len(loaded) > 0:
                    archive_json_list = loaded
        except Exception as e:
            print(f"[참고] {DATA_FILE} 로드 건너뜀: {e}")

    placeholder = "/* __ARCHIVE" + "_DATA__ */ []"
    start_marker = "const " + "ARCHIVE_DATA = ["
    end_marker = "];"

    s_idx = template.find(start_marker)
    e_idx = template.find(end_marker, s_idx) if s_idx != -1 else -1

    existing_inner_js = ""
    if s_idx != -1 and e_idx != -1:
        existing_inner_js = template[s_idx + len(start_marker):e_idx].strip()

    existing_dates = set()
    if archive_json_list:
        for item in archive_json_list:
            if isinstance(item, dict) and "date" in item:
                existing_dates.add(item["date"])
    if existing_inner_js:
        found_dates = re.findall(r'["\']?date["\']?\s*:\s*["\'](\d{4}-\d{2}-\d{2})["\']', existing_inner_js)
        existing_dates.update(found_dates)

    print(f"[확인] 기존 보관된 리포트 날짜: {sorted(existing_dates, reverse=True)}")

    # 2. 네이버 금융에서 누락된 거래일 및 오늘 시황 자동 수집
    new_records = collect_missing_and_today_records(existing_dates)

    # 3. 안전하게 ARCHIVE_DATA 병합 및 주입
    if archive_json_list is not None:
        by_date = {item["date"]: item for item in archive_json_list if isinstance(item, dict) and "date" in item}
        for rec in new_records:
            by_date[rec["date"]] = rec
        merged_list = [by_date[d] for d in sorted(by_date.keys(), reverse=True)]
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(merged_list, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        json_str = json.dumps(merged_list, ensure_ascii=False)
        if placeholder in template:
            html_out = template.replace(placeholder, json_str)
        elif s_idx != -1 and e_idx != -1:
            html_out = template[:s_idx] + f"const ARCHIVE_DATA = {json_str};" + template[e_idx + 2:]
        else:
            html_out = template
    else:
        if placeholder in template:
            json_str = json.dumps(new_records, ensure_ascii=False)
            html_out = template.replace(placeholder, json_str)
        elif s_idx != -1 and e_idx != -1:
            if new_records:
                new_json_items = ",\n".join(json.dumps(r, ensure_ascii=False, indent=4) for r in new_records)
                if existing_inner_js:
                    combined_inner = f"\n{new_json_items},\n{existing_inner_js}\n"
                else:
                    combined_inner = f"\n{new_json_items}\n"
                html_out = template[:s_idx] + f"const ARCHIVE_DATA = [{combined_inner}];" + template[e_idx + 2:]
            else:
                html_out = template
        else:
            html_out = template

    # 4. 브라우저 스크립트 중단 방지 안전장치 패치 (ARCHIVE_DATA가 비어있어도 버튼이 먹통되지 않도록 보호)
    html_out = html_out.replace(
        "let currentDate = ARCHIVE_DATA[0].date;",
        'let currentDate = (ARCHIVE_DATA && ARCHIVE_DATA.length > 0) ? ARCHIVE_DATA[0].date : "";'
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"[최종 성공] {OUTPUT_FILE} 생성 완료! (새로 추가된 일자: {len(new_records)}일, 기존 일자 보존 완료)")


if __name__ == "__main__":
    main()
