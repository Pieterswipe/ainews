import anthropic

client = anthropic.Anthropic()

def summarize_theme(theme_name, articles):
    # Bundel de titels en samenvattingen van alle artikels
    articles_text = ""
    for i, article in enumerate(articles[:10], 1):  # max 10 artikels per thema
        articles_text += f"{i}. {article['title']}\n"
        if article['summary']:
            import re
            clean = re.sub(r'<[^>]+>', '', article['summary'])[:300]
            articles_text += f"   {clean}\n"
        articles_text += "\n"

    prompt = f"""Je bent een AI-nieuwsredacteur die complexe technologie uitlegt aan gewone mensen.

Hier zijn de nieuwsartikels van deze week over het thema "{theme_name}":

{articles_text}

Schrijf een korte samenvatting (max 5 zinnen) van wat er deze week gebeurde rond dit thema.
Schrijf in eenvoudig Nederlands, alsof je het uitlegt aan iemand die geen technische achtergrond heeft.
Gebruik minstens één metafoor of vergelijking om de kern van het nieuws begrijpelijk te maken.
Begin direct met de inhoud, geen inleiding zoals "Deze week..." of "In het nieuws..."."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def summarize_all_themes(themed_articles):
    summaries = {}
    for theme, articles in themed_articles.items():
        print(f"    Samenvatting genereren voor: {theme}...")
        try:
            summaries[theme] = summarize_theme(theme, articles)
        except Exception as e:
            print(f"    Fout bij {theme}: {e}")
            summaries[theme] = ""
    return summaries
