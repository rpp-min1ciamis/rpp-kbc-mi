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
    .section-header { color: #166534; font-weight: bold; border-left: 5px solid #166534; padding-left: 10px; margin-top: 20px; margin-bottom: 10px; }
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

if 'db_rpp' not in st.session_state: st.session_state.db_rpp = []
if 'config' not in st.session_state:
    st.session_state.config = {
        "madrasah": "",
        "guru": "",
        "nip_guru": "",
        "kepala": "",
        "nip_kepala": "",
        "thn_ajar": ""
    }

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo kemenag.png", width=80) 
    except:
        st.warning("⚠️ Logo tidak ditemukan!")
    st.markdown("<h2 style='color: white; text-align:center;'>E-Perangkat KBC</h2>", unsafe_allow_html=True)
    menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])
    st.divider()
    st.caption("v13.16 - Checkbox Interface")

# --- MENU 1: PENGATURAN ---
if menu == "⚙️ Pengaturan":
    st.subheader("⚙️ Data Master Madrasah")
    st.info("Isi data ini sekali saja. Nanti otomatis masuk ke setiap RPP.")
    
    # Menambahkan placeholder agar teks terlihat samar saat kosong
    st.session_state.config['madrasah'] = st.text_input("Nama Madrasah", 
        value=st.session_state.config['madrasah'], 
        placeholder="Masukkan Nama Madrasah (Contoh: MIN 1 CIAMIS)")
        
    st.session_state.config['thn_ajar'] = st.text_input("Tahun Pelajaran", 
        value=st.session_state.config['thn_ajar'], 
        placeholder="Contoh: 2025/2026")
    
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.config['guru'] = st.text_input("Nama Guru", 
            value=st.session_state.config['guru'], 
            placeholder="Masukkan Nama Lengkap & Gelar")
            
        st.session_state.config['nip_guru'] = st.text_input("NIP Guru", 
            value=st.session_state.config['nip_guru'], 
            placeholder="Masukkan NIP (Gunakan '-' jika tidak ada)")
    with c2:
        st.session_state.config['kepala'] = st.text_input("Nama Kepala", 
            value=st.session_state.config['kepala'], 
            placeholder="Masukkan Nama Kepala Madrasah")
            
        st.session_state.config['nip_kepala'] = st.text_input("NIP Kepala", 
            value=st.session_state.config['nip_kepala'], 
            placeholder="Masukkan NIP Kepala")
    
    if st.button("Simpan Konfigurasi"):
        st.success("Data berhasil disimpan!")

# --- MENU 2: BUAT RPP BARU ---
elif menu == "➕ Buat RPP Baru":
    st.subheader("➕ Rancang RPP KBC Presisi")
    
    c_mapel, c_kls, c_materi, = st.columns(3)
    with c_mapel: mapel = st.text_input("Mata Pelajaran")
    with c_kls: kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], index=2)
    with c_materi: materi = st.text_input("Materi Pokok")
        
    st.markdown("<div class='section-header'>PENGATURAN WAKTU</div>", unsafe_allow_html=True)
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1: inp_jp = st.number_input("Total JP", min_value=1, value=5)
    with ca2: inp_menit = st.number_input("Menit/JP", min_value=1, value=35)
    with ca3: inp_pertemuan = st.number_input("Jml Pertemuan", min_value=1, value=2)
    with ca4: tgl = st.date_input("Tanggal RPP", date.today())
    
    alokasi_final = f"{inp_jp} x {inp_menit} Menit ({inp_pertemuan} Pertemuan)"

    st.markdown("<div class='section-header'>KOMPONEN KBC & DEEP LEARNING</div>", unsafe_allow_html=True)
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", height=100)
    
    model_p = st.selectbox("Model Pembelajaran", ["Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "LOK-R", "Inquiry Learning", "Cooperative Learning", "Discovery Learning", "CTL"])

    # --- MODIFIKASI CHECKBOX DIMENSI PROFIL ---
    st.markdown("**Pilih Dimensi Profil Lulusan:**")
    list_profil = ["Keimanan & Ketakwaan", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"]
    cols_p = st.columns(4)
    profil = []
    for i, p in enumerate(list_profil):
        if cols_p[i % 4].checkbox(p, key=f"p_{p}"):
            profil.append(p)

    # --- MODIFIKASI CHECKBOX TOPIK KBC ---
    st.markdown("<br>**Pilih Topik KBC (Panca Cinta):**", unsafe_allow_html=True)
    list_kbc = ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"]
    cols_k = st.columns(3)
    topik_kbc = []
    for i, k in enumerate(list_kbc):
        if cols_k[i % 3].checkbox(k, key=f"k_{k}"):
            topik_kbc.append(k)

    if st.button("🚀 GENERATE RPP SESUAI REFERENSI"):
        if not materi or not target_belajar:
            st.warning("Mohon lengkapi Materi dan TP.")
        else:
            with st.spinner("⏳ Menghubungkan TP dengan Nilai KBC..."):
                try:
                    jp_rata = inp_jp // inp_pertemuan
                    sisa = inp_jp % inp_pertemuan
                    
                    prompt = f"""
                    Berperanlah sebagai Guru Profesional KBC di {st.session_state.config['madrasah']}.
                    Buat RPP HTML lengkap materi "{materi}" ({mapel}).

                    - Profil Lulusan: {', '.join(profil)}
                    - Topik KBC: {', '.join(topik_kbc)}
                    
                    STRUKTUR HTML (WAJIB):
                    1. HEADER: Judul PERENCANAAN PEMBELAJARAN KBC, Materi.
                    
                    2. A. IDENTITAS MODUL (Tabel):
                       Isi: Madrasah, Guru, Mapel, Kelas/Sem, Materi, Alokasi, Tahun, Model Pedagogis ({model_p}).
                    
                    3. B. IDENTIFIKASI & KBC (Tabel & Narasi):
                       - 1. Kesiapan Murid (Tabel: Kondisi Murid, Materi Prasyarat)
                       - 2. Dimensi Profil Lulusan (Narasi penerapan poin: {', '.join(profil)})
                       - 3. Topik KBC (Narasi penerapan poin: {', '.join(topik_kbc)})
                       - 4. Materi Insersi KBC (Narasi singkat penerapan Panca Cinta di materi ini)
                    
                    4. C. DESAIN PEMBELAJARAN (Sub-bab):
                       - 1. Capaian Pembelajaran (CP)
                       - 2. Lintas Disiplin Ilmu (Hubungkan dengan mapel lain)
                       - 3. Tujuan Pembelajaran ( {Gabungkan narasi "{target_belajar}" dengan "{', '.join(topik_kbc)}" secara otomatis dan harmonis.)
                       - 4. Praktik Pedagogis (Peran guru sebagai fasilitator)
                       - 5. Kemitraan Pembelajaran (Peran orang tua)
                       - 6. Lingkungan Pembelajaran
                       - 7. Pemanfaatan Digital
                                                  
                    5. D. PENGALAMAN BELAJAR: {inp_pertemuan} pertemuan. Pembagian JP: P1={jp_rata + (1 if sisa > 0 else 0)}, sisanya {jp_rata}.
                    6. ASESMEN, PENGESAHAN, LAMPIRAN (LKPD & 5 Soal PG).

                    HANYA BERIKAN KODE HTML.
                    """
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    st.success("Berhasil!")
                    components.html(f"<div style='background:white; color:black; padding:40px; border:1px solid #ccc;'>{html_final}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download Dokumen (.doc)", html_final, file_name=f"RPP_{materi}.doc")
                except Exception as e:
                    st.error(f"Kesalahan: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
