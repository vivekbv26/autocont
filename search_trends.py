# Add this line at the beginning of your notebook or before importing newspaper
#!pip install lxml_html_clean
# The rest of your code follows
import requests
import re
import random
from datetime import datetime, timedelta, timezone
from newspaper import Article

# ─── CONFIGURATION ───────────────────────────────────────────────
NEWSAPI_KEY = "237aff498fb34f5dae680055da54fdb8"  # Replace with your actual NewsAPI key
API_URL = "https://newsapi.org/v2/everything"

# ─── THEMATIC KEYWORDS ───────────────────────────────────────────
KEYWORDS = [
    "sexual intercoarse", "cybercrime", "conspiracy", "unsolved mystery", "cult",
    "espionage", "paranormal", "forbidden", "secret society", "ritual",
    "black market", "scandal", "hidden truth", "classified", "covert operation",
    "did you know", "bizarre", "unbelievable", "shocking", "unexplained"
]

# ─── FUNCTION TO FETCH AND DISPLAY ARTICLES ──────────────────────
def fetch_full_articles(api_key, keywords, num_articles=3):
    to_date = datetime.now(timezone.utc)
    from_date = to_date - timedelta(days=7)

    for keyword in keywords:
        print(f"\nFetching articles for keyword: {keyword}")
        params = {
            "q": keyword,
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": num_articles,
            "apiKey": api_key
        }

        response = requests.get(API_URL, params=params)
        data = response.json()

        if data.get("status") == "ok" and data.get("articles"):
            for article_meta in data["articles"]:
                url = article_meta.get("url")
                if url:
                    try:
                        article = Article(url)
                        article.download()
                        article.parse()
                        print(f"\nTitle: {article.title}")
                        print(f"Source: {article_meta.get('source', {}).get('name', 'N/A')}")
                        print(f"Published At: {article_meta.get('publishedAt', 'N/A')}")
                        print(f"URL: {url}\n")
                        print(f"Full Article:\n{article.text}\n")
                    except Exception as e:
                        print(f"Failed to fetch full article from {url}: {e}")
        else:
            print(f"No articles found for keyword: {keyword}")

# ─── MAIN EXECUTION ──────────────────────────────────────────────
if __name__ == "__main__":
    try:
        fetch_full_articles(NEWSAPI_KEY, KEYWORDS)
    except Exception as e:
        print(f"Error: {e}")