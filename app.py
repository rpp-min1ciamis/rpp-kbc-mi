import streamlit as st

st.set_page_config(page_title="Generator RPP KBC MI", layout="wide")

st.title("📘 Generator RPP MI")
st.subheader("Versi Kemenag + Kurikulum Berbasis Cinta")

st.write("Aplikasi ieu masih tahap awal. InsyaAllah bakal dikembangkeun.")

mapel = st.text_input("Mata Pelajaran")
kelas = st.text_input("Kelas / Fase")
materi = st.text_area("Materi Pokok")

if st.button("Generate RPP"):
    st.success("Fitur generate RPP bakal aktif dina langkah salajengna.")

