from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    abort,
)
from app.forms import LoginForm, NoteForm, RegistrationForm, DeleteNoteForm
from app.models import User, Note, log_action
from app import db, limiter
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('landing_page.html')


@main.route('/register', methods=['GET', 'POST'])
@limiter.limit('8 per minute')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data

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
        else:
            limiter.reset()

    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
@limiter.limit('8 per minute')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if not user:
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('main.login'))

            if not user.check_password(password):
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('main.login'))

            login_user(user)
            log_action(user.id, 'Login berhasil')
            # flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            limiter.reset()

    return render_template('login.html', form=form)


@main.route('/logout')
@limiter.limit('2 per minute')
@login_required
def logout():
    log_action(current_user.id, 'Logout')
    logout_user()
    # flash('You have been logged out.', 'info')
    return redirect(url_for('main.landing_page'))


@main.route('/home', methods=['GET'])
@login_required
def home():
    delete_form = DeleteNoteForm()
    user_notes = current_user.notes.order_by(Note.date_created.desc()).all()
    return render_template('home.html', notes=user_notes, form=delete_form)


@main.route('/create_note', methods=['GET', 'POST'])
@limiter.limit('4 per minute')
@login_required
def create_note():
    form = NoteForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            if not title or not content:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify(
                        {
                            'success': False,
                            'message': 'Title and content cannot be empty!',
                        }
                    ), 400
                flash('Title and content cannot be empty!', 'danger')
                return redirect(url_for('main.create_note'))

            new_note = Note(title=title, content=content, author=current_user)
            db.session.add(new_note)
            log_action(current_user.id, f'Menambahkan catatan: {title}')
            db.session.commit()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(
                    {
                        'success': True,
                        'message': 'Note created successfully!',
                        'note_id': new_note.id,
                    }
                )

            # flash('Note created successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Error creating note. Please try again.', 'danger')
            limiter.reset()

    return render_template('notes_editor.html', form=form)


@main.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@limiter.limit('4 per minute')
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            abort(403)
        flash('You are not authorized to edit this note.', 'danger')
        abort(403)

    form = NoteForm(obj=note)

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            if not title or not content:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify(
                        {
                            'success': False,
                            'message': 'Title and content cannot be empty!',
                        }
                    ), 400
                flash('Title and content cannot be empty!', 'danger')
                return redirect(url_for('main.edit_note', note_id=note.id))

            note.title = title
            note.content = content
            db.session.commit()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(
                    {
                        'success': True,
                        'message': 'Note updated successfully!',
                        'note_id': note.id,
                    }
                )

            flash('Note updated successfully!', 'success')
            log_action(current_user.id, f'Mengedit catatan: {note.title}')

            return redirect(url_for('main.home'))
        else:
            flash('Error updating note. Please try again.', 'danger')
            limiter.reset()

    return render_template('notes_editor.html', note=note, form=form)


@main.route('/delete_note/<int:note_id>', methods=['POST'])
@limiter.limit('8 per minute')
@login_required
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get_or_404(note_id)
        if note.user_id != current_user.id:
            flash('You are not authorized to delete this note.', 'danger')
            abort(403)

        db.session.delete(note)
        db.session.commit()
        log_action(current_user.id, f'Menghapus catatan: {note.title}')
        # flash('Note deleted successfully!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Invalid form submission. Please try again.', 'danger')
        limiter.reset()

    return redirect(url_for('main.home'))
