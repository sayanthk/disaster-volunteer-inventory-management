from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Disaster, Assignment
from forms import DisasterForm

disaster_bp = Blueprint('disaster', __name__, url_prefix='/disasters')

@disaster_bp.route('/')
@login_required
def index():
    disasters = Disaster.query.order_by(Disaster.created_date.desc()).all()
    return render_template('disaster/index.html', disasters=disasters)

@disaster_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if current_user.role != 'Administrator':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('disaster.index'))
    
    form = DisasterForm()
    if form.validate_on_submit():
        disaster = Disaster(
            name=form.name.data,
            location=form.location.data,
            severity=form.severity.data,
            required_skills=form.required_skills.data
        )
        db.session.add(disaster)
        db.session.commit()
        flash('Disaster event created successfully.', 'success')
        return redirect(url_for('disaster.index'))
    return render_template('disaster/new.html', form=form)

@disaster_bp.route('/<int:id>')
@login_required
def view(id):
    disaster = Disaster.query.get_or_404(id)
    return render_template('disaster/view.html', disaster=disaster)
