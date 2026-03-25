from scraper import get_articles_last_week
from classifier import classify_all
from summarizer import summarize_all_themes
from pdf_maker import create_pdf, create_summary_pdf
from datetime import datetime

print("=" * 50)
print("   Weekly AI News Digest Generator")
print("=" * 50)

# Step 1: Fetch articles from all sources
print("\nStep 1: Fetching articles from last week...")
articles = get_articles_last_week()

if not articles:
    print("\nNo articles found. Check your internet connection or try again later.")
    exit()

# Step 2: Sort articles by theme
print("\nStep 2: Sorting articles by theme...")
themed = classify_all(articles)

print("\n  Themes detected:")
for theme, arts in themed.items():
    print(f"    - {theme}: {len(arts)} articles")

# Step 3: Generate summaries via Claude API
print("\nStep 3: Generating Dutch summaries per theme...")
summaries = summarize_all_themes(themed)

# Step 4: Generate the PDFs
date_str = datetime.now().strftime('%Y-%m-%d')
filename_full = f"ai_news_{date_str}.pdf"
filename_summary = f"ai_news_samenvattingen_{date_str}.pdf"

print(f"\nStep 4: Generating PDFs...")
create_pdf(themed, summaries, filename_full)
create_summary_pdf(themed, summaries, filename_summary)

print("\n" + "=" * 50)
print(f"  Klaar! Twee PDF's aangemaakt:")
print(f"  - {filename_full} (volledig overzicht)")
print(f"  - {filename_summary} (alleen samenvattingen)")
print("=" * 50)
