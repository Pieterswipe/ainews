import feedparser
from datetime import datetime, timedelta, timezone

# All news sources with their RSS feed URLs
FEEDS = [
    {"name": "OpenAI Blog",           "url": "https://openai.com/blog/rss.xml"},
    {"name": "Google DeepMind",       "url": "https://deepmind.google/blog/rss.xml"},
    {"name": "Google AI Blog",        "url": "https://blog.google/technology/ai/rss/"},
    {"name": "Hugging Face",          "url": "https://huggingface.co/blog/feed.xml"},
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"},
    {"name": "MIT News AI",           "url": "https://news.mit.edu/topic/artificial-intelligence/feed"},
    {"name": "TechCrunch AI",         "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "MarkTechPost",          "url": "https://www.marktechpost.com/feed/"},
    {"name": "KDnuggets",             "url": "https://www.kdnuggets.com/feed"},
    {"name": "ML Mastery",            "url": "https://machinelearningmastery.com/feed/"},
    {"name": "Analytics Vidhya",      "url": "https://www.analyticsvidhya.com/feed/"},
]

def get_articles_last_week():
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    articles = []

    for feed_info in FEEDS:
        print(f"  Fetching: {feed_info['name']}...")
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries:
                # Try to get the publish date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

                # Only keep articles from the last 7 days
                if published and published >= one_week_ago:
                    articles.append({
                        "title":     entry.get("title", "No title"),
                        "link":      entry.get("link", ""),
                        "summary":   entry.get("summary", ""),
                        "published": published.strftime("%Y-%m-%d"),
                        "source":    feed_info["name"],
                    })
        except Exception as e:
            print(f"    Could not fetch {feed_info['name']}: {e}")

    print(f"\n  Total articles found: {len(articles)}")
    return articles
