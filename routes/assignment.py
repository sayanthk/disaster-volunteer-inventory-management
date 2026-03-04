from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Assignment, Disaster, User
from forms import AssignmentForm

assignment_bp = Blueprint('assignment', __name__, url_prefix='/assignments')

@assignment_bp.route('/')
@login_required
def index():
    if current_user.role == 'Administrator':
        assignments = Assignment.query.order_by(Assignment.assigned_date.desc()).all()
    else:
        assignments = Assignment.query.filter_by(volunteer_id=current_user.id).order_by(Assignment.assigned_date.desc()).all()
        
    return render_template('assignment/index.html', assignments=assignments)

@assignment_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if current_user.role != 'Administrator':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('assignment.index'))
        
    form = AssignmentForm()
    # Populate volunteers
    form.volunteer_id.choices = [(v.id, f"{v.name} ({v.skills or 'No skills'})") 
                                 for v in User.query.filter_by(role='Volunteer', status='Active').all()]
    form.disaster_id.choices = [(d.id, d.name) for d in Disaster.query.filter_by(status='Active').all()]
    
    if form.validate_on_submit():
        assignment = Assignment(
            volunteer_id=form.volunteer_id.data,
            disaster_id=form.disaster_id.data
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Volunteer successfully assigned.', 'success')
        return redirect(url_for('assignment.index'))
        
    return render_template('assignment/new.html', form=form)

@assignment_bp.route('/<int:id>/complete', methods=['POST'])
@login_required
def complete(id):
    if current_user.role != 'Administrator':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('assignment.index'))
        
    assignment = Assignment.query.get_or_404(id)
    assignment.status = 'Completed'
    from datetime import datetime
    assignment.completion_date = datetime.utcnow()
    db.session.commit()
    flash('Assignment marked as completed. Please rate the volunteer.', 'success')
    return redirect(url_for('volunteer.rate', assignment_id=assignment.id))
