import json
import re
from collections import Counter
from typing import List, Dict

EMOTION_WORDS: Dict[str, List[str]] = {
    "joy": ["happy", "joy", "glad", "delighted", "hope", "triumphant", "laugh"],
    "sadness": ["sad", "down", "tear", "cry", "sorrow", "melancholy", "depressed"],
    "anger": ["angry", "rage", "furious", "irritated", "mad", "hate"],
    "fear": ["fear", "scared", "terrified", "afraid", "nervous", "panic"],
    "disgust": ["disgust", "nausea", "revulsion", "repelled", "sick"],
    "surprise": ["surprised", "shocked", "astonished", "amazed"],
}

EMOTION_COLORS = {
    "joy": "yellow",
    "sadness": "blue",
    "anger": "red",
    "fear": "purple",
    "disgust": "green",
    "surprise": "orange",
}

EMOTION_MUSIC = {
    "joy": "upbeat music",
    "sadness": "slow, calm music",
    "anger": "intense, fast-paced music",
    "fear": "suspenseful music",
    "disgust": "dissonant tones",
    "surprise": "dynamic crescendos",
}

SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?")


def analyze_text(text: str):
    """Return list of dicts with sentence and dominant emotion."""
    sentences = [s.strip() for s in SENTENCE_RE.findall(text) if s.strip()]
    results = []
    for sentence in sentences:
        word_counts = Counter(re.findall(r"\b\w+\b", sentence.lower()))
        scores = {}
        for emotion, words in EMOTION_WORDS.items():
            scores[emotion] = sum(word_counts.get(w, 0) for w in words)
        dominant = max(scores, key=scores.get) if any(scores.values()) else None
        results.append({
            "sentence": sentence,
            "scores": scores,
            "dominant_emotion": dominant,
            "color": EMOTION_COLORS.get(dominant),
            "music": EMOTION_MUSIC.get(dominant),
        })
    return results


def summarize(results):
    total = Counter()
    for item in results:
        if item["dominant_emotion"]:
            total[item["dominant_emotion"]] += 1
    if not total:
        return "Texto neutro", None, None
    dominant = total.most_common(1)[0][0]
    color = EMOTION_COLORS[dominant]
    music = EMOTION_MUSIC[dominant]
    summary = f"Texto majoritariamente {dominant}."
    return summary, color, music


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simple MoodMapper")
    parser.add_argument("input", help="path to text file")
    parser.add_argument("--json", dest="json_path", help="export analysis as JSON")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    results = analyze_text(text)
    summary, color, music = summarize(results)

    for item in results:
        print(f"{item['sentence']} -> {item['dominant_emotion']}")

    print("\nResumo:", summary)
    if color:
        print("Sugest\u00e3o de cor:", color)
    if music:
        print("Sugest\u00e3o de trilha:", music)

    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
