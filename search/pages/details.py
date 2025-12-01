import streamlit as st # type: ignore
import requests # type: ignore

API_KEY = "6c8c7672f51a4693dac99ce5037660d"
BEARER = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzhjNzY3MmY1MWE0NjkzZGNhYzk5YzVlMDM3NjYwZCIsIm5iZiI6MTc2MzM5NjkxNC40NCwic3ViIjoiNjkxYjRkMzI4ODQzNDlkZDE5ODFjMmFiIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.ulsldmsvOuLJryPScJrSHyihLdoGTQnppqmrh7RZR6I"

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos"
    headers = {"accept": "application/json", "Authorization": f"Bearer {BEARER}"}
    return requests.get(url, headers=headers).json()

st.markdown("""
    <style>
        body {
            background-color: #f5f5f7;
        }
        .title {
            display: inline;
            gap: 6px;
        }

        .judul {
            font-size: 42px;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            white-space: nowrap;
            display: inline-block;
        }

        .release {
            font-size: 14px;
            opacity: 0.7;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            white-space: nowrap;
        }

        .subtitlekiri {
            font-size: 18px;
            padding: 2px 0px;
            margin-bottom: 10px;
            overflow-wrap: break-word;
        }
        .subtitlekanan {
            background-color: black;
            width: fit-content;
            padding: 2px 12px;
            border-radius: 18px;
            font-size: 18px;
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 10px;
            overflow-wrap: break-word;
        }
        .overview {
            font-size: 20px;
            line-height: 1.6;
        }
        .section-title {
            font-size: 26px;
            margin-top: 30px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        iframe {
            border-radius: 20px;
        }
    </style>
""", unsafe_allow_html=True)

hide_details = """
<style>
/* sembunyikan item kedua di sidebar */
[data-testid="stSidebarNav"] ul li:nth-child(2) {
    display: none !important;
}
</style>
"""
st.markdown(hide_details, unsafe_allow_html=True)


if "selected_movie" not in st.session_state:
    st.error("❌ Tidak ada film yang dipilih.")
    st.stop()

movie_id = st.session_state.selected_movie
movie = get_movie_details(movie_id)

# Poster & basic info
poster_url = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
title = movie["title"]
release = movie["release_date"]
rating = movie["vote_average"]
runtime = movie["runtime"]
genre = ", ".join([g["name"] for g in movie["genres"]])
overview = movie["overview"]

# Trailer
trailer_key = None
videos = movie.get("videos", {}).get("results", [])
for v in videos:
    if v["type"] == "Trailer" and v["site"] == "YouTube":
        trailer_key = v["key"]
        break

st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        f"""
        <div class="title">
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
        st.markdown(f"<div class='judul'><br>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitlekiri'>Rating", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitlekiri'>Runtime", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitlekiri'>Genres", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<div class='judul'><br></div>", unsafe_allow_html=True)

        # Rating
        rating = 7.5

        stars_value = rating / 2

        full = int(stars_value)
        half = 1 if stars_value - full >= 0.5 else 0
        empty = 5 - full - half

        full_star = "★"
        half_star = "⯪"
        empty_star = "☆"

        stars = full_star * full + half_star * half + empty_star * empty

        st.markdown(f"<div class='subtitlekanan'>{stars}  ({rating}/10)", unsafe_allow_html=True)

        # Runtime
        st.markdown(f"<div class='subtitlekanan'>{runtime} mins", unsafe_allow_html=True)

        # Genre
        genre_list = [g.strip() for g in genre.split(",")]
        genre_html = "".join(
            [f"<span class='subtitlekanan'>{g}</span>" for g in genre_list]
        )
        st.markdown(genre_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div class='overview'>{overview}</div>", unsafe_allow_html=True)

# Trailer
st.markdown("<div class='section-title'>🎞 Trailer</div>", unsafe_allow_html=True)

if trailer_key:
    st.video(f"https://www.youtube.com/watch?v={trailer_key}", width=600)
else:
    st.info("Trailer tidak tersedia.")

st.markdown("</div>", unsafe_allow_html=True)