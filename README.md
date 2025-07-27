# MNote - Multi-Format Note Taking Application

MNote is a comprehensive, web-based note-taking application built with Python Flask that supports multiple formats of note creation and management. It provides users with a unified platform to create text notes, voice recordings, and visual drawings, all within a secure, user-friendly environment.

## 🌟 Features

### 📝 Text Notes
- **Rich Text Support**: Create formatted text notes with customizable fonts, styles, and colors
- **Note Organization**: Add titles and organize notes by date
- **Sorting Options**: Sort notes by title, creation date (ascending/descending)
- **Edit & Update**: Modify existing notes with real-time updates

### 🎤 Voice Notes
- **Audio Recording**: Record voice notes directly in the browser
- **Playback Controls**: Play, pause, and control audio recordings
- **Duration Tracking**: Automatic recording duration calculation
- **Audio Management**: Delete unwanted recordings with confirmation

### 🎨 Draw Notes
- **Canvas Drawing**: Create visual notes using an interactive drawing canvas
- **Template System**: Save and reuse drawing templates
- **Image Export**: Save drawings as image files (.jpg format)
- **Gallery View**: Browse all saved drawing templates

### 👤 User Management
- **Secure Authentication**: User registration and login system with password hashing
- **Profile Management**: Customizable user profiles with picture uploads
- **Account Security**: Password change functionality with current password verification
- **Account Deletion**: Complete account removal with data cleanup

### 📧 Feedback System
- **User Feedback**: Collect user ratings, suggestions, and feedback
- **Email Notifications**: Automatic thank-you emails sent to feedback providers
- **Admin Review**: Feedback management through admin dashboard

### 🔐 Admin Dashboard
- **User Overview**: View and manage all registered users
- **Feedback Management**: Review submitted feedback and suggestions
- **Administrative Controls**: Admin-only access to management features

## 🛠️ Technical Stack

### Backend
- **Framework**: Python Flask
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: Flask-Login for session management
- **Email**: Flask-Mail for automated email notifications
- **Security**: Werkzeug for password hashing and file handling

### Frontend
- **Templates**: Jinja2 templating engine
- **Styling**: Custom CSS with responsive design
- **Interactivity**: JavaScript for dynamic features
- **File Handling**: Support for image and audio file uploads

### Database Schema
- **Users**: Authentication, profiles, and admin roles
- **Notes**: Text content with formatting and metadata
- **Recordings**: Audio files with duration tracking
- **Canvas Templates**: Drawing data and image storage
- **Feedback**: User feedback with ratings and suggestions

## 📁 Project Structure

```
MNote/
├── main.py                 # Application entry point
├── website/                # Main application package
│   ├── __init__.py        # App factory and configuration
│   ├── models.py          # Database models and schemas
│   ├── views.py           # Main application routes
│   ├── auth.py            # Authentication routes
│   ├── admin.py           # Admin dashboard routes
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, and static assets
├── uploads/               # User profile pictures
├── audios/                # Voice note recordings
├── Canvas_Templetes/      # Drawing template storage
├── instance/              # Instance-specific files
├── README.md              # Project documentation
├── Report.md              # Technical report
└── LICENSE                # MIT License
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Dependencies
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-login
pip install flask-mail
pip install werkzeug
pip install pillow
```

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/000-dir-wmi-0001/MNote.git
   cd MNote
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:5000`

### Configuration
The application automatically creates:
- SQLite database (`database.db`)
- Required directories for file storage
- Default admin user (admin@momin.com / momin123)

## 📋 Usage Guide

### Getting Started
1. **Registration**: Create a new account through the sign-up page
2. **Login**: Access your account using email/username and password
3. **Dashboard**: Navigate through different note types using the menu

### Creating Notes
- **Text Notes**: Use the Notes section to create formatted text notes
- **Voice Notes**: Click record button to start/stop audio recording
- **Draw Notes**: Use the drawing canvas to create visual notes

### Managing Content
- **Edit**: Click on any note to modify its content
- **Delete**: Remove unwanted notes with confirmation dialogs
- **Sort**: Organize notes using various sorting options

### Profile Management
- **Update Profile**: Change email, username, or password
- **Profile Picture**: Upload and update profile images
- **Account Deletion**: Permanently remove account and all data

## 🔧 Admin Features

### Admin Access
- **Default Admin**: admin@momin.com (password: momin123)
- **Admin Dashboard**: Accessible only to users with admin privileges

### Admin Capabilities
- **User Management**: View all registered users and their details
- **Feedback Review**: Access all user feedback and suggestions
- **System Monitoring**: Monitor application usage and user activity

## 🛡️ Security Features

- **Password Hashing**: Secure password storage using PBKDF2-SHA256
- **Session Management**: Secure user sessions with Flask-Login
- **File Security**: Secure file uploads with filename sanitization
- **Admin Protection**: Role-based access control for admin features

## 📈 Future Enhancements

- **Note Sharing**: Share notes between users
- **Export Options**: Export notes to PDF, Word formats
- **Search Functionality**: Full-text search across all notes
- **Cloud Storage**: Integration with cloud storage services
- **Mobile App**: Native mobile application development
- **Collaboration**: Real-time collaborative note editing

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, feedback, or questions:
- **Email**: admin@momin.com
- **Feedback**: Use the in-app feedback system
- **Issues**: Submit GitHub issues for bug reports

## 🏢 About

Developed by Al_Ansar Technologies as a comprehensive solution for digital note-taking and organization. MNote combines the simplicity of traditional note-taking with the power of modern web technologies.

---

**MNote** - *Your Digital Note-Taking Companion* 📚✨
