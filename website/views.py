from flask import Blueprint, current_app, redirect, render_template, request, flash, jsonify, send_from_directory, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Note, Recording, FeedbackForm
from sqlalchemy.sql import func
from . import db
import json
import os
from datetime import datetime






views = Blueprint('views', __name__)






# ------------Pages--------------#

# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == "POST":
#         note_text = request.form.get("note")
#         if len(note_text) > 0:
#             new_note = Note(data=note_text, user=current_user)
#             db.session.add(new_note)
#             db.session.commit()
#         return render_template("home.html", user=current_user)
#     return redirect(url_for('auth.home'))


# this function  is used to display the notes of a specific user and sorting also included in it

# @views.route('/note', methods=['GET', 'POST'])
# @login_required
# def note():
#     if request.method == 'POST':
#         note_text = request.form.get('note')
#         title_text = request.form.get('title')
#         if len(note_text) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note_text, title=title_text, user_id=current_user.id, date=datetime.now())
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')

#     # Retrieve all notes from the database
#     # all_notes = Note.query.all()
#     all_notes = Note.query.filter_by(user_id=current_user.id).all()
    
#     # Get the sorting criterion from the query parameters (if provided)
#     sort_by = request.args.get('sort_by')

#     # Sort the notes based on the chosen criterion
#     if sort_by == 'title':
#         sorted_notes = sorted(all_notes, key=lambda x: x.title)
#     elif sort_by == 'assen':
#         sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=False)
#     elif sort_by == 'dess':
#         sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=True)
#     else:
#         # If no sorting criterion is provided or it's invalid, return the unsorted notes
#         sorted_notes = all_notes

#     return render_template('Notes.html', notes=sorted_notes, user=current_user)




@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if request.method == "POST":
            note_text = request.form.get("note")
            if len(note_text) > 0:
                new_note = Note(data=note_text, user=current_user)
                db.session.add(new_note)
                db.session.commit()
                return render_template("home.html", user=current_user,title="Home")
            else:
                flash('Note is too short!', category='error')
                return render_template("home.html", user=current_user,title="Home")
        else:
            return render_template("home.html", user=current_user,title="Home")
    else:
        return redirect(url_for('auth.home'))

# ------------Profile--------------#

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html',user=current_user, title="Profile")



@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Check if a new password is provided
        new_password = request.form.get('password')
        if new_password:
            # Check if the provided current password matches the stored hash
            current_password = request.form['current_password']
            if check_password_hash(current_user.password, current_password):

                current_user.email = request.form['email']
                current_user.user_name = request.form['username']

                # If the current password is correct, proceed with changing the password
                hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                # Update the user's password in the database
                current_user.password = hashed_new_password
                # flash('Updated successfully!', 'success')
            else:
                # If the current password is incorrect, show an error message
                flash('Incorrect current password. Update failed!.', 'error')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.profile'))

    return render_template('edit_profile.html', user=current_user,title="UpdateProfile")



@views.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Delete associated recordings, notes, or any other related data
        user = current_user
        for recording in user.recordings:
            db.session.delete(recording)
        for note in user.notes:
            db.session.delete(note)

        # Delete the user account
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting account: {e}")
        return jsonify({'error': 'Error deleting account'}), 500



# ------------Note--------------#


# @views.route('/note', methods=['GET', 'POST'])
# @login_required
# def note():
#     if request.method == 'POST':
#         note_text = request.form.get('note')
#         title_text = request.form.get('title')
#         if len(note_text) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_title_note = Note(data=note_text,title=title_text, user_id=current_user.id, date=datetime.now())
#             db.session.add(new_title_note)
#             db.session.commit()
#             flash('Note added!', category='success')
#     return render_template('Notes.html', user=current_user,title="TextNote")




# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     note_id = note['noteId']
#     note = Note.query.get(note_id)
#     if note and note.user_id == current_user.id:
#         db.session.delete(note)
#         db.session.commit()
#     return jsonify({})
    

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted successfully!', category='success')
    else:
        flash('Failed to delete note. Note not found or you do not have permission.', category='error')
    
    return jsonify({})

@views.route('/delete-notes', methods=['POST'])
def delete_notes():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted successfully!', category='success')
    else:
        flash('Failed to delete note. Note not found or you do not have permission.', category='error')
    return jsonify({})


#---updating note from the Note page  -----

