# GitHub REST API Reference

Quick reference for GitHub REST API v3 operations used in this skill.

## Authentication

### Personal Access Token (Recommended)

**Create Token:**
1. Visit: https://github.com/settings/tokens/new
2. Scopes: Select `repo` (full control of private repositories)
3. Copy token (only shown once!)

**Use Token:**
```bash
# Set environment variable
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Use in curl
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/{owner}/{repo}/issues

# Use in Python
headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"}
```

## Core Operations

### 1. Get Repository Info

**Endpoint:**
```
GET /repos/{owner}/{repo}
```

**Example:**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/ehdwns3755-byte/AI-
```

**Response (partial):**
```json
{
  "id": 123456789,
  "name": "AI-",
  "full_name": "ehdwns3755-byte/AI-",
  "owner": {
    "login": "ehdwns3755-byte",
    "type": "User"
  },
  "private": false,
  "description": "AI Trends Dashboard",
  "url": "https://api.github.com/repos/ehdwns3755-byte/AI-",
  "html_url": "https://github.com/ehdwns3755-byte/AI-"
}
```

**Use case:** Verify repository exists and you have access

---

### 2. Create an Issue

**Endpoint:**
```
POST /repos/{owner}/{repo}/issues
```

**Request Headers:**
```
Authorization: token {GITHUB_TOKEN}
Accept: application/vnd.github.v3+json
Content-Type: application/json
```

**Request Body (Minimal):**
```json
{
  "title": "XSS 취약점: HTML 콘텐츠에 대한 이스케이프 처리 부재",
  "body": "## 문제\n\n`generate_html()` 메서드에서...",
  "labels": ["bug", "security"]
}
```

**Request Body (Full):**
```json
{
  "title": "Error message here",
  "body": "Detailed description with markdown formatting",
  "labels": ["bug", "enhancement", "documentation"],
  "assignees": ["username1", "username2"],
  "milestone": 1,
  "state": "open"
}
```

**Python Example:**
```python
import requests
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = "ehdwns3755-byte"
REPO_NAME = "AI-"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

issue_data = {
    "title": "XSS Vulnerability in generate_html()",
    "body": """## Problem
The generate_html() method inserts user data without escaping.

## Solution
Use html.escape() to sanitize output.""",
    "labels": ["bug", "security"]
}

response = requests.post(API_URL, json=issue_data, headers=headers)

if response.status_code == 201:
    issue = response.json()
    print(f"✓ Issue created: #{issue['number']}")
    print(f"  URL: {issue['html_url']}")
else:
    print(f"✗ Error: {response.status_code}")
    print(response.json())
```

**Response:**
```json
{
  "url": "https://api.github.com/repos/ehdwns3755-byte/AI-/issues/42",
  "id": 1234567890,
  "number": 42,
  "title": "XSS Vulnerability in generate_html()",
  "body": "## Problem\nThe generate_html() method...",
  "state": "open",
  "labels": [
    {
      "name": "bug",
      "color": "d73a4a"
    },
    {
      "name": "security",
      "color": "ff4444"
    }
  ],
  "created_at": "2026-06-11T08:30:00Z",
  "updated_at": "2026-06-11T08:30:00Z",
  "html_url": "https://github.com/ehdwns3755-byte/AI-/issues/42"
}
```

---

### 3. Get Existing Labels

**Endpoint:**
```
GET /repos/{owner}/{repo}/labels
```

**Example:**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/ehdwns3755-byte/AI-/labels
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "bug",
    "color": "d73a4a",
    "description": "Something isn't working"
  },
  {
    "id": 2,
    "name": "enhancement",
    "color": "a2eeef",
    "description": "New feature or request"
  },
  {
    "id": 3,
    "name": "documentation",
    "color": "0075ca",
    "description": "Improvements or additions to documentation"
  }
]
```

**Use case:** See what labels are available before creating issues

---

### 4. List Issues

**Endpoint:**
```
GET /repos/{owner}/{repo}/issues
```

**Query Parameters:**
```
state: open|closed|all (default: open)
labels: comma-separated list (e.g., "bug,enhancement")
sort: created|updated|comments (default: created)
direction: asc|desc (default: desc)
per_page: 1-100 (default: 30)
page: pagination (default: 1)
```

**Example:**
```bash
# Get all open issues
curl -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/repos/ehdwns3755-byte/AI-/issues"

# Get only bug issues
curl -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/repos/ehdwns3755-byte/AI-/issues?labels=bug"

# Get closed issues, sorted by update time
curl -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/repos/ehdwns3755-byte/AI-/issues?state=closed&sort=updated"
```

**Use case:** Check if an issue already exists before creating a duplicate

---

### 5. Update an Issue

**Endpoint:**
```
PATCH /repos/{owner}/{repo}/issues/{issue_number}
```

**Request Body:**
```json
{
  "title": "New title",
  "body": "Updated body",
  "state": "closed",
  "labels": ["bug", "fixed"],
  "assignees": ["username"]
}
```

