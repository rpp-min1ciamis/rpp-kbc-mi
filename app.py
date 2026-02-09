import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- 1. SISTEM LOGIN ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "MIN1CIAMIS": # Password Anda
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align:center;'>🔐 Akses Terbatas Guru</h2>", unsafe_allow_html=True)
        st.text_input("Masukkan Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("😕 Password salah.")
        st.text_input("Masukkan Password", type="password", on_change=password_entered, key="password")
        return False
    return True

# --- 2. JALANKAN APLIKASI ---
if check_password():
    # Semua kode di bawah ini wajib masuk ke kanan (1 kali Tab)
    st.set_page_config(page_title="E-Perangkat KBC - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

    # Inisialisasi Database Kosong (Agar muncul placeholder samar)
    if 'db_rpp' not in st.session_state: st.session_state.db_rpp = []
    if 'config' not in st.session_state:
        st.session_state.config = {"madrasah": "", "guru": "", "nip_guru": "", "kepala": "", "nip_kepala": "", "thn_ajar": ""}

    with st.sidebar:
        st.markdown("<h3 style='text-align:center;'>E-Perangkat KBC</h3>", unsafe_allow_html=True)
        menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])

    # --- MENU PENGATURAN ---
    if menu == "⚙️ Pengaturan":
        st.subheader("⚙️ Data Master Madrasah")
        st.session_state.config['madrasah'] = st.text_input("Nama Madrasah", value=st.session_state.config['madrasah'], placeholder="Contoh: MIN 1 CIAMIS")
        st.session_state.config['guru'] = st.text_input("Nama Guru", value=st.session_state.config['guru'], placeholder="Nama Lengkap & Gelar")
        st.session_state.config['nip_guru'] = st.text_input("NIP Guru", value=st.session_state.config['nip_guru'], placeholder="Masukkan NIP atau '-'")
        st.session_state.config['kepala'] = st.text_input("Nama Kepala", value=st.session_state.config['kepala'], placeholder="Nama Kepala Madrasah")
        st.session_state.config['nip_kepala'] = st.text_input("NIP Kepala", value=st.session_state.config['nip_kepala'], placeholder="NIP Kepala Madrasah")
        if st.button("Simpan Konfigurasi"): st.success("Data berhasil disimpan!")

    # --- MENU BUAT RPP ---
    elif menu == "➕ Buat RPP Baru":
        st.subheader("➕ Rancang RPP Baru")
        c1, c2 = st.columns(2)
        with c1: mapel = st.text_input("Mata Pelajaran")
        with c2: materi = st.text_input("Materi Pokok")
        
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1: inp_jp = st.number_input("Total JP", min_value=1, value=5)
        with ca2: inp_mnt = st.number_input("Menit/JP", min_value=1, value=35)
        with ca3: inp_pt = st.number_input("Jml Pertemuan", min_value=1, value=2)
        with ca4: tgl_input = st.date_input("Tanggal RPP", date.today())
        
        tp_input = st.text_area("Tujuan Pembelajaran (TP)", height=100)
        
        st.write("<b>Pilih Topik KBC (Panca Cinta):</b>", unsafe_allow_html=True)
        list_kbc = ["Cinta Allah/Rasul", "Cinta Ilmu", "Cinta Diri/Sesama", "Cinta Lingkungan", "Cinta Tanah Air"]
        cols_k = st.columns(3)
        topik_kbc = [k for i, k in enumerate(list_kbc) if cols_k[i % 3].checkbox(k, key=f"k_{k}")]

        if st.button("🚀 GENERATE RPP"):
            if not materi or not tp_input:
                st.warning("Mohon lengkapi Materi dan TP.")
            else:
                with st.spinner("⏳ Menyusun RPP..."):
                    try:
                        # Logika pembagian JP
                        jp_rata = inp_jp // inp_pt
                        sisa = inp_jp % inp_pt
                        
                        prompt = f"""
                        Buat RPP HTML lengkap materi "{materi}" ({mapel}).
                        Madrasah: {st.session_state.config['madrasah']}. Guru: {st.session_state.config['guru']}.
                        Alokasi: {inp_jp}x{inp_mnt} Menit ({inp_pt} Pertemuan).
                        
                        STRUKTUR:
                        1. IDENTITAS.
                        2. C. DESAIN: Jabarkan 7 poin. Poin 3 (TP): Satukan narasi "{tp_input}" dengan nilai "{', '.join(topik_kbc)}".
                        3. D. PENGALAMAN: Bagi {inp_pt} pertemuan. P1 = {jp_rata + (1 if sisa > 0 else 0)} JP, sisanya {jp_rata} JP.
                        4. PENGESAHAN: Cantumkan tempat/tanggal 'Ciamis, {tgl_input.strftime('%d %B %Y')}'.
                        5. LAMPIRAN: LKPD & 10 Soal PG.
                        """
                        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(prompt).text
                        html_f = re.sub(r'```html|```', '', res).strip()
                        st.session_state.db_rpp.append({"tgl": tgl_input, "materi": materi, "file": html_f})
                        components.html(f"<div style='background:white; color:black; padding:20px;'>{html_f}</div>", height=800, scrolling=True)
                        st.download_button("📥 Download", html_f, file_name=f"RPP_{materi}.doc")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- MENU RIWAYAT ---
    elif menu == "📜 Riwayat RPP":
        for item in reversed(st.session_state.db_rpp):
            with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
                components.html(f"<div style='background:white; color:black; padding:20px;'>{item['file']}</div>", height=500, scrolling=True)
