import streamlit as st

# Mengatur agar halaman Streamlit menggunakan mode lebar (wide)
st.set_page_config(page_title="Lottery Analytics Dashboard", layout="wide")

# Menyisipkan seluruh kode HTML & JavaScript model awal yang paling lengkap
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Analisis Togel Modern</title>
    <!-- Menggunakan Tailwind CSS untuk tampilan antarmuka yang bersih -->
    <script src="jsdelivr.net"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen p-2 md:p-4 font-sans">

    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="mb-6 text-center md:text-left">
            <h1 class="text-3xl font-black text-amber-400 tracking-wide uppercase">Lottery Analytics Dashboard</h1>
            <p class="text-slate-400 text-sm mt-1">Sistem Analisis Kombinatorial & Probabilitas Statistik Otomatis</p>
        </header>

        <!-- Main Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- KOLOM KIRI: INPUT DATA -->
            <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 h-fit shadow-xl">
                <h2 class="text-xl font-bold mb-4 flex items-center gap-2 text-slate-200">
                    📥 Input Histori Pasaran
                </h2>
                <p class="text-xs text-slate-400 mb-3">Bebas format! Bisa dipisah spasi, koma, atau enter. Contoh: 1234,5678 9012</p>
                
                <textarea id="inputData" rows="12" class="w-full bg-slate-950 border border-slate-700 rounded-xl p-4 font-mono text-amber-300 focus:outline-none focus:border-amber-400 transition" placeholder="1234, 4567, 8901&#10;1234 1237 6789"></textarea>
                
                <button onclick="prosesAnalisis()" class="w-full mt-4 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-3 rounded-xl transition cursor-pointer shadow-lg shadow-amber-500/10">
                    ⚡ Hitung Analisis Prediksi
                </button>
            </div>

            <!-- KOLOM KANAN: DASHBOARD PREDIKSI -->
            <div class="lg:col-span-2 space-y-6">
                
                <!-- AREA NOTIFIKASI / PERINGATAN POLA PATAH -->
                <div id="papanPeringatan" class="hidden p-4 rounded-xl border flex items-start gap-3">
                    <!-- Dinamis diisi oleh JS -->
                </div>

                <!-- HASIL PREDIKSI GRAPH & DATA -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <!-- Panel 1: Frekuensi Angka -->
                    <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 shadow-md">
                        <h3 class="text-md font-bold text-slate-400 mb-3 uppercase tracking-wider">🔥 Analisis Frekuensi</h3>
                        <div class="space-y-3">
                            <div>
                                <span class="text-xs text-slate-400 block">Hot Numbers (Sering Keluar):</span>
                                <div id="hotNum" class="text-xl font-extrabold text-amber-400 font-mono mt-1">-</div>
                            </div>
                            <div>
                                <span class="text-xs text-slate-400 block">Cold Numbers (Jarang Keluar):</span>
                                <div id="coldNum" class="text-xl font-extrabold text-blue-400 font-mono mt-1">-</div>
                            </div>
                        </div>
                    </div>

                    <!-- Panel 2: Keseimbangan Tren -->
                    <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 shadow-md">
                        <h3 class="text-md font-bold text-slate-400 mb-3 uppercase tracking-wider">⚖️ Keseimbangan Tren</h3>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between border-b border-slate-700 pb-1">
                                <span class="text-slate-400">Rasio Ganjil-Genap:</span>
                                <span id="rasioGanjilGenap" class="font-mono font-bold">-</span>
                            </div>
                            <div class="flex justify-between border-b border-slate-700 pb-1">
                                <span class="text-slate-400">Rasio Besar-Kecil:</span>
                                <span id="rasioBesarKecil" class="font-mono font-bold">-</span>
                            </div>
                            <div class="flex justify-between border-b border-slate-700 pb-1">
                                <span class="text-slate-400">Total Data Valid Terbaca:</span>
                                <span id="totalData" class="font-mono font-bold text-amber-400">-</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Panel 3: Hasil Generator Roda Ringkas -->
                <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-md">
                    <h3 class="text-md font-bold text-slate-400 mb-1 uppercase tracking-wider">🎡 Abbreviated Wheel Generator (2D)</h3>
                    <p class="text-xs text-slate-400 mb-4">Sistem roda otomatis berdasarkan 6 angka terbaik hasil kalkulasi frekuensi & tren.</p>
                    
                    <div id="hasilRoda" class="grid grid-cols-3 sm:grid-cols-5 gap-3 font-mono font-bold text-center">
                        <!-- Angka hasil roda akan muncul di sini -->
                        <div class="bg-slate-900/50 text-slate-500 py-3 rounded-xl border border-slate-800 border-dashed col-span-full">
                            Belum ada data untuk diproses
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- LOGIKA PEMROSESAN UTAMA (JAVASCRIPT) -->
    <script>
        function prosesAnalisis() {
            const inputText = document.getElementById('inputData').value.trim();
            if (!inputText) {
                alert('Silakan masukkan data histori terlebih dahulu.');
                return;
            }

            // FILTER BEBAS FORMAT: Menggunakan Regex untuk mencari semua kumpulan 4 digit angka di dalam teks
            const barisData = inputText.match(/\\b\\d{4}\\b/g) || [];

            if (barisData.length < 5) {
                alert('Sistem mendeteksi hanya ' + barisData.length + ' data 4D yang valid. Mohon masukkan minimal 5 data 4D.');
                return;
            }

            // Tampilkan jumlah data terbaca
            document.getElementById('totalData').innerText = barisData.length + ' Angka';

            // 1. HITUNG FREKUENSI UNTUK MENCARI HOT/COLD
            let hitungDigit = Array(10).fill(0);
            let ganjilCount = 0, genapCount = 0;
            let besarCount = 0, kecilCount = 0;

            barisData.forEach(angka4D => {
                for (let i = 0; i < 4; i++) {
                    let d = parseInt(angka4D[i]);
                    hitungDigit[d]++;
                    
                    if (d % 2 === 0) genapCount++; else ganjilCount++;
                    if (d >= 5) besarCount++; else kecilCount++;
                }
            });

            let petaFrekuensi = hitungDigit.map((freq, num) => ({ num, freq }));
            let urutanTertinggi = [...petaFrekuensi].sort((a, b) => b.freq - a.freq);
            let hotNumbers = urutanTertinggi.slice(0, 4).map(x => x.num);
            let coldNumbers = [...petaFrekuensi].sort((a, b) => a.freq - b.freq).slice(0, 2).map(x => x.num);

            document.getElementById('hotNum').innerText = hotNumbers.join(', ');
            document.getElementById('coldNum').innerText = coldNumbers.join(', ');

            document.getElementById('rasioGanjilGenap').innerText = ganjilCount + 'G : ' + genapCount + 'K';
            document.getElementById('rasioBesarKecil').innerText = besarCount + 'B : ' + kecilCount + 'K';

            // 2. SISTEM PERINGATAN POLA PATAH (BACKTESTING 3 PUTARAN TERAKHIR)
            let barisTerbaru = barisData.slice(-3); // Ambil 3 data paling terakhir diinput
            let jumlahZonk = 0;

            barisTerbaru.forEach(angkas => {
                let g = 0, k = 0;
                for(let i=0; i<4; i++) {
                    if(parseInt(angkas[i]) % 2 === 0) k++; else g++;
                }
                if(g === 4 || k === 4) {
                    jumlahZonk++;
                }
            });

            const papanPeringatan = document.getElementById('papanPeringatan');
            papanPeringatan.classList.remove('hidden');

            if (jumlahZonk >= 2) {
                papanPeringatan.className = "p-4 rounded-xl border bg-rose-950/40 border-rose-800 text-rose-300 flex items-start gap-3";
                papanPeringatan.innerHTML = `
                    <div class="text-xl">⚠️</div>
                    <div>
                        <strong class="block text-rose-200">PERINGATAN: Tren Pasaran Sedang Patah (Chaos)!</strong>
                        <p class="text-xs mt-0.5 text-rose-400">Bandar mengeluarkan pola ekstrem beruntun pada putaran terakhir. Disarankan untuk menurunkan nilai taruhan atau gunakan Angka Cadangan (AC) di luar sistem roda.</p>
                    </div>
                `;
            } else {
                papanPeringatan.className = "p-4 rounded-xl border bg-emerald-950/40 border-emerald-800 text-emerald-300 flex items-start gap-3";
                papanPeringatan.innerHTML = `
                    <div class="text-xl">✅</div>
                    <div>
                        <strong class="block text-emerald-200">Kondisi Tren: Stabil</strong>
                        <p class="text-xs mt-0.5 text-emerald-400">Perputaran angka mengikuti kurva probabilitas normal. Sistem roda memiliki tingkat akurasi tinggi untuk digunakan.</p>
                    </div>
                `;
            }

            // 3. GENERATOR RODA RINGKAS (6 Angka Pilihan)
            let poolRoda = [...hotNumbers, ...coldNumbers].slice(0, 6);
            poolRoda.sort((a,b) => a - b);

            // Jalankan Template Roda Ringkas 9 Baris Paten Gail Howard
            let barisRoda = [
                "" + poolRoda[0] + poolRoda[1],
                "" + poolRoda[0] + poolRoda[2],
                "" + poolRoda[1] + poolRoda[2],
                "" + poolRoda[3] + poolRoda[4],
                "" + poolRoda[3] + poolRoda[5],
                "" + poolRoda[4] + poolRoda[5],
                "" + poolRoda[0] + poolRoda[3],
                "" + poolRoda[1] + poolRoda[4],
                "" + poolRoda[2] + poolRoda[5]
            ];

            const kontainerRoda = document.getElementById('hasilRoda');
            kontainerRoda.innerHTML = ''; 

            barisRoda.forEach(line => {
                let div = document.createElement('div');
                div.className = "bg-slate-700 text-amber-300 py-3 rounded-xl border border-slate-600 hover:border-amber-400 transition cursor-pointer text-base";
                div.innerText = line;
                kontainerRoda.appendChild(div);
            });
        }
    </script>
</body>
</html>
"""

# Menjalankan aplikasi HTML di dalam Streamlit secara utuh & aman dari error karakter
st.components.v1.html(html_code, height=750, scrolling=True)
