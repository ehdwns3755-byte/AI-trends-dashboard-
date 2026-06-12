"""
캐싱 시스템
"""

import time
from typing import Any, Callable, Optional, Dict
from datetime import datetime, timedelta
from agent_harness.logger import get_logger

logger = get_logger(__name__)


class CacheEntry:
    """캐시 항목"""
    def __init__(self, value: Any, ttl_seconds: int = 3600):
        self.value = value
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds

    def is_expired(self) -> bool:
        """만료되었는지 확인"""
        return (time.time() - self.created_at) > self.ttl_seconds

    def __repr__(self):
        age = time.time() - self.created_at
        return f"CacheEntry(age={age:.0f}s, ttl={self.ttl_seconds}s, expired={self.is_expired()})"


class SimpleCache:
    """메모리 기반 단순 캐시"""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Optional[Any]:
        """캐시에서 값 가져오기"""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            logger.debug(f"캐시 만료: {key}")
            return None

        logger.debug(f"캐시 히트: {key}")
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """캐시에 값 저장"""
        self._cache[key] = CacheEntry(value, ttl_seconds)
        logger.debug(f"캐시 저장: {key} (TTL: {ttl_seconds}s)")

    def clear(self) -> None:
        """캐시 전체 삭제"""
        self._cache.clear()
        logger.info("캐시 초기화")

    def cleanup_expired(self) -> int:
        """만료된 항목 정리"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self._cache[key]

        if expired_keys:
            logger.info(f"만료된 캐시 정리: {len(expired_keys)}개")

        return len(expired_keys)

    def __len__(self) -> int:
        """캐시 항목 수"""
        return len(self._cache)

    def __repr__(self) -> str:
        return f"SimpleCache(items={len(self._cache)})"


class CachedFunction:
    """함수 호출 결과 캐싱"""

    def __init__(self, func: Callable, ttl_seconds: int = 3600):
        self.func = func
        self.ttl_seconds = ttl_seconds
        self.cache = SimpleCache()

    def __call__(self, *args, **kwargs) -> Any:
        """캐싱과 함께 함수 실행"""
        cache_key = self._make_key(args, kwargs)

        cached_value = self.cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        logger.debug(f"캐시 미스: {self.func.__name__}({args}, {kwargs})")
        result = self.func(*args, **kwargs)
        self.cache.set(cache_key, result, self.ttl_seconds)

        return result

    @staticmethod
    def _make_key(args, kwargs) -> str:
        """캐시 키 생성"""
        key_parts = [str(arg) for arg in args]
        key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
        return "|".join(key_parts)


# 전역 캐시 인스턴스
_global_cache = SimpleCache()


def get_cache() -> SimpleCache:
    """전역 캐시 인스턴스"""
    return _global_cache


def cached(ttl_seconds: int = 3600):
    """캐싱 데코레이터"""
    def decorator(func: Callable) -> Callable:
        cached_func = CachedFunction(func, ttl_seconds)

        def wrapper(*args, **kwargs):
            return cached_func(*args, **kwargs)

        wrapper._cache = cached_func.cache
        return wrapper

    return decorator
