# Code Audit and GitHub Issues Automation Skill

## Quick Start

This skill automates the entire workflow of code review → issue identification → GitHub Issues creation.

### Three-Phase Process

```
┌─────────────────────┐
│  1. Code Analysis   │  Read and analyze code
│     & Validation    │  Identify bugs/improvements
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  2. Issue           │  Format findings
│     Categorization  │  Assign severity
│     & Formatting    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  3. GitHub API      │  Create issues via REST API
│     Integration     │  Track issue numbers
└─────────────────────┘
```

## Files in This Skill

- **SKILL.md** — Complete skill definition (methodology, workflows, best practices)
- **README.md** — This file (quick reference)
- **example_issues.md** — Sample issue templates and real examples
- **github_api_reference.md** — API endpoint details and examples

## When Claude Uses This Skill

The main agent will automatically apply this skill when you ask to:

```
❌ "Find bugs in my code"
✅ "Find bugs in my code AND create GitHub Issues for each one"

❌ "Review my Python script"
✅ "Review my Python script, identify issues, and post them to GitHub"

❌ "What's wrong with this code?"
✅ "Analyze this code, create a priority list of issues, and register them as GitHub Issues"
```

## Key Features

### 1. **Comprehensive Code Analysis**
- Bugs: logic errors, type mismatches, missing edge cases
- Security: XSS, SQL injection, auth issues, credential handling
- Performance: inefficient loops, memory leaks, N+1 queries
- Maintainability: unclear code, poor naming, missing tests
- Observability: logging gaps, missing metrics

### 2. **Severity-Based Categorization**
- 🔴 **Critical**: Breaks functionality, security risk, data loss
- 🟡 **Medium**: Workaround exists, non-obvious issue, impacts performance
- 🟢 **Low**: Code style, minor efficiency, improvement only

### 3. **Automated GitHub Integration**
- Creates issues via REST API (no manual clicking)
- Includes title, description, labels, and severity
- Returns issue numbers for tracking
- Handles authentication securely (token-based)

## Usage Example

### Step 1: Ask Claude to Review & Create Issues

```
User: "I built an AI trends dashboard in Python. Can you review it, 
identify bugs and improvements, and create GitHub Issues for each finding?"

Claude applies this skill to:
  ✓ Analyze ai_trends_dashboard.py
  ✓ Find 8-10 issues (bugs, security, performance, improvements)
  ✓ Format each as a GitHub Issue
  ✓ POST to https://api.github.com/repos/.../issues
  ✓ Return issue numbers (#1, #2, #3, ...) for your repo
```

### Step 2: Issues Appear on GitHub

```
Your GitHub repository now has:
  Issue #1: XSS vulnerability in HTML generation (🔴 Critical)
  Issue #2: Missing error handling in API calls (🟡 Medium)
  Issue #3: Logging should use logging module, not print() (🟡 Medium)
  ...
```

### Step 3: Track Progress

```
As you fix issues, close them on GitHub.
The skill provides reference material to guide the fixes.
```

## Prerequisites

Before using this skill, ensure:

1. **GitHub Personal Access Token** (create at settings/tokens)
   ```bash
   # Store securely
   export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
   ```

2. **Repository Access**
   - Repository is public or you have write access
   - Token has `repo` scope (full control)

3. **Code to Review**
   - Python, JavaScript, TypeScript files (or any readable code)
   - Ideally, a complete project (not just snippets)

## API Authentication

This skill uses **GitHub REST API v3** with Personal Access Tokens:

```bash
# Create Token
1. Visit: https://github.com/settings/tokens/new
2. Scopes: Select "repo" (full control of private repositories)
3. Copy token (only shown once!)
4. Store in environment: export GITHUB_TOKEN="ghp_..."

# Use Token
Authorization: token ghp_xxxxxxxxxxxxxxxxxxxx
```

## Rate Limiting

GitHub API limits:
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour ← You'll use this

For 10-20 issues per review, you'll use ~20 API calls, well under the limit.

## Examples

### Example: Python Dashboard Review

**Input:**
```python
# ai_trends_dashboard.py (500 lines)
def generate_html(self):
    items = self.fetch_all()
    html = f"<div>{items}</div>"  # ❌ XSS vulnerability!
    return html
```

**Output:**

```markdown
## Issue #42: XSS Vulnerability

### Problem
generate_html() inserts user data directly into HTML without escaping.
Malicious news titles containing `<script>alert(1)</script>` will execute.

### Location
- File: ai_trends_dashboard.py
- Lines: 347-350
- Function: generate_html()

### Solution
Use html.escape() to sanitize output:
```python
from html import escape
html = f"<div>{escape(item)}</div>"
```

### Severity
🔴 Critical (Security)
```

## Troubleshooting

### Issue Creation Failed (401 Unauthorized)
**Problem**: Token invalid or expired
**Solution**: 
1. Regenerate token at https://github.com/settings/tokens
2. Update GITHUB_TOKEN environment variable
3. Verify token has `repo` scope

### Issue Creation Failed (403 Forbidden)
**Problem**: Token doesn't have write access to repo
**Solution**:
1. Check token scope includes "repo"
2. Verify you have write access to the repository
3. If public repo, ensure token is set correctly

### Rate Limited (429)
**Problem**: Too many API calls too quickly
**Solution**:
1. Wait ~60 seconds before retrying
2. The skill includes exponential backoff
3. Batch issues together to reduce calls

## Integration with Managed Agents

This skill is available for use in Claude Managed Agents:

```python
agent = client.beta.agents.create(
    name="Code Auditor",
    model="claude-opus-4-8",
    system="You are a code quality auditor...",
    skills=[
        {
            "type": "custom",
            "skill_id": "code-audit-and-github-issues",
            "version": "latest"
        }
    ]
)
```

When you start a session with this agent and ask it to review code, it will automatically:
1. Load this skill
2. Follow the methodology defined in SKILL.md
3. Apply best practices for issue identification
4. Create GitHub Issues via the REST API

## Next Steps

1. **Store Your Token**
   ```bash
   export GITHUB_TOKEN="your_token_here"
   ```

2. **Test with Your Repo**
   ```
   "Review my code and create GitHub Issues for any bugs or improvements."
   ```

3. **Monitor Issues on GitHub**
   - Check https://github.com/yourusername/yourrepo/issues
   - Review titles, descriptions, and severity labels

4. **Fix and Close**
   - Address each issue
   - Close on GitHub when complete
   - Use issue number in commit message: `Fix #42: XSS vulnerability`

## Related Documentation

- [SKILL.md](./SKILL.md) — Complete methodology and workflows
- [example_issues.md](./example_issues.md) — Real issue examples
- [github_api_reference.md](./github_api_reference.md) — API details

## Support

For issues with this skill:
1. Check the **Prerequisites** section above
2. Review **Troubleshooting** for common problems
3. Verify your GitHub token and repository access
4. Consult [GitHub REST API docs](https://docs.github.com/en/rest)

---

**Skill Version**: 1.0  
**Last Updated**: 2026-06-11  
**Status**: Production Ready
