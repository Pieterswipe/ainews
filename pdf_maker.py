import re
from fpdf import FPDF
from datetime import datetime

class NewsPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 12, "Weekly AI News Digest", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 7, f"Generated on {datetime.now().strftime('%Y-%m-%d')} - Articles from the last 7 days", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

def clean_html(text):
    # Remove HTML tags and clean up whitespace
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def safe_text(text):
    # Replace common Unicode characters that Helvetica can't handle
    replacements = {
        "\u2014": "-",   # em dash —
        "\u2013": "-",   # en dash –
        "\u2018": "'",   # left single quote '
        "\u2019": "'",   # right single quote '
        "\u201c": '"',   # left double quote "
        "\u201d": '"',   # right double quote "
        "\u2026": "...", # ellipsis …
        "\u00b7": "*",   # middle dot ·
        "\u2022": "*",   # bullet •
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode("latin-1", errors="replace").decode("latin-1")

def create_pdf(themed_articles, summaries=None, filename="ai_news_weekly.pdf"):
    pdf = NewsPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    for theme, articles in themed_articles.items():
        # Theme header
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_fill_color(220, 235, 255)
        pdf.cell(0, 10, f"  {theme}  ({len(articles)} articles)", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # Dutch summary box
        if summaries and theme in summaries and summaries[theme]:
            pdf.set_fill_color(255, 250, 220)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, "  Samenvatting", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_fill_color(255, 253, 235)
            pdf.multi_cell(0, 5, safe_text(summaries[theme]), fill=True)
            pdf.ln(3)

        for article in articles:
            # Article title
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, safe_text(article["title"]))

            # Source and date
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 6, f"{article['source']} - {article['published']}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)

            # Summary
            if article["summary"]:
                summary = clean_html(article["summary"])
                if len(summary) > 400:
                    summary = summary[:400] + "..."
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, safe_text(summary))

            # Link (truncate if too long)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(0, 80, 200)
            link = article["link"]
            if len(link) > 100:
                link = link[:97] + "..."
            pdf.cell(0, 5, link, new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)

            pdf.ln(4)

        pdf.ln(4)

    pdf.output(filename)
    print(f"  PDF saved: {filename}")

def create_summary_pdf(themed_articles, summaries, filename="ai_news_summaries.pdf"):
    pdf = NewsPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    for theme, articles in themed_articles.items():
        if theme not in summaries or not summaries[theme]:
            continue

        # Theme header
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_fill_color(220, 235, 255)
        pdf.cell(0, 10, f"  {theme}  ({len(articles)} articles)", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # Dutch summary
        pdf.set_font("Helvetica", "", 11)
        pdf.set_fill_color(255, 253, 235)
        pdf.multi_cell(0, 6, safe_text(summaries[theme]), fill=True)
        pdf.ln(6)

    pdf.output(filename)
    print(f"  PDF saved: {filename}")
