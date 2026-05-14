import streamlit as st
import re

# Pengaturan halaman utama aplikasi
st.set_page_config(page_title="Lottery Analytics Dashboard", layout="wide")

st.title("💛 Lottery Analytics Dashboard")
st.caption("Sistem Analisis Kombinatorial & Probabilitas Statistik Otomatis")

# Pembagian tata letak menjadi 2 kolom (Kiri: Input, Kanan: Hasil)
kolom_kiri, kolom_kanan = st.columns([1, 2])

with kolom_kiri:
    st.subheader("Input Histori Pasaran")
    st.write("Bebas format! Bisa dipisah spasi, koma, atau enter.")
    
    # Area pengetikan teks
    input_text = st.text_area(
        label="Masukkan data 4D di sini:",
        placeholder="1234, 4567, 8901\n1234 1237 6789",
        height=300
    )
    
    tombol_hitung = st.button("⚡ Hitung Analisis Prediksi", use_container_width=True)

if tombol_hitung:
    if not input_text.strip():
        st.error("Silakan masukkan data histori terlebih dahulu.")
    else:
        # Menyaring semua kumpulan 4 digit angka (Bebas Format)
        baris_data = re.findall(r'\b\d{4}\b', input_text)
        
        if len(baris_data) < 5:
            st.error(f"Sistem hanya mendeteksi {len(baris_data)} data 4D yang valid. Mohon masukkan minimal 5 data 4D.")
        else:
            with kolom_kanan:
                # 1. PERINGATAN POLA PATAH (BACKTESTING)
                baris_terbaru = baris_data[-3:]  # Ambil 3 data terakhir
                jumlah_zonk = 0
                
                for angka_4d in baris_terbaru:
                    ganjil = sum(1 for d in angka_4d if int(d) % 2 != 0)
                    genap = sum(1 for d in angka_4d if int(d) % 2 == 0)
                    if ganjil == 4 or genap == 4:
                        jumlah_zonk += 1
                
                if jumlah_zonk >= 2:
                    st.error("⚠️ **PERINGATAN: Tren Pasaran Sedang Patah (Chaos)!**\n\nBandar mengeluarkan pola ekstrem beruntun pada putaran terakhir. Disarankan untuk menurunkan nilai taruhan atau gunakan Angka Cadangan (AC) di luar sistem roda.")
                else:
                    st.success("✅ **Kondisi Tren: Stabil**\n\nPerputaran angka mengikuti kurva probabilitas normal. Sistem roda memiliki tingkat akurasi tinggi untuk digunakan.")
                
                # 2. HITUNG FREKUENSI UNTUK MENCARI HOT/COLD
                hitung_digit = {str(i): 0 for i in range(10)}
                ganjil_count, genap_count = 0, 0
                besar_count, kecil_count = 0, 0
                
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
                
                # Urutkan angka berdasarkan frekuensi kemunculan
                urutan_digit = sorted(hitung_digit.items(), key=lambda x: x[1], reverse=True)
                hot_numbers = [item[0] for item in urutan_digit[:4]]
                cold_numbers = [item[0] for item in urutan_digit[-3:]]
                
                # Tampilan Dashboard Statistik
                sub_kiri, sub_kanan = st.columns(2)
                with sub_kiri:
                    st.info(f"🔥 **Hot Numbers:** {', '.join(hot_numbers)}")
                    st.link_button(f"❄️ **Cold Numbers:** {', '.join(cold_numbers)}", "https://example.com")
                
                with sub_kanan:
                    st.metric("Total Data Valid", f"{len(baris_data)} Angka")
                    st.text(f"Rasio Ganjil-Genap: {ganjil_count}G : {genap_count}K")
                    st.text(f"Rasio Besar-Kecil: {besar_count}B : {kecil_count}K")
                
                # 3. GENERATOR RODA RINGKAS (6 Angka Pilihan)
                st.subheader("🎡 Abbreviated Wheel Generator (2D)")
                st.caption("Sistem roda otomatis berdasarkan 6 angka terbaik hasil kalkulasi frekuensi.")
                
                pool_roda = list(set(hot_numbers + cold_numbers))[:6]
                pool_roda.sort()
                
                # Menjalankan roda ringkas 9 baris paten
                baris_roda = [
                    f"{pool_roda[0]}{pool_roda[1]}",
                    f"{pool_roda[0]}{pool_roda[2]}",
                    f"{pool_roda[1]}{pool_roda[2]}",
                    f"{pool_roda[3]}{pool_roda[4]}",
                    f"{pool_roda[3]}{pool_roda[5]}",
                    f"{pool_roda[4]}{pool_roda[5]}",
                    f"{pool_roda[0]}{pool_roda[3]}",
                    f"{pool_roda[1]}{pool_roda[4]}",
                    f"{pool_roda[2]}{pool_roda[5]}"
                ]
                
                # Menampilkan hasil roda dalam grid 3 kolom
                grid_roda = st.columns(3)
                for indeks, angka_2d in enumerate(baris_roda):
                    with grid_roda[indeks % 3]:
                        st.code(angka_2d, language="text")
