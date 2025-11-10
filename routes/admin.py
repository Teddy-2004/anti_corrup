from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import Admin, Report, Evidence
from datetime import datetime
import csv
from io import StringIO
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('citizen.index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    from models import Report
    from app import db
    
    # Get filter parameters
    status_filter = request.args.get('status', '')
    type_filter = request.args.get('type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    
    # Build query
    query = Report.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if type_filter:
        query = query.filter_by(corruption_type=type_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Report.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Report.created_at <= date_to_obj)
        except ValueError:
            pass
    
    # Order by most recent first
    query = query.order_by(Report.created_at.desc())
    
    # Paginate
    reports = query.paginate(page=page, per_page=current_app.config['REPORTS_PER_PAGE'], error_out=False)
    
    # Get statistics
    total_reports = Report.query.count()
    pending_reports = Report.query.filter_by(status='Pending').count()
    reviewed_reports = Report.query.filter_by(status='Reviewed').count()
    resolved_reports = Report.query.filter_by(status='Resolved').count()
    
    # Get unique corruption types
    corruption_types = db.session.query(Report.corruption_type).distinct().all()
    corruption_types = [t[0] for t in corruption_types]
    
    return render_template('admin/dashboard.html',
                         reports=reports,
                         total_reports=total_reports,
                         pending_reports=pending_reports,
                         reviewed_reports=reviewed_reports,
                         resolved_reports=resolved_reports,
                         corruption_types=corruption_types,
                         status_filter=status_filter,
                         type_filter=type_filter,
                         date_from=date_from,
                         date_to=date_to)

@admin_bp.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    from datetime import datetime
    
    report = Report.query.get_or_404(report_id)
    return render_template('admin/view_report.html', report=report, now=datetime.utcnow)

@admin_bp.route('/report/<int:report_id>/update_status', methods=['POST'])
@login_required
def update_status(report_id):
    from models import Report
    from app import db
    
    report = Report.query.get_or_404(report_id)
    new_status = request.form.get('status')
    
    if new_status in ['Pending', 'Reviewed', 'Resolved']:
        report.status = new_status
        report.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Report {report.report_id} status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin.view_report', report_id=report_id))

@admin_bp.route('/report/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    from models import Report
    from app import db
    
    report = Report.query.get_or_404(report_id)
    
    # Delete associated evidence files
    for evidence in report.evidence:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], evidence.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(report)
    db.session.commit()
    
    flash(f'Report {report.report_id} has been deleted', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/export')
@login_required
def export_reports():
    from models import Report
    
    # Get filter parameters
    status_filter = request.args.get('status', '')
    type_filter = request.args.get('type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = Report.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if type_filter:
        query = query.filter_by(corruption_type=type_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Report.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Report.created_at <= date_to_obj)
        except ValueError:
            pass
    
    reports = query.order_by(Report.created_at.desc()).all()
    
    # Create CSV
    si = StringIO()
    writer = csv.writer(si)
    
    # Write header
    writer.writerow(['Report ID', 'Corruption Type', 'Description', 'Location', 'Status', 
                     'Created At', 'Updated At', 'Evidence Count'])
    
    # Write data
    for report in reports:
        writer.writerow([
            report.report_id,
            report.corruption_type,
            report.description,
            report.location or 'N/A',
            report.status,
            report.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            report.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            len(report.evidence)
        ])
    
    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output

@admin_bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)