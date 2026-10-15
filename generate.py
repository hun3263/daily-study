from datetime import datetime

today_str = datetime.now().strftime("%Y년 %m월 %d일")

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>데일리 경제 & 증시 스터디</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #333; }}
        h1 {{ border-bottom: 2px solid #228be6; padding-bottom: 10px; color: #1c7ed6; }}
        .date {{ color: #868e96; font-size: 14px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; font-size: 14px; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #fbfbfb; }}
        .study-box {{ background-color: #e7f5ff; border-left: 4px solid #339af0; padding: 15px; margin: 20px 0; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>📈 데일리 경제 & 증시 브리핑</h1>
    <div class="date">최근 업데이트: {today_str}</div>

    <div class="study-box">
        <h3>💡 오늘의 경제/증시 핵심 공부</h3>
        <p><strong>주제: 기준금리와 시장금리의 차이</strong></p>
        <p>한국은행 금융통화위원회가 결정하는 기준금리는 초단기 정책금리이며, 국고채 같은 시장금리는 시장의 경기 전망과 수급에 따라 먼저 움직입니다.</p>
    </div>

    <h3>📅 주요 경제부처 주간 일정</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">일자</th>
                <th style="width: 20%;">기관</th>
                <th style="width: 45%;">주요 내용</th>
                <th style="width: 20%;">시장 포인트</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>월요일</strong></td>
                <td>재정경제부 / 한은</td>
                <td>대외경제장관회의, KDI 경제동향, 한은 총재 국감</td>
                <td>공급망 정책 및 금리 기조 확인</td>
            </tr>
            <tr>
                <td><strong>화요일</strong></td>
                <td>재경부 / 금융위</td>
                <td>IMF 세계경제전망(WEO), 부동산 PF 점검회의</td>
                <td>글로벌 성장률 및 PF 리스크 점검</td>
            </tr>
            <tr>
                <td><strong>수요일</strong></td>
                <td>재경부 / 금감원</td>
                <td>AI·K-뷰티 육성안, 증권사 위탁수수료 체계 개선</td>
                <td>관련 테마주 및 증권사 수익 영향</td>
            </tr>
            <tr>
                <td><strong>목요일</strong></td>
                <td>금융위 / 한은</td>
                <td>9월 가계대출 점검, 8월 통화·유동성 지표</td>
                <td>시중 유동성 및 대출 규제 강도</td>
            </tr>
            <tr>
                <td><strong>금요일</strong></td>
                <td>재경부 / 한은</td>
                <td>9월 고용동향, 10월 그린북, 수출입물가지수</td>
                <td>국내 실물 경기 흐름 점검</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html 생성 완료!")
