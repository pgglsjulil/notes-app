from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print('Database tables created successfully!')
        
        # Print database info
        database_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
        if 'mysql' in database_url.lower():
            print('Using MySQL database for production')
        else:
            print('Using SQLite database for development')
            
    except Exception as e:
        print(f'Error creating database tables: {e}')
        raise
