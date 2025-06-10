import moodmapper

def test_analyze_text_portuguese():
    text = "Estou muito feliz. Que alegria!"
    results = moodmapper.analyze_text(text, lang="pt")
    emotions = [r["dominant_emotion"] for r in results]
    assert emotions == ["joy", "joy"]
