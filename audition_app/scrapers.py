"""
실시간 오디션 데이터 수집기 (Scrapers)
- OTR (연극/뮤지컬/공연)
- Filmmakers (영화/드라마/광고)
- KOPIS Open API (공연예술통합전산망)
"""
import re
import json
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

class OTRScraper:
    BASE_URL = "https://otr.co.kr/audition/"
    
    @staticmethod
    def scrape_recent_notices():
        """
        OTR 오디션 게시판에서 최신 공고 목록을 수집합니다.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        try:
            req = urllib.request.Request(OTRScraper.BASE_URL, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
        except Exception as e:
            # 네트워크 제한 환경 또는 오류 시 빈 리스트 반환
            return []

        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # OTR 게시판 테이블 및 리스트 파싱
        rows = soup.select('table.kboard-list tbody tr, div.kboard-list-item')
        for row in rows:
            title_elem = row.select_one('.kboard-list-title, .title a')
            if not title_elem:
                continue
            
            raw_title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = "https://otr.co.kr" + link
                
            date_elem = row.select_one('.kboard-list-date, .date')
            created_date = date_elem.get_text(strip=True) if date_elem else ""
            
            category = "연극"
            if "뮤지컬" in raw_title:
                category = "뮤지컬"
                
            results.append({
                "category": category,
                "title": raw_title,
                "source_site": "OTR",
                "source_url": link,
                "created_at": created_date
            })
        return results

class FilmmakersScraper:
    BASE_URL = "https://www.filmmakers.co.kr/actorsAudition"
    
    @staticmethod
    def scrape_recent_notices():
        """
        필름메이커스 배우 오디션 게시판 수집
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            req = urllib.request.Request(FilmmakersScraper.BASE_URL, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
        except Exception:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        results = []
        rows = soup.select('table.board-table tbody tr')
        for row in rows:
            title_elem = row.select_one('td.title a')
            if not title_elem:
                continue
            raw_title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = "https://www.filmmakers.co.kr" + link
                
            category = "영화"
            if "드라마" in raw_title or "웹드라마" in raw_title or "OTT" in raw_title:
                category = "드라마"
            elif "광고" in raw_title or "CF" in raw_title or "바이럴" in raw_title:
                category = "광고"
                
            results.append({
                "category": category,
                "title": raw_title,
                "source_site": "Filmmakers",
                "source_url": link
            })
        return results

if __name__ == "__main__":
    print("Scraper module defined successfully.")
