import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- 1. PASANG FUNGSI LOGIN DI SINI ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "MIN1CIAMIS": # Ganti password sesuka hati
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align:center;'>🔐 Akses Terbatas Guru</h2>", unsafe_allow_html=True)
        st.text_input("Masukkan Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("😕 Password salah.")
        st.text_input("Masukkan Password", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# --- 2. BUNGKUS SEMUA KODE LAMA ---
if check_password():
    # Mulai dari sini sampai paling bawah, SEMUA kode lama Anda harus MASUK ke kanan (Indentasi)
     
