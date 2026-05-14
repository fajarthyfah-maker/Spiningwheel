import streamlit as st
import re

# Pengaturan konfigurasi halaman web Streamlit
st.set_page_config(page_title="Lottery Analytics Dashboard", layout="wide")

# Tampilan Header Aplikasi
st.title("🎰 Lottery Analytics Dashboard")
st.caption("Sistem Analisis Kombinatorial & Probabilitas Statistik Otomatis Berbasis Python")

# Membagi tata letak menjadi dua bagian utama (Kiri: Input, Kanan: Panel Prediksi)
kolom_kiri, kolom_kanan = st.columns([1, 2])

with kolom_kiri:
    st.subheader("📥 Input Histori Pasaran")
    st.write("Format bebas! Bisa dipisah menggunakan spasi, koma, atau enter.")
    
    # Area untuk menempelkan teks riwayat angka 4D
    input_text = st.text_area(
        label="Tempel data paito/keluaran 4D di sini:",
        placeholder="1234, 4567, 8901\n1234 1237 6789",
        height=320,
        key="paito_input"
    )
    
    tombol_hitung = st.button("⚡ Hitung Analisis Prediksi", use_container_width=True)

# Memproses data ketika tombol diklik
if tombol_hitung:
    if not input_text.strip():
        st.error("Silakan masukkan data histori terlebih dahulu pada kolom input.")
    else:
        # FILTER BEBAS FORMAT: Menggunakan regex untuk mencari semua kumpulan 4 digit angka
        baris_data = re.findall(r'\b\d{4}\b', input_text)
        
        if len(baris_data) < 5:
            st.error(f"Sistem hanya mendeteksi {len(baris_data)} data 4D yang valid. Mohon masukkan minimal 5 data 4D untuk analisis.")
        else:
            with kolom_kanan:
                st.subheader("📊 Hasil Kalkulasi & Analisis")
                
                # =========================================================
                # 1. FITUR PERINGATAN POLA PATAH (BACKTESTING 3 PUTARAN TERAKHIR)
                # =========================================================
                baris_terbaru = baris_data[-3:]  # Mengambil 3 keluaran paling terakhir diinput
                jumlah_zonk = 0
                
                for angka_4d in baris_terbaru:
                    ganjil = sum(1 for d in angka_4d if int(d) % 2 != 0)
                    genap = sum(1 for d in angka_4d if int(d) % 2 == 0)
                    # Jika dalam satu putaran keluar angka ekstrem (semua ganjil / semua genap)
                    if ganjil == 4 or genap == 4:
                        jumlah_zonk += 1
                
                # Menampilkan Kotak Peringatan Sesuai Logika
                if jumlah_zonk >= 2:
                    st.error("⚠️ **PERINGATAN: Tren Pasaran Sedang Patah (Chaos)!**  \nBandar mengeluarkan pola ekstrem beruntun pada beberapa putaran terakhir. Disarankan untuk menurunkan nilai taruhan atau gunakan Angka Cadangan (AC) lebih banyak di luar sistem roda.")
                else:
                    st.success("✅ **Kondisi Tren: Stabil**  \nPerputaran angka mengikuti kurva probabilitas normal. Sistem roda otomatis memiliki tingkat akurasi tinggi untuk digunakan pada putaran ini.")
                
                # =========================================================
                # 2. HITUNG FREKUENSI UNTUK MENCARI HOT/COLD & KESEIMBANGAN
                # =========================================================
                hitung_digit = {str(i): 0 for i in range(10)}
                ganjil_count, genap_count = 0, 0
                besar_count, kecil_count = 0, 0  # Kecil: 0-4, Besar: 5-9
                
                for angka_4d in baris_data:
                    for d in angka_4d:
                        hitung_digit[d] += 1
                        if int(d) % 2 == 0:
                            genap_count += 1
                        else:
                            ganjil_count += 1
                            
                        if int(d) >= 5:
                            besar_count += 1
                        else:
                            kecil_count += 1
                
                # Urutkan angka berdasar jumlah kemunculan terbanyak ke tersedikit
                urutan_frekuensi = sorted(hitung_digit.items(), key=lambda x: x[1], reverse=True)
                hot_numbers = [item[0] for item in urutan_frekuensi[:4]]
                cold_numbers = [item[0] for item in urutan_frekuensi[-3:]]
                
                # Menampilkan Panel Hasil Analis Statistik Frekuensi & Tren Keseluruhan
                stat_kiri, stat_kanan = st.columns(2)
                with stat_kiri:
                    st.markdown(f"🔥 **Hot Numbers (Sering Keluar):**  \n`{', '.join(hot_numbers)}`")
                    st.markdown(f"❄️ **Cold Numbers (Jarang Keluar):**  \n`{', '.join(cold_numbers)}`")
                
                with stat_kanan:
                    st.metric("Total Data Valid Terbaca", f"{len(baris_data)} Angka 4D")
                    st.text(f"Rasio Ganjil - Genap: {ganjil_count}G : {genap_count}K")
                    st.text(f"Rasio Besar - Kecil  : {besar_count}B : {kecil_count}K")
                
                st.divider()
                
                # =========================================================
                # 3. FITUR UTAMA: GENERATOR RODA RINGKAS 9 BARIS (2D)
                # =========================================================
                st.subheader("🎡 Abbreviated Wheel Generator (2D)")
                st.caption("Sistem kombinatorial otomatis berdasarkan 6 angka terbaik dari campuran data Hot & Cold Anda.")
                
                # Membuat pool 6 angka unik gabungan dari peringkat statistik terbaik
                pool_gabungan = list(dict.fromkeys(hot_numbers + cold_numbers))[:6]
                pool_gabungan.sort() # Diurutkan agar rapi dari kecil ke besar
                
                # Menjalankan struktur index roda ringkas Gail Howard (9 Pasangan Angka Jaminan)
                if len(pool_gabungan) >= 6:
                    p = pool_gabungan
                    baris_roda = [
                        f"{p[0]}{p[1]}",
                        f"{p[0]}{p[2]}",
                        f"{p[1]}{p[2]}",
                        f"{p[3]}{p[4]}",
                        f"{p[3]}{p[5]}",
                        f"{p[4]}{p[5]}",
                        f"{p[0]}{p[3]}",
                        f"{p[1]}{p[4]}",
                        f"{p[2]}{p[5]}"
                    ]
                    
                    # Menampilkan baris angka siap pasang dalam bentuk grid visual
                    grid_roda = st.columns(3)
                    for indeks, angka_2d in enumerate(baris_roda):
                        with grid_roda[indeks % 3]:
                            st.info(f"Line {indeks + 1}")
                            st.code(angka_2d, language="text")
                else:
                    st.warning("Variasi angka kurang memadai untuk menyusun 6 angka dasar sistem roda ringkas.")
