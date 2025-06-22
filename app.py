from flask import Flask, render_template, request

# Membuat instance aplikasi Flask

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

# Membuat Rute (Route) untuk Halaman Utama

@app.route('/')
def home(): # Laman home
    
    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): # Laman login
    
    if request.method == 'POST':
        
        return "Anda mencoba untuk login!"

    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup(): # Laman sign-up
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Memastikan server hanya berjalan saat file ini dieksekusi langsung
if __name__ == '__main__':

    # Server akan otomatis restart jika mengubah kode.
    app.run(debug=True)