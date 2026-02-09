import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- SISTEM KEAMANAN LOGIN ---
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "MIN1CIAMIS": # GANTI PASSWORD DI SINI
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Hapus password dari memory
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Tampilan layar login
        st.markdown("<h2 style='text-align:center;'>🔐 Akses Terbatas Guru</h2>", unsafe_allow_html=True)
        st.text_input("Masukkan Password Aplikasi", type="password", on_change=password_entered, key="password")
        st.info("Silakan hubungi Admin untuk mendapatkan password.")
        return False
    elif not st.session_state["password_correct"]:
        st.error("😕 Password salah. Silakan coba lagi.")
        st.text_input("Masukkan Password Aplikasi", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# --- EKSEKUSI APLIKASI ---
if check_password():
    # SEMUA KODE ANDA YANG ADA (Sidebars, Menus, dll) DIMASUKKAN KE DALAM BLOK INI
    # Contoh:
    with st.sidebar:
        st.success("✅ Anda berhasil login")
        # ... sisanya kode awal Anda ...

# --- KONFIGURASI HALAMAN & SECURITY ---
st.set_page_config(page_title="E-Perangkat KBC Presisi - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

# CSS TAMPILAN (Sesuai Format Awal Anda)
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
        "madrasah": "",
        "guru": "",
        "nip_guru": "",
        "kepala": "",
        "nip_kepala": "",
        "thn_ajar": ""
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
        "MIN 1 CIAMIS - “Terwujudnya Peserta Didik yang Berprestasi, Berakhlak Mulia, dan Cinta Lingkungan Berlandaskan Nilai-nilai Keimanan dan Ketakwaan.”
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Menu Utama", ["➕ Buat RPP Baru", "📜 Riwayat RPP", "⚙️ Pengaturan"])
    st.divider()
    st.caption("v13.14 - Full Component Fixed")

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
    st.info(f"Format Alokasi di RPP: **{alokasi_final}**")

    c_kls, c_sem = st.columns(2)
    with c_kls: kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], index=2)
    with c_sem: semester = st.selectbox("Semester", ["1 (Ganjil)", "2 (Genap)"], index=1)
    
    st.markdown("<div class='section-header'>KOMPONEN KBC & DEEP LEARNING</div>", unsafe_allow_html=True)
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", placeholder="Contoh: Melalui observasi, murid dapat...", height=100)
    
    # 1. Pilih Model Pembelajaran Tetap Dropdown agar Ringkas
    model_p = st.selectbox("Model Pembelajaran", [
        "Problem Based Learning (PBL)", "Project Based Learning (PjBL)", 
        "LOK-R", "Inquiry Learning", "Cooperative Learning", 
        "Discovery Learning", "Contextual Teaching and Learning (CTL)"
    ])

    # 2. Ganti Dropdown Profil Lulusan Menjadi Checkbox (Dibagi 4 Kolom)
    st.markdown("<br><b>Pilih Dimensi Profil Lulusan:</b>", unsafe_allow_html=True)
    list_profil = ["Keimanan & Ketakwaan", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"]
    cols_p = st.columns(4)
    profil = []
    for i, p in enumerate(list_profil):
        if cols_p[i % 4].checkbox(p, key=f"p_{p}"):
            profil.append(p)

    # 3. Ganti Dropdown Topik KBC Menjadi Checkbox (Dibagi 2 Kolom agar Teks Terbaca Jelas)
    st.markdown("<br><b>Pilih Topik KBC (Panca Cinta):</b>", unsafe_allow_html=True)
    list_kbc = ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"]
    cols_k = st.columns(2)
    topik_kbc = []
    for i, k in enumerate(list_kbc):
        if cols_k[i % 2].checkbox(k, key=f"k_{k}"):
            topik_kbc.append(k)

    if st.button("🚀 GENERATE RPP SESUAI REFERENSI"):
        if not materi or not target_belajar:
            st.warning("Mohon lengkapi Materi dan Tujuan Pembelajaran.")
        else:
            with st.spinner("⏳ Menyusun RPP KBC Presisi Lengkap..."):
                try:
                    # LOGIKA PEMBAGIAN JP
                    jp_rata = inp_jp // inp_pertemuan
                    sisa = inp_jp % inp_pertemuan
                    
                    prompt = f"""
                    Berperanlah sebagai Guru Profesional KBC di {st.session_state.config['madrasah']}.
                    Buat RPP HTML lengkap untuk materi "{materi}" ({mapel}) Kelas {kelas}.
                    
                    DATA INPUT:
                    - Guru: {st.session_state.config['guru']} (NIP: {st.session_state.config['nip_guru']})
                    - Kepala: {st.session_state.config['kepala']} (NIP: {st.session_state.config['nip_kepala']})
                    - Tahun: {st.session_state.config['thn_ajar']}
                    - Model: {model_p}
                    - Profil Lulusan: {', '.join(profil)}
                    - Nilai Panca Cinta: {', '.join(topik_kbc)}
                    - Tujuan Pembelajaran: {target_belajar}

                    STRUKTUR HTML (WAJIB IKUTI URUTAN INI):
                    Gunakan tag table border='1' style='border-collapse:collapse; width:100%; font-family:Times New Roman;'

                    1. HEADER: Judul PERENCANAAN PEMBELAJARAN KBC, Materi.
                    2. A. IDENTITAS MODUL (Tabel): Isi: Madrasah, Guru, Mapel, Kelas/Sem, Materi, Alokasi ({alokasi_final}), Tahun, Model ({model_p}).
                    3. B. IDENTIFIKASI & KBC (Tabel & Narasi)
                       - 1. Kesiapan Murid (Tabel: Kondisi Murid, Materi Prasyarat)
                       - 2. Dimensi Profil Lulusan (Narasi penerapan poin: {', '.join(profil)})
                       - 3. Topik KBC (Narasi penerapan poin: {', '.join(topik_kbc)})
                       - 4. Materi Insersi KBC (Narasi singkat penerapan Panca Cinta di materi ini)

                    4. C. DESAIN PEMBELAJARAN (Sub-bab Wajib Jabarkan Poin Berikut):
                       - 1. Capaian Pembelajaran (CP)
                       - 2. Lintas Disiplin Ilmu (Hubungkan dengan mapel lain)
                       - 3. Tujuan Pembelajaran
                            PENTING: Gabungkan secara otomatis antara "{target_belajar}" dengan nilai-nilai dari "{', '.join(topik_kbc)}".
                            Buatlah narasi yang harmonis.
                            Contoh: "Murid dapat [Isi TP Dasar] sebagai wujud nyata [Isi Topik KBC]..." atau narasi profesional lainnya.
                       - 4. Praktik Pedagogis (Peran guru sebagai fasilitator)
                       - 5. Kemitraan Pembelajaran (Peran orang tua)
                       - 6. Lingkungan Pembelajaran
                       - 7. Pemanfaatan Digital

                    5. D. PENGALAMAN BELAJAR (Deep Learning):
                       WAJIB bagi materi ini menjadi {inp_pertemuan} pertemuan.
                       LOGIKA PEMBAGIAN JP (WAJIB):
                       - Pertemuan 1 s.d pertemuan {inp_pertemuan-1} = {jp_rata + (1 if sisa > 0 else 0)} JP.
                       - Pertemuan terakhir = {jp_rata} JP.
                       
                       Struktur setiap pertemuan:
                       - PENDAHULUAN (Apersepsi, Lagu Nasional/Religi).
                       - INTI (3 Fase Deep Learning: Memahami, Mengaplikasi, Merefleksi dengan Sintak {model_p}).
                       - WAJIB SISIHKAN KOTAK PENGUATAN Karakter Panca Cinta ({', '.join(topik_kbc)}).
                       - PENUTUP (Refleksi, Doa).

                    6. E. ASESMEN (Awal, Proses, Akhir).
                    7. PENGESAHAN: 
                       Buat tabel tanda tangan tanpa border (border:0) yang rapi:
                       - Kolom kiri (Mengetahui): Jabatan 'Kepala Madrasah', Nama '{st.session_state.config['kepala']}', dan NIP '{st.session_state.config['nip_kepala']}'.
                       - Kolom kanan (Pembuat): Tempat dan Tanggal 'Ciamis, {tgl.strftime('%d %B %Y')}', Jabatan 'Guru Mata Pelajaran', Nama '{st.session_state.config['guru']}', dan NIP '{st.session_state.config['nip_guru']}'.
                    8. LAMPIRAN (Rubrik, LKPD, 5 Soal PG).

                    HANYA BERIKAN KODE HTML.
                    """
                    
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    st.success("RPP KBC Berhasil Disusun!")
                    
                    components.html(f"<div style='font-family:serif; background:white; color:black; padding:40px; border:1px solid #ccc;'>{html_final}</div>", height=800, scrolling=True)
                    st.download_button("📥 Download Dokumen (.doc)", html_final, file_name=f"RPP_{materi}.doc")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    st.subheader("📜 Riwayat Dokumen")
    if not st.session_state.db_rpp: st.info("Belum ada dokumen.")
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px; font-family:serif;'>{item['file']}</div>", height=500, scrolling=True)
            st.download_button("Unduh Ulang", item['file'], file_name="RPP_Re.doc", key=f"re_{i}")
