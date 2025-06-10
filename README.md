# MoodMapper

Simple tool to map emotions in text.

## Usage

1. Save your text to a file, e.g. `mytext.txt`.
2. Run the analyzer:

```bash
python3 moodmapper.py mytext.txt --json result.json
```

The script will print the dominant emotion for each sentence, a short summary
and suggestions for color and music. If `--json` is provided, the per-sentence
analysis is saved to the given file in JSON format.

### With transformers

Install additional dependencies:

```bash
pip install transformers torch matplotlib
```

Run the advanced analyzer which draws a sentiment chart and can export results to JSON or PNG:

```bash
python3 moodmapper_transformer.py mytext.txt --json result.json --image grafico.png
```
