from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from app.models import User, Note 
from app import db
from flask_login import current_user, login_user, logout_user, login_required 
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('landing_page.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('main.login'))

        if not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('main.login'))

        login_user(user)
        # flash('Login successful!', 'success') 
        return redirect(url_for('main.home'))

    return render_template('login.html')

@main.route('/logout')
@login_required 
def logout():
    logout_user()
    # flash('You have been logged out.', 'info') 
    return redirect(url_for('main.landing_page'))


@main.route('/home', methods=['GET'])
@login_required 
def home():
    user_notes = current_user.notes.order_by(Note.date_created.desc()).all()
    return render_template('home.html', notes=user_notes)


@main.route('/create_note', methods=['GET', 'POST']) 
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title') 
        content = request.form.get('content')

        if not title or not content:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Title and content cannot be empty!'}), 400
            flash('Title and content cannot be empty!', 'danger')
            return redirect(url_for('main.create_note'))

        new_note = Note(title=title, content=content, author=current_user) 
        db.session.add(new_note)
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Note created successfully!', 'note_id': new_note.id})

        # flash('Note created successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('notes_editor.html')


@main.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash('You are not authorized to view this note.', 'danger')
        abort(403) 
    
    return render_template('view_note.html', note=note)


@main.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            abort(403) 
        flash('You are not authorized to edit this note.', 'danger')
        abort(403) 

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Title and content cannot be empty!'}), 400
            flash('Title and content cannot be empty!', 'danger')
            return redirect(url_for('main.create_note', note_id=note.id))

        note.title = title
        note.content = content
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Note updated successfully!', 'note_id': note.id})

        flash('Note updated successfully!', 'success') 
        return redirect(url_for('main.home'))

    return render_template('notes_editor.html', note=note)


@main.route('/delete_note/<int:note_id>', methods=['POST']) 
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash('You are not authorized to delete this note.', 'danger')
        abort(403) 

    db.session.delete(note)
    db.session.commit()
    # flash('Note deleted successfully!', 'success')
    return redirect(url_for('main.home'))