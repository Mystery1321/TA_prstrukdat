import os
import google.generativeai as genai
import re

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def ai_recommend_movies(watchlist):
    if not watchlist:
        return []

    titles = [item[1] for item in watchlist]

    prompt = f"""
Aku punya watchlist film berikut:
{titles}

Berdasarkan film-film itu, berikan 5 rekomendasi film lain yang paling mirip.
Tulis hanya judul filmnya saja dalam list Python.
Contoh output:
["Inception", "Interstellar", "The Matrix", "Tenet", "Avatar"]
"""

    try:
        response = genai.chat.create(
            model="gemini-1.5-t",
            messages=[
                {"role": "system", "content": "Kamu adalah sistem rekomendasi film."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.last.text.strip()

        # Parsing list dengan regex lebih aman
        matches = re.findall(r'\["(.*?)"\]', raw.replace("'", '"'))
        if matches:
            rekomendasi = [x.strip() for x in matches[0].split('", "')]
        else:
            rekomendasi = []

        return rekomendasi[:5]

    except Exception as e:
        print("Error AI Gemini:", e)
        return []
