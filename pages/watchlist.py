import streamlit as st  # type: ignore
from db import get_watchlist, delete_watchlist
from login import login_page

if st.session_state["user"] is None:
    login_page()
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["user"] = None
    st.rerun()


if "error_msg" in st.session_state:
    st.error(st.session_state["error_msg"])
    del st.session_state["error_msg"]

hide_details = """
<style>
[data-testid="stSidebarNav"] ul li:nth-child(2) {
    display: none !important;
}
</style>
"""

st.markdown(hide_details, unsafe_allow_html=True)

st.header("⭐ Your Watchlist")
watchlist = get_watchlist(st.session_state["user"][0])

if not watchlist:
    st.info("There are no movies in your watchlist yet 😢")
else:
    cols = st.columns(5)

    for index, item in enumerate(watchlist):
        with cols[index % 5]:
            st.image(item[2], use_container_width=True)
            st.markdown(f"**{item[1]}**")

            if st.button("❌ Remove", key=f"del_{item[0]}"):
                delete_watchlist(item[0])

                # simpan pesan error
                st.session_state["error_msg"] = "Removed from Watchlist!"

                st.rerun()

st.write("---")
from recommend_ai import ai_recommend_movies

# Ambil judul film dari watchlist
watchlist_titles = [item[0] for item in watchlist]

# Ambil rekomendasi AI (list string)
rekomendasi_strings = ai_recommend_movies(watchlist_titles)

# Bersihkan string: ambil judul saja
rekomendasi_titles = []
for s in rekomendasi_strings:
    if "*" in s:
        title = s.replace("*", "").strip()
        rekomendasi_titles.append(title)

# Buat list tuple (judul, poster_url)
# Kalau kamu punya poster_path dari AI, masukkan di sini
# Kalau belum, pakai placeholder
rekomendasi = []
for title in rekomendasi_titles:
    # Ganti poster_path dengan yang valid kalau ada
    poster_path = ""  # kosong = pakai placeholder
    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    else :
        poster_url = "apps/empty.png"
    rekomendasi.append((title, poster_url))

# Tampilkan grid 5 kolom
st.write("## 🎥 Rekomendasi Film:")
if rekomendasi:
    cols = st.columns(5)
    for i, (title, poster_url) in enumerate(rekomendasi):
        with cols[i % 5]:
            st.image(poster_url, use_container_width=True)
            st.markdown(f"**{title}**")
else:
    st.info("Belum ada rekomendasi 😢")
