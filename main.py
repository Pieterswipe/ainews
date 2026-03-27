from scraper import get_articles_last_week
from classifier import classify_all
from summarizer import summarize_all_themes
from pdf_maker import create_pdf, create_summary_pdf
from podcast_maker import genereer_podcast
from datetime import datetime
import resend
import os
import base64

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

# Step 5: Podcast genereren
filename_podcast = f"ai_news_samenvatting_{date_str}.mp3"
print(f"\nStep 5: Audio samenvatting genereren...")
genereer_podcast(summaries, filename_podcast)

# Step 6: Mail versturen via Resend
print("\nStep 6: Mail versturen...")
resend.api_key = os.environ.get("RESEND_API_KEY")

with open(filename_summary, "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

with open(filename_podcast, "rb") as f:
    podcast_data = base64.b64encode(f.read()).decode("utf-8")

resend.Emails.send({
    "from": "noreply@dthtools.be",
    "to": "pieter@swipedrinks.com",
    "subject": f"AI Nieuws Digest – {date_str}",
    "html": f"<p>Dag Pieter,</p><p>Hierbij de AI nieuwssamenvatting van {date_str}.</p><p>Bijlagen: PDF samenvatting + audio voorlezing.</p>",
    "attachments": [
        {"filename": filename_summary, "content": pdf_data},
        {"filename": filename_podcast, "content": podcast_data},
    ]
})

print("  Mail verstuurd!")
