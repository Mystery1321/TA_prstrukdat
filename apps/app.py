import streamlit as st
import requests
from db import add_watchlist, get_watchlist, delete_watchlist
from login import login_page
from recommend_ai import ai_recommend_movies

# ---------------- KONFIGURASI APP ----------------
st.set_page_config(page_title="Now Playing Movies", layout="wide")

if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------- CEK LOGIN ----------------
if st.session_state["user"] is None:
    login_page()
else:
    user = st.session_state["user"]

    st.sidebar.success(f"Login sebagai: {user[1]}")
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

    st.title("🎬 Now Playing Movies (TMDb API)")
    tab1, tab2 = st.tabs(["🎞️ Now Playing", "⭐ Watchlist Saya"])

    # ========== TAB NOW PLAYING ==========
    with tab1:
        url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTgyZTVhYWZmNjI3NWRiODMxYmRhMGY1NGI3ZjQ5OSIsIm5iZiI6MTY4NzI0NTMyOS4zMjcwMDAxLCJzdWIiOiI2NDkxNTIxMTU1OWQyMjAxMWM0ZGY3OGMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CAGZDH8VwFdHJ1IJ-O0Y8-jFcr-n_EWxuFOtS6M-sfU"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if "results" not in data:
            st.error("Gagal mengambil data film 😢")
        else:
            movies = data["results"][:15]
            cols = st.columns(5)

            for index, movie in enumerate(movies):
                with cols[index % 5]:
                    poster_url = (
                        f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                        if movie.get("poster_path")
                        else "https://via.placeholder.com/300x450?text=No+Image"
                    )
                    title = str(movie.get("title", "Untitled"))

                    st.image(poster_url, use_container_width=True)
                    st.markdown(f"**{title[:20]}{'...' if len(title) > 20 else ''}**")
                    st.caption(f"⭐ {movie.get('vote_average', 0)} | 🗓️ {movie.get('release_date', 'N/A')}")
                    if st.button("⭐ Simpan", key=f"save_{movie['id']}"):
                        add_watchlist(user[0], movie["id"], title, poster_url)
                        st.success("Ditambahkan ke Watchlist!")

    # ========== TAB WATCHLIST ==========
    with tab2:
        st.subheader("⭐ Watchlist Kamu")
        watchlist = get_watchlist(user[0])

        if not watchlist:
            st.info("Belum ada film di watchlist kamu 🎥")
        else:
            cols = st.columns(5)
            for index, item in enumerate(watchlist):
                with cols[index % 5]:
                    st.image(item[2], use_container_width=True)
                    st.markdown(f"**{item[1]}**")
                    if st.button("❌ Hapus", key=f"del_{item[0]}"):
                        delete_watchlist(item[0])
                        st.warning("Dihapus dari watchlist!")
                        st.rerun()



        st.subheader("✨ Rekomendasi AI:")

        if watchlist:
            rekomendasi = ai_recommend_movies(watchlist)
            if rekomendasi:
                cols = st.columns(5)
                for index, r in enumerate(rekomendasi):
                    with cols[index % 5]:
                        st.markdown(f"**{r}**")
            else:
                st.info("Belum ada rekomendasi — coba cek API key atau format watchlist!")
        else:
            st.info("Belum ada film di watchlist kamu 🎥")
