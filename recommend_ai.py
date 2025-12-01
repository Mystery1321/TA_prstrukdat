import google.generativeai as genai

# SET API KEY
genai.configure(api_key="AIzaSyC9VcQFQG64CrEc5nCOpVipHeESMkF5q_I")

model = genai.GenerativeModel("models/gemini-2.5-flash")

def ai_recommend_movies(watchlist):
    if not watchlist:
        return ["Watchlist kosong. Tambahkan film dulu ya!"]

    prompt = f"""
    Pengguna memiliki watchlist film berikut: {watchlist}.
    Rekomendasikan 5 film lain yang mirip gaya, genre, atau vibes-nya.
    Balas dalam format list tanpa penjelasan panjang.
    """

    response = model.generate_content(prompt)

    # hasil model biasanya berupa teks list → convert supaya rapi
    hasil = response.text.split("\n")
    hasil = [h.replace("-", "").strip() for h in hasil if h.strip()]

    return hasil[:5]
