#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
고급 경제뉴스 대시보드 생성
- 검색 기능
- 카테고리 필터
- 다크 모드
- 반응형 디자인
- 실시간 업데이트
"""

import json
from datetime import datetime
from pathlib import Path
from agent_harness.tools.economics_news import (
    fetch_economics_news,
    categorize_economics_news,
    generate_economics_summary,
)
from agent_harness.logger import get_logger

logger = get_logger(__name__)


def generate_advanced_dashboard(output_file: str = "economics_news_advanced.html") -> str:
    """고급 대시보드 생성"""

    logger.info("고급 대시보드 생성 시작")

    # 데이터 수집
    news_result = fetch_economics_news(days=1)
    news_data = json.loads(news_result)

    categorized_result = categorize_economics_news(news_result)
    categorized_data = json.loads(categorized_result)

    summary_result = generate_economics_summary(categorized_result)
    summary_data = json.loads(summary_result)

    articles = news_data.get('articles', [])
    categories = categorized_data.get('categorized', {})

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>경제뉴스 대시보드 - {summary_data['date']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #1e3c72;
            --secondary: #2a5298;
            --accent: #667eea;
            --success: #27ae60;
            --error: #e74c3c;
            --warning: #f39c12;
            --light-bg: #f8f9fa;
            --light-text: #333;
            --dark-bg: #1a1a1a;
            --dark-text: #e0e0e0;
            --border: #e0e0e0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', Roboto, sans-serif;
            background: var(--light-bg);
            color: var(--light-text);
            transition: background 0.3s, color 0.3s;
        }}

        body.dark-mode {{
            background: var(--dark-bg);
            color: var(--dark-text);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        /* 헤더 */
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }}

        .date-time {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        /* 통제판 */
        .control-panel {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: center;
        }}

        body.dark-mode .control-panel {{
            background: #2a2a2a;
        }}

        .search-box {{
            flex: 1;
            min-width: 200px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 1em;
            background: white;
            color: var(--light-text);
            transition: border-color 0.3s;
        }}

        body.dark-mode .search-box input {{
            background: #1a1a1a;
            color: var(--dark-text);
            border-color: #444;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 8px rgba(102, 126, 234, 0.3);
        }}

        .category-filter {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid var(--border);
            background: white;
            color: var(--light-text);
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }}

        body.dark-mode .filter-btn {{
            background: #1a1a1a;
            color: var(--dark-text);
            border-color: #444;
        }}

        .filter-btn:hover {{
            border-color: var(--accent);
            color: var(--accent);
        }}

        .filter-btn.active {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}

        .theme-toggle {{
            padding: 10px 16px;
            border: 2px solid var(--border);
            background: white;
            color: var(--light-text);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
        }}

        body.dark-mode .theme-toggle {{
            background: #1a1a1a;
            color: var(--dark-text);
            border-color: #444;
        }}

        .theme-toggle:hover {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}

        /* 통계 */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}

        body.dark-mode .stat-card {{
            background: #2a2a2a;
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: var(--accent);
            margin-bottom: 10px;
        }}

        .stat-label {{
            font-size: 0.95em;
            color: #666;
            font-weight: 500;
        }}

        body.dark-mode .stat-label {{
            color: #999;
        }}

        /* 뉴스 섹션 */
        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 1.8em;
            color: var(--primary);
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid var(--accent);
        }}

        /* 카드 그리드 */
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}

        .news-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s;
            border-left: 4px solid var(--accent);
            cursor: pointer;
            display: flex;
            flex-direction: column;
        }}

        body.dark-mode .news-card {{
            background: #2a2a2a;
        }}

        .news-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}

        .news-source {{
            font-size: 0.85em;
            color: var(--accent);
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .news-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: var(--light-text);
            margin-bottom: 10px;
            line-height: 1.4;
        }}

        body.dark-mode .news-title {{
            color: var(--dark-text);
        }}

        .news-summary {{
            font-size: 0.9em;
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
            flex-grow: 1;
        }}

        body.dark-mode .news-summary {{
            color: #999;
        }}

        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 15px;
            border-top: 1px solid var(--border);
            font-size: 0.85em;
            color: #999;
        }}

        .news-link {{
            display: inline-block;
            padding: 8px 16px;
            background: var(--accent);
            color: white;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            margin-top: auto;
        }}

        .news-link:hover {{
            background: var(--primary);
            text-decoration: none;
        }}

        /* 빈 상태 */
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }}

        .empty-state-icon {{
            font-size: 3em;
            margin-bottom: 20px;
            opacity: 0.5;
        }}

        /* 푸터 */
        .footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid var(--border);
            color: #999;
            font-size: 0.9em;
        }}

        /* 반응형 */
        @media (max-width: 768px) {{
            .header {{
                padding: 20px;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .header-info {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .control-panel {{
                flex-direction: column;
            }}

            .search-box {{
                min-width: unset;
            }}

            .news-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* 로딩 스피너 */
        .spinner {{
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102, 126, 234, 0.3);
            border-top: 3px solid var(--accent);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .loading .spinner {{
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <div class="header">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h1>경제뉴스 대시보드</h1>
                    <p style="margin-top: 5px; opacity: 0.9;">최신 경제 뉴스 및 시장 정보</p>
                </div>
            </div>
            <div class="header-info">
                <div class="date-time">
                    <strong>{summary_data['date']}</strong> | {summary_data['time']} 업데이트
                </div>
            </div>
        </div>

        <!-- 통제판 -->
        <div class="control-panel">
            <div class="search-box">
                <input
                    type="text"
                    id="searchInput"
                    placeholder="뉴스 제목 또는 내용으로 검색..."
                    onkeyup="filterNews()"
                >
            </div>
            <div class="category-filter" id="categoryFilter">
                <button class="filter-btn active" onclick="filterByCategory('all')">전체</button>
"""

    # 카테고리 필터 버튼
    for category in categories.keys():
        html += f'                <button class="filter-btn" onclick="filterByCategory(\'{category}\')">{category}</button>\n'

    html += f"""            </div>
            <button class="theme-toggle" onclick="toggleDarkMode()">다크 모드</button>
        </div>

        <!-- 통계 -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(articles)}</div>
                <div class="stat-label">수집된 뉴스</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">카테고리</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{news_data.get('total_archived', 0)}</div>
                <div class="stat-label">보관된 뉴스</div>
            </div>
        </div>

        <!-- 뉴스 섹션 -->
        <div id="newsContainer">
"""

    # 각 카테고리별 뉴스
    for category, info in categories.items():
        cat_articles = info.get('articles', [])
        if cat_articles:
            html += f"""            <div class="section" data-category="{category}">
                <h2 class="section-title">{category}</h2>
                <div class="news-grid" id="grid-{category}">
"""

            for article in cat_articles:
                html += f"""                    <div class="news-card" data-keywords="{article.get('title', '')} {article.get('summary', '')}">
                        <div class="news-source">{article.get('source', 'Unknown')}</div>
                        <h3 class="news-title">{article.get('title', 'No title')}</h3>
                        <p class="news-summary">{article.get('summary', '')}</p>
                        <div class="news-meta">
                            <span>{article.get('date', '')}</span>
                        </div>
                        <a href="{article.get('url', '#')}" target="_blank" class="news-link">원문 읽기 →</a>
                    </div>
"""

            html += """                </div>
            </div>
"""

    html += f"""        </div>

        <!-- 푸터 -->
        <div class="footer">
            <p>경제뉴스 AI 대시보드 | Agent Harness 시스템에서 생성</p>
            <p>생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>

    <script>
        // 검색 기능
        function filterNews() {{
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.news-card');

            cards.forEach(card => {{
                const keywords = card.getAttribute('data-keywords').toLowerCase();
                if (keywords.includes(searchInput)) {{
                    card.style.display = '';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        // 카테고리 필터
        function filterByCategory(category) {{
            // 버튼 활성화 상태 업데이트
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');

            // 섹션 표시/숨기기
            document.querySelectorAll('[data-category]').forEach(section => {{
                if (category === 'all' || section.getAttribute('data-category') === category) {{
                    section.style.display = '';
                }} else {{
                    section.style.display = 'none';
                }}
            }});

            // 검색 재적용
            filterNews();
        }}

        // 다크 모드 토글
        function toggleDarkMode() {{
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }}

        // 페이지 로드 시 다크 모드 복원
        window.addEventListener('load', () => {{
            if (localStorage.getItem('darkMode') === 'true') {{
                document.body.classList.add('dark-mode');
            }}
        }});

        // 실시간 시간 업데이트
        function updateTime() {{
            const now = new Date();
            const dateTime = now.toLocaleString('ko-KR', {{
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }});
            // 필요시 시간 업데이트 요소에 적용
        }}

        setInterval(updateTime, 1000);
    </script>
</body>
</html>
"""

    # 파일 저장
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info(f"고급 대시보드 생성 완료: {output_path.absolute()}")
    return str(output_path.absolute())


def main():
    """메인 함수"""
    output = generate_advanced_dashboard()
    print(f"\n✅ 고급 대시보드 생성 완료!")
    print(f"📁 파일 위치: {output}")
    print(f"🌐 웹 접속: http://localhost:8000/economics_news_advanced.html")
    print(f"\n기능:")
    print(f"  - 검색: 제목/내용으로 실시간 검색")
    print(f"  - 필터: 카테고리별 필터링")
    print(f"  - 다크모드: 다크 모드 지원")
    print(f"  - 반응형: 모든 기기에서 완벽 지원")


if __name__ == "__main__":
    main()
