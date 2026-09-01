import json
import os
from scrapers import (
    OTRScraper, 
    FilmmakersScraper, 
    StarletScraper, 
    PlayDBScraper, 
    MegaphoneScraper,
    is_valid_audition
)
from data_store import load_auditions, save_auditions, add_audition

def run_full_sync():
    # 1. 기존 데이터에서 비(非)오디션 및 콘테스트코리아 글 전면 삭제
    existing_items = load_auditions()
    cleaned_items = [
        x for x in existing_items 
        if x.get("source_site") != "콘테스트코리아" and is_valid_audition(x.get("title", ""))
    ]
    
    # undefined 필드 자동 정상화
    for item in cleaned_items:
        if not item.get("gender") or item.get("gender") == "undefined": item["gender"] = "남/여"
        if not item.get("age_group") or item.get("age_group") == "undefined": item["age_group"] = "전연령 (공고 참조)"
        if not item.get("compensation") or item.get("compensation") == "undefined": item["compensation"] = "출연료/페이 협의"
        if not item.get("roles_summary") or item.get("roles_summary") == "undefined": item["roles_summary"] = "공고 본문 참조"
            
    save_auditions(cleaned_items)
    existing_urls = {x.get("source_url") for x in cleaned_items if x.get("source_url")}
    existing_titles = {x.get("title") for x in cleaned_items if x.get("title")}
    
    print(f"[*] 기존 유효 공고 수: {len(cleaned_items)}건")
    
    # 2. 순수 오디션 전문 5대 출처만 대량 수집
    scrapers = [
        ("OTR (연극/뮤지컬)", OTRScraper.scrape(pages=3)),
        ("Filmmakers (영화/드라마/광고)", FilmmakersScraper.scrape(pages=3)),
        ("스탈렛 스튜디오 (상업/독립영화)", StarletScraper.scrape()),
        ("플레이DB (대극장 뮤지컬/연극)", PlayDBScraper.scrape()),
        ("메가폰코리아 (공식 캐스팅)", MegaphoneScraper.scrape())
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
        
    print(f"[*] 최종 전체 순수 오디션 공고: {len(load_auditions())}건")

if __name__ == "__main__":
    run_full_sync()
