import streamlit as st
from docx import Document

st.set_page_config(
    page_title="Generator RPP KBC MI",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
if st.session_state.page == "input":

    st.title("📘 Generator RPP Kurikulum Berbasis Cinta")
    st.subheader("📝 Identitas RPP")

    with st.form("form_rpp"):
        nama_madrasah = st.text_input("Nama Madrasah")
        mata_pelajaran = st.text_input("Mata Pelajaran")
        materi_pokok = st.text_input("Materi Pokok")
        kelas_semester = st.text_input("Kelas / Semester")
        alokasi_waktu = st.text_input("Alokasi Waktu")
        tahun_pelajaran = st.text_input("Tahun Pelajaran")
        model_pedagogis = st.selectbox(
            "Model Pedagogis",
            [
                "Discovery Learning",
                "Problem Based Learning (PBL)",
                "Project Based Learning (PjBL)",
                "Inquiry Learning",
                "Pembelajaran Mendalam (Deep Learning)"
            ]
        )

        kerangka_file = st.file_uploader(
            "Upload file kerangka RPP (.docx)",
            type=["docx"]
        )

        submit = st.form_submit_button("🚀 Simpan & Lanjutkan")

    if submit:
        kerangka_teks = ""

        if kerangka_file is not None:
            doc = Document(kerangka_file)
            isi = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            kerangka_teks = "\n".join(isi)

        st.session_state.data = {
            "nama_madrasah": nama_madrasah,
            "mata_pelajaran": mata_pelajaran,
            "materi_pokok": materi_pokok,
            "kelas_semester": kelas_semester,
            "alokasi_waktu": alokasi_waktu,
            "tahun_pelajaran": tahun_pelajaran,
            "model_pedagogis": model_pedagogis,
            "kerangka_teks": kerangka_teks
        }

        st.session_state.page = "preview"
        st.rerun()

    st.success("Aplikasi berhasil dijalankan 🎉")
    st.caption("MI Negeri 1 Ciamis")

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
