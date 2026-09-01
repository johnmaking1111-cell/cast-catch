"""
🎭 [진짜 배우 오디션 전용 정밀 크롤러]
잡다한 일반 공모전/취업 사이트를 제거하고 100% 순수 배우 캐스팅 전문 출처만 수집합니다.
"""
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

# 🚫 배우 캐스팅과 무관한 키워드 전면 차단
EXCLUDE_KEYWORDS = [
    '서포터즈', '기자단', '취업', '국비지원', '양성과정', '인턴', '애칭', '네이밍',
    '아이디어', '해외취업', '체험단', '모니터링', '스태프만', '촬영감독만', '조명감독만',
    '회원가입', '로그인', '공지사항', '이용약관', '개인정보'
]

# ✅ 배우/오디션 필수 포함 키워드
INCLUDE_KEYWORDS = [
    '오디션', '배우', '캐스팅', '모집', '주연', '조연', '단역', '앙상블', '단원', 
    '출연', '모델', '연기', '뮤지컬', '연극', '영화', '드라마', '웹드라마', '극단'
]

def is_valid_audition(title):
    if not title or len(title) < 5: return False
    if any(ex in title for ex in EXCLUDE_KEYWORDS): return False
    if not any(inc in title for inc in INCLUDE_KEYWORDS): return False
    return True

def extract_meta_from_title(title):
    gender = "남/여"
    if any(k in title for k in ["여성", "여자", "여배우"]): gender = "여성"
    elif any(k in title for k in ["남성", "남자", "남배우"]): gender = "남성"

    age_group = "전연령 (공고 참조)"
    if "20대" in title and "30대" in title: age_group = "20대, 30대"
    elif "20대" in title: age_group = "20대"
    elif "30대" in title: age_group = "30대"
    elif "40대" in title: age_group = "40대"
    elif any(k in title for k in ["10대", "아역", "청소년", "고등학생"]): age_group = "10대 (아역/청소년)"
    elif any(k in title for k in ["50대", "시니어"]): age_group = "50대 이상"

    roles_summary = "공고 본문 및 모집요강 참조"
    if "주연" in title: roles_summary = f"{gender} 주연 배우"
    elif "조연" in title or "단역" in title: roles_summary = f"{gender} 조/단역 배우"
    elif "앙상블" in title: roles_summary = "뮤지컬/공연 앙상블"
    elif "단원" in title: roles_summary = "극단 신규 단원"
    elif "모델" in title: roles_summary = f"{gender} 광고/CF 모델"

    date_match = re.search(r'(\d{1,2})[/월.](\d{1,2})', title)
    deadline = "채용 시 마감"
    if date_match:
        m, d = int(date_match.group(1)), int(date_match.group(2))
        if 1 <= m <= 12 and 1 <= d <= 31:
            deadline = f"2026-{m:02d}-{d:02d}"

    return {
        "gender": gender,
        "age_group": age_group,
        "roles_summary": roles_summary,
        "deadline": deadline,
        "compensation": "출연료/페이 협의 (표준)",
        "contact_email": ""
    }

class OTRScraper:
    URLS = ["https://otr.co.kr/audition/", "https://otr.co.kr/otr-audition/", "https://otr.co.kr/mozip/"]
    @staticmethod
    def scrape(pages=3):
        results = []
        session = requests.Session()
        session.headers.update(HEADERS)
        for base_url in OTRScraper.URLS:
            for page in range(1, pages + 1):
                try:
                    url = f"{base_url}?mode=list&board_page={page}" if "audition" in base_url else base_url
                    res = session.get(url, timeout=8)
                    if res.status_code != 200: continue
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for a in soup.find_all('a', href=True):
                        href = a['href']
                        title = re.sub(r'\s+', ' ', a.get_text()).strip()
                        if not is_valid_audition(title): continue
                        if any(k in href for k in ['vid=', 'uid=', 'document', 'audition']):
                            full_url = href if href.startswith('http') else f"https://otr.co.kr{href}"
                            category = "뮤지컬" if "뮤지컬" in title or "음악극" in title else ("영화" if "영화" in title else "연극")
                            results.append({
                                "category": category, "title": title, "production": "극단 / 제작사",
                                "source_site": "OTR", "source_url": full_url, "created_at": datetime.now().isoformat(),
                                **extract_meta_from_title(title)
                            })
                except Exception: continue
        return results

