# Tambahkan 'request' di baris impor ini
from flask import Flask, render_template, request

# 1. Membuat instance aplikasi Flask
#    'app' adalah nama folder utama modul Anda.
app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

# 2. Membuat Rute (Route) untuk Halaman Utama
#    Ini memberi tahu Flask: "Ketika seseorang mengunjungi alamat utama ('/'),
#    jalankan fungsi ini."
@app.route('/')
def home():
    # "render_template" akan secara otomatis mencari file
    # di dalam folder 'template_folder' yang sudah kita tentukan.
    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Jika metodenya POST (saat pengguna mengirimkan form login)
    if request.method == 'POST':
        # Nanti, logika untuk memeriksa username dan password ada di sini
        return "Anda mencoba untuk login!"

    # Jika metodenya GET (saat pengguna baru mengklik link untuk ke halaman login)
    # Tampilkan halaman login.html
    return render_template('login.html')

# Ini memastikan server hanya berjalan saat file ini dieksekusi langsung
if __name__ == '__main__':
    # 'debug=True' sangat membantu saat pengembangan.
    # Server akan otomatis restart jika Anda mengubah kode.
    app.run(debug=True)