import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

# --- KONFIGURASI HALAMAN & SECURITY ---
st.set_page_config(page_title="E-Perangkat KBC Presisi - MIN 1 CIAMIS", layout="wide", page_icon="🏫")

# CSS TAMPILAN (Sembunyikan UI Streamlit & Custom Sidebar)
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
        "madrasah": "Nama Madrasah",
        "guru": "Guru Gaftek",
        "nip_guru": "NIP Guru",
        "kepala": "Nama Kamad.",
        "nip_kepala": "NIP Kamad",
        "thn_ajar": "Tahun ajaran"
    }

# --- SIDEBAR MENU DENGAN LOGO ASLI ---
with st.sidebar:
    # Menggunakan st.image dengan nama file yang ada di GitHub
    try:
        st.image("logo kemenag.png", width=80) # Pastikan nama file ini persis dengan di GitHub
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
    st.caption("v13.8 - Final Reconstruction")

# --- MENU 1: PENGATURAN DATA MASTER ---
if menu == "⚙️ Pengaturan":
    st.subheader("⚙️ Data Master Madrasah")
    st.info("Isi data ini sekali saja. Nanti otomatis masuk ke setiap RPP.")
    
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
    
    # --- INPUT DATA PELAJARAN ---
    c_mapel, c_materi = st.columns(2)
    with c_mapel: mapel = st.text_input("Mata Pelajaran")
    with c_materi: materi = st.text_input("Materi Pokok")
    
    c_kls, c_sem, c_alo, c_tgl = st.columns(4)
    with c_kls: kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], index=2)
    with c_sem: semester = st.selectbox("Semester", ["1 (Ganjil)", "2 (Genap)"], index=1)
    with c_alo: alokasi = st.text_input("Alokasi Waktu", value="4 x 35 Menit (2 Pertemuan)")
    with c_tgl: tgl = st.date_input("Tanggal RPP", date.today())
    
    # --- INPUT KOMPONEN KBC (KONEKSI UTAMA) ---
    st.markdown("<div class='section-header'>KOMPONEN KBC & DEEP LEARNING</div>", unsafe_allow_html=True)
    
    target_belajar = st.text_area("Tujuan Pembelajaran (TP)", placeholder="Contoh: Melalui observasi, murid dapat...", height=100)
    
    c_kbc1, c_kbc2 = st.columns(2)
    with c_kbc1: 
        # UPDATE: DAFTAR MODEL PEMBELAJARAN
        model_p = st.selectbox("Model Pembelajaran", [
            "Problem Based Learning (PBL)", 
            "Project Based Learning (PjBL)", 
            "Literasi, Orientasi, Kolaborasi, Refleksi (LOK-R)",
            "Inquiry Learning",
            "Cooperative Learning",
            "Discovery Learning",
            "Contextual Teaching and Learning (CTL)"
        ])
    with c_kbc2:
        # UPDATE: DAFTAR DIMENSI PROFIL LULUSAN
        profil = st.multiselect("Dimensi Profil Lulusan", [
            "Keimanan & Ketakwaan",
            "Kewargaan",
            "Penalaran Kritis",
            "Kreativitas",
            "Kolaborasi",
            "Kemandirian",
            "Kesehatan",
            "Komunikasi"
        ])
    
    # UPDATE: DAFTAR TOPIK KBC (PANCA CINTA)
    topik_kbc = st.multiselect("Topik KBC (Panca Cinta)", [
        "Cinta kepada Allah/Rasul-Nya",
        "Cinta Ilmu",
        "Cinta Diri dan Sesama",
        "Cinta Lingkungan",
        "Cinta Tanah Air"
    ])

    # --- TOMBOL EKSEKUSI ---
    if st.button("🚀 GENERATE RPP SESUAI REFERENSI"):
        if not materi or not target_belajar:
            st.warning("Mohon lengkapi Materi dan Tujuan Pembelajaran agar RPP akurat.")
        else:
            with st.spinner("⏳ Mengoneksikan data ke struktur RPP KBC..."):
                try:
                    # --- PROMPT RAJAH (SANGAT DETAIL) ---
                    prompt = f"""
                    Berperanlah sebagai Guru Profesional KBC di {st.session_state.config['madrasah']}.
                    Buat RPP HTML lengkap untuk materi "{materi}" ({mapel}) Kelas {kelas}.
                    
                    DATA INPUT (Pastikan masuk ke dokumen):
                    - Guru: {st.session_state.config['guru']} (NIP: {st.session_state.config['nip_guru']})
                    - Kepala: {st.session_state.config['kepala']} (NIP: {st.session_state.config['nip_kepala']})
                    - Tahun: {st.session_state.config['thn_ajar']}
                    - Model: {model_p}
                    - Profil Lulusan: {', '.join(profil)}
                    - Nilai Panca Cinta: {', '.join(topik_kbc)}
                    - Tujuan Pembelajaran: {target_belajar}

                    STRUKTUR HTML (WAJIB IKUTI URUTAN INI):
                    Gunakan tag table border='1' style='border-collapse:collapse; width:100%; font-family:Times New Roman;'

                    1. HEADER: Judul PERENCANAAN PEMBELAJARAN KBC, Materi, Nama Madrasah.
                    
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
                       - 3. Tujuan Pembelajaran (Ambil dari input: {target_belajar})
                       - 4. Praktik Pedagogis (Peran guru sebagai fasilitator)
                       - 5. Kemitraan Pembelajaran (Peran orang tua)
                       - 6. Lingkungan Pembelajaran
                       - 7. Pemanfaatan Digital

                    5. D. PENGALAMAN BELAJAR (Deep Learning):
                       Bagi menjadi Pertemuan 1 & 2. Setiap pertemuan WAJIB strukturnya:
                       - PENDAHULUAN (10 Menit): Apersepsi, Lagu Nasional/Religi.
                       - INTI (50 Menit): Gunakan Sintak {model_p} tapi dikelompokkan dalam 3 Fase Deep Learning:
                         a. MEMAHAMI (Orientasi, Organisasi)
                         b. MENGAPLIKASI (Penyelidikan, Pengembangan Karya)
                         c. MEREFLEKSI (Evaluasi)
                       
                       *WAJIB*: Di tengah Kegiatan Inti, sisipkan kode HTML ini persis:
                       <div style='background-color:#f0fdf4; border-left:5px solid #166534; padding:15px; margin:10px 0;'>
                         <b>Penguatan Nilai KBC (Panca Cinta):</b>
                         [Tulis narasi penguatan karakter {', '.join(topik_kbc)} di sini]
                       </div>

                       - PENUTUP (10 Menit): Refleksi, Doa.

                    6. E. ASESMEN (Awal, Proses, Akhir).

                    7. PENGESAHAN: Tabel tanda tangan Kepala & Guru dengan NIP.

                    8. LAMPIRAN:
                       - 1. Rubrik Penilaian (Tabel KKTP: Mulai Berkembang s.d Baik Sekali)
                       - 2. LKPD (Lembar Kerja Murid Lengkap)
                       - 3. Instrumen Asesmen Akhir (Kisi-kisi & Contoh Soal Pilihan Ganda 10 nomor)

                    HANYA BERIKAN KODE HTML. Jangan ada teks lain.
                    """
                    
                    # --- GENERATE ---
                    raw_response = model_ai.generate_content(prompt).text
                    html_final = re.sub(r'```html|```', '', raw_response).strip()
                    
                    # Simpan ke Riwayat
                    st.session_state.db_rpp.append({"tgl": tgl, "materi": materi, "file": html_final})
                    
                    st.success("RPP KBC Berhasil Disusun!")
                    
                    # --- RENDER HASIL ---
                    components.html(f"""
                        <div style="font-family: 'Times New Roman', serif; background-color: white; color: black; padding: 40px; border: 1px solid #ccc;">
                            {html_final}
                        </div>
                    """, height=800, scrolling=True)
                    
                    st.download_button("📥 Download Dokumen (.doc)", html_final, file_name=f"RPP_{materi}.doc")
                
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# --- MENU 3: RIWAYAT ---
elif menu == "📜 Riwayat RPP":
    st.subheader("📜 Riwayat Dokumen")
    if not st.session_state.db_rpp: st.info("Belum ada dokumen yang dibuat.")
    for i, item in enumerate(reversed(st.session_state.db_rpp)):
        with st.expander(f"📄 {item['tgl']} - {item['materi']}"):
            components.html(f"<div style='background:white; color:black; padding:20px; font-family:serif;'>{item['file']}</div>", height=500, scrolling=True)
            st.download_button("Unduh Ulang", item['file'], file_name="RPP_Re.doc", key=f"re_{i}")

