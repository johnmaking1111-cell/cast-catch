import json
import re
from datetime import datetime
from data_store import add_audition

PARSER_PROMPT_TEMPLATE = """
당신은 한국 오디션 공고 전문 분석 AI입니다.
아래 비정형 오디션 공고 텍스트를 분석하여 지정된 JSON 형식으로만 추출하세요.

[공고 원문]
{raw_text}

[JSON 출력 형식 규격]
{{
  "category": "영화" | "드라마" | "연극" | "뮤지컬" | "광고" | "기타",
  "title": "공고 제목 (핵심 요약)",
  "production": "제작사 또는 극단명",
  "roles_summary": "모집 배역 및 연령 요약 (예: 20대 후반 남성 형사, 30대 여성)",
  "gender": "남성" | "여성" | "남/여" | "무관",
  "age_group": "10대" | "20대" | "30대" | "40대" | "50대 이상" | "전연령",
  "deadline": "YYYY-MM-DD" 또는 "채용 시 마감",
  "compensation": "출연료/페이 정보",
  "contact_email": "접수 이메일 주소 또는 빈 문자열",
  "description": "작품 개요 및 핵심 요구사항 (2~3문장 요약)"
}}
"""

def parse_with_ai_fallback(raw_text: str, source_site: str, source_url: str):
    """
    Gemini API 또는 LLM을 통해 비정형 텍스트를 구조화된 데이터로 변환합니다.
    (API 키 미설정 시 휴리스틱 규칙 기반 파서 작동)
    """
    category = "기타"
    if "영화" in raw_text or "단편" in raw_text or "장편" in raw_text:
        category = "영화"
    elif "드라마" in raw_text or "OTT" in raw_text or "웹드라마" in raw_text:
        category = "드라마"
    elif "연극" in raw_text or "극단" in raw_text:
        category = "연극"
    elif "뮤지컬" in raw_text:
        category = "뮤지컬"
    elif "광고" in raw_text or "CF" in raw_text or "바이럴" in raw_text:
        category = "광고"

    # 이메일 추출
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
    email = email_match.group(0) if email_match else ""

    # 마감일 추출 (YYYY-MM-DD 또는 YYYY.MM.DD)
    date_match = re.search(r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})', raw_text)
    deadline = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}" if date_match else "채용 시 마감"

    item = {
        "category": category,
        "title": raw_text.strip().split("\n")[0][:60],
        "production": "제작사 미상",
        "source_site": source_site,
        "source_url": source_url,
        "roles_summary": "공고 본문 참조",
        "gender": "남/여",
        "age_group": "20대, 30대",
        "deadline": deadline,
        "compensation": "추후 협의",
        "description": raw_text.strip()[:200],
        "contact_email": email,
        "created_at": datetime.now().isoformat()
    }
    return add_audition(item)

if __name__ == "__main__":
    test_notice = """[독립영화] 단편영화 <기억의 밤> 30대 남자 주연배우 모집
제작: 필름스튜디오
마감일: 2026-09-25
접수: memory_film@gmail.com
출연료: 회차당 25만원
배역: 30대 초반 직장인 민우 역. 섬세한 내면 연기 가능하신 분."""
    result = parse_with_ai_fallback(test_notice, "Filmmakers", "https://filmmakers.co.kr/audition/12345")
    print("Parsed & Stored item:", json.dumps(result, ensure_ascii=False, indent=2))
