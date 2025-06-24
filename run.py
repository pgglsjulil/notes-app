from app import create_app

# Inisialisasi Flask app
app = create_app()

# Run app
if __name__ == '__main__':
    app.run(debug=True)