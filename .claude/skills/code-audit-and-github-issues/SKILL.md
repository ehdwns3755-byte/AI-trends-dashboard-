---
name: code-audit-and-github-issues
description: Comprehensive code review, bug detection, and automated GitHub Issues creation workflow
---

# Code Audit and GitHub Issues Automation Skill

## 📋 Purpose

This skill provides a structured methodology for conducting code reviews, identifying bugs and improvements, and automatically creating GitHub Issues to track findings. It's designed for continuous code quality management and systematic issue documentation.

## 🎯 When to Use

Use this skill when you need to:
- **Review Python, TypeScript, or JavaScript code** for quality, security, and performance issues
- **Analyze generated outputs** (HTML, dashboards, reports) for correctness
- **Identify bugs and improvements** in existing codebases
- **Automate GitHub Issues creation** from identified problems
- **Document findings** in a structured, actionable format
- **Maintain code quality standards** across projects

## 🔄 Complete Workflow

### Phase 1: Code Analysis & Validation
```
1. Understand the Codebase
   ├─ Read and analyze source files
   ├─ Understand purpose and architecture
   └─ Review recent commits and documentation

2. Identify Issues
   ├─ Check for bugs (logic errors, type mismatches, edge cases)
   ├─ Find security vulnerabilities (XSS, SQL injection, auth issues)
   ├─ Detect performance bottlenecks (inefficient loops, memory leaks)
   ├─ Review error handling (missing cases, overly broad catches)
   ├─ Assess logging and observability
   └─ Evaluate code maintainability and test coverage
```

### Phase 2: Issue Categorization
```
3. Classify Each Finding
   ├─ Severity: 🔴 Critical | 🟡 Medium | 🟢 Low
   ├─ Type: bug | enhancement | documentation | security
   ├─ Impact: What breaks if not fixed?
   └─ Effort: How hard to fix?

4. Format as GitHub Issues
   ├─ Clear title (what's wrong)
   ├─ Problem description (why it matters)
   ├─ Location (file path + line numbers)
   ├─ Solution approach (how to fix)
   └─ Acceptance criteria
```

### Phase 3: Automated GitHub Integration
```
5. Create GitHub Issues via REST API
   ├─ Use Personal Access Token for authentication
   ├─ POST to /repos/{owner}/{repo}/issues
   ├─ Include title, body, labels, and severity
   └─ Return issue numbers for tracking

6. Track and Update
   ├─ Store issue IDs for future reference
   ├─ Link issues to commits (if applicable)
   ├─ Set milestone or assignee as needed
   └─ Update status as fixes are completed
```

## 🛠️ Implementation Details

### Prerequisites
- **GitHub Personal Access Token** (repo scope minimum)
- **Repository URL** or (owner, repo) tuple
- **Code files to review** (local path or inline content)
- **Authentication method**: Web-based token or API key

### Tools & Technologies
```
Code Analysis:
  ├─ Manual code reading (understanding intent, architecture)
  ├─ Pattern matching (known vulnerabilities, anti-patterns)
  └─ Static analysis heuristics (unused vars, unreachable code)

Issue Tracking:
  ├─ GitHub REST API v3
  ├─ Issue schema: {title, body, labels, assignees}
  └─ Authentication: Personal Access Token (ghp_...)

Automation:
  ├─ Python: requests library + GitHub API
  ├─ JavaScript: fetch() or axios
  └─ Direct curl/HTTP calls to REST API
```

### Authentication Flow
```
1. Generate Token
   ├─ GitHub Settings → Developer settings → Personal access tokens
   ├─ Scopes: repo (full control of private repositories)
   └─ Keep token secure (environment variables or .env)

2. Verify Access
   ├─ Test API call: GET /repos/{owner}/{repo}
   ├─ Confirm token has repo scope
   └─ Ensure user has write access to repo

3. Create Issues
   ├─ POST /repos/{owner}/{repo}/issues
   ├─ Include headers: Authorization: token <TOKEN>
   └─ Return response contains issue #number
```

## 📊 Issue Template

### Minimal Structure (Required Fields)
```markdown
## Problem
[1-2 sentences describing what's wrong]

## Location
- File: path/to/file.py
- Line: 123-145
- Function/Method: function_name()

## Impact
- What breaks if not fixed?
- Who is affected?
- Severity: Critical / Medium / Low

## Solution Approach
- Recommended fix
- Alternative approaches (if multiple)
- Estimated effort: 1 hour / half day / full day
```

