# Themes with matching keywords
# Each article is assigned to the theme with the most keyword matches

THEMES = {
    "Large Language Models": [
        "gpt", "llm", "language model", "chatgpt", "gemini", "claude", "llama",
        "mistral", "transformer", "token", "prompt", "chat", "text generation",
        "fine-tun", "rag", "retrieval", "reasoning", "instruction"
    ],
    "Image & Video AI": [
        "image", "video", "diffusion", "dall-e", "sora", "vision", "visual",
        "multimodal", "pixel", "text-to-image", "text-to-video",
        "stable diffusion", "midjourney", "generate image", "generate video"
    ],
    "AI Tools & Products": [
        "tool", "launch", "release", "api", "platform", "app", "service",
        "software", "announc", "product", "update", "version", "new feature", "plugin"
    ],
    "Research & Science": [
        "research", "paper", "study", "benchmark", "dataset", "training",
        "arxiv", "university", "experiment", "result", "performance", "accuracy",
        "state-of-the-art", "sota", "neural", "algorithm"
    ],
    "AI Ethics & Safety": [
        "safety", "ethic", "bias", "regulation", "law", "policy", "risk",
        "alignment", "copyright", "privacy", "responsible", "harmful", "misinformation",
        "deepfake", "transparency"
    ],
    "AI in Business": [
        "business", "startup", "invest", "funding", "company", "enterprise",
        "revenue", "acqui", "billion", "million", "market", "valuation", "ipo",
        "deal", "partner"
    ],
    "Robotics & Hardware": [
        "robot", "hardware", "chip", "gpu", "nvidia", "compute", "quantum",
        "device", "sensor", "physical", "autonomous", "self-driving", "arm"
    ],
}

def classify_article(article):
    # Combine title and summary for matching
    text = (article["title"] + " " + article["summary"]).lower()

    scores = {}
    for theme, keywords in THEMES.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[theme] = score

    if scores:
        return max(scores, key=scores.get)
    return "General AI News"

def classify_all(articles):
    themed = {}
    for article in articles:
        theme = classify_article(article)
        if theme not in themed:
            themed[theme] = []
        themed[theme].append(article)

    # Sort themes alphabetically, but put "General AI News" last
    sorted_themed = {}
    for key in sorted(themed.keys(), key=lambda x: (x == "General AI News", x)):
        sorted_themed[key] = themed[key]

    return sorted_themed
