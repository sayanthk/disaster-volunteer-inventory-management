from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_login import login_required, current_user
from models import db, Resource, ResourceAllocation, Disaster, ResourceRequest
from forms import ResourceForm, AllocationForm

resource_bp = Blueprint('resource', __name__, url_prefix='/resources')

@resource_bp.route('/')
@login_required
def index():
    resources = Resource.query.all()
    allocations = ResourceAllocation.query.order_by(ResourceAllocation.allocated_date.desc()).all()
    return render_template('resource/index.html', resources=resources, allocations=allocations)

@resource_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if current_user.role not in ['Administrator', 'Inventory Manager']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('resource.index'))
    
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data
        )
        db.session.add(resource)
        db.session.commit()
        flash('Resource added successfully.', 'success')
        return redirect(url_for('resource.index'))
    return render_template('resource/new.html', form=form)

@resource_bp.route('/allocate', methods=['GET', 'POST'])
@login_required
def allocate():
    if current_user.role not in ['Administrator', 'Inventory Manager']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('resource.index'))
        
    form = AllocationForm()
    form.resource_id.choices = [(r.id, f"{r.name} (Available: {r.quantity})") for r in Resource.query.filter(Resource.quantity > 0).all()]
    form.disaster_id.choices = [(d.id, d.name) for d in Disaster.query.filter_by(status='Active').all()]
    
    if form.validate_on_submit():
        resource = Resource.query.get(form.resource_id.data)
        if resource.quantity < form.quantity.data:
            flash('Insufficient resource quantity.', 'danger')
            return redirect(url_for('resource.allocate'))
            
        allocation = ResourceAllocation(
            resource_id=form.resource_id.data,
            disaster_id=form.disaster_id.data,
            quantity=form.quantity.data
        )
        resource.quantity -= form.quantity.data
        db.session.add(allocation)
        db.session.commit()
        flash('Resource allocated successfully.', 'success')
        return redirect(url_for('resource.index'))
        
    return render_template('resource/allocate.html', form=form)

@resource_bp.route('/requests')
@login_required
def requests():
    if current_user.role not in ['Administrator', 'Inventory Manager']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
        
    requests = ResourceRequest.query.order_by(ResourceRequest.request_date.desc()).all()
    return render_template('resource/requests.html', requests=requests)

@resource_bp.route('/requests/<int:id>/<action>', methods=['POST'])
@login_required
def process_request(id, action):
    if current_user.role not in ['Administrator', 'Inventory Manager']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
        
    req = ResourceRequest.query.get_or_404(id)
    
    if req.status != 'Pending':
        flash('This request has already been processed.', 'warning')
        return redirect(url_for('resource.requests'))
        
    if action == 'approve':
        resource = Resource.query.get(req.resource_id)
        if resource.quantity < req.quantity:
            flash(f'Insufficient inventory to approve this request. Requested: {req.quantity}, Available: {resource.quantity}', 'danger')
            return redirect(url_for('resource.requests'))
            
        resource.quantity -= req.quantity
        req.status = 'Approved'
        db.session.commit()
        flash('Request approved.', 'success')
        
    elif action == 'reject':
        req.status = 'Rejected'
        db.session.commit()
        flash('Request rejected.', 'info')
        
    else:
        flash('Invalid action.', 'danger')
        
    return redirect(url_for('resource.requests'))
