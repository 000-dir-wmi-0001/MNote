from flask import Blueprint, flash, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user

from website.models import User
from website.models import FeedbackForm
from . import db
from flask import Blueprint, jsonify, request
from .models import db, User

admin = Blueprint('admin', __name__)

@admin.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.is_authenticated and current_user.is_admin:
            users = User.query.all()
            return render_template('admin_dashboard.html', Users=users, user=current_user.is_admin, title='Dashboard')
    elif current_user.is_authenticated and not current_user.is_admin:
        flash('You do not have permission to access the page!', category='error')
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.home'))

@admin.route('/feedM')
@login_required
def feedback():
    users = FeedbackForm.query.all()

    return render_template( 'feedMag.html',user=current_user.is_admin, Messages=users,title="FeedBack_Management" )




# @admin.route('/delete-user/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     try:
#         user = User.query.get(user_id)
#         if user:
#             for recording in user.recordings:
#                 db.session.delete(recording)
#             for note in user.notes:
#                 db.session.delete(note)

#             db.session.delete(user)
#             db.session.commit()
#             return jsonify({'message': f'User {user.user_name} deleted successfully'}), 200
#         else:
#             return jsonify({'error': 'User not found'}), 404
#     except Exception as e:
#         print(f"Error deleting user: {e}")
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while deleting the user'}), 500


@admin.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        for recording in user.recordings:
            db.session.delete(recording)
        for note in user.notes:
            db.session.delete(note)
        for canvas in user.canvastemplate:
            db.session.delete(canvas)
        db.session.delete(user.profile_picture)
        db.session.delete(user)
        db.session.commit()
        flash('The account has been deleted!','error')
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('admin.admin_dashboard'))



@admin.route('/delete_feedback/<int:feed_id>', methods=['GET', 'POST'])
def delete_feedback(feed_id):
    feedback = FeedbackForm.query.get_or_404(feed_id)
    if request.method == 'POST':
        db.session.delete(feedback)
        db.session.commit()
        flash('FeedBack has been deleted!', 'error')
        return redirect(url_for('admin.feedback'))
    return redirect(url_for('admin.feedback'))





@admin.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



# Handle 404 errors
@admin.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Handle 500 errors
@admin.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback any uncommitted database transactions
    return render_template('500.html'), 500

