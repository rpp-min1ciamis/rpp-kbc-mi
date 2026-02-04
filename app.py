import streamlit as st

st.set_page_config(
    page_title="Generator RPP KBC MI",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Generator RPP Kurikulum Berbasis Cinta")
st.subheader("MI Negeri 1 Ciamis")

st.success("Aplikasi berhasil dijalankan 🎉")

st.markdown("---")
st.header("📝 Form Input Data RPP")

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

    submit = st.form_submit_button("🚀 Simpan & Lanjutkan")

if submit:
    st.markdown("### ✅ Data berhasil diinput")
    st.write("**Nama Madrasah:**", nama_madrasah)
    st.write("**Mata Pelajaran:**", mata_pelajaran)
    st.write("**Materi Pokok:**", materi_pokok)
    st.write("**Kelas / Semester:**", kelas_semester)
    st.write("**Alokasi Waktu:**", alokasi_waktu)
    st.write("**Tahun Pelajaran:**", tahun_pelajaran)
    st.write("**Model Pedagogis:**", model_pedagogis)

if st.button("Generate Struktur RPP"):
    rpp = f"""
A. JUDUL
PERENCANAAN PEMBELAJARAN
Materi Pokok: {materi_pokok}

B. IDENTITAS
Nama Madrasah   : {madrasah}
Nama Guru       : ____________________
Mata Pelajaran  : {mapel}
Materi Pokok    : {materi}
Kelas / Semester: {kelas}
Alokasi Waktu   : {waktu}
Tahun Pelajaran : {tahun}
Model Pedagogis : {model}

C. IDENTIFIKASI
Kesiapan Murid               :
Dimensi Profil Lulusan (DPL) :
Topik Kurikulum Berbasis Cinta (KBC) :
Materi Insersi KBC           :

D. DESAIN PEMBELAJARAN
Capaian Pembelajaran :
Lintas Disiplin Ilmu :
Tujuan Pembelajaran :
Praktik Pedagogis :
Kemitraan Pembelajaran :
Lingkungan Pembelajaran :
Pemanfaatan Digital :

E. PENGALAMAN BELAJAR
Pertemuan ke- ...
1. Kegiatan Awal
2. Kegiatan Inti
   - Memahami
   - Mengaplikasi
   - Merefleksi
3. Kegiatan Penutup

F. ASESMEN PEMBELAJARAN
Asesmen Awal :
Asesmen Proses :
Asesmen Akhir :

G. LAMPIRAN
1. Rubrik Penilaian
2. LKPD
3. Asesmen Akhir
"""
    st.text_area("Hasil Struktur RPP", rpp, height=500)
