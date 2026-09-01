import json
import os
from scrapers import OTRScraper, FilmmakersScraper
from data_store import load_auditions, save_auditions
from collector import parse_with_ai_fallback

def run_full_sync():
    """
    1. 기존 공고 로드
    2. OTR 및 Filmmakers 최신 공고 스크래핑
    3. 중복 확인 (source_url 기준)
    4. 신규 공고 정제 및 DB 추가
    """
    existing_items = load_auditions()
    existing_urls = {x.get("source_url") for x in existing_items if x.get("source_url")}
    
    print(f"[*] 기존 공고 수: {len(existing_items)}건")
    
    # 1. OTR 수집
    otr_items = OTRScraper.scrape_recent_notices()
    new_otr_count = 0
    for item in otr_items:
        if item["source_url"] not in existing_urls:
            # 상세 내용 파싱 및 정제
            parsed = parse_with_ai_fallback(item["title"], item["source_site"], item["source_url"])
            existing_urls.add(item["source_url"])
            new_otr_count += 1
            
    # 2. Filmmakers 수집
    fm_items = FilmmakersScraper.scrape_recent_notices()
    new_fm_count = 0
    for item in fm_items:
        if item["source_url"] not in existing_urls:
            parsed = parse_with_ai_fallback(item["title"], item["source_site"], item["source_url"])
            existing_urls.add(item["source_url"])
            new_fm_count += 1
            
    print(f"[+] 신규 수집 완료: OTR {new_otr_count}건, Filmmakers {new_fm_count}건")

if __name__ == "__main__":
    run_full_sync()