@views.route('/update-title-note/<int:note_id>', methods=['POST'])
@login_required
def update_title_note(note_id):
    if request.method == 'POST':
        note_text = request.form.get('update-note')
        title_text = request.form.get('update-title')
        update_color = request.form.get('bg_color')  # Retrieve the background color from the form

        existing_note = Note.query.get(note_id)

        if existing_note and existing_note.user_id == current_user.id:
            existing_note.data = note_text
            existing_note.title = title_text
            existing_note.color = update_color  # Update the color attribute with the new value
            existing_note.date = func.now()

            db.session.commit()
            flash('Note updated!', category='success')
        else:
            flash('Note not found or you do not have permission!', category='error')

    return redirect(url_for('views.note'))


#--- updating from the home page -----



@views.route('/update-title-notes/<int:note_id>', methods=['POST'])
@login_required
def update_title_notes(note_id):
    if request.method == 'POST':
        note_text = request.form.get('update-notes')
        title_text = request.form.get('update-titles')
        update_color = request.form.get('bg_color')  # Retrieve the background color from the form

        existing_note = Note.query.get(note_id)

        if existing_note and existing_note.user_id == current_user.id:
            existing_note.data = note_text
            existing_note.title = title_text
            existing_note.color = update_color  # Update the color attribute with the new value
            existing_note.date = func.now()

            db.session.commit()
            flash('Note updated!', category='success')
        else:
            flash('Note not found or you do not have permission!', category='error')

    return redirect(url_for('views.home'))


#---------Voice-----------#

@views.route('/voice', methods=['POST', 'GET'])
@login_required
def voice():
    user_recordings = Recording.query.filter_by(user_id=current_user.id).all()
    return render_template('Voice.html', user=current_user, recordings=user_recordings,title="VoiceNote")
    


AUDIO_FOLDER = 'audios'

@views.route('/save_audio', methods=['POST'])
def save_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file received'}), 400

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No selected audio file'}), 400

        if audio_file:
            # Query the latest recording ID
            latest_recording = Recording.query.order_by(Recording.id.desc()).first()
            if latest_recording:
                latest_recording_id = latest_recording.id + 1
            else:
                latest_recording_id = 1
            
            # Generate filename: {user_id}_AUD_{recording_id}.webm
            filename = f"{current_user.id}_AUD_{latest_recording_id}.webm"
            filepath = os.path.join(AUDIO_FOLDER, filename)

            # Save the audio file
            audio_file.save(filepath)

            # Insert into the database
            recording = Recording(data=filename, user_id=current_user.id)
            db.session.add(recording)
            db.session.commit()

            return jsonify({'message': 'Audio saved successfully', 'filename': filename}), 200
        else:
            return jsonify({'error': 'No audio data received'}), 400
    except Exception as e:
        return jsonify({'error': f'Error saving audio: {str(e)}'}), 500


#-----------player-----------#

AUDIO_FOLDER = 'D:/My_Project/App/audios'

@views.route('/audio/<path:filename>')
def serve_audio(filename):
    # Serve audio files from the specified directory
    return send_from_directory(AUDIO_FOLDER, filename)



# --- deleting Voice Note------

@views.route('/delete-audio', methods=['POST'])
@login_required
def delete_audio():
    try:
        data = request.get_json()
        recording_id = data.get('recordingId')
        recording = Recording.query.get_or_404(recording_id)
        filepath = os.path.join(AUDIO_FOLDER, recording.data)

        db.session.delete(recording)
        db.session.commit()

        os.remove(filepath)  # Delete the audio file from the filesystem

        return jsonify({'message': 'Recording deleted successfully'})
    except Exception as e:
        print(f"Error deleting recording: {e}")
        return jsonify({'error': 'Error deleting recording'}), 500



#---------------handle the feedback form-------------#
@views.route('/feedback', methods=['POST','GET'])
@login_required
def  feedback():
    if request.method == 'POST':
        rating_option = request.form.get('rating')
        feedback_text = request.form.get('feedback')
        suggession_text = request.form.get('suggestions')
        name_f= request.form.get('name')
        email_f =request.form.get('email')
       
        new_feedback_form = FeedbackForm(rating=rating_option,answer=feedback_text,  suggestion=suggession_text,name=name_f,email=email_f ,user_id=current_user.id, date=datetime.now())
        db.session.add(new_feedback_form)
        db.session.commit()
        flash('Thank for your feedback!', category='success')

    return render_template('feedback.html',user=current_user,title="FeedBack")






