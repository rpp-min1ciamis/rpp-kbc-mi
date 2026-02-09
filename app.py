import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Perangkat KBC Presisi - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

# --- CSS TAMPILAN ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #14532d; }
    [data-testid="stSidebar"] * { color: white !important; }
    input { color: #000000 !important; }
    .stTextArea textarea { color: #000000 !important; background-color: #ffffff !important; }
    .section-header { color: #166534; font-weight: bold; border-left: 5px solid #166534; padding-left: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE AI (PERBAIKAN ERROR 404) ---
def get_model():
    if "GOOGLE_API_KEY" not in st.secrets: return None
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Mencari model yang mendukung generateContent secara otomatis
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
        return None
    except:
        return None

model_ai = get_model()

# --- DATABASE SEMENTARA ---
if 'db_rpp' not in st.session_state: st.session_state.db_rpp = []
if 'config' not in st.session_state:
    st.session_state.config = {"madrasah": "", "guru": "", "nip_guru": "", "kepala": "", "nip_kepala": "", "thn_ajar": ""}

# --- SIDEBAR MENU ---
with st.sidebar:
    try: st.image("logo kemenag.png", width=80)
    except: st.warning("⚠️ Logo!")
    st.markdown("<h3 style='text-align:center;'>E-Perangkat KBC</h3>", unsafe_allow_html=True)
    menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])

# --- MENU 1: PENGATURAN ---
if menu == "⚙️ Pengaturan":
    st.subheader("⚙️ Data Master Madrasah")
    st.session_state.config['madrasah'] = st.text_input("Nama Madrasah", value=st.session_state.config['madrasah'], placeholder="Contoh: MIN 1 CIAMIS")
    st.session_state.config['thn_ajar'] = st.text_input("Tahun Pelajaran", value=st.session_state.config['thn_ajar'], placeholder="Contoh: 2025/2026")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.config['guru'] = st.text_input("Nama Guru", value=st.session_state.config['guru'], placeholder="Nama Lengkap & Gelar")
        st.session_state.config['nip_guru'] = st.text_input("NIP Guru", value=st.session_state.config['nip_guru'], placeholder="NIP")
    with c2:
        st.session_state.config['kepala'] = st.text_input("Nama Kepala", value=st.session_state.config['kepala'], placeholder="Nama Kamad")
        st.session_state.config['nip_kepala'] = st.text_input("NIP Kepala", value=st.session_state.config['nip_kepala'], placeholder="NIP Kamad")
    if st.button("Simpan"): st.success("Data Master Berhasil Disimpan!")

# --- MENU 2: BUAT RPP BARU ---
elif menu == "➕ Buat RPP Baru":
    st.subheader("➕ Rancang RPP KBC Presisi")
    c_m1, c_m2 = st.columns(2)
    with c_m1: mapel = st.text_input("Mata Pelajaran")
    with c_m2: materi = st.text_input("Materi Pokok")
    
    st.markdown("<div class='section-header'>WAKTU & PERTEMUAN</div>", unsafe_allow_html=True)
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1: inp_jp = st.number_input("Total JP", min_value=1, value=5)
    with ca2: inp_mnt = st.number_input("Menit/JP", min_value=1, value=35)
    with ca3: inp_pt = st.number_input("Pertemuan", min_value=1, value=2)
    with ca4: tgl_in = st.date_input("Tanggal RPP", date.today())
    
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", height=100)
    model_p = st.selectbox("Model", ["PBL", "PjBL", "LOK-R", "Inquiry", "Discovery"])

    # Checkbox Profil
    st.markdown("<b>Pilih Dimensi Profil Lulusan:</b>", unsafe_allow_html=True)
    list_p = ["Keimanan & Ketakwaan", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian"]
    cols_p = st.columns(3)
    profil_sel = [p for i, p in enumerate(list_p) if cols_p[i % 3].checkbox(p, key=f"p_{p}")]

    # Checkbox Topik KBC
    st.markdown("<br><b>Pilih Topik KBC (Panca Cinta):</b>", unsafe_allow_html=True)
    list_kbc = ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"]
    cols_k = st.columns(2)
    topik_sel = [k for i, k in enumerate(list_kbc) if cols_k[i % 2].checkbox(k, key=f"k_{k}")]

    if st.button("🚀 GENERATE RPP"):
        if model_ai is None:
            st.error("API Key belum terpasang atau tidak valid.")
        elif not materi or not target_belajar:
            st.warning("Data materi atau tujuan belum diisi!")
        else:
            with st.spinner("⏳ AI sedang merancang RPP KBC Presisi..."):
                try:
                    jp_rata = inp_jp // inp_pt
                    sisa = inp_jp % inp_pt
                    prompt = f"""
                    Berperanlah sebagai pakar Kurikulum KBC Presisi. Buat RPP HTML lengkap materi "{materi}" ({mapel}).
                    
                    STRUKTUR WAJIB:
                    A. IDENTITAS MODUL (Tabel: Madrasah {st.session_state.config['madrasah']}, Alokasi {inp_jp}x{inp_mnt}).
                    
                    B. IDENTIFIKASI: Buat tabel narasi mendalam yang memetakan materi dengan Dimensi Profil ({', '.join(profil_sel)}) 
                       dan Nilai Panca Cinta ({', '.join(topik_sel)}).
                    
                    C. DESAIN PEMBELAJARAN (Jabarkan 7 Poin detail): 
                       1. CP, 2. Lintas Disiplin, 3. TP (Narasi gabungan "{target_belajar}" & "{', '.join(topik_sel)}"), 
                       4. Pedagogis, 5. Kemitraan, 6. Lingkungan, 7. Digital.
                    
                    D. PENGALAMAN BELAJAR (Deep Learning): Bagi menjadi {inp_pt} pertemuan. 
                       P1={jp_rata+(1 if sisa>0 else 0)} JP. Gunakan alur: Memahami, Mengaplikasi, Merefleksi.
                    
                    E. ASESMEN, F. PENGESAHAN (Ciamis, {tgl_in.strftime('%d %B %Y')}), G. LAMPIRAN (LKPD & 10 Soal PG).
                    """
                    res = model_ai.generate_content(prompt).text
                    html_f = re.sub(r'```html|```', '', res).strip()
                    st.session_state.db_rpp.append({"tgl": tgl_in, "materi": materi, "file": html_f})
                    st.success("RPP Berhasil Dibuat!")
                    components.html(f"<div style='background:white; color:black; padding:30px; border:1px solid #ccc;'>{html_f}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download Document", html_f, file_name=f"RPP_KBC_{materi}.doc")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat generate: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    if not st.session_state.db_rpp:
        st.info("Belum ada riwayat RPP.")
    for item in reversed(st.session_state.db_rpp):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
            st.download_button("Unduh Ulang", item['file'], file_name=f"RPP_Re_{item['materi']}.doc", key=f"re_{item['materi']}")
