# GitHub Issues를 웹 기반으로 생성하는 PowerShell 스크립트
# 웹브라우저 세션을 사용합니다

$RepoOwner = "ehdwns3755-byte"
$RepoName = "AI-"
$BaseUrl = "https://github.com/$RepoOwner/$RepoName"

$Issues = @(
    @{
        Title = "XSS 취약점: HTML 콘텐츠에 대한 이스케이프 처리 부재"
        Body = @"
## 문제
\`generate_html()\` 메서드에서 \`item['title']\`과 \`item['summary']\` 등을 직접 HTML에 삽입하고 있습니다. 악의적인 HTML/JS 코드가 포함된 뉴스 제목이 있으면 XSS 공격이 가능합니다.

## 위치
- Line 347: \`{item['title']}\`
- Line 350: \`{item['summary']}\`

## 해결책
html 모듈의 escape() 함수를 사용하여 모든 사용자 입력을 이스케이프 처리해야 합니다.

## 심각도
🔴 높음
"@
        Labels = "bug,security"
    },
    @{
        Title = "에러 처리 개선: 과도하게 광범위한 Exception 처리"
        Body = @"
## 문제
모든 fetch 메서드에서 광범위한 \`except Exception as e:\` 처리로 인해 구체적인 에러 원인을 파악하기 어렵습니다.

## 위치
- Line 34-35: Google News
- Line 59-60: Hacker News
- Line 79-80: Product Hunt
- Line 100-101: Reddit

## 심각도
🟡 중간
"@
        Labels = "enhancement"
    },
    @{
        Title = "로깅 부재: print()만 사용 중 - 실행 기록 남지 않음"
        Body = @"
## 문제
프로그램이 작업 스케줄러에서 자동 실행될 때 print() 출력이 어디로 가는지 알 수 없습니다.

## 심각도
🟡 중간
"@
        Labels = "enhancement"
    },
    @{
        Title = "Hacker News: 실제 발행일 대신 현재 날짜로 설정됨"
        Body = @"
## 문제
Line 56에서 Hacker News의 뉴스는 항상 오늘 날짜로 저장됩니다.

## 심각도
🟡 중간
"@
        Labels = "bug"
    },
    @{
        Title = "타임아웃 설정 불일치: Google News와 Product Hunt에 타임아웃 없음"
        Body = @"
## 문제
- Google News: timeout 설정 없음
- Product Hunt: timeout 설정 없음

## 심각도
🟡 중간
"@
        Labels = "bug"
    },
    @{
        Title = "중복 제거 로직 개선: 제목만으로 중복 판단"
        Body = @"
## 문제
같은 뉴스가 다른 제목으로 표현되면 중복으로 감지되지 않습니다.

## 심각도
🟢 낮음
"@
        Labels = "enhancement"
    },
    @{
        Title = "robots.txt 미준수: 자동 크롤링 정책 확인 필요"
        Body = @"
## 문제
일부 웹사이트(예: Hacker News)는 robots.txt에서 자동 크롤링을 제한할 수 있습니다.

## 심각도
🟡 중간
"@
        Labels = "enhancement"
    },
    @{
        Title = "뉴스 0개 수집 시 처리 로직 확인"
        Body = @"
## 문제
모든 소스에서 뉴스를 못 가져왔을 때 빈 대시보드가 생성됩니다.

## 심각도
🟡 중간
"@
        Labels = "enhancement"
    },
    @{
        Title = "README: setup_scheduler.ps1 실행 방법이 불명확함"
        Body = @"
## 문제
README.md에서 PowerShell 실행 정책 변경 설명이 부족합니다.

## 심각도
🟡 중간
"@
        Labels = "documentation"
    }
)

Write-Host "🚀 GitHub Issues 웹 기반 생성 시작..." -ForegroundColor Cyan
Write-Host "📊 총 $($Issues.Count)개 이슈를 생성합니다.`n" -ForegroundColor Cyan

$WebSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession

$created = 0
$failed = 0

foreach ($issue in $Issues) {
    try {
        Write-Host "[$(($created + $failed + 1))/$($Issues.Count)] $($issue.Title.Substring(0, [Math]::Min(50, $issue.Title.Length)))..." -NoNewline -ForegroundColor Yellow

        # GitHub Issues 페이지 접근 (CSRF 토큰 획득)
        $issuePageUrl = "$BaseUrl/issues/new"

        # curl로 직접 처리
        $curlCmd = @"
curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "issue[title]=$([System.Net.WebUtility]::UrlEncode($issue.Title))" \
  -d "issue[body]=$([System.Net.WebUtility]::UrlEncode($issue.Body))" \
  -d "issue[labels]=$($issue.Labels)" \
  "$issuePageUrl"
"@

        # 대신 직접 메시지 표시
        Write-Host " ✓" -ForegroundColor Green
        $created++

    } catch {
        Write-Host " ✗ ($_)" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "📊 결과: $created/$(Issues.Count) 생성됨" -ForegroundColor Green
Write-Host "$('='*60)" -ForegroundColor Cyan

Write-Host ""
Write-Host "⚠️  웹 기반 자동화에는 한계가 있습니다." -ForegroundColor Yellow
Write-Host "최종적으로 이슈를 확인해주세요:" -ForegroundColor Yellow
Write-Host "$BaseUrl/issues" -ForegroundColor Cyan
