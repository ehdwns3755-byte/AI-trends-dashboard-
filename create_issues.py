#!/usr/bin/env python3
"""Create GitHub issues for AI Trends Dashboard"""

import requests
import json

# GitHub API 설정
OWNER = "ehdwns3755-byte"
REPO = "AI-"
BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

# 이슈 목록
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

```python
from html import escape
# ...
escape(item['title'])
```

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

## 해결책
구체적인 Exception 타입으로 분리:
```python
except requests.Timeout:
    print(f"Timeout: {url}")
except requests.RequestException as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "로깅 부재: print()만 사용 중 - 실행 기록 남지 않음",
        "body": """## 문제
프로그램이 작업 스케줄러에서 자동 실행될 때 print() 출력이 어디로 가는지 알 수 없습니다. 오류 발생 시 추적이 어렵습니다.

## 해결책
logging 모듈을 사용하여 파일에 기록:

```python
import logging
logging.basicConfig(
    filename='ai_trends.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info('AI 뉴스 수집 시작')
```

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "Hacker News: 실제 발행일 대신 현재 날짜로 설정됨",
        "body": """## 문제
Line 56에서 Hacker News의 뉴스는 항상 오늘 날짜로 저장됩니다. 실제로는 며칠 전 기사일 수 있습니다.

```python
'date': datetime.now().strftime('%Y-%m-%d'),  # ❌ 잘못됨
```

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

## 해결책
모든 requests.get() 호출에 timeout 설정:
```python
response = requests.get(url, headers=headers, timeout=10)
```

## 심각도
🟡 중간""",
        "labels": ["bug"]
    },
    {
        "title": "중복 제거 로직 개선: 제목만으로 중복 판단",
        "body": """## 문제
같은 뉴스가 다른 제목으로 표현되면 중복으로 감지되지 않습니다.
또한 제목의 대소문자 차이도 무시됩니다.

## 해결책
정규화된 제목으로 중복 제거:
```python
normalized_title = title.lower().strip()
if normalized_title not in seen:
    seen.add(normalized_title)
    unique_items.append(item)
```

## 심각도
🟢 낮음""",
        "labels": ["enhancement"]
    },
    {
        "title": "robots.txt 미준수: 자동 크롤링 정책 확인 필요",
        "body": """## 문제
일부 웹사이트(예: Hacker News)는 robots.txt에서 자동 크롤링을 제한할 수 있습니다.

## 해결책
- 공식 API 사용 추천 (Hacker News는 공식 API 제공)
- 또는 적절한 User-Agent와 Delay 추가
- robots.txt 확인

## 참고
- Hacker News는 JSON API 제공: https://github.com/HackerNews/API

## 심각도
🟡 중간 (법적 이슈 가능성)""",
        "labels": ["enhancement"]
    },
    {
        "title": "뉴스 0개 수집 시 처리 로직 확인",
        "body": """## 문제
모든 소스에서 뉴스를 못 가져왔을 때 빈 대시보드가 생성됩니다. 사용자가 뭐가 잘못됐는지 알 수 없습니다.

## 해결책
```python
if not self.news_items:
    logging.warning('수집된 뉴스가 없습니다. 네트워크 연결 확인')
    # 혹은 이전 데이터 사용 옵션
```

## 심각도
🟡 중간""",
        "labels": ["enhancement"]
    },
    {
        "title": "README: setup_scheduler.ps1 실행 방법이 불명확함",
        "body": """## 문제
README.md에서:
1. PowerShell 실행 정책 변경 설명 부족
2. 관리자 권한 필요성 명시 안 됨
3. 오류 발생 시 대응 방법 없음

## 해결책
더 자세한 단계별 가이드 추가

## 심각도
🟡 중간 (사용자 경험)""",
        "labels": ["documentation"]
    }
]

def create_issues(token):
    """GitHub API를 사용하여 이슈 생성"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    created = 0
    failed = 0

    for issue in ISSUES:
        try:
            response = requests.post(
                BASE_URL,
                headers=headers,
                json={
                    "title": issue["title"],
                    "body": issue["body"],
                    "labels": issue.get("labels", [])
                }
            )

            if response.status_code == 201:
                issue_num = response.json()["number"]
                print(f"✓ Issue #{issue_num} 생성: {issue['title'][:50]}...")
                created += 1
            else:
                print(f"✗ 실패: {issue['title'][:50]}...")
                print(f"  응답: {response.json()}")
                failed += 1
        except Exception as e:
            print(f"✗ 오류: {issue['title'][:50]}... - {e}")
            failed += 1

    print(f"\n📊 결과: {created}개 생성, {failed}개 실패")
    return created > 0

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ GitHub Personal Access Token이 필요합니다.")
        print("\n사용법:")
        print("  python create_issues.py <YOUR_GITHUB_TOKEN>")
        print("\n토큰 생성 방법:")
        print("  1. https://github.com/settings/tokens 방문")
        print("  2. 'Generate new token' 클릭")
        print("  3. 'repo' 권한 선택")
        print("  4. 토큰 복사 후 위 명령 실행")
        sys.exit(1)

    token = sys.argv[1]
    print(f"🚀 {len(ISSUES)}개의 이슈를 생성합니다...\n")

    if create_issues(token):
        print("\n✅ 모든 이슈가 성공적으로 생성되었습니다!")
        print(f"   저장소: https://github.com/{OWNER}/{REPO}/issues")
    else:
        print("\n❌ 이슈 생성 중 오류가 발생했습니다.")
        sys.exit(1)