### Enhanced Structure (Full Details)
```markdown
## Problem Description
[Detailed explanation of the issue]

## Root Cause
[Why does this happen?]

## Location & Context
- File: path/to/file.py (lines 123-145)
- Current code snippet (3-5 lines)
- Related code references

## Proposed Solution
```python
# Before
old_code()

# After
new_code()
```

## Testing Strategy
- How to verify the fix works?
- Edge cases to test
- Regression tests needed

## References
- Related issues #123, #456
- Documentation links
- External resources
```

## 🔐 Security Checklist

Before running this workflow:

- [ ] **Token Security**
  - Token stored in environment variable (not in code)
  - Token has minimal required scopes (repo only)
  - Token will be rotated regularly
  - Token is not hardcoded in scripts

- [ ] **Data Privacy**
  - Code being analyzed is approved for analysis
  - No sensitive data (API keys, credentials) in files
  - Analysis results only shared with authorized team
  - GitHub Issues are in private repo if sensitive

- [ ] **API Usage**
  - Rate limits understood (60 req/hour unauthenticated, 5000 authenticated)
  - Batch operations are rate-limit-aware
  - Error handling includes 429 (rate limit) responses
  - Retries use exponential backoff

## 💡 Best Practices

### For Effective Code Reviews
1. **Read the whole file first** — understand context before flagging issues
2. **Look for patterns** — if bug exists once, check for same bug elsewhere
3. **Consider intent** — code that looks wrong might be intentional
4. **Check comments** — explanations often reveal edge-case handling
5. **Review tests** — test code reveals intended behavior and edge cases

### For Accurate Issue Reporting
1. **Be specific** — "XSS vulnerability in line 347" not "security issue somewhere"
2. **Provide examples** — show broken input, expected vs actual output
3. **Suggest solutions** — don't just report problems
4. **Link context** — reference related code, commits, or issues
5. **Update as you learn** — if analysis reveals more issues, add them

### For GitHub Integration
1. **Batch issues** — group related findings under one issue if they share a fix
2. **Use labels** — `bug`, `enhancement`, `documentation`, `security`
3. **Assign severity** — let issue-management automation handle prioritization
4. **Close duplicates** — check for existing issues before creating new ones
5. **Link pull requests** — when fixing, reference issue in PR description

## 🚀 Example Workflow

### Step 1: Code Review
```
Input: Python file (ai_trends_dashboard.py)
Process: Static analysis + pattern matching
Output: List of issues with severity and line numbers
```

### Step 2: Issue Creation
```
Input: Issues list + GitHub credentials
Process: Format each issue, call GitHub API
Output: Issue numbers (#1, #2, #3, ...) for tracking
```

### Step 3: Progress Tracking
```
Input: Repo + issue numbers
Process: Monitor issue status as fixes land
Output: Completion report (X/Y issues resolved)
```

## 📝 Integration Points

### With Continuous Integration
- Trigger code audit on every PR (pre-merge validation)
- Auto-create issues for potential regressions
- Block merge if critical issues found

### With Issue Management
- Link GitHub Issues to project management tools
- Set milestones based on severity
- Auto-assign to code owners
- Route to relevant team members

### With Development Workflow
- Include audit results in code review checklist
- Require issue-fix PRs to reference original issue
- Track metrics: avg time to fix, severity distribution
- Archive closed issues for metrics analysis

## ⚙️ Configuration

### Environment Variables (Recommended)
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"  # Your PAT
export GITHUB_OWNER="your-org"                   # Repository owner
export GITHUB_REPO="your-repo"                   # Repository name
export ANALYSIS_SEVERITY_THRESHOLD="medium"      # Report threshold
```

### API Endpoints
```
Base URL: https://api.github.com
Issues: POST /repos/{owner}/{repo}/issues
Repo Info: GET /repos/{owner}/{repo}
Rate Limit: GET /rate_limit
```

### Rate Limiting
- **Unauthenticated**: 60 requests per hour per IP
- **Authenticated**: 5,000 requests per hour per user
- **Retry-After header**: Indicates seconds to wait when rate-limited
- **Best practice**: Batch operations, use exponential backoff

## 🔗 Related Skills

- **Code Refactoring**: Large-scale code improvements
- **Test Writing**: Comprehensive test suite creation
- **Documentation**: API docs, architecture guides
- **Security Auditing**: Deep vulnerability assessment

## 📚 References

- [GitHub REST API - Issues](https://docs.github.com/en/rest/issues)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) (for security checks)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
