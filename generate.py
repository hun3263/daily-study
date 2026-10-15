Datetime 가져오기 DateTime에서

today_str = datetime.now().strftime("%Y년 %m월 %d일")

# 웹페이지 HTML 템플릿
html_content = f"""<! DOCTYPE html>
<html lang="ko">
<머리>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>데일리 경제 & 증시 스터디</title>
 < 스타일>
 본체 {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 산세리프; 최대 너비: 800px; 여백: 40px auto; 패딩: 0 20px; 줄 높이: 1.6; 색상: #333; }}
 h1 {{ border-bottom: 2px 단색 #228be6; 패딩 하단: 10px; color: #1c7ed6; }}
 .date {{ color: #868e96; 글꼴 크기: 14px; 여백 하단: 20px; }}
 표 {{ 너비: 100%; 경계 붕괴: 붕괴; 여백: 20px 0; }}
 th, td {{ border: 1px 단#dee2e6; 패딩: 12px; text-align: left; font-size: 14px; }}
 th {{ 배경색: #f8f9fa; 글꼴 굵기: 굵기; }}
 tr:nth-child(even) {{ background-color: #fbfbfb; }}
 .highlight {{ color: #d6336c; font-weight: bold; }}
 .study-box {{ 배경색: #e7f5ff; 테두리 왼쪽: 4px 단색 #339af0; padding: 15px; 여백: 20px 0; border-radius: 4px; }}
 </스타일>
</헤드>
<몸>
 <h1> 📈 데일리 경제 & 증시 브리핑</h1>
 <div class="date">近期更新: {today_str}</div>

<div class="study-box">
 <h3> 💡 오늘의 경제/증시 핵심 공부</h3>
 <p><strong>주제: 기준금리와 시장금리의 차이</strong></p>
 <p>한국은행 금융통화위원회가 결정하는 기준금리는 초단기(7일물 RP) 정책금리이며, 국고채 3년·10년물 같은 시장금리는 시장의 경기 전망과 수급에 따라 기준금리보다 먼저 움직입니다.</p>
 </div>

<h3> 📅 주요 경제부처 주간 일정</h3>
 <테이블>
 < 머리>
 <트>
 <번째 스타일="너비: 15%" >일자</th>
 <번째 스타일="너비: 20%" >기관</th>
 <번째 스타일="너비: 45%" >주요 내용</th>
 <번째 스타일="너비: 20%" >시장 포인트</th>
 </tr>
 </머리>
 < 아무도 없어>
 <트>
 <td><strong>월요일</strong></td>
 <td>재정경제부 / 한은</td>
 <td>대외경제장관회의, KDI 경제동향, 한은 총재 국감</td>
 <td>공급망 정책 및 금리 기조 확인</td>
 </tr>
 <트>
 <td><strong>화요일</strong></td>
 <td>재경부 / 금융위</td>
 <td>IMF 세계경제전망(WEO), 부동산 PF 점검회의</td>
 <td>글로벌 성장률 및 PF 리스크 점검</td>
 </tr>
 <트>
 <td><strong>수요일</strong></td>
 <td>재경부 / 금감원</td>
 <td>AI· K-뷰티 육성안, 증권사 위탁수수료 체계 개선</td>
 <td>관련 테마주 및 증권사 수익 영향</td>
 </tr>
 <트>
 <td><strong>목요일</strong></td>
 <td>금융위 / 한은</td>
 <td>9월 가계대출 점검, 8월 통화·유동성 지표</td>
 <td>시중 유동성 및 대출 규제 강도</td>
 </tr>
 <트>
 <td><strong>금요일</strong></td>
 <td>재경부 / 한은</td>
 <td>9월 고용동향, 10월 그린북, 수출입물가지수</td>
 <td>국내 실물 경기 흐름 점검</td>
 </tr>
 </몸>
 </테이블>
</몸>
</html>
"""

# index.html 파일로 저장
Open("index.html", "W", encoding="UTF-8")가 F로 설정된 경우:
 f.write(html_content)

print("index.html 생성 완료!")
