import streamlit as st # type: ignore
import requests # type: ignore
from login import login_page

if st.session_state["user"] is None:
    login_page()
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["user"] = None
    st.rerun()


API_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTgyZTVhYWZmNjI3NWRiODMxYmRhMGY1NGI3ZjQ5OSIsIm5iZiI6MTY4NzI0NTMyOS4zMjcwMDAxLCJzdWIiOiI2NDkxNTIxMTU1OWQyMjAxMWM0ZGY3OGMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CAGZDH8VwFdHJ1IJ-O0Y8-jFcr-n_EWxuFOtS6M-sfU"

# HIDE DETAILS PAGE FROM SIDEBAR
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:nth-child(2) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.header("Genre Filter")

genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
genre_res = requests.get(genre_url, headers={"accept": "application/json", "Authorization": API_TOKEN})

genres = {}
if genre_res.status_code == 200:
    data_genre = genre_res.json()
    for g in data_genre.get("genres", []):
        genres[g["name"]] = g["id"]

genre_choice = st.multiselect("Pilih Genre:", list(genres.keys()))

if "genre_page" not in st.session_state:
    st.session_state.genre_page = 1

current_page = st.session_state.genre_page

results = []
if genre_choice:
    selected_genre_ids = ",".join(str(genres[g]) for g in genre_choice)

    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "with_genres": selected_genre_ids,
        "page": current_page,
        "language": "en-US",
        "sort_by": "popularity.desc"
    }
    headers = {"accept": "application/json", "Authorization": API_TOKEN}

    movie_res = requests.get(url, params=params, headers=headers)

    if movie_res.status_code == 200:
        results = movie_res.json().get("results", [])
        total_pages = movie_res.json().get("total_pages", 1)

        st.write(f"### 🎬 Hasil Genre: {', '.join(genre_choice)}")

        cols = st.columns(5)
        for index, movie in enumerate(results):
            with cols[index % 5]:
                poster_url = (
                    f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
                    if movie.get("poster_path") else "empty.png"
                )
                title = movie.get("title", "Untitled")

                st.markdown(f"<img src='{poster_url}' class='movie-poster'/>", unsafe_allow_html=True)
                st.markdown(f"**{title[:20]}{'...' if len(title) > 20 else ''}**")
                st.caption(
                    f"⭐ {movie.get('vote_average')} | "
                    f"🗓️ {movie.get('release_date')}"
                )

        # PAGINATION
        st.markdown("---")
        col1, col2, col3 = st.columns([10, 1, 1])

        with col1:
            if st.button("⬅️ Prev", key="prev_page") and current_page > 1:
                st.session_state.genre_page -= 1
                st.rerun()

        with col2:
            if st.button("Next ➡️", key="next_page") and current_page < total_pages:
                st.session_state.genre_page += 1
                st.rerun()

        st.caption(f"📄 Halaman {current_page} dari {total_pages}")

    else:
        st.error("Gagal mengambil film berdasarkan genre.")