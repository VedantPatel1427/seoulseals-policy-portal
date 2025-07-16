from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads/policies'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Single Database initialization
def init_db():
    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    # Super Admins table
    c.execute('''CREATE TABLE IF NOT EXISTS super_admins
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Companies table
    c.execute('''CREATE TABLE IF NOT EXISTS companies
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  subscription_plan TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Users table (admins and employees)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  company_id INTEGER NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  first_name TEXT,
                  last_name TEXT,
                  role TEXT NOT NULL DEFAULT 'employee',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (company_id) REFERENCES companies (id))''')

    # Policies table
    c.execute('''CREATE TABLE IF NOT EXISTS policies
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  company_id INTEGER NOT NULL,
                  title TEXT NOT NULL,
                  filename TEXT,
                  file_path TEXT,
                  content TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (company_id) REFERENCES companies (id))''')

    # Policy acknowledgments table
    c.execute('''CREATE TABLE IF NOT EXISTS policy_acknowledgments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  policy_id INTEGER NOT NULL,
                  acknowledged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  time_taken INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (policy_id) REFERENCES policies (id))''')

    # Create super admin accounts
    super_admins = [
        ('vedant.patel@seoulseals.com', 'Ved1427ant@patel%2210'),
        ('bharat.bapotra@seoulseals.com', 'Bha1234rat@baporta&0987')
    ]

    for email, password in super_admins:
        c.execute('SELECT id FROM super_admins WHERE email = ?', (email,))
        if not c.fetchone():
            password_hash = generate_password_hash(password)
            c.execute('INSERT INTO super_admins (email, password_hash) VALUES (?, ?)',
                      (email, password_hash))

    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Super Admin Authentication
@app.route('/superadmin/login', methods=['GET', 'POST'])
def superadmin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('seoulseals.db')
        c = conn.cursor()
        c.execute('SELECT id, email, password_hash FROM super_admins WHERE email = ?', (email,))
        admin = c.fetchone()
        conn.close()

        if admin and check_password_hash(admin[2], password):
            session['super_admin_id'] = admin[0]
            session['super_admin_email'] = admin[1]
            flash('Super Admin login successful!', 'success')
            return redirect(url_for('superadmin_dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('superadmin_login.html')

@app.route('/superadmin/logout')
def superadmin_logout():
    session.clear()
    flash('Super Admin logged out', 'info')
    return redirect(url_for('home'))

@app.route('/superadmin/dashboard')
def superadmin_dashboard():
    if 'super_admin_id' not in session:
        flash('Access denied. Super Admin login required.', 'error')
        return redirect(url_for('superadmin_login'))

    # Calculate statistics
    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM companies')
    total_companies = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM users WHERE role = "employee"')
    total_employees = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM policies')
    total_policies = c.fetchone()[0]

    # Get all companies
    c.execute('SELECT * FROM companies ORDER BY created_at DESC')
    companies = c.fetchall()

    conn.close()

    stats = {
        'total_companies': total_companies,
        'total_employees': total_employees,
        'total_policies': total_policies
    }

    return render_template('superadmin_dashboard.html', companies=companies, stats=stats)

# Company Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        step = request.form.get('step', '1')

        if step == '1':
            # Step 1: Choose subscription plan
            plan = request.form['plan']
            session['selected_plan'] = plan
            return render_template('register.html', step=2, plan=plan)

        elif step == '2':
            # Step 2: Company registration form
            try:
                company_name = request.form['company_name']
                admin_email = request.form['admin_email']
                admin_password = request.form['admin_password']
                plan = session.get('selected_plan', 'starter')

                if not company_name or not admin_email or not admin_password:
                    flash('All fields are required', 'error')
                    return render_template('register.html', step=2, plan=plan)

                conn = sqlite3.connect('seoulseals.db')
                c = conn.cursor()

                # Check if email already exists
                c.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
                if c.fetchone():
                    flash('Email already exists. Please use a different email.', 'error')
                    conn.close()
                    return render_template('register.html', step=2, plan=plan)

                # Insert company
                c.execute('INSERT INTO companies (name, subscription_plan) VALUES (?, ?)',
                          (company_name, plan))
                company_id = c.lastrowid

                # Hash admin password
                admin_password_hash = generate_password_hash(admin_password)

                # Create admin user
                c.execute('''INSERT INTO users (company_id, email, password_hash, role)
                             VALUES (?, ?, ?, ?)''',
                          (company_id, admin_email, admin_password_hash, 'admin'))

                conn.commit()
                conn.close()

                # Clear session
                session.pop('selected_plan', None)

                flash('Company registered successfully! You can now login.', 'success')
                return redirect(url_for('login'))

            except Exception as e:
                flash(f'Registration failed: {str(e)}', 'error')
                return render_template('register.html', step=2, plan=session.get('selected_plan', 'starter'))

    return render_template('register.html', step=1)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('seoulseals.db')
        c = conn.cursor()

        # Find user
        c.execute('''SELECT u.id, u.email, u.password_hash, u.first_name, u.last_name, u.role, u.company_id, c.name
                     FROM users u
                     JOIN companies c ON u.company_id = c.id
                     WHERE u.email = ?''', (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_email'] = user[1]
            session['user_role'] = user[5]
            session['company_id'] = user[6]
            session['company_name'] = user[7]

            if user[5] == 'admin':
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                session['user_name'] = f"{user[3] or ''} {user[4] or ''}".strip()
                flash('Employee login successful!', 'success')
                return redirect(url_for('employee_dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('user_role') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))

    # Get statistics
    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    company_id = session['company_id']

    c.execute('SELECT COUNT(*) FROM users WHERE company_id = ? AND role = "employee"', (company_id,))
    employee_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM policies WHERE company_id = ?', (company_id,))
    policy_count = c.fetchone()[0]

    c.execute('''SELECT COUNT(DISTINCT user_id) FROM policy_acknowledgments pa
                 JOIN users u ON pa.user_id = u.id
                 WHERE u.company_id = ?''', (company_id,))
    active_employees = c.fetchone()[0]

    conn.close()

    stats = {
        'employee_count': employee_count,
        'policy_count': policy_count,
        'active_employees': active_employees,
        'completion_rate': round((active_employees / employee_count * 100) if employee_count > 0 else 0, 1)
    }

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('admin_dashboard.html', stats=stats, company_name=company_name)

# Employee Dashboard
@app.route('/employee/dashboard')
def employee_dashboard():
    if session.get('user_role') != 'employee':
        flash('Access denied. Employee login required.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    company_id = session['company_id']

    # List policies for this company
    c.execute('SELECT id, title, filename, created_at FROM policies WHERE company_id = ?', (company_id,))
    policies = c.fetchall()

    # Get acknowledged policies for this user
    c.execute('SELECT policy_id FROM policy_acknowledgments WHERE user_id = ?', (session['user_id'],))
    acknowledged = set(row[0] for row in c.fetchall())

    conn.close()

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('employee_dashboard.html', policies=policies, acknowledged=acknowledged, company_name=company_name)

# Add Employee (Admin only)
@app.route('/admin/employees/add', methods=['GET', 'POST'])
def add_employee():
    if session.get('user_role') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if not first_name or not last_name or not email or not password:
            flash('All fields are required', 'error')
            company_name = session.get('company_name', 'Unknown Company')
            return render_template('add_employee.html', company_name=company_name)

        password_hash = generate_password_hash(password)

        conn = sqlite3.connect('seoulseals.db')
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (session['company_id'], email, password_hash, first_name, last_name, 'employee'))
            conn.commit()
            flash('Employee added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Email already exists for a user.', 'error')
        finally:
            conn.close()
        return redirect(url_for('admin_dashboard'))

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('add_employee.html', company_name=company_name)

# Upload Policy (Admin only)
@app.route('/admin/policies/upload', methods=['GET', 'POST'])
def upload_policy():
    if session.get('user_role') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        file = request.files.get('file')
        content = request.form.get('content', '')

        if not title:
            flash('Title is required', 'error')
            company_name = session.get('company_name', 'Unknown Company')
            return render_template('upload_policy.html', company_name=company_name)

        file_path = None
        filename = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

        conn = sqlite3.connect('seoulseals.db')
        c = conn.cursor()
        c.execute('''INSERT INTO policies (company_id, title, filename, file_path, content)
                     VALUES (?, ?, ?, ?, ?)''',
                  (session['company_id'], title, filename, file_path, content))
        conn.commit()
        conn.close()

        flash('Policy uploaded successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('upload_policy.html', company_name=company_name)

# Manage Policies (Admin only)
@app.route('/admin/policies')
def manage_policies():
    if session.get('user_role') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()
    c.execute('SELECT * FROM policies WHERE company_id = ? ORDER BY created_at DESC', (session['company_id'],))
    policies = c.fetchall()
    conn.close()

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('manage_policies.html', policies=policies, company_name=company_name)

# Track Employees (Admin only)
@app.route('/admin/employees/track')
def track_employees():
    if session.get('user_role') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    # Get employee progress data
    c.execute('''
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            COUNT(pa.id) as policies_completed,
            (SELECT COUNT(*) FROM policies WHERE company_id = ?) as total_policies,
            MAX(pa.acknowledged_at) as last_completion,
            AVG(pa.time_taken) as avg_time_taken
        FROM users u
        LEFT JOIN policy_acknowledgments pa ON u.id = pa.user_id
        WHERE u.company_id = ? AND u.role = "employee"
        GROUP BY u.id, u.first_name, u.last_name, u.email
        ORDER BY u.first_name, u.last_name
    ''', (session['company_id'], session['company_id']))

    employee_progress = c.fetchall()
    conn.close()

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('track_employees.html', employee_progress=employee_progress, company_name=company_name)

# Edit Policy (Admin only)
@app.route('/admin/policies/<int:policy_id>/edit', methods=['GET', 'POST'])
def edit_policy(policy_id):
    if session.get('user_role') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    # Get policy details (must belong to same company)
    c.execute('SELECT * FROM policies WHERE id = ? AND company_id = ?', (policy_id, session['company_id']))
    policy = c.fetchone()

    if not policy:
        flash('Policy not found', 'error')
        conn.close()
        return redirect(url_for('manage_policies'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required', 'error')
            conn.close()
            company_name = session.get('company_name', 'Unknown Company')
            return render_template('edit_policy.html', policy=policy, company_name=company_name)

        # Update policy
        c.execute('''UPDATE policies SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
                     WHERE id = ? AND company_id = ?''',
                  (title, content, policy_id, session['company_id']))
        conn.commit()
        conn.close()

        flash('Policy updated successfully!', 'success')
        return redirect(url_for('manage_policies'))

    conn.close()
    company_name = session.get('company_name', 'Unknown Company')
    return render_template('edit_policy.html', policy=policy, company_name=company_name)

# Delete Policy (Admin only)
@app.route('/admin/policies/<int:policy_id>/delete', methods=['DELETE', 'POST'])
def delete_policy(policy_id):
    if session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    # Verify policy belongs to same company
    c.execute('SELECT id FROM policies WHERE id = ? AND company_id = ?', (policy_id, session['company_id']))
    if not c.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Policy not found'}), 404

    # Delete policy acknowledgments first (cascade)
    c.execute('DELETE FROM policy_acknowledgments WHERE policy_id = ?', (policy_id,))

    # Delete the policy
    c.execute('DELETE FROM policies WHERE id = ? AND company_id = ?', (policy_id, session['company_id']))

    conn.commit()
    conn.close()

    if request.method == 'DELETE':
        return jsonify({'success': True, 'message': 'Policy deleted successfully'})
    else:
        flash('Policy deleted successfully!', 'success')
        return redirect(url_for('manage_policies'))

# View Policy (Employee)
@app.route('/employee/policy/<int:policy_id>')
def view_policy(policy_id):
    if session.get('user_role') != 'employee':
        flash('Access denied. Employee login required.', 'error')
        return redirect(url_for('login'))

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    # Get policy details (must belong to same company)
    c.execute('SELECT * FROM policies WHERE id = ? AND company_id = ?', (policy_id, session['company_id']))
    policy = c.fetchone()

    # Check if already acknowledged
    c.execute('SELECT id FROM policy_acknowledgments WHERE user_id = ? AND policy_id = ?',
              (session['user_id'], policy_id))
    acknowledged = c.fetchone() is not None

    conn.close()

    if not policy:
        flash('Policy not found', 'error')
        return redirect(url_for('employee_dashboard'))

    company_name = session.get('company_name', 'Unknown Company')
    return render_template('view_policy.html', policy=policy, acknowledged=acknowledged, company_name=company_name)

# Policy acknowledgment (Employee only)
@app.route('/employee/acknowledge/<int:policy_id>', methods=['POST'])
def acknowledge_policy(policy_id):
    if session.get('user_role') != 'employee':
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    conn = sqlite3.connect('seoulseals.db')
    c = conn.cursor()

    # Verify policy belongs to same company
    c.execute('SELECT id FROM policies WHERE id = ? AND company_id = ?', (policy_id, session['company_id']))
    if not c.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Policy not found'}), 404

    c.execute('''INSERT INTO policy_acknowledgments (user_id, policy_id, acknowledged_at)
                 VALUES (?, ?, ?)''', (session['user_id'], policy_id, datetime.utcnow()))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Policy acknowledged'})

# Main navigation pages (public)
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact-sales')
def contact_sales():
    return render_template('contact_sales.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/compliance')
def compliance():
    return render_template('compliance.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)