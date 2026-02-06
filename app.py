import streamlit as st

# =====================================
# CONFIG APLIKASI
# =====================================
st.set_page_config(
    page_title="Generator RPP KBC MI",
    page_icon="📘",
    layout="centered"
)

# =====================================
# TEMA WARNA MADRASAH (CSS)
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #f4f7f5;
}

h1, h2, h3 {
    color: #0f5132;
    font-weight: 700;
}

label {
    font-weight: 600;
}

div[data-testid="stForm"] {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

button[kind="primary"] {
    background-color: #198754 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600;
}

button[kind="primary"]:hover {
    background-color: #146c43 !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER APLIKASI
# =====================================
st.title("📘 Generator RPP Kurikulum Berbasis Cinta")
st.caption("MIN 1 CIAMIS • Madrasah Maju Bermutu Mendunia")
st.markdown("---")

# =====================================
# FORM INPUT DATA RPP (FIX & BERSIH)
# =====================================
st.subheader("📝 Formulir Input RPP Baru")

with st.form("form_input_rpp"):

    nama_madrasah = st.text_input(
        "Nama Madrasah",
        value="MI Negeri 1 Ciamis"
    )

    mata_pelajaran = st.text_input(
        "Mata Pelajaran",
        placeholder="Contoh: Akidah Akhlak"
    )

    materi_pokok = st.text_input(
        "Materi Pokok / Tema",
        placeholder="Contoh: Adab Terhadap Tetangga"
    )

    col1, col2 = st.columns(2)
    with col1:
        kelas = st.selectbox(
            "Kelas",
            ["I", "II", "III", "IV", "V", "VI"]
        )
    with col2:
        semester = st.selectbox(
            "Semester",
            ["Ganjil", "Genap"]
        )

    col3, col4 = st.columns(2)
    with col3:
        alokasi_waktu = st.text_input(
            "Alokasi Waktu",
            placeholder="Contoh: 2 x 35 menit"
        )
    with col4:
        tahun_pelajaran = st.text_input(
            "Tahun Pelajaran",
            value="2025 / 2026"
        )

    model_pedagogis = st.selectbox(
        "Model Pembelajaran",
        [
            "Discovery Learning",
            "Problem Based Learning (PBL)",
            "Project Based Learning (PjBL)",
            "Inquiry Learning",
            "Pembelajaran Mendalam (Deep Learning)"
        ]
    )

    submit = st.form_submit_button("🚀 Simpan & Lanjutkan", type="primary")

# =====================================
# HASIL SIMPAN (BELUM KERANGKA)
# =====================================
if submit:
    st.success("✅ Data RPP berhasil disimpan")
    st.markdown("### 📌 Ringkasan Input")
    st.write("**Madrasah:**", nama_madrasah)
    st.write("**Mapel:**", mata_pelajaran)
    st.write("**Materi:**", materi_pokok)
    st.write("**Kelas / Semester:**", f"{kelas} / {semester}")
    st.write("**Alokasi Waktu:**", alokasi_waktu)
    st.write("**Tahun Pelajaran:**", tahun_pelajaran)
    st.write("**Model Pembelajaran:**", model_pedagogis)

st.markdown("---")
st.caption("© 2026 • Generator RPP KBC • MIN 1 Ciamis")

# ==============================
# HALAMAN PREVIEW (FIX)
# ==============================
elif st.session_state.page == "preview":

    # AMAN: cek heula data aya atawa henteu
    if "data" not in st.session_state or not st.session_state.data:
        st.error("❌ Data RPP belum tersedia. Silakan isi form terlebih dahulu.")
        if st.button("⬅️ Kembali ke Form Input"):
            st.session_state.page = "input"
            st.rerun()
        st.stop()

    data = st.session_state.data

    st.title("🔍 Preview Data RPP")
    st.caption("Periksa kembali sebelum generate struktur RPP")

    st.markdown("---")

    st.subheader("📌 Identitas RPP")
    st.write("**Nama Madrasah:**", data.get("nama_madrasah", "-"))
    st.write("**Mata Pelajaran:**", data.get("mata_pelajaran", "-"))
    st.write("**Materi Pokok:**", data.get("materi_pokok", "-"))
    st.write("**Kelas / Semester:**", data.get("kelas_semester", "-"))
    st.write("**Alokasi Waktu:**", data.get("alokasi_waktu", "-"))
    st.write("**Tahun Pelajaran:**", data.get("tahun_pelajaran", "-"))
    st.write("**Model Pedagogis:**", data.get("model_pedagogis", "-"))

    if data.get("kerangka_teks"):
        st.subheader("📄 Kerangka RPP")
        st.text_area(
            "Isi Kerangka:",
            data["kerangka_teks"],
            height=250
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧾 Generate Struktur RPP"):
            st.session_state.page = "generate"
            st.rerun()

    with col2:
        if st.button("⬅️ Kembali ke Input"):
            st.session_state.page = "input"
            st.rerun()

if st.button("🧾 Generate Struktur RPP"):

    rpp = f"""
PERENCANAAN PEMBELAJARAN

A. IDENTITAS
Nama Madrasah   : {data.get('nama_madrasah', '')}
Mata Pelajaran  : {data.get('mata_pelajaran', '')}
Kelas/Semester  : {data.get('kelas_semester', '')}
Materi Pokok    : {data.get('materi_pokok', '')}
Alokasi Waktu   : {data.get('alokasi_waktu', '')}
Tahun Pelajaran : {data.get('tahun_pelajaran', '')}
Model Pedagogis : {data.get('model_pedagogis', '')}

B. IDENTIFIKASI
1. Kesiapan Murid
2. Dimensi Profil Lulusan (DPL)
3. Topik Kurikulum Berbasis Cinta (KBC)
4. Materi Insersi KBC

C. DESAIN PEMBELAJARAN
1. Capaian Pembelajaran
2. Tujuan Pembelajaran
3. Langkah Pembelajaran

D. PENGALAMAN BELAJAR
1. Kegiatan Awal
2. Kegiatan Inti
3. Kegiatan Penutup

E. ASESMEN PEMBELAJARAN
1. Asesmen Awal
2. Asesmen Proses
3. Asesmen Akhir

F. LAMPIRAN
LKPD, Rubrik, Instrumen
"""

    st.text_area(
        "📘 Draft RPP",
        rpp,
        height=450
    )
    if st.button("⬅️ Kembali ke Input"):
        st.session_state.page = "input"
        st.rerun()
