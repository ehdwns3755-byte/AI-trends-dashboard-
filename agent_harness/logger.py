"""
프로젝트 로깅 시스템
"""

import logging
import logging.handlers
from pathlib import Path
from agent_harness.constants import LOG_FORMAT, LOG_DATE_FORMAT, LOG_LEVEL, LOG_FILE


class ProjectLogger:
    """중앙화된 로깅 관리자"""

    _loggers = {}

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """로거 인스턴스 반환 (싱글톤 패턴)"""
        if name not in ProjectLogger._loggers:
            ProjectLogger._loggers[name] = ProjectLogger._create_logger(name)
        return ProjectLogger._loggers[name]

    @staticmethod
    def _create_logger(name: str) -> logging.Logger:
        """로거 생성"""
        logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL)

        # 로그 디렉토리 생성
        log_dir = Path(LOG_FILE).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # 포매터 설정
        formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

        # 파일 핸들러 (로테이션)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger


def get_logger(name: str) -> logging.Logger:
    """편의 함수: 로거 가져오기"""
    return ProjectLogger.get_logger(name)
