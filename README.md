# 🔐 SeoulSeals - Policy Acknowledgment Portal

A comprehensive web application for managing IT/security policy acknowledgment between companies and their employees.

## 🚀 Features

### Core Services
- **Global Public Portal** - Professional company interface with client management
- **Private Internal Dashboard** - Administrative control for monitoring and management
- **Client Sub-Sites** - Unique secure portals for each company

### Enterprise Features
- ✅ SSO Integration (Google/Azure)
- ✅ Multi-Factor Authentication (MFA)
- ✅ Digital Signature Integration
- ✅ Policy Quiz & Assessment
- ✅ Auto-Reminder System
- ✅ Mobile Responsive Design
- ✅ Advanced Reporting & Analytics
- ✅ Audit Log Export (CSV/PDF)
- ✅ Policy Version Control
- ✅ Escalation Workflows
- ✅ Multilingual Support
- ✅ End-to-End Data Encryption

## 📁 Project Structure

```
seoulseals-policy-portal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── seoulseals.db         # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Homepage with company info
│   ├── login.html        # User login page
│   ├── register.html     # User registration page
│   ├── admin_dashboard.html    # Admin dashboard
│   ├── employee_dashboard.html # Employee dashboard
│   ├── add_employee.html       # Add employee form
│   ├── upload_policy.html      # Policy upload form
│   ├── manage_policies.html    # Policy management
│   ├── edit_policy.html        # Policy editing
│   ├── track_employees.html    # Employee tracking
│   ├── view_policy.html        # Policy viewing
│   ├── services.html     # Services overview
│   ├── features.html     # Features showcase
│   ├── pricing.html      # Subscription plans
│   ├── contact.html      # Contact information
│   ├── contact_sales.html # Sales contact form
│   ├── security.html     # Security information
│   ├── docs.html         # Documentation
│   ├── help.html         # Help center
│   ├── privacy.html      # Privacy policy
│   ├── terms.html        # Terms of service
│   ├── compliance.html   # Compliance standards
│   └── superadmin_*.html # Super admin templates
├── uploads/              # File upload directory
│   └── policies/         # Policy document storage
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VedantPatel1427/seoulseals-policy-portal.git
   cd seoulseals-policy-portal
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - The database will be automatically created on first run

### 🎯 Default Super Admin Accounts

For demonstration purposes, the application creates two super admin accounts:

- **Email:** `vedant.patel@seoulseals.com` | **Password:** `Ved1427ant@patel%2210`
- **Email:** `bharat.bapotra@seoulseals.com` | **Password:** `Bha1234rat@baporta&0987`

⚠️ **Security Note:** Change these default credentials in production!

## 🔗 Available Routes

### Main Navigation
- `/` - Homepage with company information
- `/services` - Services overview page
- `/features` - Features showcase page
- `/pricing` - Subscription plans page
- `/contact` - Contact information page
- `/register` - Company registration
- `/login` - User login

### Super Admin Portal
- `/superadmin/login` - Super admin login
- `/superadmin/dashboard` - Super admin dashboard
- `/superadmin/logout` - Super admin logout

### Company Admin Portal
- `/admin/dashboard` - Company admin dashboard
- `/admin/employees/add` - Add new employee
- `/admin/employees/track` - Track employee progress
- `/admin/policies` - Manage policies
- `/admin/policies/upload` - Upload new policy
- `/admin/policies/<id>/edit` - Edit policy
- `/admin/policies/<id>/delete` - Delete policy

### Employee Portal
- `/employee/dashboard` - Employee dashboard
- `/employee/policy/<id>` - View and acknowledge policy
- `/employee/acknowledge/<id>` - Policy acknowledgment endpoint

### Information Pages
- `/security` - Security and compliance information
- `/docs` - Documentation center
- `/help` - Help and FAQ
- `/privacy` - Privacy policy
- `/terms` - Terms of service
- `/compliance` - Compliance standards

## 💾 Database Schema

The application uses SQLite with the following tables:

### Super Admins Table
- `id` - Primary key
- `email` - Unique email address
- `password_hash` - Hashed password
- `created_at` - Registration timestamp

### Companies Table
- `id` - Primary key
- `name` - Company name
- `subscription_plan` - Plan type (starter/professional/enterprise)
- `created_at` - Registration timestamp

### Users Table
- `id` - Primary key
- `company_id` - Foreign key to companies
- `email` - Unique email address
- `password_hash` - Hashed password
- `first_name` - Employee first name
- `last_name` - Employee last name
- `role` - User role (admin/employee)
- `created_at` - Registration timestamp

### Policies Table
- `id` - Primary key
- `company_id` - Foreign key to companies
- `title` - Policy title
- `filename` - Original filename
- `file_path` - Storage path
- `content` - Text content
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Policy Acknowledgments Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `policy_id` - Foreign key to policies
- `acknowledged_at` - Acknowledgment timestamp
- `time_taken` - Time spent reading (seconds)

## 🎨 Design Features

### Responsive Design
- Mobile-first responsive layout
- Consistent navigation across all pages
- Professional color scheme (orange/blue gradient)
- Clean typography and spacing
- Hover effects and smooth transitions

### User Experience
- Flash messaging system for notifications
- Progress tracking for policy reading
- Interactive dashboards with statistics
- File upload with drag & drop support
- Real-time form validation

## 🔐 Security Features

- Password hashing with Werkzeug
- Session management for user authentication
- Role-based access control
- SQL injection prevention (parameterized queries)
- File upload security (type validation)
- CSRF protection (Flask built-in)

## 📝 Usage Instructions

### For Companies

1. **Register Your Company:**
   - Visit the homepage and click "Register Company"
   - Choose your subscription plan
   - Fill in company details and admin credentials

2. **Admin Dashboard:**
   - Login with admin credentials
   - Add employees to your system
   - Upload and manage policies
   - Track employee acknowledgment progress

3. **Employee Management:**
   - Add employees with auto-generated emails
   - Set initial passwords for team members
   - Monitor completion rates and progress

### For Employees

1. **Access Portal:**
   - Login with credentials provided by admin
   - View company policies requiring acknowledgment

2. **Policy Acknowledgment:**
   - Read policies thoroughly (progress tracked)
   - Confirm understanding via checkbox
   - Submit acknowledgment (time tracked)

### For Super Admins

1. **System Management:**
   - Login via `/superadmin/login`
   - Monitor all companies and statistics
   - View system-wide analytics

## 🚀 Deployment

### Local Development
```bash
# Clone and setup
git clone https://github.com/VedantPatel1427/seoulseals-policy-portal.git
cd seoulseals-policy-portal
pip install -r requirements.txt
python app.py
```

### Production Deployment

1. **Environment Variables:**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY="your-secure-secret-key-here"
   ```

2. **Database:**
   - For production, consider upgrading to PostgreSQL or MySQL
   - Update connection strings in `app.py`

3. **Web Server:**
   - Use Gunicorn or similar WSGI server
   - Configure reverse proxy (Nginx)
   - Enable HTTPS/SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support:
- Visit `/contact` for contact information
- Use `/help` for frequently asked questions
- Check `/docs` for documentation
- Open an issue on GitHub

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
  - Company registration and management
  - Policy upload and acknowledgment system
  - Admin and employee dashboards
  - Progress tracking and reporting
  - Responsive design and security features

---

**SeoulSeals** - Streamlining IT & Security Policy Management for Modern Enterprises

🌟 **Star this repository** if you find it useful!