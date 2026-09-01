import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "auditions.json")

SAMPLE_DATA = [
    {
        "id": 1,
        "category": "영화",
        "title": "[상업영화] 휴먼 드라마 장편영화 20대 후반~30대 초반 남/여 조연 배우 모집",
        "production": "케이엔터테인먼트",
        "source_site": "Filmmakers",
        "source_url": "https://www.filmmakers.co.kr",
        "roles_summary": "남성 형사(30대 초), 여성 변호사(20대 후)",
        "gender": "남/여",
        "age_group": "20대, 30대",
        "deadline": "2026-09-12",
        "compensation": "회차당 50만원 (협의)",
        "description": "하반기 크랭크인 예정인 상업영화입니다. 일상적이고 자연스러운 생활 연기 가능자 우대합니다.",
        "contact_email": "audition@knent-film.com",
        "created_at": "2026-08-31T09:00:00"
    },
    {
        "id": 2,
        "category": "드라마",
        "title": "[OTT 시리즈] 8부작 스릴러 드라마 주요 단역 및 이미지 단역 캐스팅",
        "production": "스튜디오 블루",
        "source_site": "플필",
        "source_url": "https://plfil.com",
        "roles_summary": "카페 알바생(20대 여), 회사원(30대 남), 베테랑 형사(40~50대 남)",
        "gender": "남/여",
        "age_group": "20대, 30대, 40대, 50대 이상",
        "deadline": "2026-09-08",
        "compensation": "출연료 지급 (추후 협의)",
        "description": "글로벌 OTT 플랫폼 편성 확정작으로, 개성 있는 마스크와 탄탄한 연기력을 갖춘 신인/경력 배우님들의 많은 지원 바랍니다.",
        "contact_email": "casting@studioblue.tv",
        "created_at": "2026-08-31T11:30:00"
    },
    {
        "id": 3,
        "category": "연극",
        "title": "[연극] 2026 하반기 정기공연 블랙코미디 연극 전 배역 오디션",
        "production": "극단 청년무대",
        "source_site": "OTR",
        "source_url": "https://otr.co.kr/audition/",
        "roles_summary": "주인공 진우(20대 중후반 남), 수연(20대 여), 멀티(20~30대)",
        "gender": "남/여",
        "age_group": "20대, 30대",
        "deadline": "2026-09-05",
        "compensation": "티켓 수익 쉐어 및 회당 출연료 지급",
        "description": "대학로 소극장에서 3개월간 장기 상연 예정인 블랙코미디 창작극입니다. 열정과 에너지가 넘치는 배우님을 모십니다.",
        "contact_email": "theatre_stage@naver.com",
        "created_at": "2026-08-31T14:15:00"
    },
    {
        "id": 4,
        "category": "뮤지컬",
        "title": "[창작뮤지컬] 2026 대극장 창작 뮤지컬 앙상블 및 주/조연 커버 모집",
        "production": "(주)뮤지컬아트컴퍼니",
        "source_site": "OTR",
        "source_url": "https://otr.co.kr/audition/",
        "roles_summary": "남/여 앙상블(댄스/아크로바틱 특기자 우대), 조연 커버",
        "gender": "남/여",
        "age_group": "20대, 30대",
        "deadline": "2026-09-20",
        "compensation": "공연 회당 페이 및 연습실 식대 지급",
        "description": "음악적 감각과 안정적인 보컬, 안무 소화 능력을 겸비한 뮤지컬 배우님을 선발합니다.",
        "contact_email": "musical_art@casting.kr",
        "created_at": "2026-08-31T15:00:00"
    },
    {
        "id": 5,
        "category": "광고",
        "title": "[TV/디지털 CF] 프리미엄 뷰티 스킨케어 브랜드 바이럴 광고 메인 모델",
        "production": "플랜에이 프로덕션",
        "source_site": "Filmmakers",
        "source_url": "https://www.filmmakers.co.kr",
        "roles_summary": "맑고 깨끗한 이미지의 여성 모델(20대~30대 초), 남성 모델(20대)",
        "gender": "남/여",
        "age_group": "20대, 30대",
        "deadline": "2026-09-04",
        "compensation": "300만원 ~ 500만원 (매체 협의)",
        "description": "피부결이 정돈되고 표정 연기가 자연스러운 모델을 찾습니다. 무보정 프로필 및 영상 링크 필수 첨부.",
        "contact_email": "ad_model@plana-prod.com",
        "created_at": "2026-08-31T16:20:00"
    },
    {
        "id": 6,
        "category": "영화",
        "title": "[단편영화] 한국예술종합학교 전문사 졸업작품 주연 배우 모집",
        "production": "한예종 영상원",
        "source_site": "Filmmakers",
        "source_url": "https://www.filmmakers.co.kr",
        "roles_summary": "20대 초반 대학생 민호(남성), 은서(여성)",
        "gender": "남/여",
        "age_group": "20대",
        "deadline": "2026-09-15",
        "compensation": "일비 및 식대, 교통비 제공 (회차당 15만원)",
        "description": "국내외 영화제 출품을 목표로 하는 독립 단편영화입니다. 섬세한 감정 표현이 가능한 배우를 찾습니다.",
        "contact_email": "knua_film2026@gmail.com",
        "created_at": "2026-08-30T10:00:00"
    },
    {
        "id": 7,
        "category": "드라마",
        "title": "[웹드라마] 청춘 캠퍼스 로맨스 코미디 주연 4인 공개 캐스팅",
        "production": "넥스트미디어",
        "source_site": "메가폰코리아",
        "source_url": "http://megaphonekorea.com/",
        "roles_summary": "남주(20대 초반), 여주(20대 초반), 서브남주(20대 중반), 여사친(20대 초반)",
        "gender": "남/여",
        "age_group": "20대",
        "deadline": "2026-09-18",
        "compensation": "회당 40만원",
        "description": "유튜브 및 숏폼 플랫폼 송출 예정인 10부작 웹시리즈입니다. 밝고 통통 튀는 매력의 신인 배우 지원 환영합니다.",
        "contact_email": "webdrama@nextmedia.co.kr",
        "created_at": "2026-08-30T14:30:00"
    },
    {
        "id": 8,
        "category": "연극",
        "title": "[소극장 연극] 혜화동 대학로 스테디셀러 로맨틱 코미디 5기 배우 모집",
        "production": "극단 봄날",
        "source_site": "OTR",
        "source_url": "https://otr.co.kr/audition/",
        "roles_summary": "남주 강우(20대 후~30대 초), 여주 지민(20대 중후반)",
        "gender": "남/여",
        "age_group": "20대, 30대",
        "deadline": "2026-09-10",
        "compensation": "월 고정급 + 인센티브",
        "description": "관객과의 소통 능력과 순발력 있는 코믹 연기가 뛰어난 배우님을 기다립니다.",
        "contact_email": "spring_theatre@daum.net",
        "created_at": "2026-08-29T18:00:00"
    }
]

def load_auditions():
    if not os.path.exists(DATA_FILE):
        save_auditions(SAMPLE_DATA)
        return SAMPLE_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return SAMPLE_DATA

def save_auditions(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_audition(item):
    data = load_auditions()
    max_id = max([x.get("id", 0) for x in data], default=0)
    item["id"] = max_id + 1
    if "created_at" not in item:
        item["created_at"] = datetime.now().isoformat()
    data.insert(0, item)
    save_auditions(data)
    return item

if __name__ == "__main__":
    items = load_auditions()
    print(f"Loaded {len(items)} audition notices successfully.")
