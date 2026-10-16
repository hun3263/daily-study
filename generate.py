<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>데일리 증시 시황 & 심화 스터디 아카이브</title>
    <script src="https://cdn.tailwindcss.com/3.4.17"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans KR', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f4f6f9;
            color: #1e293b;
        }
        .hl-yellow {
            background: linear-gradient(180deg, rgba(255,255,255,0) 55%, #fef08a 55%);
            font-weight: 600;
            padding: 0 2px;
        }
        .hl-red {
            background-color: #fee2e2;
            color: #991b1b;
            font-weight: 600;
            padding: 1px 6px;
            border-radius: 4px;
        }
        .up-text { color: #e11d48; }
        .down-text { color: #2563eb; }
        .badge-sang {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #ffe4e6;
            color: #e11d48;
            border: 1px solid #fecdd3;
            font-size: 11px;
            font-weight: 700;
            padding: 1px 5px;
            border-radius: 4px;
            margin-left: 4px;
        }
        .section-bar {
            border-left: 4px solid #2563eb;
            padding-left: 10px;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col md:flex-row">

    <!-- 좌측 사이드바: 일자별 아카이브 링크 -->
    <aside class="w-full md:w-72 bg-slate-900 text-slate-100 flex-shrink-0 flex flex-col border-b md:border-b-0 md:border-r border-slate-800">
        <div class="p-5 border-b border-slate-800 flex items-center justify-between">
            <div>
                <div class="text-xs font-semibold uppercase tracking-wider text-blue-400">DAILY MARKET ARCHIVE</div>
                <h1 class="text-lg font-bold text-white mt-0.5">📈 증시 시황 & 스터디</h1>
            </div>
            <button id="toggleCodeBtn" type="button" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1.5 rounded-lg border border-slate-700 transition">
                ⚙️ GitHub 코드
            </button>
        </div>

        <!-- 검색 및 필터 -->
        <div class="p-3 border-b border-slate-800">
            <input id="dateSearchInput" type="text" placeholder="날짜 또는 키워드 검색..." class="w-full bg-slate-800 text-slate-200 text-xs rounded-lg px-3 py-2 border border-slate-700 focus:outline-none focus:border-blue-500">
        </div>

        <!-- 일자별 링크 리스트 -->
        <div class="px-3 py-2 text-xs font-semibold text-slate-400 flex items-center justify-between">
            <span>📅 일자별 브리핑 저장소</span>
            <span id="archiveCountBadge" class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded-full text-[11px]">3일</span>
        </div>
        <nav id="dateListNav" class="flex-1 overflow-y-auto px-3 pb-4 space-y-1.5">
            <!-- JS로 렌더링 -->
        </nav>

        <div class="p-4 border-t border-slate-800 bg-slate-950/60 text-xs text-slate-400 space-y-1">
            <div class="font-medium text-slate-300">💡 하이브리드 리포트 사양</div>
            <div>• 한글파일 4단 핵심 데이터 표</div>
            <div>• NH PB 선행지표 & 대응 전략</div>
            <div>• 하단 날짜별 댓글형 복기 메모장</div>
        </div>
    </aside>

    <!-- 우측 메인 콘텐츠 영역 -->
    <main class="flex-1 min-w-0 overflow-y-auto">
        <!-- 상단 고정 헤더 -->
        <header class="bg-white border-b border-slate-200 sticky top-0 z-10 px-4 md:px-8 py-4 flex flex-wrap items-center justify-between gap-3 shadow-sm">
            <div>
                <div class="flex items-center gap-2">
                    <span id="headerDateBadge" class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded-md">2026-10-14 (수) 마감</span>
                    <span id="headerTagBadge" class="bg-amber-100 text-amber-800 text-xs font-semibold px-2.5 py-1 rounded-md">반대매매 개시 · 주도주 교체</span>
                </div>
                <h2 id="headerTitle" class="text-lg md:text-xl font-bold text-slate-900 mt-1">국내 증시 마감 시황 & 500억↑ 주도주 · 심화 스터디</h2>
            </div>

            <!-- 뷰 전환 탭 -->
            <div class="flex items-center gap-1.5 bg-slate-100 p-1 rounded-lg">
                <button id="tabReportBtn" type="button" class="px-3 py-1.5 rounded-md text-xs font-semibold bg-white text-blue-600 shadow-sm transition">
                    📊 통합 시황 리포트
                </button>
                <button id="tabCompareBtn" type="button" class="px-3 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-slate-900 transition">
                    🔍 양식 비교분석
                </button>
                <button id="tabGithubBtn" type="button" class="px-3 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-slate-900 transition">
                    💻 generate.py 코드
                </button>
            </div>
        </header>

        <!-- 탭 1: 통합 시황 리포트 뷰 -->
        <div id="viewReport" class="max-w-5xl mx-auto p-4 md:p-8 space-y-6">
            <!-- 동적 렌더링 컨테이너 -->
            <div id="reportContentContainer" class="space-y-6"></div>

            <!-- 하단 댓글형 생각 정리 & 피드백 메모 공간 -->
            <section id="memoSection" class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 md:p-6">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-200">
                    <div>
                        <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <span>💬 오늘의 생각 & 피드백 메모장</span>
                            <span id="memoCountBadge" class="bg-blue-100 text-blue-700 text-xs font-bold px-2 py-0.5 rounded-full">0</span>
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">선택한 날짜(<span id="memoCurrentDateText" class="font-semibold text-slate-700"></span>)에 귀속되어 브라우저에 자동 보관됩니다. 좌측 날짜를 클릭하면 그날 적은 메모를 다시 복기할 수 있습니다.</p>
                    </div>
                    <button id="exportMemosBtn" type="button" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium px-3 py-1.5 rounded-lg transition">
                        📥 전체 메모 텍스트 복사
                    </button>
                </div>

                <!-- 댓글 입력 폼 -->
                <div class="mt-4 bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-3">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="text-xs font-semibold text-slate-600">분류 태그:</span>
                        <button type="button" data-tag="시장생각" class="memo-tag-btn text-xs px-2.5 py-1 rounded-full font-semibold bg-blue-600 text-white">💡 시장생각</button>
                        <button type="button" data-tag="매매복기" class="memo-tag-btn text-xs px-2.5 py-1 rounded-full font-semibold bg-white text-slate-600 border border-slate-300">🎯 매매복기</button>
                        <button type="button" data-tag="종목체크" class="memo-tag-btn text-xs px-2.5 py-1 rounded-full font-semibold bg-white text-slate-600 border border-slate-300">📌 종목체크</button>
                        <button type="button" data-tag="질문/피드백" class="memo-tag-btn text-xs px-2.5 py-1 rounded-full font-semibold bg-white text-slate-600 border border-slate-300">❓ 질문/피드백</button>
                    </div>
                    <textarea id="memoInput" rows="3" placeholder="오늘 시황이나 공부 내용을 보며 든 생각, 내일 장 대응 계획, 종목 피드백을 댓글처럼 남겨보세요..." class="w-full rounded-lg border border-slate-300 p-3 text-sm focus:outline-none focus:border-blue-600 bg-white"></textarea>
                    <div class="flex items-center justify-between">
                        <span id="memoToast" class="text-xs text-emerald-600 font-medium"></span>
                        <button id="addMemoBtn" type="button" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-lg shadow-sm transition">
                            + 댓글 메모 등록
                        </button>
                    </div>
                </div>

                <!-- 등록된 댓글 리스트 -->
                <div id="memoListContainer" class="mt-5 space-y-3"></div>
            </section>
        </div>

        <!-- 탭 2: 한글파일 vs PB 리포트 비교분석 뷰 -->
        <div id="viewCompare" class="hidden max-w-5xl mx-auto p-4 md:p-8 space-y-6">
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-5">
                <h3 class="text-lg font-bold text-slate-900 section-bar">1. 한글파일(HWPX) 양식 vs NH투자증권 PB 자료 비교 분석</h3>
                <p class="text-sm text-slate-600">두 자료는 상호 보완성이 매우 뛰어납니다. 한글파일 양식이 <strong>'직관적인 정량 랭킹과 테마 분류'</strong>에 강점이 있다면, PB 리포트는 <strong>'수급의 이면 해석과 조건부 매매 전략'</strong>에 강점이 있습니다.</p>

                <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse border border-slate-200">
                        <thead>
                            <tr class="bg-slate-100 text-slate-800">
                                <th class="border border-slate-200 p-3 text-left w-28">비교 항목</th>
                                <th class="border border-slate-200 p-3 text-left">한글파일(HWPX) 캡처 양식</th>
                                <th class="border border-slate-200 p-3 text-left">NH투자증권 PB 리포트</th>
                                <th class="border border-slate-200 p-3 text-left bg-blue-50 text-blue-900">통합 대시보드 반영 방식 (장점 결합)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200">
                            <tr>
                                <td class="border border-slate-200 p-3 font-semibold bg-slate-50">시황 요약</td>
                                <td class="border border-slate-200 p-3">코스피·코스닥 종가, 거래대금, 투자자별 순매수 표 + 하단 종합 시황 박스</td>
                                <td class="border border-slate-200 p-3">비차익 매도, 달러선물, 신용잔고·반대매매, ADR·VKOSPI 등 선행 수급 진단</td>
                                <td class="border border-slate-200 p-3 bg-blue-50/40 font-medium">한글파일의 깔끔한 지수 표 + PB의 선행 수급 지표 & 노란/빨간 형광펜 핵심 요약 결합</td>
                            </tr>
                            <tr>
                                <td class="border border-slate-200 p-3 font-semibold bg-slate-50">급등주 선별</td>
                                <td class="border border-slate-200 p-3">단순 상승률 TOP 15(소액 잡주 혼재)와 500억 이상 상승률 상위를 분리</td>
                                <td class="border border-slate-200 p-3">상한가 종목 테이블 및 52주 신고가 섹터 변화 추적</td>
                                <td class="border border-slate-200 p-3 bg-blue-50/40 font-medium">요청하신 대로 2·3번을 통합하여 <strong>[거래대금 500억 이상 & 상승률 TOP 15]</strong>로 일원화 (실질 주도주만 압축)</td>
                            </tr>
                            <tr>
                                <td class="border border-slate-200 p-3 font-semibold bg-slate-50">테마 & 섹터</td>
                                <td class="border border-slate-200 p-3">7대 핵심 테마 그룹 + 연관 키워드 배지 + 소속 종목(등락률) 알약 배지</td>
                                <td class="border border-slate-200 p-3">돈 될 섹터별 팩트 체크 + 추격 금지/분할 매수 등 구체적 대응 원칙 제시</td>
                                <td class="border border-slate-200 p-3 bg-blue-50/40 font-medium">한글파일의 <strong>배지형 테마 묶음 표</strong>에 PB의 <strong>섹터별 실전 대응 전략</strong> 컬럼 추가</td>
                            </tr>
                            <tr>
                                <td class="border border-slate-200 p-3 font-semibold bg-slate-50">거래대금 상위</td>
                                <td class="border border-slate-200 p-3">합산 거래대금(KRX+NXT) TOP 15 종목 및 변동 원인</td>
                                <td class="border border-slate-200 p-3">삼전·하이닉스 거래대금 쏠림 비중(68.1%) 및 디커플링 원인 분석</td>
                                <td class="border border-slate-200 p-3 bg-blue-50/40 font-medium">합산 거래대금 TOP 15 리스트 + 상단에 시장 쏠림도 지표 표시</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 탭 3: GitHub generate.py 코드 복사 뷰 -->
        <div id="viewGithub" class="hidden max-w-5xl mx-auto p-4 md:p-8 space-y-6">
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
                <div class="flex flex-wrap items-center justify-between gap-2">
                    <div>
                        <h3 class="text-lg font-bold text-slate-900 section-bar">GitHub 저장소 적용 가이드 (`generate.py`)</h3>
                        <p class="text-xs text-slate-500 mt-1">아래 코드를 복사하여 GitHub의 `generate.py`에 붙여넣으시면 좌측 날짜별 아카이브, 4단 통합 시황 표, 심화 스터디, 하단 댓글 메모장이 포함된 웹페이지가 생성됩니다.</p>
                    </div>
                    <button id="copyPythonCodeBtn" type="button" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-lg shadow-sm transition">
                        📋 generate.py 전체 코드 복사
                    </button>
                </div>
                <div id="copyCodeToast" class="text-xs font-semibold text-emerald-600"></div>
                <pre id="pythonCodeBlock" class="bg-slate-900 text-slate-100 p-4 rounded-xl text-xs overflow-x-auto leading-relaxed max-h-96"></pre>
            </div>
        </div>
    </main>

    <script>
        // 일자별 아카이브 데이터 (한글파일 HWPX + NH투자증권 PB 리포트 실제 데이터 통합)
        const ARCHIVE_DATA = [
            {
                date: "2026-10-14",
                label: "2026-10-14 (수)",
                badge: "투매 진정 · 신용 반대매매 개시",
                title: "매도 압력 1/4 급감 속 개인→기관 수급 교대 & 해운·정유 주도주 부상",
                indices: [
                    {
                        name: "코스피 (KOSPI)",
                        close: "6,008.81",
                        change: "▼ 26.54 (-0.44%)",
                        isUp: false,
                        volume: "312,450 천 주",
                        tradingVal: "21조 4,000억 원 (NXT 포함 시 27.6조)",
                        investors: "개인 <span class='down-text font-semibold'>-4,678억</span> / 외인 <span class='down-text font-semibold'>-1조 2,969억</span> / 기관 <span class='up-text font-semibold'>+1조 105억</span>"
                    },
                    {
                        name: "코스닥 (KOSDAQ)",
                        close: "823.88",
                        change: "▼ 13.15 (-1.57%)",
                        isUp: false,
                        volume: "489,120 천 주",
                        tradingVal: "6조 2,000억 원",
                        investors: "개인 <span class='up-text font-semibold'>+4,196억</span> / 외인 <span class='down-text font-semibold'>-2,557억</span> / 기관 <span class='down-text font-semibold'>-1,797억</span>"
                    }
                ],
                macroMetrics: [
                    { label: "원/달러 환율", val: "1,338.3원 (-6.8원)", note: "야간 1,336.7원 · 외인 달러선물 -4,829억 전향" },
                    { label: "국고채 3년 / VKOSPI", val: "3.883% (+2.6bp) / 44.91 (-7.46%)", note: "채권 피신 중단 · 공포지수 사흘 만에 하락" },
                    { label: "고객예탁금 / 신용잔고", val: "100.4조 (+3,289억) / 34.2조 (+4,774억)", note: "대기자금 유지 vs 동시호가 반대매매 출회" },
                    { label: "코스피 ADR / 상승:하락", val: "72.06 (+1.34) / 507 : 371", note: "지수는 약보합이나 상승 종목 수가 4일 만에 우위" }
                ],
                summaryHtml: `
                    <p>• <span class="hl-yellow">외국인 코스피 순매도가 전일 -5.18조에서 -1.29조로 4분의 1 수준으로 급감</span>하고 비차익 매도(-1,622억)가 사실상 소멸하며 3일간의 패닉 투매는 일단락되었습니다.</p>
                    <p>• 다만 5거래일간 12.2조를 받아내던 개인이 -4,678억 순매도로 돌아서고, <span class="hl-red">장 초반 동시호가부터 신용 반대매매 물량이 출회</span>되었습니다. 반대매매는 통상 3~5거래일간 소화되므로 장중 출렁임을 활용한 현금 분할 대응이 유효합니다.</p>
                    <p>• ASML의 실적 상회에도 '셀온(Sell-on)'이 나오며 반도체 52주 신고가가 8종에서 0종으로 줄어든 반면, <span class="hl-yellow">백악관의 알래스카 LNG 투자 언급 및 유가($94.14) 고착 수혜로 해운·피팅·정유주가 새로운 주도주로 교체</span>되었습니다.</p>
                `,
                scheduleCheck: [
                    { day: "10/14 (수)", event: "재경부 AI·K-뷰티 지원방안 / 금감원 증권사 위탁수수료 개편 / ASML 실적 셀온", impact: "에이피알 +4.06% 반등, 소부장 장 막판 조정" },
                    { day: "10/15 (목) ★", event: "TSMC 3Q 실적 & 2027 CapEx 가이던스 / 美 9월 PPI·소매판매 / 금융위 가계부채 점검회의", impact: "소부장 재진입 여부 결정할 핵심 분수령" },
                    { day: "10/16 (금) ★", event: "케빈 워시 연준의장 × IMF 총재 대담(12:30) / 韓 9월 고용동향·10월 그린북 / 美 옵션만기", impact: "10/17 FOMC 블랙아웃 전 마지막 통화정책 힌트" }
                ],
                top500UpList: [
                    { rank: 1, name: "팬오션", price: "+10.30% (신고가)", val: "1,840억 원", reason: "VLCC 운임 60년래 최고치 및 미국 알래스카 LNG 운송 수혜 기대감에 해운업종 대장주 등극" },
                    { rank: 2, name: "한선엔지니어링", price: "+26.93%", val: "1,120억 원", reason: "백악관 대변인 첫 브리핑서 '한국 알래스카 LNG 투자' 언급에 따른 가스 파이프라인 피팅·밸브 수혜" },
                    { rank: 3, name: "화성밸브", price: "+18.09%", val: "940억 원", reason: "알래스카 LNG 프로젝트 가스 밸브 공급 기대감으로 대량 거래 수반 급등" },
                    { rank: 4, name: "대한제강", price: "+13.77%", val: "680억 원", reason: "LNG 파이프라인 및 에너지 인프라용 철강재 수요 확대 부각" },
                    { rank: 5, name: "삼성SDI", price: "+6.43%", val: "9,840억 원", reason: "EU의 중국산 전기차·하이브리드 규제 및 과매도 인식 속 거래대금 상위 4위 기록하며 강한 반등" },
                    { rank: 6, name: "HMM", price: "+5.60% (신고가)", val: "2,150억 원", reason: "해운 운임 강세 및 USTR 입항 수수료 시행에 따른 반사이익 기대" },
                    { rank: 7, name: "SK이노베이션", price: "+4.53% (신고가)", val: "2,822억 원", reason: "WTI 94달러 고착이 정제마진 및 재고이익 수혜 프레임으로 전환되며 기관 매수 유입" },
                    { rank: 8, name: "에이피알", price: "+4.06%", val: "2,675억 원", reason: "전일(-18.89%) 과매도 되돌림 및 정부의 AI·융복합 K-뷰티 서비스 지원방안 발표 모멘텀" },
                    { rank: 9, name: "안랩", price: "+2.50% (신고가)", val: "790억 원", reason: "국가 AI 안전망(N2SF) 구축 모멘텀 지속으로 이틀 연속 52주 신고가 경신" },
                    { rank: 10, name: "LG에너지솔루션", price: "+2.44%", val: "4,142억 원", reason: "중국 NEV 수출세 환급률 인하 및 EU 정상회의 중국산 EV 축소 추인 기대감" }
                ],
                themes: [
                    {
                        group: "1. 해운 · 알래스카 LNG · 피팅 (신규 1순위 주도축)",
                        badges: ["알래스카LNG", "VLCC운임최고", "파이프라인피팅"],
                        stocks: ["한선엔지니어링 (+26.93%)", "화성밸브 (+18.09%)", "대한제강 (+13.77%)", "팬오션 (+10.30%)", "HMM (+5.60%)"],
                        strategy: "운임·제도 실물 지표가 받치는 섹터. 단 피팅주는 당일 급등 추격 금지, 해운주는 조정 시 분할 접근"
                    },
                    {
                        group: "2. 정유 · 화학 (유가 94달러 수혜 전환)",
                        badges: ["WTI94달러", "정제마진개선", "재고평가이익"],
                        stocks: ["SK이노베이션 (+4.53%)", "S-Oil (+3.10%)", "롯데케미칼 (+2.45%)"],
                        strategy: "유가 고착이 금리 악재에서 정유·화학 수혜로 해석 전환. 9월 CPI 결과 확인 후 비중 결정"
                    },
                    {
                        group: "3. 2차전지 & 우주항공 배터리 (과매도 되돌림)",
                        badges: ["중국의무감축", "EU관세추인", "위성용배터리"],
                        stocks: ["에스엠벡셀 (+29.93% 상)", "삼성SDI (+6.43%)", "LG에너지솔루션 (+2.44%)"],
                        strategy: "과매도 기술적 반등 구간(2~3일 호흡). 10/15~16 EU 정상회의 추인 여부 확인 후 중기 전환 판단"
                    },
                    {
                        group: "4. M&A · 경영권 매각 & 자산 재평가 테마",
                        badges: ["로봇인수", "경영권매각", "터미널복합개발"],
                        stocks: ["유니켐 (+30.00% 상)", "씨엑스아이 (+29.99% 상)", "프롬바이오 (+29.96% 상)", "천일고속 (+29.78% 상)"],
                        strategy: "상폐 가처분 테마(6종→3종 축소)에서 이탈한 개인 자금이 개별 M&A·자산주 테마로 순환"
                    },
                    {
                        group: "5. 반도체 메가캡 디커플링 & 소부장 셀온 조정",
                        badges: ["이재용증여수령", "ASML셀온", "TSMC대기"],
                        stocks: ["삼성전자 (+1.08%)", "삼성전기 (+1.10%)", "SK하이닉스 (-1.25%)", "한미반도체 (-5.02%)", "주성엔지니어링 (-7.63%)"],
                        strategy: "삼전(배당 명분)과 하이닉스(HBM4 장비 연기 보도) 차별화. 소부장은 10/15 TSMC CapEx 확인 후 진입"
                    }
                ],
                topTradingValList: [
                    { rank: 1, name: "SK하이닉스", price: "-1.25%", isUp: false, val: "7조 7,400억 원", reason: "HBM4 장비 도입 연기 보도 및 자사주 매입 종료 임박 속 약보합" },
                    { rank: 2, name: "삼성전자", price: "+1.08%", isUp: true, val: "6조 8,300억 원", reason: "이재용 회장 약 1,100만주 증여 수령 완료(상속세 블록딜 우려 해소 및 배당 확대 기대)" },
                    { rank: 3, name: "삼성전기", price: "+1.10%", isUp: true, val: "1조 2,200억 원", reason: "AI 서버용 MLCC 견조한 수요에 힘입어 기관 매수세 유입" },
                    { rank: 4, name: "삼성SDI", price: "+6.43%", isUp: true, val: "9,840억 원", reason: "전일 급락 과매도 인식 및 유럽 시장 반사이익 기대감에 대형 2차전지 중 최대 반등" },
                    { rank: 5, name: "삼성전자우", price: "+0.23%", isUp: true, val: "8,053억 원", reason: "본주 배당 확대 명분 부각에 따른 우선주 방어적 매수 유입" },
                    { rank: 6, name: "SK스퀘어", price: "-0.47%", isUp: false, val: "7,044억 원", reason: "SK하이닉스 숨고르기에 연동된 지주사 단기 보합권 등락" },
                    { rank: 7, name: "주성엔지니어링", price: "-7.63%", isUp: false, val: "4,867억 원", reason: "전일 나홀로 강세(+3.75%) 이후 ASML 셀온 여파로 차익실현 매물 출회" },
                    { rank: 8, name: "LG에너지솔루션", price: "+2.44%", isUp: true, val: "4,142억 원", reason: "북미 ESS 및 LFP 공급계약 모멘텀 지속으로 이틀 연속 상승" },
                    { rank: 9, name: "두산에너빌리티", price: "-1.85%", isUp: false, val: "2,845억 원", reason: "원전주 단기 수급 공백 속 해운·정유로의 메이저 수급 이동 영향" },
                    { rank: 10, name: "SK이노베이션", price: "+4.53%", isUp: true, val: "2,822억 원", reason: "유가 94달러 정착에 따른 정유·화학 섹터 수혜 전환으로 52주 신고가" }
                ],
                study: {
                    title: "전환사채(CB) 발행 공시 행간 읽기 — 표면적인 '희석 악재'와 '설비투자 호재' 구별법",
                    caseRef: "실전 사례: 10/14 대주전자재료 사모 전환사채 700억 발행 공시 (전환가 120,000원, 당일 주가 상승)",
                    points: [
                        "1. 전환가액(Conversion Price) 프리미엄 확인: 통상 CB는 주가 희석 우려로 악재로 읽히지만, 전환가액이 현재 주가보다 높은 할증 발행이거나 상단에 설정된 경우 당장의 물량 출회 부담이 낮고 기업의 성장 자신감으로 해석됩니다.",
                        "2. 자금 조달 목적(시설자금 vs 운영·채무상환자금): 조달 자금이 단순 빚 갚기(채무상환)나 적자 메우기(운영자금)면 악재이나, 핵심 성장 산업(예: 실리콘 음극재 캐파 증설)을 위한 '시설자금'일 경우 중장기 매출 증대 트리거가 됩니다.",
                        "3. 리픽싱(Refixing·전환가 조정) 조항 유무: 주가 하락 시 전환가를 낮추는 리픽싱 한도(통상 70~80%)가 있는지, 혹은 무리픽싱(100% 고정)인지 DART 공시 세부표에서 반드시 확인해야 오버행(잠재 매도물량) 규모를 추산할 수 있습니다."
                    ]
                }
            },
            {
                date: "2026-10-13",
                label: "2026-10-13 (화)",
                badge: "코스피 -5.46% · 매도 사이드카",
                title: "CXMT DDR5 진출 우려 및 외인 4.5조 투매 속 500억↑ 호남 클러스터·2차전지 선별 강세",
                indices: [
                    {
                        name: "코스피 (KOSPI)",
                        close: "6,035.35",
                        change: "▼ 348.89 (-5.46%)",
                        isUp: false,
                        volume: "399,872 천 주",
                        tradingVal: "26조 7,946억 원 (NXT 포함 시 50.7조)",
                        investors: "개인 <span class='up-text font-semibold'>+2조 2,361억</span> / 외인 <span class='down-text font-semibold'>-4조 5,200억</span> / 기관 <span class='up-text font-semibold'>+1조 6,885억</span>"
                    },
                    {
                        name: "코스닥 (KOSDAQ)",
                        close: "837.03",
                        change: "▼ 12.16 (-1.43%)",
                        isUp: false,
                        volume: "513,476 천 주",
                        tradingVal: "6조 8,424억 원",
                        investors: "개인 <span class='down-text font-semibold'>-1,909억</span> / 외인 <span class='up-text font-semibold'>+1,382억</span> / 기관 <span class='up-text font-semibold'>+429억</span>"
                    }
                ],
                macroMetrics: [
                    { label: "원/달러 환율", val: "1,343.40원 (+7.40원)", note: "외국인 현·선물 동반 매도에 환율 급등" },
                    { label: "시장 변동성", val: "매도 사이드카 발동", note: "장중 코스피 6% 이상 급락하며 프로그램 호가 정지" },
                    { label: "자사주 수급 변화", val: "삼성전자 15조 매입 완료", note: "일평균 1.61조 흡수하던 수급 안전판 반감" },
                    { label: "500억↑ 상승 종목", val: "양 시장 합산 6개 종목", note: "폭락장 속 수급이 검증된 극소수 종목만 생존" }
                ],
                summaryHtml: `
                    <p>• 13일 국내 증시는 중국 창신메모리(CXMT)의 연내 서버용 DDR5 시장 진출 소식에 따른 메모리 경쟁 심화 우려와 <span class="hl-red">삼성전자 자사주 매입 완료로 외국인 매물을 흡수할 안전판이 부재해진 가운데 외인이 4.5조 원 이상 투매</span>하며 -5.46% 폭락했습니다.</p>
                    <p>• 반면 한국거래소의 시가총액 요건 미달 상장폐지 절차 잠정 유예 결정으로 관리종목 중심의 상한가 랠리가 펼쳐졌고, <span class="hl-yellow">거래대금 500억 이상 종목 중에서는 호남 반도체 클러스터(서산·금호전기) 및 LFP 대형 계약을 맺은 LG에너지솔루션 등 6종목만 상승</span> 마감했습니다.</p>
                `,
                scheduleCheck: [
                    { day: "10/13 (화) ★", event: "IMF 10월 세계경제전망(WEO) / 금융위 부동산 PF 점검회의 / 한은 금통위 의사록 공개", impact: "대형 반도체 투매로 매도 사이드카 발동" },
                    { day: "10/14 (수)", event: "ASML 3분기 실적 발표 / 정부 AI·K-뷰티 지원방안 발표", impact: "반도체 장비 사이클 지속 여부 판가름" }
                ],
                top500UpList: [
                    { rank: 1, name: "서산", price: "8,780원 (+29.88%) 상", val: "880.6억 원 (KRX 880.6억)", reason: "최태원 SK그룹 회장의 호남 방문 및 반도체 클러스터 투자 의지 재확인 소식에 지역 레미콘·인프라 대장주 상한가" },
                    { rank: 2, name: "두산테스나", price: "132,900원 (+7.35%)", val: "1,000.3억 원 (NXT 1,000.3억)", reason: "시스템반도체 후공정(OSAT) 테스트 가동률 회복 및 4분기 실적 개선 기대감에 강세" },
                    { rank: 3, name: "라온시큐어", price: "17,290원 (+5.75%)", val: "2,585.5억 원 (KRX 2,585.5억)", reason: "금융권 AI 해킹 대응 보안 솔루션 및 모바일 신분증(DID) 확대 기대감에 대규모 자금 유입" },
                    { rank: 4, name: "주성엔지니어링", price: "262,500원 (+3.75%)", val: "5,440.1억 원 (KRX 5,440.1억)", reason: "차세대 반도체 공정 증착 장비 글로벌 수주 기대감 부각되며 대형 IT 폭락 속 나홀로 상승" },
                    { rank: 5, name: "LG에너지솔루션", price: "410,500원 (+3.14%)", val: "3,486.5억 원 (KRX 2,462.5억 + NXT 1,024.0억)", reason: "엘앤에프와의 조 단위 LFP 양극재 대형 공급계약 체결 및 북미 ESS 점유율 확대 모멘텀 부각" },
                    { rank: 6, name: "금호전기", price: "11,380원 (+2.80%)", val: "4,056.9억 원 (KRX 4,056.9억)", reason: "호남 반도체 메가클러스터 전력 송배전 및 산업용 특수조명 공급 수혜 기대감에 4천억대 거래 수반" }
                ],
                themes: [
                    {
                        group: "1. 상장폐지 절차 유예 안도 랠리",
                        badges: ["상폐유예", "시총미달제동", "관리종목반등"],
                        stocks: ["하이퍼코퍼레이션 (+30.00% 상)", "예선테크 (+29.97% 상)", "바이오인프라 (+29.92% 상)", "형지I&C (+29.89% 상)", "뉴인텍 (+29.78% 상)", "형지글로벌 (+29.78% 상)", "모아데이타 (+20.81%)"],
                        strategy: "소액 찌라시·품절주 성격이 강하므로 1,000원 미만 종목 배제 및 포트 비중 엄격 제한"
                    },
                    {
                        group: "2. 2차전지 & LFP 소재",
                        badges: ["LFP양극재", "대형수주", "북미ESS"],
                        stocks: ["LG에너지솔루션 (+3.14%)", "STX (+3.32%)", "SK이노베이션 (+2.09%)", "엘앤에프 (+1.87%)", "SFA넥셀 (+0.72%)"],
                        strategy: "반도체에서 빠져나온 기관 수급이 유입되는 방어축. 대형 셀·소재주 중심 대응"
                    },
                    {
                        group: "3. 호남 반도체 클러스터 & 인프라",
                        badges: ["호남클러스터", "SK투자", "지역건자재"],
                        stocks: ["서산 (+29.88% 상)", "금호전기 (+2.80%)", "유신 (+2.15%)"],
                        strategy: "거래대금 500억 이상이 실린 대장주(서산·금호전기) 위주로만 단기 트레이딩 유효"
                    },
                    {
                        group: "4. 시스템반도체 & 후공정 장비",
                        badges: ["OSAT테스트", "차세대증착", "소부장선별"],
                        stocks: ["두산테스나 (+7.35%)", "주성엔지니어링 (+3.75%)", "레이저쎌 (+2.45%)"],
                        strategy: "ASML 및 TSMC 실적 발표 전까지는 추격 매수 자제 및 가이던스 확인 필수"
                    },
                    {
                        group: "5. 사이버보안 & 디지털인증 (DID)",
                        badges: ["AI보안위협", "모바일신분증", "생체인증"],
                        stocks: ["라온시큐어 (+5.75%)", "코나아이 (+1.12%)"],
                        strategy: "2,500억대 거래대금이 터진 라온시큐어 중심 눌림목 관찰"
                    }
                ],
                topTradingValList: [
                    { rank: 1, name: "SK하이닉스", price: "1,453,000원 (-9.47%)", isUp: false, val: "11조 2,802억 원 (KRX 7.63조 + NXT 3.64조)", reason: "중국 CXMT의 서버용 DDR5 시장 진출 계획 공개 및 외국인 대량 순매도 폭탄에 급락" },
                    { rank: 2, name: "삼성전자", price: "233,500원 (-6.79%)", isUp: false, val: "9조 2,543억 원 (KRX 5.62조 + NXT 3.62조)", reason: "자사주 매입 완료 후 수급 안전판 부재 속에 코스피 외인 4.5조 원 매도 집중되며 급락" },
                    { rank: 3, name: "삼성전기", price: "1,377,000원 (-7.40%)", isUp: false, val: "1조 9,002억 원 (KRX 1.22조 + NXT 6,751억)", reason: "IT 세트 수요 회복 지연 우려 및 반도체 섹터 급랭 여파로 외인·기관 투매" },
                    { rank: 4, name: "SK스퀘어", price: "867,000원 (-11.89%)", isUp: false, val: "1조 2,706억 원 (KRX 9,883억 + NXT 2,823억)", reason: "자회사 SK하이닉스 폭락에 따른 지주사 지분 가치 급감 우려로 두 자릿수 하락" },
                    { rank: 5, name: "삼성전자우", price: "174,600원 (-6.53%)", isUp: false, val: "8,807억 원 (KRX 8,807억)", reason: "삼성전자 본주 폭락에 동조화된 패시브 외국인 매도세 집중" },
                    { rank: 6, name: "삼성SDI", price: "557,000원 (-0.71%)", isUp: false, val: "6,510억 원 (KRX 3,581억 + NXT 2,929억)", reason: "증시 전반의 급락세 속에서도 2차전지 반등세 힘입어 보합권 방어" },
                    { rank: 7, name: "주성엔지니어링", price: "262,500원 (+3.75%)", isUp: true, val: "5,440.1억 원 (KRX 5,440.1억)", reason: "차세대 반도체 공정 장비 글로벌 수주 기대감에 코스피 폭락 속 나홀로 상승" },
                    { rank: 8, name: "에이피알", price: "284,500원 (-19.18%)", isUp: false, val: "4,632억 원 (KRX 3,619억 + NXT 1,013억)", reason: "해외 물류비 부담으로 3분기 실적이 시장 컨센서스를 대폭 하회할 것이라는 우려" }
                ],
                study: {
                    title: "거래대금 500억 필터의 의미와 KRX·NXT(대체거래소) 합산 수급 해석법",
                    caseRef: "실전 사례: 10/13 코스피 -5.46% 폭락장 속 단순 상승률 상위 vs 500억 이상 상승 상위 비교",
                    points: [
                        "1. 왜 '거래대금 500억 원 이상'인가?: 지수 급락장에서는 호가창이 얇은 거래대금 5억~30억 원대 품절주·관리종목이 적은 돈으로도 상한가에 직행합니다. 반면 500억 원 이상 터지며 상승한 종목은 기관·외인·메이저 트레이더의 실질 자금이 유입된 진짜 주도주입니다.",
                        "2. KRX(정규거래소) + NXT(대체거래소) 합산 확인: 프리마켓(08:00~)·메인마켓·애프터마켓 거래대금을 합산해야 하루 동안 특정 종목에 쏠린 총 유동성 규모와 장전/장후 수급 변화를 정확히 추적할 수 있습니다.",
                        "3. 메가캡 거래대금 쏠림 지표: 삼성전자+SK하이닉스 합산 거래대금이 코스피 전체의 65~80%를 넘어가면 중소형주 유동성이 마르는 구간이므로 지수보다 거래대금 쏠림 완화 여부를 먼저 체크해야 합니다."
                    ]
                }
            },
            {
                date: "2026-10-12",
                label: "2026-10-12 (월)",
                badge: "삼성전자 자사주 완료 · 신용잔고 급증",
                title: "대외경제장관회의 공급망 점검 및 반도체 대형주 차익실현 조정",
                indices: [
                    {
                        name: "코스피 (KOSPI)",
                        close: "6,384.24",
                        change: "▼ 241.80 (-3.65%)",
                        isUp: false,
                        volume: "345,110 천 주",
                        tradingVal: "24조 1,200억 원",
                        investors: "개인 <span class='up-text font-semibold'>+2조 1,700억</span> / 외인 <span class='down-text font-semibold'>-2조 5,089억</span> / 기관 <span class='down-text font-semibold'>-3,196억</span>"
                    },
                    {
                        name: "코스닥 (KOSDAQ)",
                        close: "849.19",
                        change: "▼ 18.40 (-2.12%)",
                        isUp: false,
                        volume: "460,800 천 주",
                        tradingVal: "6조 5,100억 원",
                        investors: "개인 <span class='up-text font-semibold'>+3,120억</span> / 외인 <span class='down-text font-semibold'>-1,850억</span> / 기관 <span class='down-text font-semibold'>-1,100억</span>"
                    }
                ],
                macroMetrics: [
                    { label: "신용잔고 변화", val: "34조 2,887억 (+4,774억)", note: "지수 하락 구간에 오히려 저가매수 레버리지 급증 (반대매매 경고등)" },
                    { label: "수급 이벤트", val: "삼성전자 15조 자사주 완료", note: "8~9월 지수를 방어하던 핵심 수급 완충재 종료" },
                    { label: "정부 주요 일정", val: "대외경제장관회의 · 한은 국감", note: "공급망안정화위원회 개최 및 통화정책 질의" },
                    { label: "원/달러 환율", val: "1,336.0원 (+4.2원)", note: "외국인 현물 매도에 따른 원화 약세 압력" }
                ],
                summaryHtml: `
                    <p>• 삼성전자의 15조 원 규모 자사주 매입 프로그램이 최종 완료되면서 수급 공백 우려가 부각되었고, 외국인이 코스피에서 2.5조 원을 순매도하며 지수가 -3.65% 조정받았습니다.</p>
                    <p>• 특히 지수가 밀리는 와중에 <span class="hl-red">신용잔고가 +4,774억 원 급증하며 34.2조 원에 도달</span>해 추가 하락 시 담보부족 반대매매가 나올 수 있는 취약한 수급 구조가 형성되었습니다.</p>
                `,
                scheduleCheck: [
                    { day: "10/12 (월) ★", event: "재경부 제274차 대외경제장관회의·공급망안정화위 / 한국은행 총재 국정감사 / KDI 경제동향", impact: "공급망 선도사업자 지원 및 금리 신중론 확인" }
                ],
                top500UpList: [
                    { rank: 1, name: "안랩", price: "+12.30% (신고가)", val: "920억 원", reason: "정부 국가 AI 안전망(N2SF) 보안 가이드라인 수혜 부각" },
                    { rank: 2, name: "피에스케이", price: "+6.80% (신고가)", val: "740억 원", reason: "반도체 전공정 PR 스트립 장비 글로벌 수주 모멘텀" },
                    { rank: 3, name: "디아이", price: "+5.40% (신고가)", val: "810억 원", reason: "HBM용 번인 테스터 공급 확대 기대감" }
                ],
                themes: [
                    {
                        group: "1. 사이버보안 & 국가망 보안",
                        badges: ["국가AI안전망", "클라우드보안"],
                        stocks: ["안랩 (+12.30%)", "라온시큐어 (+4.10%)"],
                        strategy: "지수 조정과 무관한 정책 모멘텀 섹터로 거래대금 수반 여부 체크"
                    }
                ],
                topTradingValList: [
                    { rank: 1, name: "삼성전자", price: "-3.80%", isUp: false, val: "5조 4,200억 원", reason: "15조 자사주 매입 완료 당일 수급 공백 우려 반영" },
                    { rank: 2, name: "SK하이닉스", price: "-4.10%", isUp: false, val: "4조 8,900억 원", reason: "외국인 반도체 차익실현 매물 출회" }
                ],
                study: {
                    title: "자사주 매입(Buyback) vs 자사주 소각(Cancellation)이 주가와 수급에 미치는 차이",
                    caseRef: "실전 사례: 10/12 삼성전자 자사주 매입 완료와 10/15 HDC 자사주 341만주 소각 비교",
                    points: [
                        "1. 자사주 매입 기간의 '수급 방어판' 효과: 대기업이 장내에서 매일 수천억 원씩 자사주를 매입하는 동안에는 외국인 패시브 매도를 받아내는 하방 경직성이 작동하지만, 매입 완료 직후에는 일시적 수급 공백(Air Pocket)이 발생할 수 있습니다.",
                        "2. 단순 매입과 소각의 결정적 차이: 매입만 한 자사주는 향후 블록딜이나 교환사채(EB) 형태로 다시 시장에 나올 수 있지만, '소각'은 발행주식수 자체를 영구히 줄여 주당순이익(EPS)과 주당순자산가치(BPS)를 비가역적으로 높입니다."
                    ]
                }
            }
        ];

        // 상태 변수
        let currentDate = ARCHIVE_DATA[0].date;
        let selectedMemoTag = "시장생각";

        // 안전하게 localStorage 읽기/쓰기
        function loadMemos(dateStr) {
            try {
                const raw = localStorage.getItem("market_memos_" + dateStr);
                if (raw) return JSON.parse(raw);
            } catch (e) {}
            // 기본 샘플 메모 제공 (최초 열람 시)
            if (dateStr === "2026-10-14") {
                return [
                    {
                        id: "sample-1",
                        tag: "시장생각",
                        text: "외국인 매도가 1/4로 줄어든 점은 긍정적이나 신용 반대매매가 이제 막 시작됐으니 3거래일 정도는 현금 비중을 지키며 해운·정유 눌림목을 봐야겠다.",
                        time: "2026-10-14 21:15"
                    }
                ];
            }
            return [];
        }

        function saveMemos(dateStr, list) {
            try {
                localStorage.setItem("market_memos_" + dateStr, JSON.stringify(list));
            } catch (e) {}
        }

        // 좌측 날짜 아카이브 렌더링
        function renderSidebar(filterText = "") {
            const nav = document.getElementById("dateListNav");
            const q = filterText.trim().toLowerCase();
            const filtered = ARCHIVE_DATA.filter(item =>
                item.date.includes(q) ||
                item.label.toLowerCase().includes(q) ||
                item.title.toLowerCase().includes(q) ||
                item.badge.toLowerCase().includes(q)
            );

            document.getElementById("archiveCountBadge").textContent = filtered.length + "일";

            nav.innerHTML = filtered.map(item => {
                const isSelected = item.date === currentDate;
                const memoCount = loadMemos(item.date).length;
                return `
                    <button type="button" data-date="${item.date}" class="date-nav-item w-full text-left p-3 rounded-xl transition border ${
                        isSelected
                            ? "bg-blue-600 text-white border-blue-500 shadow-sm"
                            : "bg-slate-800/70 hover:bg-slate-800 text-slate-200 border-slate-700/80"
                    }">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold">${item.label}</span>
                            <span class="text-[11px] px-1.5 py-0.5 rounded ${
                                isSelected ? "bg-blue-700 text-blue-100" : "bg-slate-700 text-slate-300"
                            }">💬 ${memoCount}</span>
                        </div>
                        <div class="text-[11px] mt-1 font-medium truncate ${
                            isSelected ? "text-blue-100" : "text-amber-400"
                        }">${item.badge}</div>
                        <div class="text-[11px] mt-0.5 truncate ${
                            isSelected ? "text-blue-200" : "text-slate-400"
                        }">${item.title}</div>
                    </button>
                `;
            }).join("");

            nav.querySelectorAll(".date-nav-item").forEach(btn => {
                btn.addEventListener("click", () => {
                    currentDate = btn.getAttribute("data-date");
                    switchTab("report");
                    renderSidebar(document.getElementById("dateSearchInput").value);
                    renderReport(currentDate);
                    renderMemos(currentDate);
                });
            });
        }

        // 메인 리포트 렌더링
        function renderReport(dateStr) {
            const data = ARCHIVE_DATA.find(d => d.date === dateStr) || ARCHIVE_DATA[0];
            document.getElementById("headerDateBadge").textContent = data.label + " 마감 기준";
            document.getElementById("headerTagBadge").textContent = data.badge;
            document.getElementById("headerTitle").textContent = data.title;
            document.getElementById("memoCurrentDateText").textContent = data.label;

            const container = document.getElementById("reportContentContainer");

            // 1. 국내 주요 지수 마감 현황 + PB 선행 지표
            const indicesRows = data.indices.map(idx => `
                <tr class="border-b border-slate-100">
                    <td class="p-3.5 font-bold text-slate-900">${idx.name}</td>
                    <td class="p-3.5 font-bold text-slate-900">${idx.close}</td>
                    <td class="p-3.5 font-bold ${idx.isUp ? 'up-text' : 'down-text'}">${idx.change}</td>
                    <td class="p-3.5 text-slate-600">${idx.volume}</td>
                    <td class="p-3.5 font-semibold text-slate-800">${idx.tradingVal}</td>
                    <td class="p-3.5 text-xs leading-relaxed">${idx.investors}</td>
                </tr>
            `).join("");

            const macroCards = data.macroMetrics.map(m => `
                <div class="bg-slate-50 rounded-lg p-3 border border-slate-200">
                    <div class="text-xs text-slate-500 font-medium">${m.label}</div>
                    <div class="text-sm font-bold text-slate-900 mt-0.5">${m.val}</div>
                    <div class="text-[11px] text-slate-600 mt-1">${m.note}</div>
                </div>
            `).join("");

            const scheduleRows = data.scheduleCheck.map(s => `
                <tr class="border-b border-slate-100">
                    <td class="p-2.5 font-bold text-xs text-blue-700 whitespace-nowrap">${s.day}</td>
                    <td class="p-2.5 text-xs text-slate-800 font-medium">${s.event}</td>
                    <td class="p-2.5 text-xs text-slate-600">${s.impact}</td>
                </tr>
            `).join("");

            // 2. 거래대금 500억 이상 & 상승률 TOP 15
            const top500Rows = data.top500UpList.map(item => {
                const badgeColor = item.rank <= 3 ? "bg-amber-100 text-amber-800" : "bg-slate-100 text-slate-600";
                const hasSang = item.price.includes("상");
                const cleanPrice = item.price.replace(" 상", "");
                return `
                    <tr class="border-b border-slate-100 hover:bg-slate-50/70">
                        <td class="p-3 text-center">
                            <span class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${badgeColor}">${item.rank}</span>
                        </td>
                        <td class="p-3 font-bold text-slate-900">${item.name}</td>
                        <td class="p-3">
                            <div class="font-bold up-text">${cleanPrice}${hasSang ? '<span class="badge-sang">상</span>' : ''}</div>
                            <div class="text-xs font-semibold text-slate-800 mt-0.5">${item.val}</div>
                        </td>
                        <td class="p-3 text-xs text-slate-700 leading-relaxed">${item.reason}</td>
                    </tr>
                `;
            }).join("");

            // 3. 주요 테마별 묶음 리스트
            const themeRows = data.themes.map(t => {
                const badgesHtml = t.badges.map(b => `<span class="inline-block bg-amber-50 text-amber-800 border border-amber-200 text-[11px] font-semibold px-2 py-0.5 rounded mr-1 mb-1">${b}</span>`).join("");
                const stocksHtml = t.stocks.map(st => `<span class="inline-block bg-slate-50 border border-slate-200 text-slate-800 text-xs font-semibold px-2.5 py-1 rounded-lg mr-1.5 mb-1.5">${st.replace(/(\+[0-9.]+%[^)]*)/g, '<span class="up-text font-bold">$1</span>').replace(/(-[0-9.]+%)/g, '<span class="down-text font-bold">$1</span>')}</span>`).join("");
                return `
                    <tr class="border-b border-slate-100">
                        <td class="p-3.5 font-bold text-slate-900 align-top">${t.group}</td>
                        <td class="p-3.5 align-top">${badgesHtml}</td>
                        <td class="p-3.5 align-top">${stocksHtml}</td>
                        <td class="p-3.5 text-xs text-slate-700 bg-blue-50/30 align-top font-medium">${t.strategy}</td>
                    </tr>
                `;
            }).join("");

            // 4. 합산 거래대금 TOP 15
            const topValRows = data.topTradingValList.map(item => {
                const badgeColor = item.rank <= 3 ? "bg-amber-100 text-amber-800" : "bg-slate-100 text-slate-600";
                return `
                    <tr class="border-b border-slate-100 hover:bg-slate-50/70">
                        <td class="p-3 text-center">
                            <span class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${badgeColor}">${item.rank}</span>
                        </td>
                        <td class="p-3 font-bold text-slate-900">${item.name}</td>
                        <td class="p-3">
                            <div class="font-bold ${item.isUp ? 'up-text' : 'down-text'}">${item.price}</div>
                            <div class="text-xs font-semibold text-slate-800 mt-0.5">${item.val}</div>
                        </td>
                        <td class="p-3 text-xs text-slate-700 leading-relaxed">${item.reason}</td>
                    </tr>
                `;
            }).join("");

            // 5. 오늘의 심화 스터디
            const studyPointsHtml = data.study.points.map(p => `<li class="text-sm text-slate-700 leading-relaxed">${p}</li>`).join("");

            container.innerHTML = `
                <!-- 섹션 1 -->
                <section class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 md:p-6 space-y-4">
                    <h3 class="text-base md:text-lg font-bold text-slate-900 section-bar">1. 국내 주요 지수 마감 현황 및 시장 종합 시황 (PB 선행지표 통합)</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm border-collapse">
                            <thead>
                                <tr class="bg-slate-50 text-slate-600 border-y border-slate-200 text-xs">
                                    <th class="p-3 text-left">구분</th>
                                    <th class="p-3 text-left">마감 종가</th>
                                    <th class="p-3 text-left">전일대비 등락</th>
                                    <th class="p-3 text-left">거래량</th>
                                    <th class="p-3 text-left">거래대금</th>
                                    <th class="p-3 text-left">투자자별 순매수 동향</th>
                                </tr>
                            </thead>
                            <tbody>${indicesRows}</tbody>
                        </table>
                    </div>

                    <!-- PB 선행 수급 지표 4종 카드 -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                        ${macroCards}
                    </div>

                    <!-- 종합 시황 요약 박스 -->
                    <div class="bg-slate-50 rounded-xl p-4 border-l-4 border-blue-600 space-y-2 text-sm text-slate-700 leading-relaxed">
                        <div class="font-bold text-slate-900 flex items-center gap-1.5">💡 종합 시황 요약 & PB 수급 체크</div>
                        ${data.summaryHtml}
                    </div>

                    <!-- 주간 정부·매크로 핵심 일정 미니 테이블 -->
                    <div class="pt-2">
                        <div class="text-xs font-bold text-slate-700 mb-2">📅 당일 및 향후 핵심 정부·매크로 일정</div>
                        <div class="overflow-x-auto border border-slate-200 rounded-lg">
                            <table class="w-full text-left border-collapse">
                                <thead>
                                    <tr class="bg-slate-50 text-slate-600 text-xs border-b border-slate-200">
                                        <th class="p-2.5 w-28">일자</th>
                                        <th class="p-2.5">핵심 일정 (정부/한은/글로벌)</th>
                                        <th class="p-2.5 w-64">시장 영향 포인트</th>
                                    </tr>
                                </thead>
                                <tbody>${scheduleRows}</tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- 섹션 2 -->
                <section class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 md:p-6 space-y-4">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <h3 class="text-base md:text-lg font-bold text-slate-900 section-bar">2. 거래대금 500억 이상 & 상승률 TOP 15 종목 리스트</h3>
                        <span class="text-xs bg-rose-50 text-rose-700 border border-rose-200 px-2.5 py-1 rounded-full font-semibold">소액 품절주 배제 · 실질 수급 주도주</span>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm border-collapse">
                            <thead>
                                <tr class="bg-slate-50 text-slate-600 border-y border-slate-200 text-xs">
                                    <th class="p-3 w-14 text-center">순위</th>
                                    <th class="p-3 w-40 text-left">종목명</th>
                                    <th class="p-3 w-56 text-left">현재가(등락률) / 거래대금</th>
                                    <th class="p-3 text-left">핵심 상승 사유 (뉴스·공시 팩트체크)</th>
                                </tr>
                            </thead>
                            <tbody>${top500Rows}</tbody>
                        </table>
                    </div>
                </section>

                <!-- 섹션 3 -->
                <section class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 md:p-6 space-y-4">
                    <h3 class="text-base md:text-lg font-bold text-slate-900 section-bar">3. 주요 테마별 묶음 리스트 & 실전 대응 전략</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm border-collapse">
                            <thead>
                                <tr class="bg-slate-50 text-slate-600 border-y border-slate-200 text-xs">
                                    <th class="p-3 w-52 text-left">테마 그룹</th>
                                    <th class="p-3 w-44 text-left">연관 테마 배지</th>
                                    <th class="p-3 text-left">소속 종목 (등락률)</th>
                                    <th class="p-3 w-64 text-left">PB식 대응 원칙</th>
                                </tr>
                            </thead>
                            <tbody>${themeRows}</tbody>
                        </table>
                    </div>
                </section>

                <!-- 섹션 4 -->
                <section class="bg-white rounded-xl border border-slate-200 shadow-sm p-5 md:p-6 space-y-4">
                    <h3 class="text-base md:text-lg font-bold text-slate-900 section-bar">4. 합산 거래대금(KRX + NXT) 상위 TOP 15 종목 리스트</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm border-collapse">
                            <thead>
                                <tr class="bg-slate-50 text-slate-600 border-y border-slate-200 text-xs">
                                    <th class="p-3 w-14 text-center">순위</th>
                                    <th class="p-3 w-40 text-left">종목명</th>
                                    <th class="p-3 w-60 text-left">현재가(등락률) / 합산 거래대금</th>
                                    <th class="p-3 text-left">변동 원인 및 수급 세부 내역</th>
                                </tr>
                            </thead>
                            <tbody>${topValRows}</tbody>
                        </table>
                    </div>
                </section>

                <!-- 섹션 5: 심화 스터디 -->
                <section class="bg-indigo-50/70 rounded-xl border border-indigo-200 shadow-sm p-5 md:p-6 space-y-3">
                    <div class="flex items-center gap-2">
                        <span class="bg-indigo-600 text-white text-xs font-bold px-2.5 py-1 rounded">DEEP STUDY</span>
                        <h3 class="text-base md:text-lg font-bold text-indigo-950">5. 오늘의 심화 투자 스터디 — ${data.study.title}</h3>
                    </div>
                    <div class="text-xs font-semibold text-indigo-700 bg-white/80 px-3 py-2 rounded-lg border border-indigo-100">
                        📌 ${data.study.caseRef}
                    </div>
                    <ul class="space-y-2 pl-1">
                        ${studyPointsHtml}
                    </ul>
                </section>
            `;
        }

        // 하단 댓글형 메모 렌더링
        function renderMemos(dateStr) {
            const list = loadMemos(dateStr);
            document.getElementById("memoCountBadge").textContent = list.length;
            const container = document.getElementById("memoListContainer");

            if (list.length === 0) {
                container.innerHTML = `<div class="text-center py-6 text-xs text-slate-400 bg-slate-50 rounded-lg border border-dashed border-slate-200">아직 이 날짜에 작성된 메모가 없습니다. 위에 첫 번째 생각이나 피드백을 남겨보세요!</div>`;
                return;
            }

            container.innerHTML = list.map(m => `
                <div class="bg-white rounded-lg p-3.5 border border-slate-200 shadow-sm flex items-start justify-between gap-3">
                    <div class="space-y-1">
                        <div class="flex items-center gap-2">
                            <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">${m.tag}</span>
                            <span class="text-[11px] text-slate-400">${m.time}</span>
                        </div>
                        <p class="text-sm text-slate-800 whitespace-pre-line leading-relaxed">${m.text}</p>
                    </div>
                    <button type="button" data-id="${m.id}" class="delete-memo-btn text-xs text-slate-400 hover:text-rose-600 px-2 py-1">삭제</button>
                </div>
            `).join("");

            container.querySelectorAll(".delete-memo-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const id = btn.getAttribute("data-id");
                    const updated = loadMemos(currentDate).filter(item => item.id !== id);
                    saveMemos(currentDate, updated);
                    renderMemos(currentDate);
                    renderSidebar(document.getElementById("dateSearchInput").value);
                });
            });
        }

        // 탭 전환 함수
        function switchTab(tabName) {
            const vReport = document.getElementById("viewReport");
            const vCompare = document.getElementById("viewCompare");
            const vGithub = document.getElementById("viewGithub");
            const bReport = document.getElementById("tabReportBtn");
            const bCompare = document.getElementById("tabCompareBtn");
            const bGithub = document.getElementById("tabGithubBtn");

            vReport.classList.add("hidden");
            vCompare.classList.add("hidden");
            vGithub.classList.add("hidden");

            [bReport, bCompare, bGithub].forEach(b => {
                b.className = "px-3 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-slate-900 transition";
            });

            if (tabName === "report") {
                vReport.classList.remove("hidden");
                bReport.className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-white text-blue-600 shadow-sm transition";
            } else if (tabName === "compare") {
                vCompare.classList.remove("hidden");
                bCompare.className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-white text-blue-600 shadow-sm transition";
            } else if (tabName === "github") {
                vGithub.classList.remove("hidden");
                bGithub.className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-white text-blue-600 shadow-sm transition";
            }
        }

        // GitHub용 generate.py 코드 생성
        function buildGeneratePyString() {
            const fullHtml = "<!DOCTYPE html>\n" + document.documentElement.outerHTML;
            return [
                "from datetime import datetime",
                "",
                "# 좌측 일자별 아카이브 + 4단 통합 시황(한글파일 양식 + PB 전략) + 심화 스터디 + 하단 댓글형 메모장 생성 코드",
                "html_content = " + JSON.stringify(fullHtml),
                "",
                'with open("index.html", "w", encoding="utf-8") as f:',
                "    f.write(html_content)",
                "",
                'print("index.html 생성 완료:", datetime.now().strftime("%Y-%m-%d %H:%M"))'
            ].join("\n");
        }

        function populatePythonScript() {
            const previewLines = [
                "from datetime import datetime",
                "",
                "# [안내] 우측 상단 [📋 generate.py 전체 코드 복사] 버튼을 누르면",
                "# 현재 보고 계신 좌측 날짜별 아카이브 + 4단 통합 시황 + 심화 스터디 + 하단 댓글 메모장이",
                "# 모두 포함된 완성형 generate.py 파이썬 코드가 클립보드에 복사됩니다.",
                "",
                'with open("index.html", "w", encoding="utf-8") as f:',
                "    f.write(html_content)",
                "",
                'print("index.html 생성 완료!")'
            ].join("\n");
            document.getElementById("pythonCodeBlock").textContent = previewLines;
        }

        // 이벤트 바인딩
        window.addEventListener("DOMContentLoaded", () => {
            renderSidebar();
            renderReport(currentDate);
            renderMemos(currentDate);
            populatePythonScript();

            document.getElementById("dateSearchInput").addEventListener("input", (e) => {
                renderSidebar(e.target.value);
            });

            document.getElementById("tabReportBtn").addEventListener("click", () => switchTab("report"));
            document.getElementById("tabCompareBtn").addEventListener("click", () => switchTab("compare"));
            document.getElementById("tabGithubBtn").addEventListener("click", () => switchTab("github"));
            document.getElementById("toggleCodeBtn").addEventListener("click", () => switchTab("github"));

            // 메모 태그 선택
            document.querySelectorAll(".memo-tag-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    selectedMemoTag = btn.getAttribute("data-tag");
                    document.querySelectorAll(".memo-tag-btn").forEach(b => {
                        b.className = "memo-tag-btn text-xs px-2.5 py-1 rounded-full font-semibold bg-white text-slate-600 border border-slate-300";
                    });
                    btn.className = "memo-tag-btn text-xs px-2.5 py-1 rounded-full font-semibold bg-blue-600 text-white";
                });
            });

            // 댓글 메모 추가
            document.getElementById("addMemoBtn").addEventListener("click", () => {
                const input = document.getElementById("memoInput");
                const text = input.value.trim();
                if (!text) return;

                const now = new Date();
                const timeStr = now.getFullYear() + "-" +
                    String(now.getMonth() + 1).padStart(2, "0") + "-" +
                    String(now.getDate()).padStart(2, "0") + " " +
                    String(now.getHours()).padStart(2, "0") + ":" +
                    String(now.getMinutes()).padStart(2, "0");

                const list = loadMemos(currentDate);
                list.unshift({
                    id: "m-" + Date.now(),
                    tag: selectedMemoTag,
                    text: text,
                    time: timeStr
                });
                saveMemos(currentDate, list);
                input.value = "";
                renderMemos(currentDate);
                renderSidebar(document.getElementById("dateSearchInput").value);

                const toast = document.getElementById("memoToast");
                toast.textContent = "✓ 이 날짜에 메모가 저장되었습니다.";
                setTimeout(() => { toast.textContent = ""; }, 2500);
            });

            // 전체 메모 복사
            document.getElementById("exportMemosBtn").addEventListener("click", () => {
                const list = loadMemos(currentDate);
                const formatted = list.map(m => `[${m.time}] [${m.tag}] ${m.text}`).join("\n");
                const temp = document.createElement("textarea");
                temp.value = formatted || "작성된 메모가 없습니다.";
                document.body.appendChild(temp);
                temp.select();
                document.execCommand("copy");
                document.body.removeChild(temp);

                const toast = document.getElementById("memoToast");
                toast.textContent = "✓ 클립보드에 메모가 복사되었습니다.";
                setTimeout(() => { toast.textContent = ""; }, 2500);
            });

            // 파이썬 코드 복사
            document.getElementById("copyPythonCodeBtn").addEventListener("click", () => {
                const temp = document.createElement("textarea");
                temp.value = buildGeneratePyString();
                document.body.appendChild(temp);
                temp.select();
                document.execCommand("copy");
                document.body.removeChild(temp);

                const toast = document.getElementById("copyCodeToast");
                toast.textContent = "✓ GitHub의 generate.py에 바로 붙여넣을 수 있는 전체 파이썬 코드가 복사되었습니다!";
                setTimeout(() => { toast.textContent = ""; }, 3000);
            });
        });
    </script>
</body>
</html>
