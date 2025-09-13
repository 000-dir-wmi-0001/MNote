
import base64
from http.client import HTTPException
from itertools import count
from typing import Optional
from flask import Blueprint,  make_response, redirect, render_template, render_template_string, request, flash, jsonify, send_file, send_from_directory, url_for,current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import CanvasTemplate, Note, Recording, FeedbackForm, User
from sqlalchemy.sql import func
from . import create_app
from . import db
import json
import os
from datetime import datetime
from flask import send_from_directory
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
from flask_mail import Message
from flask_mail import Mail
from . import mail

views = Blueprint('views', __name__)

# mail = Mail(current_app)


# ------------Pages--------------#

@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated and current_user.is_admin:
        
        return redirect (url_for('admin.admin_dashboard'))
    
    elif current_user.is_authenticated and not current_user.is_admin:
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





@views.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Delete associated recordings, notes, canvases, or any other related data
        user = current_user
        for recording in user.recordings:
            db.session.delete(recording)
        for note in user.notes:
            db.session.delete(note)
        for canvas in user.canvastemplate:
            db.session.delete(canvas)
        
        # Delete the user account
        db.session.delete(user.profile_picture)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting account: {e}")
        return jsonify({'error': 'Error deleting account'}), 500

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Check if a new password is provided
        new_password = request.form.get('password')
        # Check if the provided current password matches the stored hash
        current_password = request.form['current_password']
        
        if check_password_hash(current_user.password, current_password):
            # If the current password is correct, proceed with changing the password
            if new_password:
                hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                current_user.password = hashed_new_password

            # Update other profile information
            current_user.email = request.form['email']
            current_user.user_name = request.form['username']

            # Check if a profile picture is uploaded
            if 'profile-picture' in request.files:
                file = request.files['profile-picture']
                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['IMAGE_FOLDER'], filename))
                    current_user.profile_picture = filename

            flash('Profile updated successfully!', 'success')
            db.session.commit()
            return redirect(url_for('views.profile'))
        else:
            # If the current password is incorrect, show an error message
            flash('Incorrect current password. Update failed!', 'error')

    return render_template('edit_profile.html', user=current_user, title="Update Profile")






@views.route('/upload-profile-picture', methods=['POST'])
def upload_profile_picture():
  if request.method == 'POST':
    file = request.files['profile-picture']
    if file:
      filename = secure_filename(file.filename)
      file.save(os.path.join(current_app.config['IMAGE_FOLDER'], filename))
      return 'Profile picture uploaded successfully!'



IMAGE_FOLDER = 'D:/My_Project/App/uploads'

@views.route('/serve-profile/<string:filename>')
@login_required
def serve_profile(filename):
    # Serve audio files from the specified directory
    return send_from_directory(IMAGE_FOLDER, filename)



# ------------Note--------------#

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

    return render_template('Notes.html', notes=sorted_notes, user=current_user, title='Notes')


 

 # ------------Note-Deletion--------------#


@views.route('/delete-note', methods=['POST'])
@login_required
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


#--- updating from the home page -----#

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

        # audio_file = request.files['audio']
        audio_file = request.files['audio']
        duration = request.form.get('duration')


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
            recording = Recording(data=filename,  user_id=current_user.id,duration=duration)
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
# @views.route('/feedback', methods=['POST','GET'])
# @login_required
# def  feedback():
#     if request.method == 'POST':
#         rating_option = request.form.get('rating')
#         feedback_text = request.form.get('feedback')
#         suggession_text = request.form.get('suggestions')
#         name_f= request.form.get('name')
#         email_f =request.form.get('email')
       
#         new_feedback_form = FeedbackForm(rating=rating_option,answer=feedback_text,  suggestion=suggession_text,name=name_f,email=email_f ,user_id=current_user.id, date=datetime.now())
#         db.session.add(new_feedback_form)
#         db.session.commit()
#         flash('Thank for your feedback!', category='success')

#     return render_template('feedback.html',user=current_user,title="FeedBack")



                # testing


@views.route('/feedback', methods=['POST', 'GET'])
@login_required
def feedback():
    if request.method == 'POST':
        rating_option = request.form.get('rating')
        feedback_text = request.form.get('feedback')
        suggession_text = request.form.get('suggestions')
        name_f = request.form.get('name')
        email_f = request.form.get('email')

        new_feedback_form = FeedbackForm(rating=rating_option, answer=feedback_text, suggestion=suggession_text, name=name_f, email=email_f, user_id=current_user.id, date=datetime.now())
        db.session.add(new_feedback_form)
        db.session.commit()
        flash('Thank you for your feedback!', category='success')

        # Send greeting email
        send_greeting_email(email_f,name_f)

    return render_template('feedback.html', user=current_user, title="Feedback")

