import json
import pandas as pd
import streamlit as st
from moodmapper_transformer import analyze_text, overall_music

st.title("MoodMapper Web")

st.write("Digite seu texto (uma frase por linha):")
text = st.text_area("Texto", height=200)

if st.button("Analisar"):
    if not text.strip():
        st.warning("Digite algum texto para analisar.")
    else:
        with st.spinner("Analisando..."):
            results = analyze_text(text)
        st.subheader("Resultados")
        for item in results:
            st.write(f"{item['line']} -> {item['label']} ({item['score']:.2f})")
        music = overall_music(results)
        if music:
            st.write("Trilha sugerida:", music)
        # Prepare data for bar chart
        df = pd.DataFrame({
            'Trecho': [f"{i+1}" for i in range(len(results))],
            'Score': [r['score'] for r in results],
            'Cor': [r['color'] for r in results]
        })
        chart = pd.DataFrame({'Score': df['Score']}, index=df['Trecho'])
        st.bar_chart(chart)
        json_data = json.dumps(results, ensure_ascii=False, indent=2)
        st.download_button('Baixar JSON', json_data, 'resultado.json', 'application/json')
