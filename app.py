import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date
import re

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
        "madrasah": "Nama Madrasah",
        "guru": "Guru Gaftek",
        "nip_guru": "NIP Guru",
        "kepala": "Nama Kamad.",
        "nip_kepala": "NIP Kamad",
        "thn_ajar": "Tahun ajaran"
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
    st.caption("v13.14 - Full Component Fixed")

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
    
    c_kbc1, c_kbc2 = st.columns(2)
    with c_kbc1: 
        model_p = st.selectbox("Model Pembelajaran", ["Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "Literasi, Orientasi, Kolaborasi, Refleksi (LOK-R)", "Inquiry Learning", "Cooperative Learning", "Discovery Learning", "Contextual Teaching and Learning (CTL)"])
    with c_kbc2:
        profil = st.multiselect("Dimensi Profil Lulusan", ["Keimanan & Ketakwaan", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"])
    
    topik_kbc = st.multiselect("Topik KBC (Panca Cinta)", ["Cinta kepada Allah/Rasul-Nya", "Cinta Ilmu", "Cinta Diri dan Sesama", "Cinta Lingkungan", "Cinta Tanah Air"])

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
                    7. PENGESAHAN (Tabel tanda tangan Kamad & Guru).
                    8. LAMPIRAN (Rubrik, LKPD, 10 Soal PG).

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
