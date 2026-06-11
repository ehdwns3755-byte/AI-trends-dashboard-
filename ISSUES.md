# GitHub Issues - AI Trends Dashboard

## 이전 이슈들 (완료됨)

모든 초기 9개 이슈가 이미 완료되었습니다:
- ✅ XSS 취약점 해결
- ✅ 에러 처리 개선
- ✅ 로깅 부재 해결
- ✅ Hacker News 날짜 버그 수정
- ✅ 타임아웃 설정 통일
- ✅ 중복 제거 개선
- ✅ robots.txt 미준수 해결
- ✅ 빈 결과 처리 추가
- ✅ README 가이드 개선

---

## 새로운 개선 이슈들

## Issue 1️⃣0️⃣: 중복 파일 정리: 이전 GitHub issue 생성 스크립트 제거

**Type:** Chore 🧹
**Priority:** 🟢 Low

### 문제
create_issues.py, auto_create_issues.py, create_issues_api.py 등 여러 개의 레거시 스크립트가 있습니다.
이들은 이전에 GitHub Issues를 자동으로 생성하기 위해 만들었으나, 현재는 사용되지 않습니다.

### 위치
- create_issues.py (252줄)
- auto_create_issues.py (221줄)
- create_issues_api.py (216줄)

### 해결책
- 더 이상 필요 없는 파일들 제거
- .gitignore 업데이트
- 필요시 아카이브

---

## Issue 1️⃣1️⃣: 성능 개선: Hacker News API N+1 호출 문제

**Type:** Improvement 📈
**Priority:** 🟡 Medium

### 문제
현재 코드는 Hacker News에서:
1. 30개의 story ID를 가져옴
2. 각 ID에 대해 개별 API 호출 (30번의 HTTP 요청)

이는 불필요한 네트워크 호출을 많이 발생시킵니다. 실행 시간이 30초 이상 걸릴 수 있습니다.

### 위치
- ai_trends_dashboard.py, Line 74-96: fetch_hacker_news() 메서드

### 현재 코드 문제
```python
for story_id in story_ids:
    story_response = requests.get(story_url, timeout=10)  # 각 ID마다 호출
    # ...
```

### 해결책
- 병렬 요청 사용 (concurrent.futures 또는 asyncio)
- 또는 배치 처리로 요청 수 줄이기
- 결과 캐싱 추가

---

## Issue 1️⃣2️⃣: 설정 외부화: 하드코딩된 값들을 설정 파일로 분리

**Type:** Improvement 📈
**Priority:** 🟡 Medium

### 문제
코드에 하드코딩된 설정값들:
- 각 뉴스 소스마다 가져올 항목 수 (10, 15, 30)
- 카테고리 키워드 리스트
- API URL들
- 대시보드 업데이트 주기 (3600초)
- 타임아웃 값 (10초)

### 위치
- ai_trends_dashboard.py 전체 (여러 곳)

### 해결책
config.json 파일 생성:
```json
{
  "sources": {
    "google_news": {"limit": 15, "timeout": 10},
    "hacker_news": {"limit": 10, "timeout": 10},
    "product_hunt": {"limit": 10, "timeout": 10},
    "reddit": {"limit": 10, "timeout": 10}
  },
  "categories": {
    "Large Language Models": ["llm", "gpt", "transformer", "language model"],
    "Computer Vision": ["computer vision", "image", "video"],
    "Automation & Robotics": ["robot", "automation", "agent"]
  },
  "dashboard": {
    "refresh_interval": 3600,
    "max_items_per_category": 6
  }
}
```

---

## Issue 1️⃣3️⃣: 테스트 부재: 단위 테스트 및 통합 테스트 추가

**Type:** Improvement 📈
**Priority:** 🟡 Medium

### 문제
프로젝트에 테스트가 전혀 없습니다:
- 카테고리화 로직 테스트 없음
- 데이터 필터링 로직 테스트 없음
- HTML 생성 로직 테스트 없음
- API 호출 에러 처리 테스트 없음
- 중복 제거 로직 테스트 없음

### 해결책
pytest 추가:
```bash
pip install pytest pytest-mock
```

test_ai_trends.py 생성:
- test_categorize(): 카테고리화 로직 검증
- test_fetch_*(): API 호출 에러 처리
- test_generate_html(): HTML 문법 검증 및 XSS 방지 검증
- test_duplicate_removal(): 중복 제거 검증

---

## Issue 1️⃣4️⃣: 환경 변수 관리: 경로와 설정값을 환경 변수로

**Type:** Improvement 📈
**Priority:** 🟡 Medium

### 문제
하드코딩된 경로와 설정:
- 스크립트 디렉토리 (현재 자동 감지하지만 명시적 설정 가능)
- 데이터 파일 위치
- 로그 파일 위치
- API 타임아웃 값

### 해결책
.env 파일 사용:
```
DATA_DIR=./data
LOG_DIR=./logs
LOG_LEVEL=INFO
API_TIMEOUT=10
DEBUG=false
```

python-dotenv 사용:
```python
from dotenv import load_dotenv
load_dotenv()
timeout = int(os.getenv('API_TIMEOUT', '10'))
```

---

## Issue 1️⃣5️⃣: 캐싱 메커니즘: 네트워크 실패 시 이전 데이터 사용

**Type:** Improvement 📈
**Priority:** 🟡 Medium

### 문제
모든 뉴스 수집이 실패하면 빈 대시보드가 생성됩니다.
사용자는 이전 데이터를 보는 것이 낫습니다.

### 위치
- ai_trends_dashboard.py, run() 메서드

### 해결책
이전 데이터를 백업해놨다가 복구:
```python
def _load_previous_data(self):
    """Load previous data if current fetch fails"""
    backup_file = self.data_file + '.backup'
    if os.path.exists(backup_file):
        with open(backup_file) as f:
            return json.load(f)
    return {'items': []}

# 수집 성공 후
self._backup_data()
```

---

## Summary

| Issue | Type | Priority | 상태 |
|-------|------|----------|------|
| 중복 파일 정리 | Chore | 🟢 Low | TODO |
| Hacker News 성능 | Improvement | 🟡 Medium | TODO |
| 설정 외부화 | Improvement | 🟡 Medium | TODO |
| 테스트 추가 | Improvement | 🟡 Medium | TODO |
| 환경 변수 | Improvement | 🟡 Medium | TODO |
| 캐싱 메커니즘 | Improvement | 🟡 Medium | TODO |

---

**생성 일시**: 2026-06-11
**분석 도구**: code-audit-and-github-issues skill
