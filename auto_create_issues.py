#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatically create GitHub issues using Playwright
웹브라우저 인증으로 GitHub Issues를 자동으로 생성합니다
"""

import asyncio
from playwright.async_api import async_playwright
import json
import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

ISSUES = [
    {
        "title": "XSS 취약점: HTML 콘텐츠에 대한 이스케이프 처리 부재",
        "body": """## 문제
`generate_html()` 메서드에서 `item['title']`과 `item['summary']` 등을 직접 HTML에 삽입하고 있습니다. 악의적인 HTML/JS 코드가 포함된 뉴스 제목이 있으면 XSS 공격이 가능합니다.

## 위치
- Line 347: `{item['title']}`
- Line 350: `{item['summary']}`

## 해결책
html 모듈의 escape() 함수를 사용하여 모든 사용자 입력을 이스케이프 처리해야 합니다.

## 심각도
🔴 높음""",
        "labels": ["bug", "security"]
    },
    {
        "title": "에러 처리 개선: 과도하게 광범위한 Exception 처리",
        "body": """## 문제
모든 fetch 메서드에서 광범위한 `except Exception as e:` 처리로 인해 구체적인 에러 원인을 파악하기 어렵습니다.

## 위치
- Line 34-35: Google News
- Line 59-60: Hacker News
- Line 79-80: Product Hunt
- Line 100-101: Reddit

## 문제점
- 네트워크 타임아웃 vs API 에러 vs 파싱 에러 구분 불가
- 중요한 에러 정보가 손실됨
- 디버깅 어려움

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "로깅 부재: print()만 사용 중 - 실행 기록 남지 않음",
        "body": """## 문제
프로그램이 작업 스케줄러에서 자동 실행될 때 print() 출력이 어디로 가는지 알 수 없습니다. 오류 발생 시 추적이 어렵습니다.

## 해결책
logging 모듈을 사용하여 파일에 기록합니다.

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "Hacker News: 실제 발행일 대신 현재 날짜로 설정됨",
        "body": """## 문제
Line 56에서 Hacker News의 뉴스는 항상 오늘 날짜로 저장됩니다. 실제로는 며칠 전 기사일 수 있습니다.

## 해결책
BeautifulSoup으로 실제 발행일을 파싱해서 사용해야 합니다.

## 심각도
🟡 중간""",
        "labels": ["bug"]
    },
    {
        "title": "타임아웃 설정 불일치: Google News와 Product Hunt에 타임아웃 없음",
        "body": """## 문제
- Google News: timeout 설정 없음
- Product Hunt: timeout 설정 없음
- Hacker News, Reddit: timeout=10

네트워크가 느릴 때 무한 대기할 수 있습니다.

## 심각도
🟡 중간""",
        "labels": ["bug"]
    },
    {
        "title": "중복 제거 로직 개선: 제목만으로 중복 판단",
        "body": """## 문제
같은 뉴스가 다른 제목으로 표현되면 중복으로 감지되지 않습니다.

## 해결책
정규화된 제목으로 중복 제거합니다.

## 심각도
🟢 낮음""",
        "labels": ["enhancement"]
    },
    {
        "title": "robots.txt 미준수: 자동 크롤링 정책 확인 필요",
        "body": """## 문제
일부 웹사이트(예: Hacker News)는 robots.txt에서 자동 크롤링을 제한할 수 있습니다.

## 해결책
공식 API 사용 추천 (Hacker News는 공식 API 제공)

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "뉴스 0개 수집 시 처리 로직 확인",
        "body": """## 문제
모든 소스에서 뉴스를 못 가져왔을 때 빈 대시보드가 생성됩니다.

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "README: setup_scheduler.ps1 실행 방법이 불명확함",
        "body": """## 문제
README.md에서 PowerShell 실행 정책 변경 설명이 부족합니다.

## 심각도
🟡 중간""",
        "labels": ["documentation"]
    }
]

async def create_issues():
    """웹브라우저를 자동으로 제어해서 GitHub Issues 생성"""

    print("🚀 Playwright로 GitHub 자동화 시작...")
    print(f"📊 총 {len(ISSUES)}개 이슈를 생성합니다.\n")

    async with async_playwright() as p:
        # 사용자의 기본 브라우저로 실행 (이미 로그인된 상태 활용)
        browser = await p.chromium.launch(
            headless=False,  # 보이는 창으로 실행
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context()
        page = await context.new_page()

        created = 0
        failed = 0

        try:
            for i, issue in enumerate(ISSUES, 1):
                try:
                    print(f"[{i}/{len(ISSUES)}] {issue['title'][:50]}...", end=" ")

                    # GitHub Issues 페이지로 이동
                    await page.goto("https://github.com/ehdwns3755-byte/AI-/issues/new", wait_until="networkidle")

                    # Title 입력
                    await page.fill('input[name="issue[title]"]', issue['title'])

                    # Body/Description 입력
                    await page.fill('textarea[name="issue[body]"]', issue['body'])

                    # Labels 추가
                    for label in issue['labels']:
                        try:
                            # Label 입력 필드 찾기
                            await page.fill('input[placeholder="Label"]', label)
                            await page.wait_for_timeout(500)

                            # 드롭다운에서 선택
                            label_option = await page.query_selector(f'a:has-text("{label}")')
                            if label_option:
                                await label_option.click()
                                await page.wait_for_timeout(300)
                        except:
                            pass  # Label이 없으면 스킵

                    # "Submit new issue" 버튼 클릭
                    await page.click('button:has-text("Submit new issue")')

                    # 이슈 생성 확인 (URL 변경 대기)
                    await page.wait_for_url(lambda url: "/issues/" in url, timeout=5000)

                    print("✅")
                    created += 1

                except Exception as e:
                    print(f"❌ 오류: {str(e)[:50]}")
                    failed += 1

                # 다음 이슈 전에 잠시 대기
                await page.wait_for_timeout(2000)

        finally:
            await browser.close()

        print(f"\n{'='*50}")
        print(f"📊 결과: {created}개 생성, {failed}개 실패")
        print(f"{'='*50}")

        if created == len(ISSUES):
            print("✨ 모든 이슈가 성공적으로 생성되었습니다!")
            print(f"📍 확인: https://github.com/ehdwns3755-byte/AI-/issues")
            return True
        else:
            print(f"⚠️  {failed}개 이슈 생성 실패")
            return False

async def main():
    """메인 함수"""
    success = await create_issues()
    exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
