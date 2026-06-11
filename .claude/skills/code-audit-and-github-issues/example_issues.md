# Example Issues

Real examples of issues identified by this skill, formatted as GitHub Issues.

---

## Example 1: Security - XSS Vulnerability

```markdown
## XSS 취약점: HTML 콘텐츠에 대한 이스케이프 처리 부재

### Problem
The `generate_html()` method inserts user data directly into HTML without escaping.
Malicious content in news titles (e.g., `<script>alert(1)</script>`) will execute.

### Location
- File: `ai_trends_dashboard.py`
- Lines: 347-350
- Method: `AITrendsDashboard.generate_html()`

### Current Code
```python
# Line 347-350 (VULNERABLE)
for item in self.news_items:
    html += f"<div class='news-item'>"
    html += f"  <h3>{item['title']}</h3>"
    html += f"  <p>{item['summary']}</p>"
```

### Solution
Use `html.escape()` to sanitize all user input:

```python
from html import escape

for item in self.news_items:
    html += f"<div class='news-item'>"
    html += f"  <h3>{escape(item['title'])}</h3>"
    html += f"  <p>{escape(item['summary'])}</p>"
```

### Testing
- [ ] Pass a title with `<script>` tag — verify it's rendered as text, not executed
- [ ] Verify legitimate HTML characters are preserved (e.g., `&`, `"`, `'`)
- [ ] Test with various payloads: `<img src=x onerror=alert(1)>`, etc.

### Severity
🔴 **Critical** (Security - XSS Attack Vector)

### Labels
- bug
- security
- high-priority
```

---

## Example 2: Error Handling - Overly Broad Exception

```markdown
## 에러 처리 개선: 과도하게 광범위한 Exception 처리

### Problem
All `fetch_*()` methods catch `Exception` broadly, making it impossible to distinguish
between network timeouts, API errors, and parsing failures. This hides bugs during
development and complicates debugging in production.

### Location
- File: `ai_trends_dashboard.py`
- Multiple methods: `fetch_google_news()`, `fetch_hacker_news()`, `fetch_product_hunt()`, `fetch_reddit()`
- Lines: 34-35, 59-60, 79-80, 100-101

### Current Code
```python
# Line 34-35 (OVERLY BROAD)
try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print(f"Error: {e}")  # Can't distinguish what went wrong
```

### Solution
Catch specific exceptions with informative logging:

```python
import logging
from requests.exceptions import Timeout, RequestException

logger = logging.getLogger(__name__)

try:
    response = requests.get(url, timeout=10)
    data = response.json()
except Timeout:
    logger.error(f"Timeout fetching {url} after 10 seconds")
except RequestException as e:
    logger.error(f"Network error fetching {url}: {e}")
except ValueError as e:
    logger.error(f"JSON parse error from {url}: {e}")
except Exception as e:
    logger.exception(f"Unexpected error fetching {url}: {e}")
```

### Benefits
✅ Timeout vs network error vs JSON error are now distinguishable  
✅ Logging captures full exception traceback for debugging  
✅ Different recovery strategies per error type  
✅ Easier monitoring and alerting in production  

### Testing
- [ ] Mock `requests.get()` to raise Timeout
- [ ] Mock `response.json()` to raise ValueError
- [ ] Verify each exception type is handled correctly
- [ ] Check log messages are informative

### Severity
🟡 **Medium** (Maintainability - Debugging difficulty)

### Labels
- enhancement
- refactoring
- logging
```

---

## Example 3: Logging - Missing Observability

```markdown
## 로깅 부재: print()만 사용 중 - 실행 기록 남지 않음

### Problem
The script uses `print()` for debugging but when run by Windows Task Scheduler
or cron, output is lost. There's no audit trail of executions, errors, or data
collection results.

### Location
- File: `ai_trends_dashboard.py`
- Throughout: Lines with `print()` calls in main(), fetch methods, HTML generation

### Current Code
```python
# Line 12-15
print("Starting AI trends dashboard...")
print(f"Collected {len(items)} items")
print("HTML file generated at ai_dashboard.html")
```

### Solution
Use Python's `logging` module for persistent, configurable logging:

```python
import logging

logging.basicConfig(
    filename='ai_trends.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Line 12-15
logger.info("Starting AI trends dashboard...")
logger.info(f"Collected {len(items)} items")
logger.info("HTML file generated at ai_dashboard.html")
```

### Log Output
```
2026-06-11 08:00:01 - INFO - Starting AI trends dashboard...
2026-06-11 08:00:05 - INFO - Collected 47 items from Google News
2026-06-11 08:00:08 - INFO - Collected 23 items from Hacker News
2026-06-11 08:00:15 - INFO - HTML file generated at ai_dashboard.html
2026-06-11 08:00:16 - INFO - Execution completed in 15.2 seconds
```

### Benefits
✅ Execution history persists in `ai_trends.log`  
✅ Task Scheduler can log to event viewer  
✅ Timestamps for performance analysis  
✅ Error stack traces for debugging  
✅ Log levels (DEBUG, INFO, WARNING, ERROR) for filtering  