**Python Example:**
```python
issue_number = 42
update_url = f"{API_URL}/{issue_number}"

update_data = {
    "state": "closed",
    "labels": ["bug", "fixed"]
}

response = requests.patch(update_url, json=update_data, headers=headers)
print(f"✓ Issue #{issue_number} updated")
```

**Use case:** Close issues when fixes are completed

---

## Error Handling

### Common HTTP Status Codes

| Status | Meaning | Cause |
|--------|---------|-------|
| 201 | Created | Issue created successfully |
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Invalid/missing token |
| 403 | Forbidden | No permission for repo |
| 404 | Not Found | Repo doesn't exist |
| 422 | Unprocessable Entity | Validation failed (e.g., invalid label) |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | GitHub server error (retry later) |

### Rate Limiting

**Headers in Response:**
```
X-RateLimit-Limit: 5000          # Max requests per hour
X-RateLimit-Remaining: 4999      # Remaining in current hour
X-RateLimit-Reset: 1686466200    # Unix timestamp when limit resets
```

**Handling 429 (Rate Limited):**
```python
import time

response = requests.post(API_URL, json=issue_data, headers=headers)

if response.status_code == 429:
    reset_time = int(response.headers['X-RateLimit-Reset'])
    sleep_seconds = reset_time - time.time() + 1
    
    if sleep_seconds > 0:
        print(f"Rate limited. Waiting {sleep_seconds} seconds...")
        time.sleep(sleep_seconds)
        # Retry the request
        response = requests.post(API_URL, json=issue_data, headers=headers)
```

---

## Batch Operations

### Create Multiple Issues

**Recommended approach:**

```python
def create_issues_batch(issues_list):
    results = []
    
    for i, issue in enumerate(issues_list, 1):
        print(f"[{i}/{len(issues_list)}] Creating issue: {issue['title'][:50]}...")
        
        try:
            response = requests.post(
                API_URL,
                json=issue,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                issue_num = response.json()['number']
                print(f"  ✓ Created #{issue_num}")
                results.append({'status': 'success', 'number': issue_num})
            else:
                print(f"  ✗ Failed: {response.status_code}")
                results.append({'status': 'failed', 'code': response.status_code})
                
        except requests.Timeout:
            print(f"  ✗ Timeout")
            results.append({'status': 'timeout'})
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append({'status': 'error', 'message': str(e)})
    
    return results

# Usage
issues = [
    {"title": "Issue 1", "body": "...", "labels": ["bug"]},
    {"title": "Issue 2", "body": "...", "labels": ["enhancement"]},
    # ... more issues
]

results = create_issues_batch(issues)
print(f"\n✓ {sum(1 for r in results if r['status']=='success')}/{len(issues)} created")
```

---

## Complete Example Script

```python
#!/usr/bin/env python3
"""
GitHub Issues Creation Script
Usage: python create_issues.py <repo_owner> <repo_name>
"""

import requests
import json
import os
import sys
from typing import List, Dict

class GitHubIssueCreator:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo
        self.token = os.getenv('GITHUB_TOKEN')
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        
        self.api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict:
        """Create a single issue."""
        
        payload = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            headers=self.headers,
            timeout=10
        )
        
        if response.status_code == 201:
            return {
                'success': True,
                'number': response.json()['number'],
                'url': response.json()['html_url']
            }
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.json().get('message', 'Unknown error')
            }
    
    def create_issues_batch(self, issues: List[Dict]) -> List[Dict]:
        """Create multiple issues."""
        
        results = []
        
        for i, issue in enumerate(issues, 1):
            print(f"[{i}/{len(issues)}] {issue['title'][:50]}...", end=" ")
            
            result = self.create_issue(
                title=issue['title'],
                body=issue['body'],
                labels=issue.get('labels', [])
            )
            
            if result['success']:
                print(f"✓ #{result['number']}")
            else:
                print(f"✗ {result['status_code']}")
            
            results.append(result)
        
        return results

if __name__ == "__main__":
    creator = GitHubIssueCreator("ehdwns3755-byte", "AI-")
    
    issues = [
        {
            "title": "XSS Vulnerability",
            "body": "HTML content needs escaping",
            "labels": ["bug", "security"]
        },
        {
            "title": "Missing Error Handling",
            "body": "Exceptions are too broad",
            "labels": ["enhancement"]
        }
    ]
    
    results = creator.create_issues_batch(issues)
    
    successful = sum(1 for r in results if r['success'])
    print(f"\n✓ {successful}/{len(issues)} issues created successfully")
```

---

## Useful Links

- **GitHub API Docs**: https://docs.github.com/en/rest
- **Issues API Reference**: https://docs.github.com/en/rest/issues
- **Personal Access Tokens**: https://github.com/settings/tokens
- **Rate Limiting**: https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api

---

**Version**: 1.0  
**Last Updated**: 2026-06-11
