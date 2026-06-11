#!/usr/bin/env python3
"""AI Trends Daily Dashboard Generator"""

import requests
import feedparser
import json
import os
import logging
from datetime import datetime
from html import escape
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

class AITrendsDashboard:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.script_dir, 'ai_trends_data.json')
        self.html_file = os.path.join(self.script_dir, 'ai_dashboard.html')
        self.log_file = os.path.join(self.script_dir, 'ai_trends.log')
        self.news_items = []
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging to both file and console"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def fetch_google_news(self):
        """Fetch AI news from Google News"""
        try:
            url = 'https://news.google.com/rss/search?q=artificial+intelligence+OR+machine+learning+OR+AI&hl=en-US&gl=US&ceid=US:en'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)

            if not feed.entries:
                logging.warning("No entries found in Google News feed")
                return

            for entry in feed.entries[:15]:
                self.news_items.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'source': 'Google News',
                    'category': self._categorize(entry.get('title', '')),
                    'date': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200]
                })
        except requests.Timeout:
            logging.error("Timeout while fetching Google News")
        except requests.RequestException as e:
            logging.error(f"Network error fetching Google News: {e}")
        except Exception as e:
            logging.error(f"Unexpected error fetching Google News: {e}")

    def fetch_hacker_news(self):
        """Fetch AI-related stories from Hacker News using official API with parallel requests"""
        try:
            url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:30]

            if not story_ids:
                logging.warning("No stories found in Hacker News API")
                return

            def fetch_story(story_id):
                """Fetch individual story data"""
                try:
                    story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
                    story_response = requests.get(story_url, timeout=10)
                    story_response.raise_for_status()
                    return story_response.json()
                except Exception:
                    return None

            hn_count = len([x for x in self.news_items if x['source'] == 'Hacker News'])

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(fetch_story, sid): sid for sid in story_ids}

                for future in as_completed(futures):
                    if hn_count >= 10:
                        break

                    story = future.result()
                    if not story:
                        continue

                    title = story.get('title', '')
                    if any(keyword in title.lower() for keyword in ['ai', 'ml', 'llm', 'neural', 'gpt', 'claude']):
                        story_link = story.get('url', f"https://news.ycombinator.com/item?id={futures[future]}")
                        story_date = datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d')
                        self.news_items.append({
                            'title': title,
                            'link': story_link,
                            'source': 'Hacker News',
                            'category': self._categorize(title),
                            'date': story_date,
                            'summary': ''
                        })
                        hn_count += 1
        except requests.Timeout:
            logging.error("Timeout while fetching Hacker News")
        except requests.RequestException as e:
            logging.error(f"Network error fetching Hacker News: {e}")
        except Exception as e:
            logging.error(f"Unexpected error fetching Hacker News: {e}")

    def fetch_product_hunt(self):
        """Fetch AI products from Product Hunt"""
        try:
            url = 'https://www.producthunt.com/feed'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)

            if not feed.entries:
                logging.warning("No entries found in Product Hunt feed")
                return

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
        except requests.Timeout:
            logging.error("Timeout while fetching Product Hunt")
        except requests.RequestException as e:
            logging.error(f"Network error fetching Product Hunt: {e}")
        except Exception as e:
            logging.error(f"Unexpected error fetching Product Hunt: {e}")

    def fetch_reddit(self):
        """Fetch AI discussions from Reddit"""
        try:
            url = 'https://www.reddit.com/r/MachineLearning/new.json'
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; AITrendsDashboard/1.0)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            children = data.get('data', {}).get('children', [])
            if not children:
                logging.warning("No posts found in Reddit feed")
                return

            for post in children[:10]:
                post_data = post.get('data', {})
                self.news_items.append({
                    'title': post_data.get('title', ''),
                    'link': f"https://reddit.com{post_data.get('permalink', '')}",
                    'source': 'Reddit',
                    'category': self._categorize(post_data.get('title', '')),
                    'date': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d'),
                    'summary': post_data.get('selftext', '')[:200]
                })
        except requests.Timeout:
            logging.error("Timeout while fetching Reddit")
        except requests.RequestException as e:
            logging.error(f"Network error fetching Reddit: {e}")
        except Exception as e:
            logging.error(f"Unexpected error fetching Reddit: {e}")

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
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'items': self.news_items
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"Data saved: {len(self.news_items)} items")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

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
                    escaped_title = escape(item['title'])
                    escaped_summary = escape(item['summary']) if item['summary'] else ''
                    escaped_link = escape(item['link'])
                    escaped_source = escape(item['source'])
                    escaped_date = escape(item['date'])
                    html_content += f"""
                <div class="news-card">
                    <div class="news-card-header">
                        <span class="news-source">{escaped_source}</span>
                        <span class="news-date">{escaped_date}</span>
                    </div>
                    <h3 class="news-title">
                        <a href="{escaped_link}" target="_blank" rel="noopener noreferrer">
                            {escaped_title}
                        </a>
                    </h3>
                    {f'<p class="news-summary">{escaped_summary}</p>' if escaped_summary else ''}
                    <a href="{escaped_link}" class="news-link" target="_blank" rel="noopener noreferrer">
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

        try:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logging.info(f"HTML dashboard generated: {self.html_file}")
        except Exception as e:
            logging.error(f"Error generating HTML: {e}")

    def run(self):
        """Main execution"""
        logging.info("=" * 50)
        logging.info("Starting AI news collection")
        logging.info("=" * 50)

        self.fetch_google_news()
        google_count = len([x for x in self.news_items if x['source'] == 'Google News'])
        logging.info(f"Google News: {google_count} items")

        self.fetch_hacker_news()
        hn_count = len([x for x in self.news_items if x['source'] == 'Hacker News'])
        logging.info(f"Hacker News: {hn_count} items")

        self.fetch_product_hunt()
        ph_count = len([x for x in self.news_items if x['source'] == 'Product Hunt'])
        logging.info(f"Product Hunt: {ph_count} items")

        self.fetch_reddit()
        reddit_count = len([x for x in self.news_items if x['source'] == 'Reddit'])
        logging.info(f"Reddit: {reddit_count} items")

        if not self.news_items:
            logging.warning("No news items collected. Checking network connection and API status.")
            return

        # Remove duplicates by normalized title
        seen = set()
        unique_items = []
        for item in self.news_items:
            normalized_title = item['title'].lower().strip()
            if normalized_title not in seen:
                seen.add(normalized_title)
                unique_items.append(item)

        duplicates_removed = len(self.news_items) - len(unique_items)
        self.news_items = unique_items
        logging.info(f"Removed {duplicates_removed} duplicates. Total items: {len(self.news_items)}")

        self.save_data()
        self.generate_html()

        # Open in default browser (optional)
        try:
            import webbrowser
            webbrowser.open(f'file:///{self.html_file.replace(chr(92), "/")}')
            logging.info("Opened dashboard in default browser")
        except Exception as e:
            logging.debug(f"Failed to open browser: {e}")

        logging.info("Collection and dashboard generation completed successfully")
        logging.info("=" * 50)

if __name__ == '__main__':
    dashboard = AITrendsDashboard()
    dashboard.run()
