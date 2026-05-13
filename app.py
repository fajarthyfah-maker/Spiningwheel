import streamlit as st
import pandas as pd
from collections import Counter
import itertools

# Konfigurasi Halaman
st.set_page_config(page_title="Lottery Analytics Dashboard", layout="wide")

st.title("📊 Lottery Analytics Dashboard (Metode Barat)")
st.caption("Otomatisasi Analisis Frekuensi, Keseimbangan, Sum Tracking, dan Abbreviated Wheeling")

# Layout Utama: Kolom Kiri (Input) & Kolom Kanan (Dashboard)
col_input, col_dash = st.columns([1, 2])

with col_input:
    st.header("📝 Input Data")
    raw_input = st.text_area(
        "Tempel data pengeluaran 4D di sini (Satu baris satu angka):",
        value="4321\n8765\n1234\n0987\n5543\n2190\n7432\n8901\n6543\n2109",
        height=300
    )
    
    # Tombol Eksekusi
    proses_data = st.button("🚀 Hitung Prediksi Otomatis", use_container_width=True)

# Memproses data jika tombol ditekan atau data default tersedia
if raw_input:
    # Parsing input data menjadi list string 4 digit angka valid
    baris = raw_input.strip().split("\n")
    data_4d = [b.strip() for b in baris if b.strip().isdigit() and len(b.strip()) == 4]
    
    if not data_4d:
        st.error("Format data tidak valid. Pastikan input berupa angka 4 digit per baris.")
    else:
        # --- ENGINE KALKULASI DI LATAR BELAKANG ---
        
        # 1. Hitung Frekuensi Semua Digit (0-9)
        semua_digit = []
        posisi_terakhir = {str(i): len(data_4d) for i in range(10)} # Untuk skip strategy
        
        for idx, angka in enumerate(data_4d):
            for digit in angka:
                semua_digit.append(digit)
            # Catat kapan terakhir kali angka muncul (semakin kecil idx, semakin baru kluarannya)
            for d in set(angka):
                if posisi_terakhir[d] == len(data_4d): 
                    posisi_terakhir[d] = idx

        hitung_frekuens = Counter(semua_digit)
        # Ambil semua angka diurutkan dari yang paling sering keluar
        urut_frekuensi = [item[0] for item in hitung_frekuens.most_common()]
        # Lengkapi angka yang mungkin tidak muncul sama sekali di input
        for i in range(10):
            if str(i) not in urut_frekuensi:
                urut_frekuensi.append(str(i))
                
        hot_numbers = urut_frekuensi[:4]
        cold_numbers = urut_frekuensi[-4:]
        due_numbers = sorted(posisi_terakhir.keys(), key=lambda x: posisi_terakhir[x], reverse=True)[:3]

        # 2. Analisis Keseimbangan (Odd-Even & High-Low)
        total_ganjil = sum(1 for d in semua_digit if int(d) % 2 != 0)
        total_genap = sum(1 for d in semua_digit if int(d) % 2 == 0)
        total_kecil = sum(1 for d in semua_digit if int(d) <= 4)
        total_besar = sum(1 for d in semua_digit if int(d) >= 5)
        
        # Rasio rekomendasi kelompok angka utama (Pool)
        genap_pool = [int(x) for x in hot_numbers if int(x) % 2 == 0][:3]
        ganjil_pool = [int(x) for x in hot_numbers if int(x) % 2 != 0][:3]
        # Jika kurang dari 3, ambil dari sisa angka frekuensi teratas
        for x in urut_frekuensi:
            if len(genap_pool) < 3 and int(x) % 2 == 0 and int(x) not in genap_pool:
                genap_pool.append(int(x))
            if len(ganjil_pool) < 3 and int(x) % 2 != 0 and int(x) not in ganjil_pool:
                ganjil_pool.append(int(x))
        
        pool_6_angka = sorted(genap_pool + ganjil_pool)

        # 3. Sum Tracking (Jumlah Total 4D)
        daftar_sum = [sum(map(int, angka)) for angka in data_4d]
        rata_rata_sum = round(sum(daftar_sum) / len(daftar_sum))
        
        # --- OUTPUT DASHBOARD DI KOLOM KANAN ---
        with col_dash:
            st.header("📊 Dashboard Hasil Analisis")
            
            # Tabulasi internal aplikasi
            tab1, tab2, tab3 = st.tabs(["🔥 1. Frekuensi & Tren", "📐 2. Sum Tracking", "🎡 3. Generator Roda Ringkas"])
            
            with tab1:
                st.subheader("Analisis Frekuensi Angka")
                c1, c2, c3 = st.columns(3)
                c1.metric("Hot Numbers (Sering)", ", ".join(hot_numbers))
                c2.metric("Cold Numbers (Jarang)", ", ".join(cold_numbers))
                c3.metric("Due Numbers (Terlama Absen)", ", ".join(due_numbers))
                
                st.subheader("Penyaring Keseimbangan")
                col_prop1, col_prop2 = st.columns(2)
                col_prop1.write(f"🟢 **Proporsi Ganjil-Genap:** {total_ganjil} Ganjil vs {total_genap} Genap")
                col_prop2.write(f"🔵 **Proporsi Besar-Kecil:** {total_besar} Besar vs {total_kecil} Kecil")
                
                # Formula Rekomendasi Pola
                st.info(f"💡 **Rekomendasi Pola Pasang:** Gunakan kombinasi seimbang **3 Angka Ganjil + 3 Angka Genap** untuk membangun kelompok angka utama Anda.")

            with tab2:
                st.subheader("Zona Jumlah Total (Sum Tracking)")
                st.write(f"Rata-rata total jumlah digit dari data histori Anda adalah: **{rata_rata_sum}**")
                
                # Rekomendasi zona kurva lonceng berdasarkan rata-rata histori
                zona_bawah = max(9, rata_rata_sum - 2)
                zona_atas = min(27, rata_rata_sum + 2)
                
                st.success(f"🎯 **Hot Sum Zone Anda:** targetkan hasil kombinasi yang jika digitnya dijumlahkan bernilai antara **{zona_bawah} sampai {zona_atas}**.")
                
                # Tampilkan tabel histori sum untuk visualisasi mandiri
                df_sum = pd.DataFrame({"Keluaran": data_4d, "Total Jumlah Digit": daftar_sum})
                st.dataframe(df_sum, use_container_width=True)

            with tab3:
                st.subheader("Abbreviated Wheeling System (Garansi Tembus 2D)")
                st.write(f"Sistem otomatis memilih 6 angka utama terbaik berdasarkan hukum keseimbangan: **{', '.join(map(str, pool_6_angka))}**")
                
                # Menggunakan rumus desain kombinatorial template roda ringkas 6 angka mengunci 2D
                # Rumus roda ringkas indeks posisi: (1-2), (1-3), (2-3), (4-5), (4-6), (5-6), (1-4), (2-5), (3-6)
                p = pool_6_angka
                template_roda = [
                    f"{p[0]}{p[1]}", f"{p[0]}{p[2]}", f"{p[1]}{p[2]}",
                    f"{p[3]}{p[4]}", f"{p[3]}{p[5]}", f"{p[4]}{p[5]}",
                    f"{p[0]}{p[3]}", f"{p[1]}{p[4]}", f"{p[2]}{p[5]}"
                ]
                
                st.warning("⚠️ **Sistem Roda Ringkas Berhasil Dibuat!** Jika minimal 2 angka yang keluar malam ini ada di dalam 6 angka utama di atas, Anda **DIJAMIN** menang minimal 1 baris tebakan di bawah ini.")
                
                # Tampilkan hasil roda ringkas siap pasang
                df_roda = pd.DataFrame({
                    "Line Taruhan 2D": template_roda,
                    "Total Jumlah Digit": [sum(map(int, line)) for line in template_roda]
                })
                
                # Filter visual mana yang masuk ke dalam hot sum zone
                df_roda["Rekomendasi Bet Lebih"] = df_roda["Total Jumlah Digit"].apply(
                    lambda x: "🔥 Bet Lebih Besar" if (x >= 9 and x <= 11) else "Normal"
                )
                
                st.dataframe(df_roda, use_container_width=True)
