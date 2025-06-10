from transformers import pipeline
import matplotlib.pyplot as plt
import argparse
import json

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Mapping for sentiment to color and music suggestion
SENTIMENT_COLORS = {
    'POSITIVE': 'green',
    'NEGATIVE': 'red'
}
SENTIMENT_MUSIC = {
    'POSITIVE': 'Upbeat tunes',
    'NEGATIVE': 'Relaxing melodies'
}

def analyze_text(text):
    """Return list with analysis for each non-empty line"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    results = sentiment_pipeline(lines)
    processed = []
    for line, result in zip(lines, results):
        label = result['label']
        score = result['score'] if label == 'POSITIVE' else -result['score']
        processed.append({
            'line': line,
            'label': label,
            'score': score,
            'color': SENTIMENT_COLORS[label]
        })
    return processed

def overall_music(results):
    if not results:
        return None
    avg = sum(r['score'] for r in results) / len(results)
    label = 'POSITIVE' if avg >= 0 else 'NEGATIVE'
    return SENTIMENT_MUSIC[label]

def plot_results(results, image_path=None):
    scores = [r['score'] for r in results]
    lines = [r['line'] for r in results]
    colors = [r['color'] for r in results]
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, len(scores) + 1), scores, color=colors)
    plt.title('Varia\u00e7\u00e3o Emocional por Trecho')
    plt.xlabel('Trecho (linha)')
    plt.ylabel('Intensidade Emocional')
    plt.axhline(0, color='gray', linestyle='--')
    plt.xticks(range(1, len(scores) + 1), labels=lines, rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    if image_path:
        plt.savefig(image_path)
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='MoodMapper com transformers')
    parser.add_argument('input', help='caminho do arquivo de texto')
    parser.add_argument('--json', dest='json_path', help='exportar resultados em JSON')
    parser.add_argument('--image', dest='image_path', help='caminho para salvar o gr\u00e1fico PNG')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()

    results = analyze_text(text)
    music = overall_music(results)

    for r in results:
        print(f"{r['line']} -> {r['label']} ({r['score']:.3f})")

    if music:
        print('\nRecomenda\u00e7\u00e3o musical:', music)

    if args.json_path:
        with open(args.json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    plot_results(results, args.image_path)

if __name__ == '__main__':
    main()
