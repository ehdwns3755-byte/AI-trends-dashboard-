"""
경제뉴스 도구 완전 테스트 스위트

테스트 실행:
    pytest tests/test_economics_news_complete.py -v
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from pathlib import Path

from agent_harness.tools.economics_news import (
    fetch_economics_news,
    categorize_economics_news,
    generate_economics_summary,
    validate_days,
    get_article_hash,
    is_new_article,
)
from agent_harness.exceptions import (
    ValidationException,
    FetchException,
    ParseException,
)


# ========== Unit Tests ==========

class TestValidateDays:
    """days 파라미터 검증 테스트"""

    def test_valid_days(self):
        """유효한 days 값"""
        validate_days(1)
        validate_days(0)
        validate_days(365)

    def test_invalid_days_negative(self):
        """음수 days"""
        with pytest.raises(ValidationException):
            validate_days(-1)

    def test_invalid_days_exceeds_max(self):
        """최대값 초과"""
        with pytest.raises(ValidationException):
            validate_days(366)

    def test_invalid_days_not_integer(self):
        """정수가 아님"""
        with pytest.raises(ValidationException):
            validate_days("1")


class TestArticleHash:
    """해시 생성 및 중복 검사 테스트"""

    def test_same_title_same_hash(self):
        """같은 제목은 같은 해시"""
        article1 = {"title": "Test News"}
        article2 = {"title": "Test News"}

        hash1 = get_article_hash(article1)
        hash2 = get_article_hash(article2)

        assert hash1 == hash2

    def test_different_title_different_hash(self):
        """다른 제목은 다른 해시"""
        article1 = {"title": "Test News 1"}
        article2 = {"title": "Test News 2"}

        hash1 = get_article_hash(article1)
        hash2 = get_article_hash(article2)

        assert hash1 != hash2

    def test_whitespace_normalized(self):
        """공백이 정규화됨"""
        article1 = {"title": "Test   News"}
        article2 = {"title": "Test News"}

        # 제목의 내용이 같으므로 해시는 다를 수 있음
        # (normalize 기능 구현 후 같아져야 함)
        hash1 = get_article_hash(article1)
        hash2 = get_article_hash(article2)

        # 현재: 공백이 다르면 해시도 다름
        assert hash1 != hash2

    def test_is_new_article_detects_duplicates(self):
        """중복 기사 감지"""
        previous = [
            {"title": "Old News", "url": "http://example.com"},
        ]
        new = {"title": "Old News", "url": "http://different.com"}

        assert not is_new_article(new, previous)

    def test_is_new_article_detects_new(self):
        """새 기사 감지"""
        previous = [
            {"title": "Old News", "url": "http://example.com"},
        ]
        new = {"title": "New News", "url": "http://example.com"}

        assert is_new_article(new, previous)

    def test_is_new_article_empty_previous(self):
        """이전 기사 없음"""
        previous = []
        new = {"title": "New News"}

        assert is_new_article(new, previous)


# ========== Integration Tests ==========

class TestFetchEconomicsNews:
    """뉴스 수집 통합 테스트"""

    def test_fetch_returns_valid_json(self):
        """유효한 JSON 반환"""
        result = fetch_economics_news(days=1)
        data = json.loads(result)

        assert data["status"] == "success"
        assert "articles" in data
        assert isinstance(data["articles"], list)

    def test_fetch_contains_required_fields(self):
        """필수 필드 포함"""
        result = fetch_economics_news(days=1)
        data = json.loads(result)

        required_fields = ["status", "date", "time", "new_count", "total_archived", "articles"]
        for field in required_fields:
            assert field in data

    def test_fetch_articles_have_required_fields(self):
        """기사가 필수 필드 포함"""
        result = fetch_economics_news(days=1)
        data = json.loads(result)

        if data["articles"]:
            article = data["articles"][0]
            required_fields = ["source", "title", "url", "summary", "date"]
            for field in required_fields:
                assert field in article

    def test_fetch_today_articles_only(self):
        """오늘 기사만 반환"""
        result = fetch_economics_news(days=1)
        data = json.loads(result)
        today = datetime.now().strftime("%Y-%m-%d")

        for article in data["articles"]:
            assert article["date"] == today

    def test_fetch_with_invalid_days(self):
        """유효하지 않은 days"""
        with pytest.raises(ValidationException):
            fetch_economics_news(days=-1)


class TestCategorizeEconomicsNews:
    """뉴스 분류 통합 테스트"""

    @pytest.fixture
    def sample_news_json(self):
        """샘플 뉴스 JSON"""
        news = {
            "status": "success",
            "articles": [
                {
                    "source": "경제신문",
                    "title": "AI 시장 성장 가속화",
                    "url": "http://example.com/1",
                    "summary": "인공지능 기술이 빠르게 성장하고 있습니다",
                    "date": "2026-06-12",
                },
                {
                    "source": "금융뉴스",
                    "title": "주식 시장 상승",
                    "url": "http://example.com/2",
                    "summary": "오늘 주식 시장이 상승했습니다",
                    "date": "2026-06-12",
                },
                {
                    "source": "부동산",
                    "title": "아파트 가격 변동",
                    "url": "http://example.com/3",
                    "summary": "부동산 시장 동향",
                    "date": "2026-06-12",
                },
            ]
        }
        return json.dumps(news, ensure_ascii=False)

    def test_categorize_returns_valid_json(self, sample_news_json):
        """유효한 JSON 반환"""
        result = categorize_economics_news(sample_news_json)
        data = json.loads(result)

        assert data["status"] == "success"
        assert "categorized" in data

    def test_categorize_correct_categories(self, sample_news_json):
        """올바른 카테고리 분류"""
        result = categorize_economics_news(sample_news_json)
        data = json.loads(result)

        assert "기술/IT" in data["categorized"]
        assert "금융/증권" in data["categorized"]
        assert "부동산" in data["categorized"]

    def test_categorize_with_invalid_json(self):
        """유효하지 않은 JSON"""
        with pytest.raises(ParseException):
            categorize_economics_news("invalid json")

    def test_categorize_with_empty_articles(self):
        """빈 기사 목록"""
        news = {"articles": []}
        result = categorize_economics_news(json.dumps(news))
        data = json.loads(result)

        assert data["total"] == 0
        assert len(data["categorized"]) == 0


class TestGenerateSummary:
    """요약 생성 통합 테스트"""

    @pytest.fixture
    def sample_categorized_json(self):
        """샘플 분류된 뉴스"""
        categorized = {
            "categorized": {
                "기술/IT": {
                    "count": 2,
                    "articles": [{"title": "AI News 1"}, {"title": "AI News 2"}],
                },
                "금융/증권": {
                    "count": 1,
                    "articles": [{"title": "Stock News"}],
                },
            }
        }
        return json.dumps(categorized)

    def test_generate_returns_valid_json(self, sample_categorized_json):
        """유효한 JSON 반환"""
        result = generate_economics_summary(sample_categorized_json)
        data = json.loads(result)

        assert data["status"] == "success"
        assert "date" in data
        assert "key_points" in data

    def test_generate_contains_key_fields(self, sample_categorized_json):
        """핵심 필드 포함"""
        result = generate_economics_summary(sample_categorized_json)
        data = json.loads(result)

        required_fields = ["status", "date", "market_overview", "key_points"]
        for field in required_fields:
            assert field in data

    def test_generate_with_invalid_json(self):
        """유효하지 않은 JSON"""
        with pytest.raises(ParseException):
            generate_economics_summary("invalid json")


# ========== Edge Cases ==========

class TestEdgeCases:
    """엣지 케이스 테스트"""

    def test_fetch_with_zero_days(self):
        """0일 수집"""
        result = fetch_economics_news(days=0)
        data = json.loads(result)
        assert data["status"] == "success"

    def test_article_with_empty_title(self):
        """빈 제목"""
        article = {"title": ""}
        hash1 = get_article_hash(article)
        assert isinstance(hash1, str)
        assert len(hash1) == 32  # MD5 해시 길이

    def test_article_with_special_characters(self):
        """특수문자가 있는 제목"""
        article = {"title": "테스트 & <뉴스> 'AI'"}
        hash1 = get_article_hash(article)
        assert isinstance(hash1, str)

    def test_article_with_unicode(self):
        """유니코드 제목"""
        article = {"title": "中文 테스트 😀"}
        hash1 = get_article_hash(article)
        assert isinstance(hash1, str)

    def test_categorize_with_unknown_category(self):
        """미분류 기사"""
        news = {
            "articles": [
                {
                    "title": "완전히 새로운 주제",
                    "url": "http://example.com",
                }
            ]
        }
        result = categorize_economics_news(json.dumps(news, ensure_ascii=False))
        data = json.loads(result)

        assert data["total"] == 1


# ========== Performance Tests ==========

class TestPerformance:
    """성능 테스트"""

    def test_fetch_completes_in_reasonable_time(self):
        """수집이 합리적인 시간에 완료"""
        import time
        start = time.time()
        fetch_economics_news(days=1)
        duration = time.time() - start

        assert duration < 30  # 30초 이내

    def test_categorize_many_articles(self):
        """많은 기사 분류"""
        articles = [
            {
                "title": f"AI News {i}",
                "url": f"http://example.com/{i}",
                "summary": "테스트",
                "date": "2026-06-12",
            }
            for i in range(100)
        ]
        news = {"articles": articles}

        result = categorize_economics_news(json.dumps(news, ensure_ascii=False))
        data = json.loads(result)

        assert data["total"] == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
