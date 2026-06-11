#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Issues를 REST API로 생성합니다.
Personal Access Token이나 웹 세션을 사용합니다.
"""

import requests
import json
import os

REPO_OWNER = "ehdwns3755-byte"
REPO_NAME = "AI-"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

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

def get_token():
    """토큰 가져오기"""
    # 환경변수 확인
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token

    # 사용자 입력
    print("\n" + "="*60)
    print("GitHub Personal Access Token이 필요합니다.")
    print("="*60)
    print("\n토큰 생성 방법:")
    print("1. https://github.com/settings/tokens/new 방문")
    print("2. 'repo' 권한만 체크")
    print("3. 토큰 복사\n")

    token = input("📝 토큰을 붙여넣으세요 (ghp_...): ").strip()

    if not token:
        print("❌ 토큰이 필요합니다!")
        return None

    return token

def create_issues(token):
    """API로 이슈 생성"""

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    print(f"\n🚀 {len(ISSUES)}개 이슈 생성 시작...\n")

    created = 0
    failed = 0

    for i, issue in enumerate(ISSUES, 1):
        try:
            print(f"[{i}/{len(ISSUES)}] {issue['title'][:50]}...", end=" ")

            response = requests.post(
                API_URL,
                headers=headers,
                json={
                    "title": issue["title"],
                    "body": issue["body"],
                    "labels": issue.get("labels", [])
                },
                timeout=10
            )

            if response.status_code == 201:
                issue_data = response.json()
                issue_num = issue_data["number"]
                print(f"✓ (#{issue_num})")
                created += 1
            else:
                print(f"✗ (HTTP {response.status_code})")
                if response.status_code == 401:
                    print("  └─ 토큰이 유효하지 않습니다!")
                    return False
                failed += 1
        except Exception as e:
            print(f"✗ ({str(e)[:30]})")
            failed += 1

    print(f"\n{'='*60}")
    print(f"📊 결과: {created}/{len(ISSUES)} 생성됨")
    print(f"{'='*60}\n")

    if created == len(ISSUES):
        print("✨ 모든 이슈가 성공적으로 생성되었습니다!")
        print(f"📍 확인: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues\n")
        return True
    else:
        print(f"⚠️  {failed}개 이슈 생성 실패\n")
        return False

if __name__ == "__main__":
    token = get_token()
    if token:
        success = create_issues(token)
        exit(0 if success else 1)
    else:
        print("❌ 토큰 없이 진행할 수 없습니다.")
        exit(1)
