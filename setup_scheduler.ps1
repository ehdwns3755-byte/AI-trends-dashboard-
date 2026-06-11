# Windows Task Scheduler Setup for AI Trends Dashboard
# 관리자 권한으로 실행 필요: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

$ScriptPath = "C:\Users\Admin\Desktop\AI\ai_trends_dashboard.py"
$TaskName = "AI-Trends-Daily-Dashboard"
$TaskDescription = "매일 오전 8시에 AI 동향 대시보드를 업데이트합니다"

# Python 경로 찾기
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PythonPath) {
    $PythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
}

if (-not $PythonPath) {
    Write-Host "❌ Python을 찾을 수 없습니다. Python이 설치되어 있고 PATH에 추가되어 있는지 확인하세요." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python 경로: $PythonPath" -ForegroundColor Green

# 기존 작업이 있으면 삭제
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Write-Host "기존 작업을 삭제합니다..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# 새 작업 생성
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory "C:\Users\Admin\Desktop\AI"
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
