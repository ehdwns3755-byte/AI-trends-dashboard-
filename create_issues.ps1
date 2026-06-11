#!/usr/bin/env pwsh
<#
.SYNOPSIS
Create GitHub Issues from JSON file for AI Trends Dashboard project.

.DESCRIPTION
Reads ai_dashboard_issues.json and creates GitHub Issues with labels and milestones.

.EXAMPLE
$env:GITHUB_TOKEN = "ghp_xxxxx..."
./create_issues.ps1
#>

param(
    [string]$IssuesFile = "ai_dashboard_issues.json",
    [string]$Owner = "ehdwns3755-byte",
    [string]$Repo = "AI-"
)

# Validate token
$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Host "❌ Error: GITHUB_TOKEN environment variable not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "To set it:" -ForegroundColor Yellow
    Write-Host '$env:GITHUB_TOKEN = "ghp_xxxxx..."' -ForegroundColor Cyan
    exit 1
}

# Validate file
if (-not (Test-Path $IssuesFile)) {
    Write-Host "❌ Error: $IssuesFile not found" -ForegroundColor Red
    exit 1
}

# Read issues
try {
    $issues = Get-Content $IssuesFile | ConvertFrom-Json
    Write-Host "✅ Loaded $($issues.Count) issues from $IssuesFile" -ForegroundColor Green
} catch {
    Write-Host "❌ Error reading JSON: $_" -ForegroundColor Red
    exit 1
}

# Prepare API headers
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

$baseUrl = "https://api.github.com/repos/$Owner/$Repo"
$issuesUrl = "$baseUrl/issues"

Write-Host ""
Write-Host "🚀 Creating GitHub Issues..." -ForegroundColor Cyan
Write-Host "Repository: https://github.com/$Owner/$Repo" -ForegroundColor Cyan
Write-Host ""

$created = 0
$failed = 0
$issueUrls = @()

foreach ($issue in $issues) {
    try {
        $issueName = $issue.title
        Write-Host "[$($created + $failed + 1)/$($issues.Count)] Creating: $issueName... " -NoNewline -ForegroundColor Yellow

        # Build request body
        $body = @{
            title = $issue.title
            body = $issue.body
        }

        if ($issue.labels) {
            $body.labels = $issue.labels
        }

        if ($issue.milestone) {
            # Note: Milestone name will be converted to ID by the API or skip if doesn't exist
            $body.milestone = $issue.milestone
        }

        # Make API call
        $response = Invoke-WebRequest -Uri $issuesUrl `
            -Method POST `
            -Headers $headers `
            -Body ($body | ConvertTo-Json -Depth 10) `
            -UseBasicParsing

        $result = $response.Content | ConvertFrom-Json
        $issueNumber = $result.number
        $issueUrl = $result.html_url

        Write-Host "✅ #$issueNumber" -ForegroundColor Green
        $created++
        $issueUrls += $issueUrl

    } catch {
        Write-Host "❌ Failed" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ Created: $created / $($issues.Count)" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "❌ Failed: $failed" -ForegroundColor Red
}
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if ($created -gt 0) {
    Write-Host ""
    Write-Host "📝 Created Issues:" -ForegroundColor Cyan
    foreach ($url in $issueUrls) {
        Write-Host "  → $url" -ForegroundColor Cyan
    }

    Write-Host ""
    Write-Host "🔗 View all issues:" -ForegroundColor Cyan
    Write-Host "  → https://github.com/$Owner/$Repo/issues" -ForegroundColor Cyan
}

Write-Host ""
if ($failed -eq 0) {
    Write-Host "🎉 All issues created successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "⚠️  Some issues failed to create" -ForegroundColor Yellow
    exit 1
}
