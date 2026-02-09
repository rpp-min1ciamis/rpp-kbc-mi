import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Perangkat KBC Presisi - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

# --- CSS TAMPILAN (Sesuai Format Awal Anda) ---
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

# --- DATABASE SEMENTARA (DENGAN PLACEHOLDER KOSONG) ---
if 'db_rpp' not in st.session_state: 
    st.session_state.db_rpp = []
if 'config' not in st.session_state:
    st.session_state.config = {
        "madrasah": "", "guru": "", "nip_guru": "",
        "kepala": "", "nip_kepala": "", "thn_ajar": ""
    }

# --- SIDEBAR MENU ---
with st.sidebar:
    try:
        st.image("logo kemenag.png", width=80)
    except:
        st.warning("⚠️ Logo tidak ditemukan!")
    
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
    st.caption("v13.18 - Stable Restoration")

# --- MENU 1: PENGATURAN DATA MASTER ---
if menu == "⚙️ Pengaturan":
    st.subheader("⚙️ Data Master Madrasah")
    st.info("Isi data ini sekali saja. Nanti otomatis masuk ke setiap RPP.")
    
    st.session_state.config['madrasah'] = st.text_input("Nama Madrasah", value=st.session_state.config['madrasah'], placeholder="Contoh: MIN 1 CIAMIS")
    st.session_state.config['thn_ajar'] = st.text_input("Tahun Pelajaran", value=st.session_state.config['thn_ajar'], placeholder="Contoh: 2025/2026")
    
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.config['guru'] = st.text_input("Nama Guru", value=st.session_state.config['guru'], placeholder="Nama Lengkap & Gelar")
        st.session_state.config['nip_guru'] = st.text_input("NIP Guru", value=st.session_state.config['nip_guru'], placeholder="Masukkan NIP atau '-'")
    with c2:
        st.session_state.config['kepala'] = st.text_input("Nama Kepala", value=st.session_state.config['kepala'], placeholder="Nama Kepala Madrasah")
        st.session_state.config['nip_kepala'] = st.text_input("NIP Kepala", value=st.session_state.config['nip_kepala'], placeholder="NIP Kepala Madrasah")
    
    if st.button("Simpan Konfigurasi"):
        st.success("Data berhasil disimpan!")

# --- MENU 2: BUAT RPP BARU ---
elif menu == "➕ Buat RPP Baru":
    st.subheader("➕ Rancang RPP KBC Presisi")
    
    c_mapel, c_materi = st.columns(2)
    with c_mapel: mapel = st.text_input("Mata Pelajaran")
    with c_materi: materi = st.text_input("Materi Pokok")
    
    st.markdown("<div class='section-header'>PENGATURAN WAKTU & PERTEMUAN</div>", unsafe_allow_html=True)
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1: inp_jp = st.number_input("Total JP", min_value=1, value=5)
    with ca2: inp_menit = st.number_input("Menit/JP", min_value=1, value=35)
    with ca3: inp_pertemuan = st.number_input("Jml Pertemuan", min_value=1, value=2)
    with ca4: tgl = st.date_input("Tanggal RPP", date.today())
    
    alokasi_final = f"{inp_jp} x {inp_menit} Menit ({inp_pertemuan} Pertemuan)"
    st.info(f"Format Alokasi: **{alokasi_final}**")

    st.markdown("<div class='section-header'>KOMPONEN KBC & DEEP LEARNING</div>", unsafe_allow_html=True)
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", placeholder="Contoh: Murid dapat memahami...", height=100)
    
    model_p = st.selectbox("Model Pembelajaran", ["Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "LOK-R", "Inquiry Learning", "Cooperative Learning", "Discovery Learning", "CTL"])

    # --- INPUT PROFIL (CHECKBOX) ---
    st.markdown("<b>Pilih Dimensi Profil Lulusan:</b>", unsafe_allow_html=True)
    list_profil = ["Keimanan & Ketakwaan", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"]
    cols_p = st.columns(4)
    profil = [p for i, p in enumerate(list_profil) if cols_p[i % 4].checkbox(p, key=f"p_{p}")]

    # --- INPUT KBC (CHECKBOX) ---
    st.markdown("<br><b>Pilih Topik KBC (Panca Cinta):</b>", unsafe_allow_html=True)
    list_kbc = ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"]
    cols_k = st.columns(2)
    topik_kbc = [k for i, k in enumerate(list_kbc) if cols_k[i % 2].checkbox(k, key=f"k_{k}")]

    if st.button("🚀 GENERATE RPP SESUAI REFERENSI"):
        if not materi or not target_belajar:
            st.warning("Mohon lengkapi Materi dan Tujuan Pembelajaran.")
        else:
            with st.spinner("⏳ AI sedang menyusun RPP KBC Presisi..."):
                try:
                    jp_rata = inp_jp // inp_pertemuan
                    sisa = inp_jp % inp_pertemuan
                    
                    prompt = f"""
                    Berperanlah sebagai Guru Profesional KBC di {st.session_state.config['madrasah']}.
                    Buat RPP HTML lengkap materi "{materi}" ({mapel}).
                    
                    DATA INPUT:
                    - Guru: {st.session_state.config['guru']} (NIP: {st.session_state.config['nip_guru']})
                    - Kepala: {st.session_state.config['kepala']} (NIP: {st.session_state.config['nip_kepala']})
                    - Alokasi: {alokasi_final}
                    - Nilai Panca Cinta: {', '.join(topik_kbc)}

                    STRUKTUR HTML (WAJIB):
                    1. HEADER & IDENTITAS: Gunakan tabel border='1'.
                    2. C. DESAIN PEMBELAJARAN: Jabarkan 7 poin (CP, Lintas Ilmu, TP, Pedagogis, Kemitraan, Lingkungan, Digital).
                       PENTING pada poin 3 (TP): Satukan narasi "{target_belajar}" dengan nilai "{', '.join(topik_kbc)}" secara harmonis.
                    3. D. PENGALAMAN BELAJAR: Bagi menjadi {inp_pertemuan} pertemuan. 
                       Logika JP: P1 = {jp_rata + (1 if sisa > 0 else 0)} JP, sisanya {jp_rata} JP.
                       Sertakan kotak Penguatan Nilai KBC di setiap pertemuan.
                    4. PENGESAHAN: Cantumkan 'Ciamis, {tgl.strftime('%d %B %Y')}'.
                       Tampilkan Nama Guru: {st.session_state.config['guru']} dan Nama Kepala: {st.session_state.config['kepala']}.
                    5. LAMPIRAN: LKPD & 10 Soal PG.

                    HANYA BERIKAN KODE HTML.
                    """
                    
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    st.success("RPP KBC Berhasil Disusun!")
                    
                    components.html(f"<div style='background:white; color:black; padding:40px; border:1px solid #ccc;'>{html_final}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download Dokumen (.doc)", html_final, file_name=f"RPP_{materi}.doc")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# --- MENU 3: RIWAYAT RPP ---
elif menu == "📜 Riwayat RPP":
    st.subheader("📜 Riwayat Dokumen")
    if not st.session_state.db_rpp: st.info("Belum ada dokumen.")
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
            st.download_button("Unduh Ulang", item['file'], file_name="RPP_Re.doc", key=f"re_{i}")
