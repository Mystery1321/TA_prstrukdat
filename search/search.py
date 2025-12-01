import streamlit as st
import requests

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* GRID */

.apple-card:hover {
    transform: scale(1.03);
    box-shadow: 0 12px 28px rgba(0,0,0,0.16);
}

/* POSTER */
.apple-poster {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: 0.25s;
}

.apple-poster:hover {
    transform: scale(1.05);
}

/* BUTTON ala Apple */
.apple-btn {
    background: linear-gradient(180deg, #ffffffcc, #e8e8e8cc);
    border-radius: 14px;
    padding: 6px 14px;
    border: 1px solid rgba(255,255,255,0.5);
    color: black !important;
    font-weight: 600;
    transition: 0.2s;
}

.apple-btn:hover {
    background: white;
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)



API_KEY = "6c8c7672f51a4693dac99ce5037660d"
BEARER = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzhjNzY3MmY1MWE0NjkzZGNhYzk5YzVlMDM3NjYwZCIsIm5iZiI6MTc2MzM5NjkxNC40NCwic3ViIjoiNjkxYjRkMzI4ODQzNDlkZDE5ODFjMmFiIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.ulsldmsvOuLJryPScJrSHyihLdoGTQnppqmrh7RZR6I"

def search_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&api_key={API_KEY}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {BEARER}"
    }
    r = requests.get(url, headers=headers)
    return r.json().get("results", [])

st.title("🎬 Movie Finder")

query = st.text_input("Cari film berdasarkan judul:")

if query:
    results = search_movies(query)

    cols = st.columns(4)

index = 0
for movie in results:

    with cols[index % 4]:
        with st.container():
            st.markdown('<div class="apple-card">', unsafe_allow_html=True)

            # Safe poster
            poster_path = movie.get("poster_path")
            poster = (
                f"https://image.tmdb.org/t/p/w500{poster_path}"
                if poster_path
                else "https://via.placeholder.com/500x750?text=No+Image"
            )

            st.markdown(
                f'<img src="{poster}" class="apple-poster" width="100%">',
                unsafe_allow_html=True
            )

            # Judul maximal 18 char
            st.write(f"### {movie.get('title', 'Unknown')[:18]}")

            # Tombol
            if st.button("Lihat", key=f"btn_{movie['id']}"):
                st.session_state.selected_movie = movie["id"]
                st.switch_page("pages/details.py")

            st.markdown('</div>', unsafe_allow_html=True)

    index += 1
