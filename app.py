import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Perangkat KBC - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

# CSS TAMPILAN AGAR RAPI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #14532d; }
    [data-testid="stSidebar"] * { color: white !important; }
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

# --- DATABASE SEMENTARA ---
if 'db_rpp' not in st.session_state: st.session_state.db_rpp = []
if 'config' not in st.session_state:
    st.session_state.config = {
        "madrasah": "MIN 1 CIAMIS",
        "guru": "Nama Guru",
        "nip_guru": "-",
        "kepala": "Nama Kepala",
        "nip_kepala": "-",
        "thn_ajar": "2025/2026"
    }

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>E-Perangkat KBC</h2>", unsafe_allow_html=True)
    menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])
    st.divider()
    st.caption("v13.11 - Fixed Template KBC")

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

# --- MENU 2: BUAT RPP BARU ---
elif menu == "➕ Buat RPP Baru":
    st.subheader("➕ Rancang RPP KBC Presisi")
    
    col1, col2 = st.columns(2)
    with col1: mapel = st.text_input("Mata Pelajaran")
    with col2: materi = st.text_input("Materi Pokok")
    
    st.markdown("<div class='section-header'>PENGATURAN WAKTU</div>", unsafe_allow_html=True)
    ca1, ca2, ca3, ca4 = st.columns(4)
    with ca1: inp_jp = st.number_input("Total JP", min_value=1, value=5)
    with ca2: inp_menit = st.number_input("Menit/JP", min_value=1, value=35)
    with ca3: inp_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, value=2)
    with ca4: tgl = st.date_input("Tanggal RPP", date.today())
    
    alokasi_final = f"{inp_jp} x {inp_menit} Menit ({inp_pertemuan} Pertemuan)"
    
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)")
    
    c_kbc1, c_kbc2 = st.columns(2)
    with c_kbc1: model_p = st.selectbox("Model Pembelajaran", ["PBL", "PjBL", "LOK-R", "Inquiry Learning"])
    with c_kbc2: topik_kbc = st.multiselect("Topik KBC", ["Cinta Allah/Rasul", "Cinta Ilmu", "Cinta Diri/Sesama", "Cinta Lingkungan", "Cinta Tanah Air"])

    if st.button("🚀 GENERATE RPP"):
        if not materi or not target_belajar:
            st.warning("Data belum lengkap!")
        else:
            with st.spinner("⏳ Menyusun dokumen dengan format tabel baku..."):
                try:
                    # Logika perhitungan JP
                    jp_per_pt = inp_jp // inp_pertemuan
                    sisa = inp_jp % inp_pertemuan
                    
                    prompt = f"""
                    Buat RPP dalam format HTML untuk materi "{materi}" ({mapel}).
                    Gunakan font 'Times New Roman' dan border tabel '1'.

                    STRUKTUR WAJIB (Jangan Diubah):
                    1. **HEADER**: Judul "PERENCANAAN PEMBELAJARAN (MODUL AJAR) KBC PRESISI".
                    2. **TABEL IDENTITAS**: Buat tabel 2 kolom untuk Madrasah ({st.session_state.config['madrasah']}), Guru, Mapel, Alokasi ({alokasi_final}), Tahun.
                    3. **KOMPONEN KBC**: Tabel berisi Profil Lulusan dan Panca Cinta ({', '.join(topik_kbc)}).
                    4. **TUJUAN PEMBELAJARAN**: Tuliskan {target_belajar}.
                    5. **PENGALAMAN BELAJAR (TABEL)**: 
                       Buat tabel untuk tiap pertemuan (Total {inp_pertemuan} pertemuan).
                       Logika pembagian: Pertemuan awal {jp_per_pt + (1 if sisa > 0 else 0)} JP, sisanya {jp_per_pt} JP.
                       Kolom Tabel: Langkah, Kegiatan, Durasi.
                       Kegiatan Inti WAJIB ada 3 Fase: Memahami, Mengaplikasi, Merefleksi.
                    6. **PENGESAHAN**: Tabel tanda tangan Kepala Madrasah dan Guru di bagian bawah.
                    7. **LAMPIRAN**: Sertakan LKPD dan 10 Soal PG secara rapi di bawah pengesahan.

                    Berikan HANYA kode HTML saja tanpa penjelasan apapun.
                    """
                    
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    st.success("Selesai!")
                    
                    components.html(f"<div style='background:white; color:black; padding:20px;'>{html_final}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download Document", html_final, file_name=f"RPP_{materi}.doc")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:10px;'>{item['file']}</div>", height=500, scrolling=True)
