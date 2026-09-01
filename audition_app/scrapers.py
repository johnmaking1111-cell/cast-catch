"""
🛡️ [비로그인 100% 완전 공개 사이트 전용 크롤러 (6대 출처)]
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

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip() if text else ""

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
                        title = clean_text(a.get_text())
                        if len(title) < 5 or any(ex in title for ex in ['로그인', '회원가입', '공지사항', '이용약관', '개인정보']): continue
                        if any(k in href for k in ['vid=', 'uid=', 'document', 'audition']):
                            full_url = href if href.startswith('http') else f"https://otr.co.kr{href}"
                            category = "뮤지컬" if "뮤지컬" in title or "음악극" in title else ("영화" if "영화" in title else "연극")
                            results.append({"category": category, "title": title, "source_site": "OTR", "source_url": full_url, "created_at": datetime.now().isoformat()})
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
                        title = clean_text(a.get_text())
                        if len(title) < 6 or any(ex in title for ex in ['로그인', '회원가입', '공지', '필독']): continue
                        if any(k in href for k in ['actorsAudition/', 'modelRecruit/', 'document_srl=']):
                            full_url = href if href.startswith('http') else f"https://www.filmmakers.co.kr{href}"
                            category = "영화"
                            if any(k in title for k in ["드라마", "웹드라마", "OTT", "시리즈"]): category = "드라마"
                            elif any(k in title for k in ["광고", "CF", "바이럴", "모델"]): category = "광고"
                            elif "연극" in title: category = "연극"
                            elif "뮤지컬" in title: category = "뮤지컬"
                            results.append({"category": category, "title": title, "source_site": "Filmmakers", "source_url": full_url, "created_at": datetime.now().isoformat()})
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
                    href, title = a['href'], clean_text(a.get_text())
                    if "/audition/detail/" in href and len(title) > 5:
                        full_url = href if href.startswith('http') else f"https://www.starlet-studio.co.kr{href}"
                        category = "드라마" if "드라마" in title or "OTT" in title else ("광고" if "광고" in title or "숏폼" in title else "영화")
                        results.append({"category": category, "title": title, "source_site": "스탈렛 스튜디오", "source_url": full_url, "created_at": datetime.now().isoformat()})
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
                    href, title = a['href'], clean_text(a.get_text())
                    if "Publicity_Detail.asp" in href and len(title) > 5:
                        full_url = href if href.startswith('http') else f"http://www.playdb.co.kr/community/{href}"
                        category = "뮤지컬" if "뮤지컬" in title else "연극"
                        results.append({"category": category, "title": title, "source_site": "플레이DB", "source_url": full_url, "created_at": datetime.now().isoformat()})
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
                    href, title = a['href'], clean_text(a.get_text())
                    if "/audition/detail/" in href and len(title) > 4:
                        full_url = href if href.startswith('http') else f"http://www.megaphonekorea.com{href}"
                        category = "드라마" if "드라마" in title else ("뮤지컬" if "뮤지컬" in title else ("광고" if "광고" in title else "영화"))
                        results.append({"category": category, "title": title, "source_site": "메가폰코리아", "source_url": full_url, "created_at": datetime.now().isoformat()})
            except Exception: continue
        return results

class ContestKoreaScraper:
    @staticmethod
    def scrape():
        results = []
        session = requests.Session()
        session.headers.update(HEADERS)
        try:
            res = session.get("https://www.contestkorea.com/sub/list.php?int_gbn=1&Txt_bcode=030410001", timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href, title = a['href'], clean_text(a.get_text())
                    if "view.php" in href and len(title) > 5 and not any(ex in title for ex in ['로그인', '회원가입']):
                        full_url = href if href.startswith('http') else f"https://www.contestkorea.com/sub/{href}"
                        results.append({"category": "광고", "title": title, "source_site": "콘테스트코리아", "source_url": full_url, "created_at": datetime.now().isoformat()})
        except Exception: pass
        return results
