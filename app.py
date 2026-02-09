import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- KONFIGURASI HALAMAN & SECURITY ---
st.set_page_config(page_title="E-Perangkat KBC Presisi - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

# CSS TAMPILAN
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #14532d; }
    [data-testid="stSidebar"] * { color: white !important; }
    input { color: #000000 !important; }
    .stTextArea textarea { color: #000000 !important; background-color: #ffffff !important; }
    .section-header { color: #166534; font-weight: bold; border-left: 5px solid #166534; padding-left: 10px; margin-top: 20px; }
    .sidebar-brand { text-align: center; padding: 10px; border-bottom: 1px solid #ffffff33; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE AI ---
def get_model():
    if "GOOGLE_API_KEY" not in st.secrets: return None
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(models[0]) if models else None
    except: return None

model_ai = get_model()

# --- DATABASE SEMENTARA ---
if 'db_rpp' not in st.session_state: st.session_state.db_rpp = []
if 'config' not in st.session_state:
    st.session_state.config = {
        "madrasah": "MIN 1 CIAMIS",
        "guru": "Nama Guru",
        "nip_guru": "NIP Guru",
        "kepala": "Nama Kamad",
        "nip_kepala": "NIP Kamad",
        "thn_ajar": "2025/2026"
    }

# --- SIDEBAR MENU ---
with st.sidebar:
    try:
        st.image("logo kemenag.png", width=80)
    except:
        st.warning("⚠️ File logo tidak ditemukan!")

    st.markdown("""
    <div style='text-align: center; border-bottom: 1px solid #ffffff33; margin-bottom: 20px; padding-bottom: 10px;'>
        <h2 style='color: white; margin-top:0px; font-size: 1.5em;'>E-Perangkat KBC Presisi</h2>
        <p style='font-size:0.85em; font-style:italic; color:#c8e6c9;'>
        "MIN 1 CIAMIS - Unggul, Maju, Mendunia."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])
    st.divider()
    st.caption("v13.9 - Alokasi Waktu Dinamis")

# --- MENU 1: PENGATURAN ---
if menu == "⚙️ Pengaturan":
    st.subheader("⚙️ Data Master Madrasah")
    st.session_state.config['madrasah'] = st.text_input("Nama Madrasah", st.session_state.config['madrasah'])
    st.session_state.config['thn_ajar'] = st.text_input("Tahun Pelajaran", st.session_state.config['thn_ajar'])
    
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.config['guru'] = st.text_input("Nama Guru", st.session_state.config['guru'])
        st.session_state.config['nip_guru'] = st.text_input("NIP Guru", st.session_state.config['nip_guru'])
    with c2:
        st.session_state.config['kepala'] = st.text_input("Nama Kepala", st.session_state.config['kepala'])
        st.session_state.config['nip_kepala'] = st.text_input("NIP Kepala", st.session_state.config['nip_kepala'])
    
    if st.button("Simpan Konfigurasi"):
        st.success("Data berhasil disimpan!")

# --- MENU 2: BUAT RPP BARU ---
elif menu == "➕ Buat RPP Baru":
    st.subheader("➕ Rancang RPP KBC Presisi")
    
    c_mapel, c_materi = st.columns(2)
    with c_mapel: mapel = st.text_input("Mata Pelajaran")
    with c_materi: materi = st.text_input("Materi Pokok")
    
    # --- LOGIKA ALOKASI WAKTU OTOMATIS ---
    st.markdown("<div class='section-header'>PENGATURAN WAKTU</div>", unsafe_allow_html=True)
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1:
        inp_jp = st.number_input("Total JP", min_value=1, value=4)
    with ca2:
        inp_menit = st.number_input("Menit per JP", min_value=1, value=35)
    with ca3:
        inp_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, value=2)
    with ca4:
        tgl = st.date_input("Tanggal RPP", date.today())
    
    # Hasil penggabungan otomatis
    alokasi_final = f"{inp_jp} x {inp_menit} Menit ({inp_pertemuan} Pertemuan)"
    st.info(f"Format Alokasi Terdeteksi: **{alokasi_final}**")

    c_kls, c_sem = st.columns(2)
    with c_kls: kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], index=2)
    with c_sem: semester = st.selectbox("Semester", ["1 (Ganjil)", "2 (Genap)"], index=1)
    
    st.markdown("<div class='section-header'>KOMPONEN KBC & DEEP LEARNING</div>", unsafe_allow_html=True)
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", height=100)
    
    c_kbc1, c_kbc2 = st.columns(2)
    with c_kbc1: 
        model_p = st.selectbox("Model Pembelajaran", ["Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "LOK-R", "Inquiry Learning", "Cooperative Learning"])
    with c_kbc2:
        profil = st.multiselect("Dimensi Profil Lulusan", ["Keimanan & Ketakwaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian"])
    
    topik_kbc = st.multiselect("Topik KBC (Panca Cinta)", ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"])

    if st.button("🚀 GENERATE RPP SESUAI REFERENSI"):
        if not materi or not target_belajar:
            st.warning("Mohon lengkapi Materi dan Tujuan Pembelajaran.")
        else:
            with st.spinner("⏳ Mengoneksikan data ke struktur RPP KBC..."):
                try:
                    prompt = f"""
                    Berperanlah sebagai Guru Profesional KBC di {st.session_state.config['madrasah']}.
                    Buat RPP HTML lengkap untuk materi "{materi}" ({mapel}) Kelas {kelas}.
                    
                    DATA IDENTITAS:
                    - Guru: {st.session_state.config['guru']} (NIP: {st.session_state.config['nip_guru']})
                    - Alokasi: {alokasi_final} (Artinya ada {inp_pertemuan} pertemuan)
                    
                    LOGIKA PERTEMUAN:
                    - Anda HARUS membagi RPP ini menjadi tepat {inp_pertemuan} pertemuan.
                    - Jika ada 1 pertemuan, buat detail dari Pendahuluan sampai Penutup.
                    - Jika ada {inp_pertemuan} pertemuan, buat sub-bab 'Pertemuan 1', 'Pertemuan 2', dst.
                    - Durasi total per pertemuan adalah (Total JP/Total Pertemuan) x {inp_menit} menit.

                    STRUKTUR HTML:
                    1. HEADER: Perencanaan Pembelajaran KBC.
                    2. TABEL IDENTITAS: Madrasah, Guru, Mapel, Kelas, Alokasi ({alokasi_final}).
                    3. IDENTIFIKASI KBC: Profil Lulusan ({', '.join(profil)}), Panca Cinta ({', '.join(topik_kbc)}).
                    4. DESAIN PEMBELAJARAN: TP ({target_belajar}).
                    5. PENGALAMAN BELAJAR: (Sesuai jumlah {inp_pertemuan} pertemuan). Gunakan fase Memahami, Mengaplikasi, Merefleksi.
                    6. ASESMEN & PENGESAHAN.
                    7. LAMPIRAN: LKPD & Instrumen Soal.

                    HANYA BERIKAN KODE HTML.
                    """
                    
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    st.success("RPP Berhasil Disusun!")
                    
                    components.html(f"<div style='font-family:serif; background:white; color:black; padding:30px;'>{html_final}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download Dokumen (.doc)", html_final, file_name=f"RPP_{materi}.doc")
                
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    st.subheader("📜 Riwayat Dokumen")
    if not st.session_state.db_rpp: st.info("Belum ada dokumen.")
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
            st.download_button("Unduh Ulang", item['file'], file_name="RPP_Re.doc", key=f"re_{i}")