def send_greeting_email(recipient_email,name):
    # Create a greeting message
    msg = Message(subject="Thank you for your feedback!",
                  sender="Admin@example.com",
                  recipients=[recipient_email])
    # msg.body = f"Dear {name},\n\nThank you for taking the time to share your feedback with us. Your insights are incredibly valuable as they help us understand how we can better serve you and improve our services.\n\nWe are committed to continuously enhancing your experience and your feedback plays a crucial role in that process.\n\nShould you have any further thoughts or suggestions, please don't hesitate to reach out. We're here to listen!\n\nThank you once again for your contribution to making 'Al_Ansar Technologies' even better.\n\nBest regards,\nThe 'Al_Ansar Technologies' Team"
#     msg.body = f"""Dear {name},

# Thank you for taking the time to share your feedback with us. Your insights are incredibly valuable as they help us understand how we can better serve you and improve our services.

# We are committed to continuously enhancing your experience and your feedback plays a crucial role in that process.

# Should you have any further thoughts or suggestions, please don't hesitate to reach out. We're here to listen!

# Thank you once again for your contribution to making <span style="background-color: lightgreen; padding: 2px; border-radius: 3px;">Al_Ansar Technologies</span> even better.

# Best regards,
# The Al_Ansar Technologies Team"""


#     # Send the email
#     mail.send(msg)

    body = (
        f"Dear *{name}*,\n\n"
        "Thank you for taking the time to share your feedback with us. "
        "Your insights are incredibly valuable as they help us understand how "
        "we can better serve you and improve our services.\n\n"
        "We are committed to continuously enhancing your experience, and your "
        "feedback plays a crucial role in that process.\n\n"
        "Should you have any further thoughts or suggestions, please don't "
        "hesitate to reach out. We're here to listen!\n\n"
        "Thank you once again for your contribution to making 'Al_Ansar Technologies' even better.\n\n"
        "Best regards,\n"
        "The *Al_Ansar Technologies* Team"
    )

    # Set the email body
    msg.body = body
    # Send the email
    mail.send(msg)

#----------------------about-us-------------------------#
@views.route('/about', methods=['POST','GET'])
def about():
    return render_template("about.html",user=current_user, title="AboutUs")






#------------Draw_tamplates-----------#



@views.route('/display_canvas')
@login_required
def display_canvas():
    canvases_list = CanvasTemplate.query.filter_by(user_id=current_user.id).all()
    # canvases = CanvasTemplate.query.filter_by(current_user.id).order_by(CanvasTemplate.id.desc()).all()
    return render_template('display_canvas.html', user=current_user, title="All Pattern", canvases=canvases_list)

@views.route('/draw')
@login_required
def draw():
    return render_template('draw.html', user=current_user, title="DrawNotes")

@views.route('/save_canvas_image', methods=['POST'])
def save_canvas_image():
    try:
        # Get the canvas data, user ID, and template ID from the request
        canvas_data = request.json.get('canvasData')
        user_id = request.json.get('userId')
        
        template_id = request.json.get('templateId')

        image_data = canvas_data.split(',')[1]  # Remove the data URL prefix
        image_bytes = base64.b64decode(image_data)
        existing_files_count = CanvasTemplate.query.filter_by(user_id=user_id).count()
        filename = f"canvas_{user_id}_{template_id}_{existing_files_count + 1}.jpg"  # Use .jpg extension
        filepath = os.path.join(current_app.config['CANVAS_FOLDER'], filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # Add entry in the database for the canvas template
        canvas_template = CanvasTemplate(user_id=user_id, template_data=filename, is_draft=True)
        db.session.add(canvas_template)
        db.session.commit()

        return jsonify({'message': 'Canvas image saved successfully', 'filename': filename}), 200
    except Exception as e:
        return jsonify({'error': f'Error saving canvas image: {str(e)}'}), 500


CANVAS_FOLDER = 'D:/My_Project/App/Canvas_Templetes'

@views.route('/image/<path:filename>')
def serve_image(filename):
    # Serve audio files from the specified directory
    return send_from_directory(CANVAS_FOLDER, filename)




@views.route('/delete-images', methods=['POST'])
@login_required
def delete_image():
    try:
        data = request.get_json()
        image_id = data.get('imageId')
        canvas_template = CanvasTemplate.query.get_or_404(image_id)
        filepath = os.path.join(current_app.config['CANVAS_FOLDER'], canvas_template.template_data)

        db.session.delete(canvas_template)
        db.session.commit()

        os.remove(filepath)  # Delete the canvas image file from the filesystem

        return jsonify({'message': 'Canvas image deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting canvas image: {e}")
        return jsonify({'error': 'Error deleting canvas image'}), 500











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