#----------------------about-us-------------------------#
@views.route('/about', methods=['POST','GET'])
def about():
    return render_template("about.html",user=current_user)






#------------Draw_tamplates-----------#
TEMPLATES_FOLDER = 'D:\My_Project\App\can_Tampletes'
@views.route('/draw')
@login_required
def draw():
    return render_template('draw.html',user=current_user,title="DrawNotes")




























#---------------handle the backing---------------#

@views.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



# Handle 404 errors
@views.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Handle 500 errors
@views.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback any uncommitted database transactions
    return render_template('500.html'), 500







# testing


# from flask import request

# @views.route('/note', methods=['GET', 'POST'])
# @login_required
# def note():
#     if request.method == 'POST':
#         note_text = request.form.get('note')
#         title_text = request.form.get('title')
#         font_style = request.form.get('font_style')  # Get font style from the form

#         if len(note_text) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note_text, title=title_text, user_id=current_user.id, date=datetime.now(), style=font_style)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')

#     # Retrieve all notes from the database for the current user
#     all_notes = Note.query.filter_by(user_id=current_user.id).all()
    
#     # Get the sorting criterion from the query parameters (if provided)
#     sort_by = request.args.get('sort_by')

#     # Sort the notes based on the chosen criterion
#     if sort_by == 'title':
#         sorted_notes = sorted(all_notes, key=lambda x: x.title)
#     elif sort_by == 'assen':
#         sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=False)
#     elif sort_by == 'dess':
#         sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=True)
#     else:
#         # If no sorting criterion is provided or it's invalid, return the unsorted notes
#         sorted_notes = all_notes

#     return render_template('Notes.html', notes=sorted_notes, user=current_user)


from flask import request
from datetime import datetime
from .models import Note

# @views.route('/note', methods=['GET', 'POST'])
# @login_required
# def note():
#     if request.method == 'POST':
#         note_text = request.form.get('note')
#         title_text = request.form.get('title')
#         font_style = request.form.get('font_style')  # Get font style from the form
#         fontype = request.form.get('fontype')  # Get font style from the form

#         if len(note_text) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note_text, title=title_text, user_id=current_user.id, date=datetime.now(), style=font_style,ftype=fontype)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')

#     # Retrieve all notes from the database for the current user
#     all_notes = Note.query.filter_by(user_id=current_user.id).all()
    
#     # Get the sorting criterion from the query parameters (if provided)
#     sort_by = request.args.get('sort_by')

#     # Sort the notes based on the chosen criterion
#     if sort_by == 'title':
#         sorted_notes = sorted(all_notes, key=lambda x: x.title)
#     elif sort_by == 'assen':
#         sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=False)
#     elif sort_by == 'dess':
#         sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=True)
#     else:
#         # If no sorting criterion is provided or it's invalid, return the unsorted notes
#         sorted_notes = all_notes

#     return render_template('Notes.html', notes=sorted_notes, user=current_user)



@views.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    if request.method == 'POST':
        note_text = request.form.get('note')
        title_text = request.form.get('title')
        font_style = request.form.get('font_style')  # Get font style from the form
        font_italic = request.form.get('font_style_italic')  # Retrieve font italic value
        bg_color = request.form.get('bg_color')


        if len(note_text) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note_text, title=title_text, user_id=current_user.id, date=datetime.now(), style=font_style, ftype=font_italic,color=bg_color)  # Store italic style in ftype column
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    # Retrieve all notes from the database for the current user
    all_notes = Note.query.filter_by(user_id=current_user.id).all()
    
    # Get the sorting criterion from the query parameters (if provided)
    sort_by = request.args.get('sort_by')

    # Sort the notes based on the chosen criterion
    if sort_by == 'title':
        sorted_notes = sorted(all_notes, key=lambda x: x.title)
    elif sort_by == 'assen':
        sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=False)
    elif sort_by == 'dess':
        sorted_notes = sorted(all_notes, key=lambda x: x.id, reverse=True)
    else:
        # If no sorting criterion is provided or it's invalid, return the unsorted notes
        sorted_notes = all_notes

    return render_template('Notes.html', notes=sorted_notes, user=current_user)
