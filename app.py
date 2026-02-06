import streamlit as st
from docx import Document

st.set_page_config(
    page_title="Generator RPP KBC MI",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* Background utama */
.stApp {
    background-color: #f4f7f5;
}

/* Judul utama */
h1, h2, h3 {
    color: #0f5132;
    font-weight: 700;
}

/* Card putih */
.block-container {
    padding-top: 2rem;
}

/* Form card */
div[data-testid="stForm"] {
    background: white;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #d1e7dd;
}

/* Input */
input, textarea, select {
    border-radius: 8px !important;
}

/* Tombol utama */
.stButton>button {
    background-color: #198754;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #157347;
}

/* Success box */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Caption madrasah */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
if "page" not in st.session_state:
    st.session_state.page = "input"

if "data" not in st.session_state:
    st.session_state.data = {}

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="Generator RPP KBC MI",
    page_icon="📘",
    layout="centered"
)

# ==============================
# HALAMAN INPUT
# ==============================
st.markdown("""
<div style="background:#198754;padding:18px;border-radius:12px">
    <h2 style="color:white;margin:0">📘 Generator RPP Digital</h2>
    <p style="color:#d1e7dd;margin:0">
        MI Negeri 1 Ciamis — Kurikulum Berbasis Cinta
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# ==============================
# HALAMAN PREVIEW
# ==============================
elif st.session_state.page == "preview":

    data = st.session_state.data

    st.title("🔍 Preview & Generate RPP")

    st.subheader("📌 Identitas")
    st.write("**Nama Madrasah:**", data["nama_madrasah"])
    st.write("**Mata Pelajaran:**", data["mata_pelajaran"])
    st.write("**Materi Pokok:**", data["materi_pokok"])
    st.write("**Kelas / Semester:**", data["kelas_semester"])
    st.write("**Alokasi Waktu:**", data["alokasi_waktu"])
    st.write("**Tahun Pelajaran:**", data["tahun_pelajaran"])
    st.write("**Model Pedagogis:**", data["model_pedagogis"])

    if data["kerangka_teks"]:
        st.subheader("📄 Kerangka RPP")
        st.text_area(
            "Isi Kerangka:",
            data["kerangka_teks"],
            height=250
        )

    if st.button("🧾 Generate Struktur RPP"):
        rpp = f"""
PERENCANAAN PEMBELAJARAN

A. IDENTITAS
Nama Madrasah   : {data['nama_madrasah']}
Mata Pelajaran  : {data['mata_pelajaran']}
Kelas/Semester  : {data['kelas_semester']}
Materi Pokok    : {data['materi_pokok']}
Alokasi Waktu   : {data['alokasi_waktu']}
Tahun Pelajaran : {data['tahun_pelajaran']}
Model Pedagogis : {data['model_pedagogis']}

B. IDENTIFIKASI
    1.	Kesiapan Murid
    2.	Dimensi Profil Lulusan (DPL)
    3.	Topik Kurikulum Berbasis Cinta (KBC)
    4.	Materi Insersi Kurikulum Berbasis Cinta (KBC)

C. DESAIN PEMBELAJARAN
    1.	Capaian Pembelajaran
    2.	Lintas Disiplin Ilmu
    3.	Tujuan Pembelajaran
    4.	Praktik Pedagogis
    5.	Kemitraan Pembelajaran
    6.	Lingkungan Pembelajaran
    7.	Pemanfaatan Digital
    
D. PENGALAMAN BELAJAR
Langkah-langkah Pembelajaran:
    Pertemuan Ke-....
    1. Kegiatan Awal

    2. Kegiatan Inti
        a.	Memahami
        b.	Mengaplikasi
        c.	Merefleksi
        
    3. Kegiatan Penutup

E. ASESMEN PEMBELAJARAN
    1.	Asesmen pada Awal Pembelajaran
    2.	Asesmen pada Proses Pembelajaran
    3.	Asesmen pada Akhir Pembelajaran

F. LAMPIRAN
LKPD, Rubrik, Instrumen
"""
        st.text_area("📘 Draft RPP", rpp, height=450)

    if st.button("⬅️ Kembali ke Input"):
        st.session_state.page = "input"
        st.rerun()
