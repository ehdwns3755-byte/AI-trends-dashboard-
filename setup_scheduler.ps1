# Windows Task Scheduler Setup for AI Trends Dashboard
# 관리자 권한으로 실행 필요: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# ========================================
# 환경 변수 설정 (이식성을 위해)
# ========================================

# 프로젝트 루트 디렉토리 (현재 스크립트 위치 기반)
$ProjectRoot = Split-Path -Parent (Get-Item $PSCommandPath).FullName
if (-not (Test-Path (Join-Path $ProjectRoot "ai_trends_dashboard.py"))) {
    Write-Host "❌ 프로젝트 루트를 찾을 수 없습니다." -ForegroundColor Red
    Write-Host "   이 스크립트는 ai_trends_dashboard.py와 같은 디렉토리에 있어야 합니다." -ForegroundColor Red
    exit 1
}

$ScriptPath = Join-Path $ProjectRoot "ai_trends_dashboard.py"
$LogPath = Join-Path $ProjectRoot "logs"
$TaskName = "AI-Trends-Daily-Dashboard"
$TaskDescription = "매일 오전 8시에 AI 동향 대시보드를 업데이트합니다"

# 로그 디렉토리 생성
if (-not (Test-Path $LogPath)) {
    New-Item -ItemType Directory -Path $LogPath -Force | Out-Null
    Write-Host "✓ 로그 디렉토리 생성: $LogPath" -ForegroundColor Green
}

# Python 경로 찾기
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PythonPath) {
    $PythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
}

if (-not $PythonPath) {
    Write-Host "❌ Python을 찾을 수 없습니다. Python이 설치되어 있고 PATH에 추가되어 있는지 확인하세요." -ForegroundColor Red
    exit 1
}

Write-Host "✓ 프로젝트 경로: $ProjectRoot" -ForegroundColor Green
Write-Host "✓ Python 경로: $PythonPath" -ForegroundColor Green
Write-Host "✓ 스크립트 경로: $ScriptPath" -ForegroundColor Green
Write-Host "✓ 로그 디렉토리: $LogPath" -ForegroundColor Green
Write-Host ""

# 기존 작업이 있으면 삭제
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Write-Host "기존 작업을 삭제합니다..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# 새 작업 생성
# 로그 파일: logs/ai_trends_YYYY-MM-DD.log
$LogFile = Join-Path $LogPath "ai_trends_$(Get-Date -Format 'yyyy-MM-dd').log"
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

$Task = Register-ScheduledTask -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description $TaskDescription `
    -User $env:USERNAME `
    -RunLevel Highest

if ($Task) {
    Write-Host "✅ 작업이 성공적으로 등록되었습니다!" -ForegroundColor Green
    Write-Host "   작업명: $TaskName" -ForegroundColor Cyan
    Write-Host "   실행 시간: 매일 오전 8:00" -ForegroundColor Cyan
    Write-Host "   스크립트: $ScriptPath" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor Yellow
    Write-Host "💡 팁: 작업 스케줄러에서 직접 확인할 수 있습니다." -ForegroundColor Yellow
    Write-Host "   명령: taskschd.msc" -ForegroundColor Cyan
} else {
    Write-Host "❌ 작업 등록에 실패했습니다." -ForegroundColor Red
    exit 1
}

# 수동으로 테스트하기
Write-Host "" -ForegroundColor Yellow
Write-Host "📝 작업을 수동으로 테스트하려면 다음 명령을 실행하세요:" -ForegroundColor Yellow
Write-Host "   Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Cyan

Write-Host "" -ForegroundColor Yellow
Write-Host "📋 로그 파일 위치:" -ForegroundColor Yellow
Write-Host "   $LogPath" -ForegroundColor Cyan

Write-Host "" -ForegroundColor Yellow
Write-Host "❌ 작업을 제거하려면 다음을 실행하세요:" -ForegroundColor Yellow
Write-Host "   Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:\$false" -ForegroundColor Cyan
