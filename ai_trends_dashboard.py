#!/usr/bin/env python3
"""AI Trends Daily Dashboard Generator"""

import requests
import feedparser
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class AITrendsDashboard:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.script_dir, 'ai_trends_data.json')
        self.html_file = os.path.join(self.script_dir, 'ai_dashboard.html')
        self.news_items = []

    def fetch_google_news(self):
        """Fetch AI news from Google News"""
        try:
            url = 'https://news.google.com/rss/search?q=artificial+intelligence+OR+machine+learning+OR+AI&hl=en-US&gl=US&ceid=US:en'
            feed = feedparser.parse(url)

            for entry in feed.entries[:15]:
                self.news_items.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'source': 'Google News',
                    'category': self._categorize(entry.get('title', '')),
                    'date': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200]
                })
        except Exception as e:
            print(f"Error fetching Google News: {e}")

    def fetch_hacker_news(self):
        """Fetch AI-related stories from Hacker News"""
        try:
            url = 'https://news.ycombinator.com/newest'
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            stories = soup.find_all('span', class_='titleline')[:10]
            for story in stories:
                link_elem = story.find('a')
                if link_elem:
                    title = link_elem.get_text()
                    if any(keyword in title.lower() for keyword in ['ai', 'ml', 'llm', 'neural', 'gpt', 'claude']):
                        self.news_items.append({
                            'title': title,
                            'link': link_elem.get('href', ''),
                            'source': 'Hacker News',
                            'category': self._categorize(title),
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'summary': ''
                        })
        except Exception as e:
            print(f"Error fetching Hacker News: {e}")

    def fetch_product_hunt(self):
        """Fetch AI products from Product Hunt"""
        try:
            url = 'https://www.producthunt.com/feed'
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:
                title = entry.get('title', '')
                if any(keyword in title.lower() for keyword in ['ai', 'gpt', 'llm', 'ml']):
                    self.news_items.append({
                        'title': title,
                        'link': entry.get('link', ''),
                        'source': 'Product Hunt',
                        'category': self._categorize(title),
                        'date': entry.get('published', ''),
                        'summary': entry.get('summary', '')[:200]
                    })
        except Exception as e:
            print(f"Error fetching Product Hunt: {e}")

    def fetch_reddit(self):
        """Fetch AI discussions from Reddit"""
        try:
            url = 'https://www.reddit.com/r/MachineLearning/new.json'
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            for post in data.get('data', {}).get('children', [])[:10]:
                post_data = post.get('data', {})
                self.news_items.append({
                    'title': post_data.get('title', ''),
                    'link': f"https://reddit.com{post_data.get('permalink', '')}",
                    'source': 'Reddit',
                    'category': self._categorize(post_data.get('title', '')),
                    'date': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d'),
                    'summary': post_data.get('selftext', '')[:200]
                })
        except Exception as e:
            print(f"Error fetching Reddit: {e}")

    def _categorize(self, text):
        """Categorize news based on keywords"""
        text = text.lower()
        if any(word in text for word in ['llm', 'gpt', 'transformer', 'language model', 'chatgpt', 'claude']):
            return 'Large Language Models'
        elif any(word in text for word in ['computer vision', 'image', 'video', 'neural network']):
            return 'Computer Vision'
        elif any(word in text for word in ['robot', 'automation', 'agent']):
            return 'Automation & Robotics'
        elif any(word in text for word in ['multimodal', 'vision']):
            return 'Multimodal AI'
        elif any(word in text for word in ['startup', 'funding', 'investment']):
            return 'AI Startups'
        else:
            return 'General AI'

    def save_data(self):
        """Save collected data to JSON"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'items': self.news_items
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def generate_html(self):
        """Generate HTML dashboard"""
        categories = {}
        for item in self.news_items:
            cat = item['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)

        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3600">
    <title>AI 동향 대시보드</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --accent-blue: #3b82f6;
            --accent-purple: #a855f7;
            --accent-green: #10b981;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid var(--accent-blue);
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .timestamp {{
            color: var(--text-secondary);
            font-size: 0.95em;
        }}

        .category-section {{
            margin-bottom: 40px;
        }}

        .category-title {{
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent-purple);
            color: var(--accent-purple);
        }}

        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}

        .news-card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}

        .news-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-blue);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
        }}

        .news-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}

        .news-source {{
            background: var(--accent-blue);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            white-space: nowrap;
        }}

        .news-date {{
            color: var(--text-secondary);
            font-size: 0.85em;
        }}

        .news-title {{
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 10px;
            line-height: 1.4;
        }}

        .news-title a {{
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.3s ease;
        }}

        .news-title a:hover {{
            color: var(--accent-blue);
        }}

        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.9em;
            margin-bottom: 15px;
            flex-grow: 1;
        }}

        .news-link {{
            display: inline-block;
            color: var(--accent-blue);
            text-decoration: none;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        .news-link:hover {{
            color: var(--accent-purple);
        }}

        .empty-state {{
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary);
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8em;
            }}

            .news-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI 동향 대시보드</h1>
            <p class="timestamp">마지막 업데이트: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}</p>
        </header>

        <main>
"""

        if not self.news_items:
            html_content += """
            <div class="empty-state">
                <p>현재 표시할 뉴스가 없습니다. 나중에 다시 시도해주세요.</p>
            </div>
"""
        else:
            for category in sorted(categories.keys()):
                items = categories[category]
                html_content += f"""
        <section class="category-section">
            <h2 class="category-title">{category}</h2>
            <div class="news-grid">
"""
                for item in items[:6]:
                    html_content += f"""
                <div class="news-card">
                    <div class="news-card-header">
                        <span class="news-source">{item['source']}</span>
                        <span class="news-date">{item['date']}</span>
                    </div>
                    <h3 class="news-title">
                        <a href="{item['link']}" target="_blank" rel="noopener noreferrer">
                            {item['title']}
                        </a>
                    </h3>
                    {f'<p class="news-summary">{item["summary"]}</p>' if item['summary'] else ''}
                    <a href="{item['link']}" class="news-link" target="_blank" rel="noopener noreferrer">
                        전체 보기 →
                    </a>
                </div>
"""
                html_content += """
            </div>
        </section>
"""

        html_content += """
        </main>

        <footer>
            <p>자동으로 매일 오전 8시에 업데이트됩니다.</p>
            <p style="margin-top: 10px; opacity: 0.7;">
                이 대시보드는 여러 뉴스 소스에서 AI 관련 기사를 수집합니다.
            </p>
        </footer>
    </div>
</body>
</html>
"""

        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def run(self):
        """Main execution"""
        print("🔍 AI 뉴스 수집 중...")
        self.fetch_google_news()
        print(f"  ✓ Google News: {len([x for x in self.news_items if x['source'] == 'Google News'])} items")

        self.fetch_hacker_news()
        print(f"  ✓ Hacker News: {len([x for x in self.news_items if x['source'] == 'Hacker News'])} items")

        self.fetch_product_hunt()
        print(f"  ✓ Product Hunt: {len([x for x in self.news_items if x['source'] == 'Product Hunt'])} items")

        self.fetch_reddit()
        print(f"  ✓ Reddit: {len([x for x in self.news_items if x['source'] == 'Reddit'])} items")

        # Remove duplicates by title
        seen = set()
        unique_items = []
        for item in self.news_items:
            if item['title'] not in seen:
                seen.add(item['title'])
                unique_items.append(item)
        self.news_items = unique_items

        print(f"\n📊 수집 완료: 총 {len(self.news_items)} 개 항목")

        self.save_data()
        print(f"💾 데이터 저장: {self.data_file}")

        self.generate_html()
        print(f"🎨 대시보드 생성: {self.html_file}")

        # Open in default browser (optional)
        try:
            import webbrowser
            webbrowser.open(f'file:///{self.html_file.replace(chr(92), "/")}')
            print("🌐 브라우저에서 열었습니다.")
        except Exception as e:
            print(f"  (브라우저 열기 실패: {e})")

        print("\n✅ 완료!")

if __name__ == '__main__':
    dashboard = AITrendsDashboard()
    dashboard.run()
