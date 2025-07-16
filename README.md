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
│   ├── view_policy.html        # Policy viewing
│   ├── track_employees.html    # Employee tracking
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
│   └── compliance.html   # Compliance standards
├── uploads/              # Upload directories
│   └── policies/         # Policy files (auto-created)
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

2. **Install Python dependencies:**
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

### Super Admin Access
Two super admin accounts are pre-configured:
- Email: `vedant.patel@seoulseals.com` | Password: `Ved1427ant@patel%2210`
- Email: `bharat.bapotra@seoulseals.com` | Password: `Bha1234rat@baporta&0987`

Access super admin panel at: `http://localhost:5000/superadmin/login`

## 🔗 Available Routes

### Public Pages
- `/` - Homepage with company information
- `/services` - Services overview page
- `/features` - Features showcase page
- `/pricing` - Subscription plans page
- `/contact` - Contact information page
- `/security` - Security and compliance information
- `/docs` - Documentation center
- `/help` - Help and FAQ
- `/privacy` - Privacy policy
- `/terms` - Terms of service
- `/compliance` - Compliance standards

### Authentication
- `/register` - Company registration (2-step process)
- `/login` - User login (admin/employee)
- `/logout` - User logout
- `/superadmin/login` - Super admin login

### Admin Dashboard (requires admin login)
- `/admin/dashboard` - Main admin dashboard
- `/admin/employees/add` - Add new employee
- `/admin/policies/upload` - Upload new policy
- `/admin/policies` - Manage all policies
- `/admin/policies/<id>/edit` - Edit specific policy
- `/admin/employees/track` - Track employee progress

### Employee Portal (requires employee login)
- `/employee/dashboard` - Employee dashboard
- `/employee/policy/<id>` - View and acknowledge policy
- `/employee/acknowledge/<id>` - Acknowledge policy (POST)

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

### Users Table (Admin & Employees)
- `id` - Primary key
- `company_id` - Foreign key to companies
- `email` - Unique email address
- `password_hash` - Hashed password
- `first_name` - First name
- `last_name` - Last name
- `role` - User role (admin/employee)
- `created_at` - Registration timestamp

### Policies Table
- `id` - Primary key
- `company_id` - Foreign key to companies
- `title` - Policy title
- `filename` - Original file name
- `file_path` - Path to uploaded file
- `content` - Policy content (text)
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
- Real-time form validation
- Auto-save functionality (where applicable)
- Intuitive navigation and workflows

## 🔐 Security Features

- Password hashing with Werkzeug
- Session management for user authentication
- Role-based access control
- CSRF protection (Flask built-in)
- SQL injection prevention (parameterized queries)
- File upload validation and security
- Secure filename handling

## 📝 Usage Instructions

### For Super Admins
1. Access super admin panel at `/superadmin/login`
2. Monitor all companies and overall statistics
3. View company registrations and user activity

### For Company Registration
1. Visit `/register` to start registration
2. Choose subscription plan (Starter/Professional/Enterprise)
3. Enter company details and admin credentials
4. Login with admin account to access dashboard

### For Company Admins
1. Login at `/login` with admin credentials
2. Access admin dashboard to manage:
   - Add employees to the system
   - Upload and manage company policies
   - Track employee policy acknowledgment progress
   - Edit existing policies and content

### For Employees
1. Login at `/login` with employee credentials
2. View assigned company policies
3. Read policies in full-screen view
4. Acknowledge policies after reading
5. Track personal progress

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
For production deployment, consider:
- Change the `secret_key` in `app.py`
- Use a production WSGI server (gunicorn, uWSGI)
- Set up proper database (PostgreSQL, MySQL)
- Configure reverse proxy (nginx, Apache)
- Enable HTTPS/SSL
- Set up file storage (AWS S3, etc.)

### Environment Variables
For production, set these environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=your-database-url
```

## 📊 Features Highlights

### Admin Features
- **Employee Management**: Add employees with auto-generated emails
- **Policy Management**: Upload, edit, and organize company policies
- **Progress Tracking**: Real-time monitoring of employee compliance
- **Analytics Dashboard**: Visual statistics and completion rates
- **File Management**: Support for PDF, DOC, DOCX, and TXT files

### Employee Features
- **Policy Portal**: Clean interface for viewing company policies
- **Reading Tracking**: System tracks reading progress and time
- **Acknowledgment System**: Secure policy acknowledgment workflow
- **Progress Dashboard**: Personal compliance tracking
- **Mobile Responsive**: Full functionality on mobile devices

### Enterprise Features
- **Multi-Company Support**: Isolated company environments
- **Role-Based Access**: Separate admin and employee interfaces
- **Audit Trail**: Complete acknowledgment history
- **Export Capabilities**: CSV export for compliance reporting
- **Scalable Architecture**: SQLite for development, easily upgradeable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions, issues, or support:
- Create an issue on GitHub
- Visit `/contact` for contact information
- Use `/help` for frequently asked questions
- Check `/docs` for detailed documentation

## 🔄 Recent Updates

- ✅ Complete Flask application with authentication
- ✅ Admin and employee dashboards
- ✅ Policy upload and management system
- ✅ Employee progress tracking
- ✅ Responsive design for all devices
- ✅ File upload support for multiple formats
- ✅ Real-time progress monitoring
- ✅ Export functionality for compliance

---

**SeoulSeals** - Streamlining IT & Security Policy Management for Modern Enterprises

🌟 **Star this repository** if you find it useful!

📧 **Contact**: For enterprise inquiries, reach out through the contact page.