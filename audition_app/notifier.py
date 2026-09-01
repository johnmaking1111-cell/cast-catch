import json
from datetime import datetime
from data_store import load_auditions

def generate_daily_briefing_text():
    items = load_auditions()
    today_str = datetime.now().strftime("%Y년 %m월 %d일")
    
    lines = [
        f"📢 [배우 오디션 모아보기] 오늘의 오디션 브리핑 ({today_str})",
        "─" * 30,
        f"총 {len(items)}건의 활성 공고가 등록되어 있습니다.\n"
    ]
    
    # 카테고리별 분류
    categories = ["영화", "드라마", "연극", "뮤지컬", "광고"]
    for cat in categories:
        cat_items = [x for x in items if x.get("category") == cat]
        if cat_items:
            lines.append(f"【{cat}】 ({len(cat_items)}건)")
            for item in cat_items[:2]: # 각 2건씩 요약
                d_day = item.get("deadline", "마감 미정")
                lines.append(f"• {item.get('title')}")
                lines.append(f"  - 역할: {item.get('roles_summary', '-')}")
                lines.append(f"  - 마감: {d_day} | 출처: {item.get('source_site')}")
            lines.append("")
            
    lines.append("─" * 30)
    lines.append("👉 웹에서 조건별 전체 공고 및 원문 링크 확인하기:")
    lines.append("https://your-audition-app.vercel.app")
    
    return "\n".join(lines)

def generate_kakaotalk_carousel_payload():
    """
    카카오톡 챗봇 스킬 서버 응답용 Carousel(카드형) JSON Payload
    """
    items = load_auditions()[:5] # 상위 5건
    cards = []
    
    for item in items:
        cards.append({
            "title": f"[{item.get('category')}] {item.get('title')[:30]}",
            "description": f"• 역할: {item.get('roles_summary')}\n• 마감: {item.get('deadline')}\n• {item.get('compensation')}",
            "buttons": [
                {
                    "action": "webLink",
                    "label": "원문 공고 보기",
                    "webLinkUrl": item.get("source_url")
                },
                {
                    "action": "webLink",
                    "label": "전체 오디션 피드",
                    "webLinkUrl": "https://your-audition-app.vercel.app"
                }
            ]
        })
        
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "itemCard",
                        "items": cards
                    }
                }
            ]
        }
    }
    return payload

if __name__ == "__main__":
    print(generate_daily_briefing_text())
