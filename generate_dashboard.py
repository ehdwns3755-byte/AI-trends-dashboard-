#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate AI Trends Dashboard HTML
하네스가 수집한 데이터를 시각적인 대시보드로 표현
"""

import json
from datetime import datetime
from agent_harness.tools.trend_collector import (
    fetch_hacker_news_trends,
    fetch_arxiv_trends,
    fetch_reddit_trends,
)


def generate_dashboard_html(hn_data, reddit_data, arxiv_data):
    """HTML 대시보드 생성"""

    html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trends Dashboard - Weekly Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 20px;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }

        /* Tabs */
        .tabs {
            display: flex;
            background: #f5f5f5;
            border-bottom: 2px solid #e0e0e0;
            padding: 0;
            margin: 0;
        }

        .tab-button {
            flex: 1;
            padding: 20px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
        }

        .tab-button.active {
            color: #667eea;
            border-bottom-color: #667eea;
            background: white;
        }

        .tab-button:hover {
            background: white;
            color: #667eea;
        }

        /* Tab Content */
        .content {
            padding: 40px;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Cards */
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }

        .card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            text-decoration: none;
            color: inherit;
            display: block;
        }

        a.card {
            color: inherit;
            text-decoration: none;
        }

        a.card:hover {
            text-decoration: none;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }

        .card:hover {
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            transform: translateY(-5px);
        }

        .card h3 {
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 10px;
            margin-top: 5px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .card p {
            color: #666;
            font-size: 0.9em;
            line-height: 1.6;
            margin-bottom: 15px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
            color: #999;
            padding-top: 15px;
            border-top: 1px solid #f0f0f0;
        }

        .badge {
            display: inline-block;
            background: #f0f0f0;
            color: #667eea;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }

        .points {
            color: #ff6b6b;
            font-weight: bold;
        }

        /* Category Stats */
        .category-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .category-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
        }

        .category-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .category-name {
            font-size: 1.1em;
            opacity: 0.9;
        }

        /* Footer */
        .footer {
            background: #f5f5f5;
            padding: 30px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }

        .footer-info {
            margin-bottom: 10px;
        }

        .footer-credit {
            font-size: 0.85em;
            color: #667eea;
            font-weight: 600;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state svg {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            opacity: 0.3;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }

            .stats {
                gap: 20px;
            }

            .stat-number {
                font-size: 2em;
            }

            .cards {
                grid-template-columns: 1fr;
            }

            .tabs {
                flex-wrap: wrap;
            }

            .tab-button {
                flex: 0 1 auto;
                padding: 15px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>AI Trends Dashboard</h1>
            <p>Latest AI/ML Trends and News</p>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">""" + str(len(hn_data)) + """</span>
                    <span class="stat-label">HN Stories</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">""" + str(len(reddit_data)) + """</span>
                    <span class="stat-label">Reddit Discussions</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">""" + str(len(hn_data) + len(reddit_data) + len(arxiv_data)) + """</span>
                    <span class="stat-label">Total Items</span>
                </div>
            </div>
        </div>

        <!-- Tabs -->
        <div class="tabs">
            <button class="tab-button active" onclick="showTab('hacker-news')">
                Hacker News (""" + str(len(hn_data)) + """)
            </button>
            <button class="tab-button" onclick="showTab('reddit')">
                Reddit (""" + str(len(reddit_data)) + """)
            </button>
            <button class="tab-button" onclick="showTab('arxiv')">
                arXiv (""" + str(len(arxiv_data)) + """)
            </button>
            <button class="tab-button" onclick="showTab('summary')">
                Summary
            </button>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- Hacker News Tab -->
            <div id="hacker-news" class="tab-content active">
                <div class="cards">
"""

    # Hacker News Cards
    for item in hn_data[:10]:
        url = item.get('url', '#')
        target = 'target="_blank"' if url != '#' else ''
        html += f"""
                    <a href="{url}" {target} class="card">
                        <h3>{item['title']}</h3>
                        <div class="card-footer">
                            <span class="points">{item['points']} pts</span>
                            <span class="badge">HN</span>
                        </div>
                    </a>
"""

    html += """
                </div>
            </div>

            <!-- Reddit Tab -->
            <div id="reddit" class="tab-content">
                <div class="cards">
"""

    # Reddit Cards
    for item in reddit_data[:10]:
        url = item.get('url', '#')
        target = 'target="_blank"' if url != '#' else ''
        html += f"""
                    <a href="{url}" {target} class="card">
                        <h3>{item['title']}</h3>
                        <p>r/{item['subreddit']}</p>
                        <div class="card-footer">
                            <span class="badge">Reddit</span>
                        </div>
                    </a>
"""

    html += """
                </div>
            </div>

            <!-- arXiv Tab -->
            <div id="arxiv" class="tab-content">
"""

    if arxiv_data:
        html += """
                <div class="cards">
"""
        for item in arxiv_data[:10]:
            url = item.get('url', '#')
            target = 'target="_blank"' if url != '#' else ''
            html += f"""
                    <a href="{url}" {target} class="card">
                        <h3>{item['title']}</h3>
                        <p>{item['authors'][:100]}...</p>
                        <div class="card-footer">
                            <span class="badge">Paper</span>
                        </div>
                    </a>
"""
        html += """
                </div>
"""
    else:
        html += """
                <div class="empty-state">
                    <p>No papers found today</p>
                </div>
"""

    html += """
            </div>

            <!-- Summary Tab -->
            <div id="summary" class="tab-content">
                <h2 style="margin-bottom: 30px; color: #667eea;">Weekly Summary</h2>

                <div class="category-stats">
                    <div class="category-card">
                        <div class="category-number">""" + str(len(hn_data)) + """</div>
                        <div class="category-name">Hacker News</div>
                    </div>
                    <div class="category-card">
                        <div class="category-number">""" + str(len(reddit_data)) + """</div>
                        <div class="category-name">Reddit</div>
                    </div>
                    <div class="category-card">
                        <div class="category-number">""" + str(len(arxiv_data)) + """</div>
                        <div class="category-name">arXiv</div>
                    </div>
                    <div class="category-card">
                        <div class="category-number">""" + str(len(hn_data) + len(reddit_data) + len(arxiv_data)) + """</div>
                        <div class="category-name">Total</div>
                    </div>
                </div>

                <div style="background: #f5f5f5; padding: 30px; border-radius: 12px; margin-top: 40px;">
                    <h3 style="color: #667eea; margin-bottom: 20px;">Report Details</h3>
                    <ul style="list-style: none; line-height: 2;">
                        <li><strong>Generated:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</li>
                        <li><strong>Data Sources:</strong> Hacker News, Reddit, arXiv</li>
                        <li><strong>Total Trends Analyzed:</strong> """ + str(len(hn_data) + len(reddit_data) + len(arxiv_data)) + """</li>
                        <li><strong>System:</strong> AI Trends Dashboard - Agent Harness</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-info">
                Generated by AI Trends Dashboard - Agent Harness System
            </div>
            <div class="footer-credit">
                Powered by Claude AI + Python Tools
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tabs
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // Remove active class from buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(button => {
                button.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');

            // Add active class to clicked button
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
"""

    return html


def main():
    """메인 실행"""
    print("Fetching data...")

    # 데이터 수집
    hn_result = fetch_hacker_news_trends(days=7)
    hn_data = json.loads(hn_result).get('trends', [])

    reddit_result = fetch_reddit_trends(days=7)
    reddit_data = json.loads(reddit_result).get('posts', [])

    arxiv_result = fetch_arxiv_trends(days=7)
    arxiv_data = json.loads(arxiv_result).get('papers', [])

    print(f"Collected: {len(hn_data)} HN + {len(reddit_data)} Reddit + {len(arxiv_data)} arXiv")

    # HTML 생성
    html = generate_dashboard_html(hn_data, reddit_data, arxiv_data)

    # 파일 저장
    output_path = "ai_trends_dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nDashboard created: {output_path}")
    print(f"Open in browser: file:///{output_path}")


if __name__ == "__main__":
    main()
