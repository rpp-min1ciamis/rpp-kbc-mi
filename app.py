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

    st.markdown("<h2 style='color: white;'>E-Perangkat KBC</h2>", unsafe_allow_html=True)
    menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])
    st.divider()
    st.caption("v13.10 - Fix Time Logic")

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
        st.success("Data disimpan!")

# --- MENU 2: BUAT RPP BARU ---
elif menu == "➕ Buat RPP Baru":
    st.subheader("➕ Rancang RPP KBC Presisi")
    
    c_mapel, c_materi = st.columns(2)
    with c_mapel: mapel = st.text_input("Mata Pelajaran")
    with c_materi: materi = st.text_input("Materi Pokok")
    
    st.markdown("<div class='section-header'>PENGATURAN WAKTU & PERTEMUAN</div>", unsafe_allow_html=True)
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1:
        inp_jp = st.number_input("Total JP", min_value=1, value=5)
    with ca2:
        inp_menit = st.number_input("Menit per JP", min_value=1, value=35)
    with ca3:
        inp_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, value=2)
    with ca4:
        tgl = st.date_input("Tanggal RPP", date.today())
    
    alokasi_final = f"{inp_jp} x {inp_menit} Menit ({inp_pertemuan} Pertemuan)"
    st.info(f"Rencana: **{alokasi_final}**")

    c_kls, c_sem = st.columns(2)
    with c_kls: kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], index=2)
    with c_sem: semester = st.selectbox("Semester", ["1 (Ganjil)", "2 (Genap)"], index=1)
    
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", height=100)
    
    c_kbc1, c_kbc2 = st.columns(2)
    with c_kbc1: 
        model_p = st.selectbox("Model Pembelajaran", ["Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "LOK-R", "Inquiry Learning"])
    with c_kbc2:
        profil = st.multiselect("Dimensi Profil Lulusan", ["Keimanan & Ketakwaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi"])
    
    topik_kbc = st.multiselect("Topik KBC (Panca Cinta)", ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"])

    if st.button("🚀 GENERATE RPP"):
        if not materi or not target_belajar:
            st.warning("Isi Materi dan TP dulu ya.")
        else:
            with st.spinner("⏳ Menghitung pembagian jam dan menyusun RPP..."):
                try:
                    # LOGIKA PEMBAGIAN JAM (Diletakkan di dalam button agar variabel terbaca)
                    jp_rata = inp_jp // inp_pertemuan
                    sisa = inp_jp % inp_pertemuan
                    
                    prompt = f"""
                    Berperanlah sebagai Guru Profesional KBC. 
                    Buat RPP HTML lengkap untuk materi "{materi}" ({mapel}).
                    
                    DATA WAKTU:
                    - Total: {inp_jp} JP.
                    - Dibagi dalam: {inp_pertemuan} Pertemuan.
                    - Aturan: Pertemuan awal dapat {jp_rata + (1 if sisa > 0 else 0)} JP, pertemuan sisa/akhir dapat {jp_rata} JP. 
                    - Pastikan total JP tetap {inp_jp}.
                    
                    STRUKTUR HTML:
                    1. IDENTITAS: Sertakan Madrasah {st.session_state.config['madrasah']}, Guru {st.session_state.config['guru']}, Alokasi {alokasi_final}.
                    2. PENGALAMAN BELAJAR: Buat sub-bab untuk SETIAP pertemuan (Pertemuan 1, 2, dst).
                    3. Setiap pertemuan berisi: Pendahuluan, Inti (Fase Memahami, Mengaplikasi, Merefleksi), dan Penutup.
                    4. Masukkan narasi Karakter Panca Cinta: {', '.join(topik_kbc)}.
                    5. LAMPIRAN: LKPD dan 10 Soal PG.

                    Berikan hanya kode HTML saja.
                    """
                    
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    st.success("RPP Berhasil Dibuat!")
                    
                    components.html(f"<div style='font-family:serif; background:white; color:black; padding:30px;'>{html_final}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download (.doc)", html_final, file_name=f"RPP_{materi}.doc")
                
                except Exception as e:
                    st.error(f"Aduh, ada error: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    st.subheader("📜 Riwayat")
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
            st.download_button("Download", item['file'], file_name="RPP_Lama.doc", key=f"re_{i}")
