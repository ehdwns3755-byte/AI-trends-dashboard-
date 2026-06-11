# 🤖 AI Trends Daily Dashboard

매일 오전 8시에 최신 AI 뉴스를 자동으로 수집하고 깔끔한 대시보드로 표시하는 시스템입니다.

## ✨ 주요 기능

- **자동 뉴스 수집**: Google News, Hacker News, Product Hunt, Reddit에서 AI 관련 뉴스 수집
- **카테고리 분류**: Large Language Models, Computer Vision, Automation & Robotics 등으로 자동 분류
- **깔끔한 대시보드**: 다크모드 지원, 반응형 디자인
- **일일 자동 업데이트**: Windows 작업 스케줄러로 매일 오전 8시에 자동 실행
- **로컬 저장**: 데이터는 로컬에 JSON으로 저장

## 🚀 설치

### 1. Python 설치 확인
Python 3.7+ 이 설치되어 있는지 확인하세요:
```bash
python --version
```

### 2. 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3. Windows 작업 스케줄러 설정 (관리자 권한 필요)
PowerShell을 **관리자로 실행**한 후:
```powershell
# 실행 정책 변경 (한 번만 필요)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 스케줄러 설정 실행
.\setup_scheduler.ps1
```

## 📖 사용법

### 수동 실행
```bash
python ai_trends_dashboard.py
```

결과:
- `ai_dashboard.html` - 생성된 대시보드 (브라우저에서 열기)
- `ai_trends_data.json` - 수집된 뉴스 데이터

### 자동 실행
Windows 작업 스케줄러에 등록되면 매일 오전 8시에 자동으로 실행됩니다.

## 📁 파일 구조

```
AI/
├── ai_trends_dashboard.py      # 메인 스크립트
├── ai_dashboard.html           # 생성되는 대시보드
├── ai_trends_data.json         # 캐시된 뉴스 데이터
├── requirements.txt            # Python 패키지
├── setup_scheduler.ps1         # Windows 스케줄러 설정
├── README.md                   # 이 파일
└── .gitignore                  # Git 무시 파일
```

## 🔧 트러블슈팅

### Python을 찾을 수 없음
PATH에 Python이 추가되어 있지 않을 수 있습니다. Python을 설치할 때 "Add Python to PATH" 옵션을 선택하세요.

### 스케줄러 작업이 실행되지 않음
1. 작업 스케줄러 열기: `taskschd.msc`
2. "AI-Trends-Daily-Dashboard" 작업 찾기
3. 우클릭 → "실행" 클릭

### 네트워크 오류
스크립트가 인터넷 연결을 필요로 합니다. 방화벽 설정을 확인하세요.

## 🌐 뉴스 소스

- **Google News**: 전 세계 AI 뉴스
- **Hacker News**: 개발자 커뮤니티 뉴스
- **Product Hunt**: AI 제품과 도구
- **Reddit**: r/MachineLearning 커뮤니티 토론

## 📊 데이터 구조

`ai_trends_data.json`:
```json
{
  "timestamp": "2026-06-11T10:30:00",
  "items": [
    {
      "title": "뉴스 제목",
      "link": "https://...",
      "source": "Google News",
      "category": "Large Language Models",
      "date": "2026-06-11",
      "summary": "뉴스 요약..."
    }
  ]
}
```

## 🎨 커스터마이징

### 업데이트 시간 변경
`setup_scheduler.ps1`에서 다음 줄을 수정:
```powershell
$Trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM  # 9시로 변경
```

### 특정 뉴스 소스만 사용
`ai_trends_dashboard.py`에서 `run()` 메서드의 해당 줄을 주석 처리:
```python
# self.fetch_reddit()  # Reddit 비활성화
```

## 📝 라이선스

MIT License

## 💡 팁

- 대시보드는 HTML 파일이므로 인터넷 연결이 없어도 열 수 있습니다
- JSON 파일은 데이터 분석이나 다른 애플리케이션에 사용할 수 있습니다
- 매 실행마다 데이터가 덮어써집니다 (선택사항: 날짜별로 저장하도록 수정 가능)

## 🤝 기여

개선 사항이나 버그 리포트는 GitHub Issues에서 가능합니다.
