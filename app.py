import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- 1. SISTEM KEAMANAN LOGIN ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "MIN1CIAMIS":  # <--- GANTI PASSWORD DI SINI
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align:center;'>🔐 Akses Terbatas Guru MIN 1 CIAMIS</h2>", unsafe_allow_html=True)
        st.text_input("Masukkan Password Aplikasi", type="password", on_change=password_entered, key="password")
        st.info("Silakan hubungi Admin untuk mendapatkan akses.")
        return False
    elif not st.session_state["password_correct"]:
        st.error("😕 Password salah. Silakan coba lagi.")
        st.text_input("Masukkan Password Aplikasi", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# Jalankan aplikasi hanya jika login berhasil
if check_password():
    # --- 2. KONFIGURASI HALAMAN ---
    st.set_page_config(page_title="E-Perangkat KBC Presisi - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

    # CSS TAMPILAN
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
    if 'db_rpp' not in st.session_state: st.session_state.db_rpp = []
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
        
        st.markdown("<h3 style='text-align:center;'>E-Perangkat KBC</h3>", unsafe_allow_html=True)
        menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])
        st.divider()
        st.caption("v13.16 - Final Secure Version")

    # --- MENU 1: PENGATURAN ---
    if menu == "⚙️ Pengaturan":
        st.subheader("⚙️ Data Master Madrasah")
        st.session_state.config['madrasah'] = st.text_input("Nama Madrasah", value=st.session_state.config['madrasah'], placeholder="Contoh: MIN 1 CIAMIS")
        st.session_state.config['thn_ajar'] = st.text_input("Tahun Pelajaran", value=st.session_state.config['thn_ajar'], placeholder="Contoh: 2025/2026")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.config['guru'] = st.text_input("Nama Guru", value=st.session_state.config['guru'], placeholder="Nama Lengkap & Gelar")
            st.session_state.config['nip_guru'] = st.text_input("NIP Guru", value=st.session_state.config['nip_guru'], placeholder="NIP atau '-'")
        with c2:
            st.session_state.config['kepala'] = st.text_input("Nama Kepala", value=st.session_state.config['kepala'], placeholder="Nama Kamad")
            st.session_state.config['nip_kepala'] = st.text_input("NIP Kepala", value=st.session_state.config['nip_kepala'], placeholder="NIP Kamad")
        if st.button("Simpan Konfigurasi"):
            st.success("Data tersimpan!")

    # --- MENU 2: BUAT RPP BARU ---
    elif menu == "➕ Buat RPP Baru":
        st.subheader("➕ Rancang RPP KBC Presisi")
        c_mapel, c_materi = st.columns(2)
        with c_mapel: mapel = st.text_input("Mata Pelajaran")
        with c_materi: materi = st.text_input("Materi Pokok")
        
        st.markdown("<div class='section-header'>PENGATURAN WAKTU</div>", unsafe_allow_html=True)
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1: inp_jp = st.number_input("Total JP", min_value=1, value=5)
        with ca2: inp_menit = st.number_input("Menit/JP", min_value=1, value=35)
        with ca3: inp_pertemuan = st.number_input("Jml Pertemuan", min_value=1, value=2)
        with ca4: tgl = st.date_input("Tanggal RPP", date.today())
        
        alokasi_final = f"{inp_jp} x {inp_menit} Menit ({inp_pertemuan} Pertemuan)"
        st.info(f"Format Alokasi: **{alokasi_final}**")

        st.markdown("<div class='section-header'>KOMPONEN KBC & DEEP LEARNING</div>", unsafe_allow_html=True)
        target_belajar = st.text_area("Tujuan Pembelajaran (TP)", height=100)
        
        model_p = st.selectbox("Model Pembelajaran", ["PBL", "PjBL", "LOK-R", "Inquiry Learning", "Cooperative Learning"])

        # Checkbox Profil
        st.markdown("<b>Pilih Dimensi Profil Lulusan:</b>", unsafe_allow_html=True)
        list_profil = ["Keimanan & Ketakwaan", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian"]
        cols_p = st.columns(3)
        profil = [p for i, p in enumerate(list_profil) if cols_p[i % 3].checkbox(p, key=f"p_{p}")]

        # Checkbox Topik KBC
        st.markdown("<br><b>Pilih Topik KBC (Panca Cinta):</b>", unsafe_allow_html=True)
        list_kbc = ["Cinta Allah/Rasul", "Cinta Ilmu", "Cinta Diri/Sesama", "Cinta Lingkungan", "Cinta Tanah Air"]
        cols_k = st.columns(3)
        topik_kbc = [k for i, k in enumerate(list_kbc) if cols_k[i % 3].checkbox(k, key=f"k_{k}")]

        if st.button("🚀 GENERATE RPP"):
            if not materi or not target_belajar:
                st.warning("Isi Materi & TP!")
            else:
                with st.spinner("⏳ Menyusun RPP..."):
                    try:
                        jp_rata = inp_jp // inp_pertemuan
                        sisa = inp_jp % inp_pertemuan
                        
                        prompt = f"""
                        Buat RPP HTML lengkap materi "{materi}" ({mapel}).
                        Madrasah: {st.session_state.config['madrasah']}. Guru: {st.session_state.config['guru']}.
                        
                        STRUKTUR:
                        1. IDENTITAS: Alokasi {alokasi_final}.
                        2. C. DESAIN: Jabarkan 7 poin (CP, Lintas Ilmu, TP, Pedagogis, Kemitraan, Lingkungan, Digital). 
                           Khusus TP: Satukan narasi "{target_belajar}" dengan nilai "{', '.join(topik_kbc)}".
                        3. D. PENGALAMAN: Bagi {inp_pertemuan} pertemuan. P1 = {jp_rata + (1 if sisa > 0 else 0)} JP, sisanya {jp_rata} JP.
                        4. PENGESAHAN: Cantumkan tempat/tanggal 'Ciamis, {tgl.strftime('%d %B %Y')}'.
                        5. LAMPIRAN: LKPD & 10 Soal PG.
                        """
                        raw_response = model_ai.generate_content(prompt).text
                        html_final = re.sub(r'```html|```', '', raw_response).strip()
                        st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                        components.html(f"<div style='background:white; color:black; padding:30px;'>{html_final}</div>", height=800, scrolling=True)
                        st.download_button("📥 Download", html_final, file_name=f"RPP_{materi}.doc")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- MENU 3: RIWAYAT ---
    elif menu == "📜 Riwayat RPP":
        for i, item in enumerate(reversed(st.session_state.db_rpp)):
            with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
                components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
