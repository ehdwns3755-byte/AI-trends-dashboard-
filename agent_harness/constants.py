"""
프로젝트 전역 상수 정의
"""

# ========== 뉴스 수집 설정 ==========
DEFAULT_DAYS = 1
MAX_ARTICLES_PER_SOURCE = 10
MAX_ARCHIVED_ARTICLES = 100

# RSS 피드 URL
RSS_FEEDS = {
    "네이버 경제": "https://rss.news.naver.com/ranking/article/1.rss",
    "한국경제": "https://feeds.hankyung.com/feed/economy",
    "이데일리": "https://feeds.edaily.co.kr/feed/finance",
}

# 뉴스 카테고리
CATEGORIES = {
    "기술/IT": ["ai", "인공지능", "기술", "디지털", "it", "소프트웨어", "테크"],
    "금융/증권": ["주식", "나스닥", "지수", "투자", "증권", "펀드", "금리"],
    "부동산": ["부동산", "아파트", "주택", "건설", "개발"],
    "통화/환율": ["환율", "원화", "달러", "환전", "통화"],
    "산업/기업": ["기업", "회사", "산업", "비즈니스", "경영"],
}

# ========== 스케줄링 설정 ==========
SCHEDULER_TIME = "08:00"  # 매일 8시
SCHEDULER_INTERVAL_SECONDS = 60  # 1분마다 확인

# ========== 성능 설정 ==========
REQUEST_TIMEOUT_SECONDS = 10
MAX_CONCURRENT_REQUESTS = 5
CACHE_EXPIRE_HOURS = 24

# ========== 파일 경로 ==========
ARCHIVE_FILE = "news_archive.json"
DASHBOARD_FILE = "economics_news_daily.html"
LOG_FILE = "logs/app.log"

# ========== 로깅 설정 ==========
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = "INFO"

# ========== 에러 메시지 ==========
ERROR_MESSAGES = {
    "fetch_failed": "뉴스 수집 실패: {source}",
    "parse_failed": "JSON 파싱 실패",
    "invalid_date": "잘못된 날짜 형식",
    "no_articles": "수집된 뉴스가 없습니다",
    "timeout": "요청 시간 초과 ({seconds}초)",
}

# ========== 성공 메시지 ==========
SUCCESS_MESSAGES = {
    "fetch_success": "뉴스 수집 완료: {count}개",
    "categorize_success": "분류 완료: {categories}개 카테고리",
    "archive_saved": "아카이브 저장 완료: {count}개",
}

# ========== 대시보드 설정 ==========
DASHBOARD_THEME = {
    "primary_color": "#1e3c72",
    "secondary_color": "#2a5298",
    "accent_color": "#667eea",
    "success_color": "#27ae60",
    "error_color": "#e74c3c",
    "warning_color": "#f39c12",
}

DASHBOARD_CARDS_PER_CATEGORY = 3
DASHBOARD_SUMMARY_LENGTH = 150
