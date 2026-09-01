import json
import os
from scrapers import (
    OTRScraper, 
    FilmmakersScraper, 
    StarletScraper, 
    PlayDBScraper, 
    MegaphoneScraper, 
    ContestKoreaScraper
)
from data_store import load_auditions, add_audition

def run_full_sync():
    existing_items = load_auditions()
    existing_urls = {x.get("source_url") for x in existing_items if x.get("source_url")}
    existing_titles = {x.get("title") for x in existing_items if x.get("title")}
    
    print(f"[*] 기존 등록 공고: {len(existing_items)}건")
    
    scrapers = [
        ("OTR (연극/뮤지컬)", OTRScraper.scrape(pages=3)),
        ("Filmmakers (영화/드라마/광고)", FilmmakersScraper.scrape(pages=3)),
        ("스탈렛 스튜디오 (상업/독립영화)", StarletScraper.scrape()),
        ("플레이DB (대극장 뮤지컬/연극)", PlayDBScraper.scrape()),
        ("메가폰코리아 (공식 캐스팅)", MegaphoneScraper.scrape()),
        ("콘테스트코리아 (선발대회/공모전)", ContestKoreaScraper.scrape())
    ]
    
    total_added = 0
    for name, items in scrapers:
        added_count = 0
        for item in items:
            if item["source_url"] not in existing_urls and item["title"] not in existing_titles:
                add_audition(item)
                existing_urls.add(item["source_url"])
                existing_titles.add(item["title"])
                added_count += 1
                total_added += 1
        print(f"[+] {name}: {added_count}건 신규 수집 완료")
        
    print(f"[*] 총 신규 추가: {total_added}건 | 누적 전체 공고: {len(load_auditions())}건")

if __name__ == "__main__":
    run_full_sync()
