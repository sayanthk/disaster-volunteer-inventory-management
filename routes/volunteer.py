from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Rating, Assignment
from forms import RatingForm

volunteer_bp = Blueprint('volunteer', __name__, url_prefix='/volunteers')

@volunteer_bp.route('/')
@login_required
def index():
    if current_user.role != 'Administrator':
        flash('Unauthorized.', 'danger')
        return redirect(url_for('main.index'))
        
    volunteers = User.query.filter_by(role='Volunteer').all()
    return render_template('volunteer/index.html', volunteers=volunteers)

@volunteer_bp.route('/rate/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def rate(assignment_id):
    if current_user.role != 'Administrator':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
        
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.status != 'Completed':
        flash('Volunteer must complete assignment before rating.', 'danger')
        return redirect(url_for('assignment.index'))
        
    form = RatingForm()
    if form.validate_on_submit():
        rating = Rating(
            volunteer_id=assignment.volunteer_id,
            disaster_id=assignment.disaster_id,
            rating_score=form.rating_score.data,
            remarks=form.remarks.data
        )
        db.session.add(rating)
        
        # Recalculate average rating
        volunteer = User.query.get(assignment.volunteer_id)
        current_ratings = Rating.query.filter_by(volunteer_id=volunteer.id).all()
        total_score = sum(r.rating_score for r in current_ratings)
        volunteer.average_rating = total_score / len(current_ratings)
        
        db.session.commit()
        flash('Rating submitted successfully.', 'success')
        return redirect(url_for('volunteer.index'))
        
    return render_template('volunteer/rate.html', form=form, assignment=assignment)
@volunteer_bp.route('/complete_training', methods=['POST'])
@login_required
def complete_training():
    if current_user.role != 'Volunteer':
        flash('Only volunteers can complete training.', 'danger')
        return redirect(url_for('main.index'))
    
    from models import TrainingStatus
    from datetime import datetime
    
    training = TrainingStatus.query.filter_by(user_id=current_user.id, status='Pending').first()
    if training:
        training.status = 'Completed'
        training.completion_date = datetime.utcnow()
        current_user.status = 'Active'
        db.session.commit()
        flash('Congratulations! You have completed the Basic Training and are now active.', 'success')
    else:
        flash('No pending training found.', 'info')
        
    return redirect(url_for('main.index'))
