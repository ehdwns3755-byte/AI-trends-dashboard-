"""
프로젝트 커스텀 예외 클래스
"""


class AgentHarnessException(Exception):
    """기본 에이전트 하네스 예외"""
    pass


class FetchException(AgentHarnessException):
    """뉴스 수집 실패"""
    def __init__(self, source: str, message: str = None):
        self.source = source
        self.message = message or f"Failed to fetch from {source}"
        super().__init__(self.message)


class ParseException(AgentHarnessException):
    """데이터 파싱 실패"""
    def __init__(self, data_type: str, message: str = None):
        self.data_type = data_type
        self.message = message or f"Failed to parse {data_type}"
        super().__init__(self.message)


class ValidationException(AgentHarnessException):
    """데이터 검증 실패"""
    def __init__(self, field: str, value: str, message: str = None):
        self.field = field
        self.value = value
        self.message = message or f"Invalid {field}: {value}"
        super().__init__(self.message)


class TimeoutException(AgentHarnessException):
    """요청 시간 초과"""
    def __init__(self, source: str, timeout_seconds: int):
        self.source = source
        self.timeout_seconds = timeout_seconds
        self.message = f"Timeout fetching {source} ({timeout_seconds}s)"
        super().__init__(self.message)


class ArchiveException(AgentHarnessException):
    """아카이브 작업 실패"""
    def __init__(self, operation: str, message: str = None):
        self.operation = operation
        self.message = message or f"Archive {operation} failed"
        super().__init__(self.message)


class ConfigException(AgentHarnessException):
    """설정 오류"""
    def __init__(self, key: str, message: str = None):
        self.key = key
        self.message = message or f"Configuration error for {key}"
        super().__init__(self.message)
