import streamlit as st  # type: ignore
from db import register_user, login_user

def login_page():
    # Hide sidebar
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }

        .login-subtitle {
            text-align: center;
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 1.5rem;
        }

        .stTabs [role="tab"] {
            padding: 0.6rem 1rem;
            font-size: 0.95rem;
        }

        .stTextInput > div > div > input {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-title">Hi There! Welcome to Naga Hitam</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Silakan login untuk melanjutkan</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])

        with tab1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            login_btn = st.container()
            with login_btn:
                if st.button("Login", key="login_btn", use_container_width=True):
                    user = login_user(username, password)
                    if user:
                        st.session_state["user"] = user
                        st.success(f"Selamat datang kembali, {username}! 🎉")
                        st.rerun()
                    else:
                        st.error("Username atau password salah!")

        with tab2:
            new_user = st.text_input("Buat Username")
            new_pass = st.text_input("Buat Password", type="password")
            confirm_pass = st.text_input("Konfirmasi Password", type="password")

            if st.button("Register", key="register_btn", use_container_width=True):
                
                # Validasi input kosong
                if not new_user:
                    st.error("Username tidak boleh kosong!")
                elif not new_pass:
                    st.error("Password tidak boleh kosong!")
                elif not confirm_pass:
                    st.error("Konfirmasi password tidak boleh kosong!")
                elif new_pass != confirm_pass:
                    st.error("Password dan konfirmasi password tidak sama!")
                else:
                    # Proses register
                    if register_user(new_user, new_pass):
                        st.success("Akun berhasil dibuat! Silakan login.")
                    else:
                        st.warning("Username sudah digunakan!")

        st.markdown('</div>', unsafe_allow_html=True)