### Testing
- [ ] Verify log file is created after first run
- [ ] Check log entries have correct timestamps
- [ ] Run from Task Scheduler and verify logging works
- [ ] Test log rotation (keep old logs, don't infinitely grow)

### Severity
🟡 **Medium** (Observability - Ops/Debugging)

### Labels
- enhancement
- logging
- operations
```

---

## Example 4: Performance - Timeout Mismatch

```markdown
## 타임아웃 설정 불일치: Google News와 Product Hunt에 타임아웃 없음

### Problem
Different API calls have inconsistent timeout settings:
- **Hacker News & Reddit**: 10-second timeout
- **Google News & Product Hunt**: No timeout (can hang indefinitely)

If a server is slow or network is unstable, the script hangs instead of failing gracefully.

### Location
- File: `ai_trends_dashboard.py`
- Lines:
  - Line 15: `requests.get(url)` ← No timeout
  - Line 45: `requests.get(url, timeout=10)` ← Has timeout
  - Line 78: `requests.get(url)` ← No timeout
  - Line 85: `requests.get(url, timeout=10)` ← Has timeout

### Current Code
```python
# Line 15 (Google News - NO TIMEOUT)
response = requests.get(GOOGLE_NEWS_URL, headers=headers)

# Line 45 (Hacker News - HAS TIMEOUT)
response = requests.get(HACKER_NEWS_URL, timeout=10)

# Line 78 (Product Hunt - NO TIMEOUT)
response = requests.get(PRODUCT_HUNT_URL, headers=headers)

# Line 85 (Reddit - HAS TIMEOUT)
response = requests.get(REDDIT_URL, timeout=10)
```

### Solution
Add consistent timeout (10-15 seconds) to all requests:

```python
# All four fetch methods should include timeout
TIMEOUT = 10

def fetch_google_news(self):
    response = requests.get(GOOGLE_NEWS_URL, headers=headers, timeout=TIMEOUT)

def fetch_product_hunt(self):
    response = requests.get(PRODUCT_HUNT_URL, headers=headers, timeout=TIMEOUT)
```

### Why 10 Seconds?
- Typical network response: 1-3 seconds
- Slow network/server: 3-8 seconds
- Buffer for retry logic: 10 seconds is reasonable
- Task Scheduler task timeout: Usually 15-30 minutes, so 10s per source is fine

### Testing
- [ ] Mock slow server (5-second delay) — verify request times out
- [ ] Mock no-response server (infinite delay) — verify timeout triggers
- [ ] Normal server — verify response completes in <5 seconds
- [ ] Stress test with slow internet connection

### Severity
🟡 **Medium** (Reliability - Hang Risk)

### Labels
- bug
- reliability
- timeout
```

---

## Example 5: Enhancement - Improvement Suggestion

```markdown
## 중복 제거 로직 개선: 제목만으로 중복 판단

### Problem
Current duplicate detection only checks if a title has been seen before.
Same news reported by different sources with slightly different headlines
(e.g., "AI Breakthrough" vs "Breakthrough in AI") are treated as unique items.

### Location
- File: `ai_trends_dashboard.py`
- Method: `_remove_duplicates()`
- Line: 220-225

### Current Code
```python
def _remove_duplicates(self):
    seen_titles = set()
    unique_items = []
    
    for item in self.news_items:
        title = item['title']  # ← Exact match only
        if title not in seen_titles:
            seen_titles.add(title)
            unique_items.append(item)
    
    return unique_items
```

### Improved Approach
Normalize titles before comparison (lowercase, remove common words):

```python
import re

def _remove_duplicates(self):
    seen_normalized = set()
    unique_items = []
    
    for item in self.news_items:
        title = item['title']
        # Normalize: lowercase + remove punctuation + deduplicate whitespace
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        if normalized not in seen_normalized:
            seen_normalized.add(normalized)
            unique_items.append(item)
    
    return unique_items
```

### Examples
```
Input:  "AI Breakthrough in Machine Learning" (News Source A)
        "Breakthrough in AI & ML Systems" (News Source B)

Before: Both kept (different titles)
After:  First one kept, second marked as duplicate
```

### Benefits
✅ Reduces duplicates across sources  
✅ Cleaner news feed (less repetition)  
✅ Better user experience  
✅ More reliable deduplication  

### Testing
- [ ] Test with identical titles (should dedupe)
- [ ] Test with different punctuation ("AI" vs "A.I.")
- [ ] Test with synonyms ("ML" vs "Machine Learning")
- [ ] Verify no false positives (different stories marked duplicate)

### Severity
🟢 **Low** (Enhancement - Nice to have)

### Labels
- enhancement
- deduplication
- low-priority
```

---

## How to Use These Examples

1. **Copy the format** when creating new issues
2. **Always include**: Problem, Location, Current Code, Solution
3. **Use severity labels**: 🔴 Critical, 🟡 Medium, 🟢 Low
4. **Be specific**: Line numbers, method names, exact symptoms
5. **Show examples**: Before/after code, test cases, expected behavior

---

**More examples available in your GitHub Issues once the skill is applied to your codebase.**
