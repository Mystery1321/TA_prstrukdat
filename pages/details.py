import streamlit as st  # type: ignore
import requests  # type: ignore

API_KEY = "6c8c7672f51a4693dac99ce5037660d"
BEARER = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzhjNzY3MmY1MWE0NjkzZGNhYzk5YzVlMDM3NjYwZCIsIm5iZiI6MTc2MzM5NjkxNC40NCwic3ViIjoiNjkxYjRkMzI4ODQzNDlkZDE5ODFjMmFiIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.ulsldmsvOuLJryPScJrSHyihLdoGTQnppqmrh7RZR6I"

headers = {"accept": "application/json", "Authorization": f"Bearer {BEARER}"}


# ======================= FUNCTIONS ============================
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos"
    return requests.get(url, headers=headers).json()


def get_movie_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("cast", [])
    return []


# ====================== STYLING ===============================
st.markdown("""
    <style>
        body { background-color: #f5f5f7; }
        .judul { 
            font-size: 42px; font-weight: 600; 
            font-family: -apple-system; 
            margin-right: 10px;}
        .release { font-size: 15px; opacity: 0.7; }
        .subtitlekiri { font-size: 18px; margin-bottom: 10px; }
        .subtitlekanan {
            background-color: rgba(255,255,255,0.12);
            padding: 2px 12px;
            border-radius: 18px;
            font-size: 18px;
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 10px;
            backdrop-filter: blur(12px);
            box-shadow: 0 3px 12px rgba(0,0,0,0.4);
        }
        .overview {
            color: rgba(255,255,255,0.6);
            font-size: 20px;
            line-height: 1.6;
        }
        .section-title {
            font-size: 26px;
            margin-top: 30px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        iframe { border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)


hide_details = """
<style>
[data-testid="stSidebarNav"] ul li:nth-child(2) {
    display: none !important;
}
</style>
"""
st.markdown(hide_details, unsafe_allow_html=True)


#VALIDASI
if "selected_movie" not in st.session_state:
    st.error("❌ Tidak ada film yang dipilih.")
    st.stop()

movie_id = st.session_state.selected_movie
movie = get_movie_details(movie_id)


#INFORMATION
poster_path = movie.get("poster_path")
if poster_path:
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
else:
    poster_url = "apps/empty.png"

title = movie["title"]
release = movie["release_date"]
rating = movie["vote_average"]
runtime = movie["runtime"]
overview = movie["overview"]

# ambil genre ids & names
genre_list = movie.get("genres", [])
genre_names = [g["name"] for g in genre_list]
genre_ids = [g["id"] for g in genre_list]


#POSTER AND INFO
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        f"""
        <div>
            <span class="judul">{title}</span>
            <span class="release">({release})</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image(poster_url, use_container_width=True)


with col2:
    col3, col4 = st.columns([3, 4])

    with col3:
        st.markdown("<div class='judul'><br>", unsafe_allow_html=True)
        st.markdown("<div class='subtitlekiri'>Rating</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitlekiri'>Runtime</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitlekiri'>Genres</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='judul'><br>", unsafe_allow_html=True)

        # Rating
        stars_value = rating / 2
        full = int(stars_value)
        half = 1 if stars_value - full >= 0.5 else 0
        empty = 5 - full - half
        stars = "★" * full + "⯪" * half + "☆" * empty

        st.markdown(f"<div class='subtitlekanan'>{stars} ({rating}/10)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitlekanan'>{runtime} mins</div>", unsafe_allow_html=True)

        # Genre
        genre_html = "".join([f"<span class='subtitlekanan'>{g}</span>" for g in genre_names])
        st.markdown(genre_html, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2 = st.tabs(["Info", "Cast"])

    with tab1:
        st.markdown("### Synopsis")
        st.markdown(f"<div class='overview'>{overview}</div>", unsafe_allow_html=True)

    with tab2:
        cast_list = get_movie_cast(movie_id)

        st.markdown("### Cast")

        no_image = "apps/empty.png"

        if cast_list:
            cast_html = """
<div style="
    display: flex;
    overflow-x: auto;
    gap: 16px;
    padding-bottom: 10px;
    scroll-snap-type: x mandatory;
    white-space: nowrap;
">
"""

            for actor in cast_list:
                if actor.get("profile_path"):
                    profile_url = f"https://image.tmdb.org/t/p/w185{actor['profile_path']}"
                else:
                    profile_url = no_image

                cast_html += f"""
<div style="
    flex: 0 0 auto;
    width: 160px;
    text-align: center;
    background-color: #1d1d1d;
    padding: 10px;
    border-radius: 12px;
">
    <img src="{profile_url}" style="width: 100%; border-radius: 10px; height: 230px; object-fit: cover;">
    <div style="margin-top: 8px; font-size: 15px; font-weight:600;">{actor['name']}</div>
    <div style="font-size: 13px; opacity: 0.7;">{actor['character']}</div>
</div>
"""

            cast_html += "</div>"

            st.markdown(cast_html, unsafe_allow_html=True)


#TRAILER
st.markdown("<div class='section-title'>Trailer</div>", unsafe_allow_html=True)

trailer_key = None
videos = movie.get("videos", {}).get("results", [])
for v in videos:
    if v["type"] == "Trailer" and v["site"] == "YouTube":
        trailer_key = v["key"]
        break

if trailer_key:
    st.video(f"https://www.youtube.com/watch?v={trailer_key}", width=600)
else:
    st.info("Trailer tidak tersedia.")


#RECOMENDATION
st.markdown("---")
st.subheader("Recommendation")

if genre_ids:
    g_id = genre_ids[0]
    rec_url = f"https://api.themoviedb.org/3/discover/movie?with_genres={g_id}&sort_by=popularity.desc"
    rec_response = requests.get(rec_url, headers=headers)

    if rec_response.status_code == 200:
        rec_data = rec_response.json().get("results", [])[:10]

        cols = st.columns(5)
        for i, rec in enumerate(rec_data):
            with cols[i % 5]:
                rec_poster = (
                    f"https://image.tmdb.org/t/p/w500{rec['poster_path']}"
                    if rec.get("poster_path")
                    else "https://via.placeholder.com/300x450?text=No+Image"
                )
                st.image(rec_poster, use_container_width=True)

                short_title = rec["title"][:18] + ("..." if len(rec["title"]) > 18 else "")
                if st.button(short_title, key=f"rec_{rec['id']}"):
                    st.session_state.selected_movie = rec["id"]
                    st.rerun()
else:
    st.write("Genre tidak ditemukan.")


#BACK TO HOME
st.markdown("---")
if st.button("⬅️ Back to Home"):
    st.switch_page("home.py")
