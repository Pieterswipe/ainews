import os
import subprocess
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

STEM = "alloy"  # Beschikbare stemmen: alloy, echo, fable, onyx, nova, shimmer


def maak_voorleestekst(summaries: dict) -> str:
    """Zet alle samenvattingen samen tot één leesbare tekst."""
    tekst = "Hier zijn de AI-nieuwssamenvattingen van deze week. "
    for thema, samenvatting in summaries.items():
        if samenvatting:
            tekst += f"{thema}. {samenvatting} "
    return tekst.strip()


def genereer_podcast(summaries: dict, uitvoerbestand: str = "samenvatting_audio.mp3") -> str:
    """Leest de samenvattingen voor met één stem en slaat op als MP3."""

    tekst = maak_voorleestekst(summaries)

    # OpenAI TTS heeft een limiet van 4096 tekens per aanroep — splits indien nodig
    max_tekens = 4000
    stukken = [tekst[i:i+max_tekens] for i in range(0, len(tekst), max_tekens)]

    tijdelijke_bestanden = []

    for i, stuk in enumerate(stukken):
        print(f"  Audio genereren deel {i+1}/{len(stukken)}...")
        tijdelijk = f"audio_fragment_{i}.mp3"
        antwoord = client.audio.speech.create(
            model="tts-1",
            voice=STEM,
            input=stuk,
        )
        antwoord.stream_to_file(tijdelijk)
        tijdelijke_bestanden.append(tijdelijk)

    # Samenvoegen via ffmpeg
    if len(tijdelijke_bestanden) == 1:
        # Slechts één deel: gewoon hernoemen
        Path(tijdelijke_bestanden[0]).rename(uitvoerbestand)
    else:
        print("  Audio samenvoegen...")
        lijst_bestand = "audio_fragmenten.txt"
        with open(lijst_bestand, "w") as f:
            for bestand in tijdelijke_bestanden:
                f.write(f"file '{bestand}'\n")

        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lijst_bestand, "-c", "copy", uitvoerbestand],
            check=True,
            capture_output=True,
        )

        for bestand in tijdelijke_bestanden:
            Path(bestand).unlink(missing_ok=True)
        Path(lijst_bestand).unlink(missing_ok=True)

    print(f"  Audio klaar: {uitvoerbestand}")
    return uitvoerbestand
