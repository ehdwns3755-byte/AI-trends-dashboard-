#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
경제뉴스 시스템 테스트
"""

import sys
import json
from pathlib import Path

print("[테스트 시작]")
print(f"작업 디렉토리: {Path.cwd()}")
print()

try:
    print("[1단계] economics_news 모듈 임포트...")
    from agent_harness.tools.economics_news import (
        fetch_economics_news,
        categorize_economics_news,
        generate_economics_summary,
    )
    print("[OK] 모듈 임포트 성공")
    print()

    print("[2단계] 뉴스 수집 중...")
    news_result = fetch_economics_news(days=1)
    news_data = json.loads(news_result)
    print(f"[OK] 수집 완료")
    print(f"   상태: {news_data.get('status')}")
    print(f"   날짜: {news_data.get('date')}")
    print(f"   시간: {news_data.get('time')}")
    print(f"   새로운 뉴스: {news_data.get('new_count')}개")
    print(f"   보관된 뉴스: {news_data.get('total_archived')}개")
    print()

    # 뉴스 미리보기
    articles = news_data.get('articles', [])
    if articles:
        print("[뉴스 샘플]")
        for i, article in enumerate(articles[:2], 1):
            print(f"   {i}. {article.get('title', 'No title')[:60]}...")
            print(f"      출처: {article.get('source')}")
            print()

    print("[3단계] 뉴스 분류 중...")
    categorized_result = categorize_economics_news(news_result)
    categorized_data = json.loads(categorized_result)
    print(f"[OK] 분류 완료")
    print(f"   카테고리: {len(categorized_data.get('categorized', {}))}")
    print()

    print("[4단계] 요약 생성 중...")
    summary_result = generate_economics_summary(categorized_result)
    summary_data = json.loads(summary_result)
    print(f"[OK] 요약 완료")
    print(f"   날짜: {summary_data.get('date')}")
    print()

    # news_archive.json 확인
    print("[5단계] 아카이브 확인...")
    archive_file = Path("news_archive.json")
    if archive_file.exists():
        with open(archive_file, "r", encoding="utf-8") as f:
            archive = json.load(f)
        print(f"[OK] 아카이브 파일 존재")
        print(f"   파일 위치: {archive_file.absolute()}")
        print(f"   저장된 뉴스: {archive.get('total_articles')}개")
        print(f"   마지막 업데이트: {archive.get('last_updated')}")
    else:
        print(f"[경고] 아카이브 파일이 없습니다")
    print()

    print("[성공] 모든 테스트 통과!")
    print()
    print("[다음 단계]")
    print("1. html 대시보드 확인: economics_news_daily.html")
    print("2. 웹 서버 실행: python -m http.server 8000")
    print("3. 브라우저 접속: http://localhost:8000/economics_news_daily.html")

except Exception as e:
    print(f"[에러] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
