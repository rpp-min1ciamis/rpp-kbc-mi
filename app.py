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
