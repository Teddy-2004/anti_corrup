from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models import Report, Evidence
import os
import secrets
from datetime import datetime

citizen_bp = Blueprint('citizen', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_report_id():
    """Generate unique report ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    random_str = secrets.token_hex(4).upper()
    return f'ACR-{timestamp}-{random_str}'

@citizen_bp.route('/')
def index():
    return render_template('citizen/index.html')

@citizen_bp.route('/report', methods=['GET', 'POST'])
def submit_report():
    from models import Report, Evidence
    from app import db
    if request.method == 'POST':
        corruption_type = request.form.get('corruption_type')
        description = request.form.get('description')
        location = request.form.get('location')
        
        # Validate required fields
        if not corruption_type or not description:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('citizen.submit_report'))
        
        # Create new report
        report = Report(
            report_id=generate_report_id(),
            corruption_type=corruption_type,
            description=description,
            location=location
        )
        
        db.session.add(report)
        db.session.flush()  # Get report ID before committing
        
        # Handle file uploads
        if 'evidence' in request.files:
            files = request.files.getlist('evidence')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to filename to prevent collisions
                    name, ext = os.path.splitext(filename)
                    unique_filename = f"{name}_{secrets.token_hex(8)}{ext}"
                    
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(filepath)
                    
                    # Get file size
                    file_size = os.path.getsize(filepath)
                    
                    # Create evidence record
                    evidence = Evidence(
                        filename=unique_filename,
                        original_filename=filename,
                        file_type=ext[1:],
                        file_size=file_size,
                        report_id=report.id
                    )
                    db.session.add(evidence)
        
        db.session.commit()
        
        flash(f'Report submitted successfully! Your report ID is: {report.report_id}', 'success')
        return redirect(url_for('citizen.success', report_id=report.report_id))
    
    return render_template('citizen/report_form.html')

@citizen_bp.route('/success/<report_id>')
def success(report_id):
    report = Report.query.filter_by(report_id=report_id).first_or_404()
    return render_template('citizen/success.html', report=report)

@citizen_bp.route('/track', methods=['GET', 'POST'])
def track_report():
    if request.method == 'POST':
        report_id = request.form.get('report_id')
        
        if not report_id:
            flash('Please enter a Report ID.', 'danger')
            return redirect(url_for('citizen.track_report'))
        
        report = Report.query.filter_by(report_id=report_id.strip().upper()).first()
        
        if not report:
            flash('Report not found. Please check your Report ID and try again.', 'danger')
            return redirect(url_for('citizen.track_report'))
        
        return redirect(url_for('citizen.manage_report', report_id=report.report_id))
    
    return render_template('citizen/track_report.html')

@citizen_bp.route('/manage/<report_id>', methods=['GET', 'POST'])
def manage_report(report_id):
    report = Report.query.filter_by(report_id=report_id).first_or_404()
    
    # Check if report can be edited (only if status is still Pending)
    can_edit = report.status == 'Pending'
    
    if request.method == 'POST' and can_edit:
        action = request.form.get('action')
        
        if action == 'update':
            # Update report details
            corruption_type = request.form.get('corruption_type')
            description = request.form.get('description')
            location = request.form.get('location')
            
            if corruption_type and description:
                report.corruption_type = corruption_type
                report.description = description
                report.location = location
                report.updated_at = datetime.utcnow()
                
                # Handle new evidence uploads
                if 'evidence' in request.files:
                    files = request.files.getlist('evidence')
                    for file in files:
                        if file and file.filename and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            name, ext = os.path.splitext(filename)
                            unique_filename = f"{name}_{secrets.token_hex(8)}{ext}"
                            
                            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                            file.save(filepath)
                            
                            file_size = os.path.getsize(filepath)
                            
                            evidence = Evidence(
                                filename=unique_filename,
                                original_filename=filename,
                                file_type=ext[1:],
                                file_size=file_size,
                                report_id=report.id
                            )
                            db.session.add(evidence)
                
                db.session.commit()
                flash('Report updated successfully!', 'success')
            else:
                flash('Please fill in all required fields.', 'danger')
        
        elif action == 'delete_evidence':
            evidence_id = request.form.get('evidence_id')
            evidence = Evidence.query.filter_by(id=evidence_id, report_id=report.id).first()
            
            if evidence:
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], evidence.filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                db.session.delete(evidence)
                db.session.commit()
                flash('Evidence file deleted successfully!', 'success')
        
        return redirect(url_for('citizen.manage_report', report_id=report_id))
    
    return render_template('citizen/manage_report.html', report=report, can_edit=can_edit)