class FilmmakersScraper:
    URLS = ["https://www.filmmakers.co.kr/actorsAudition", "https://www.filmmakers.co.kr/modelRecruit"]
    @staticmethod
    def scrape(pages=3):
        results = []
        session = requests.Session()
        session.headers.update(HEADERS)
        for base_url in FilmmakersScraper.URLS:
            for page in range(1, pages + 1):
                try:
                    url = f"{base_url}?page={page}" if page > 1 else base_url
                    res = session.get(url, timeout=8)
                    if res.status_code != 200: continue
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for a in soup.find_all('a', href=True):
                        href = a['href']
                        title = re.sub(r'\s+', ' ', a.get_text()).strip()
                        if not is_valid_audition(title): continue
                        if any(k in href for k in ['actorsAudition/', 'modelRecruit/', 'document_srl=']):
                            full_url = href if href.startswith('http') else f"https://www.filmmakers.co.kr{href}"
                            category = "영화"
                            if any(k in title for k in ["드라마", "웹드라마", "OTT", "시리즈"]): category = "드라마"
                            elif any(k in title for k in ["광고", "CF", "바이럴", "모델"]): category = "광고"
                            elif "연극" in title: category = "연극"
                            elif "뮤지컬" in title: category = "뮤지컬"
                            results.append({
                                "category": category, "title": title, "production": "영화/영상 제작사",
                                "source_site": "Filmmakers", "source_url": full_url, "created_at": datetime.now().isoformat(),
                                **extract_meta_from_title(title)
                            })
                except Exception: continue
        return results

class StarletScraper:
    @staticmethod
    def scrape():
        results = []
        session = requests.Session()
        session.headers.update(HEADERS)
        try:
            res = session.get("https://www.starlet-studio.co.kr/audition", timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href, title = a['href'], re.sub(r'\s+', ' ', a.get_text()).strip()
                    if "/audition/detail/" in href and is_valid_audition(title):
                        full_url = href if href.startswith('http') else f"https://www.starlet-studio.co.kr{href}"
                        category = "드라마" if "드라마" in title or "OTT" in title else ("광고" if "광고" in title or "숏폼" in title else "영화")
                        results.append({
                            "category": category, "title": title, "production": "영화/드라마 제작사",
                            "source_site": "스탈렛 스튜디오", "source_url": full_url, "created_at": datetime.now().isoformat(),
                            **extract_meta_from_title(title)
                        })
        except Exception: pass
        return results

class PlayDBScraper:
    @staticmethod
    def scrape():
        results = []
        session = requests.Session()
        session.headers.update(HEADERS)
        try:
            res = session.get("http://www.playdb.co.kr/community/Publicity_list.asp?bbsno=29", timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href, title = a['href'], re.sub(r'\s+', ' ', a.get_text()).strip()
                    if "Publicity_Detail.asp" in href and is_valid_audition(title):
                        full_url = href if href.startswith('http') else f"http://www.playdb.co.kr/community/{href}"
                        category = "뮤지컬" if "뮤지컬" in title else "연극"
                        results.append({
                            "category": category, "title": title, "production": "공연 기획/제작사",
                            "source_site": "플레이DB", "source_url": full_url, "created_at": datetime.now().isoformat(),
                            **extract_meta_from_title(title)
                        })
        except Exception: pass
        return results

class MegaphoneScraper:
    URLS = ["http://www.megaphonekorea.com/audition/variety", "http://www.megaphonekorea.com/audition/index"]
    @staticmethod
    def scrape():
        results = []
        session = requests.Session()
        session.headers.update(HEADERS)
        for url in MegaphoneScraper.URLS:
            try:
                res = session.get(url, timeout=8)
                if res.status_code != 200: continue
                soup = BeautifulSoup(res.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href, title = a['href'], re.sub(r'\s+', ' ', a.get_text()).strip()
                    if "/audition/detail/" in href and is_valid_audition(title):
                        full_url = href if href.startswith('http') else f"http://www.megaphonekorea.com{href}"
                        category = "드라마" if "드라마" in title else ("뮤지컬" if "뮤지컬" in title else ("광고" if "광고" in title else "영화"))
                        results.append({
                            "category": category, "title": title, "production": "캐스팅 디렉터 / 제작사",
                            "source_site": "메가폰코리아", "source_url": full_url, "created_at": datetime.now().isoformat(),
                            **extract_meta_from_title(title)
                        })
            except Exception: continue
        return results
