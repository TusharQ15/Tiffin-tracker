# Tiffin Tracker

A web application for managing tiffin orders with user authentication and order tracking.

## Features

- **User Authentication**
- User registration and login/logout
- Password hashing using Werkzeug's security utilities
- Session-based authentication using Flask's session

- **Order Management**
- Place new tiffin orders
- View order status updates

- **Admin Features**
- View all user orders
- Update order status

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, basic JavaScript, Tailwind CSS (via CDN)
- **Database**: SQLite
- **Authentication**: Flask's session management
- **Development**: Pytest for testing

## Project Structure

```text
tiffin-tracker/
├── static/              # Static files
│   └── css/
│       └── style.css    # Custom styles
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── profile.html     # User profile
│   └── admin.html       # Admin dashboard
├── app.py               # Main application entry point
├── config.py            # Configuration settings
├── config_test.py       # Test configuration
├── db_utils.py          # Database helper functions
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── schema.sql           # Database schema
└── wsgi.py             # WSGI entry point
```

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/TusharQ15/Tiffin-tracker.git
   cd Tiffin-tracker
   ```

2. **Create and activate a virtual environment**

   **Windows**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   
   The first run will create the SQLite database automatically. Just start the app and it will initialize the schema if needed.

## Running the Application

### Development Mode

Set environment variables (Windows PowerShell):
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
```

Or on macOS/Linux:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

Run the app:
```bash
flask run
```

The application will be available at `http://localhost:5000`

### Development Credentials

**Warning: For development use only**

- Username: `admin` 
- Password: `admin123` 

In production, change these immediately and use environment variables instead of hardcoding.

## Project Structure

```
tiffin-tracker/
├── app/                 # Application package (views, forms, helpers)
├── static/              # Static files
│   └── css/
│       └── style.css    # Custom styles
├── templates/           # HTML templates
├── app.py               # Application entry point
├── config.py            # Configuration settings
├── db_utils.py          # Database helper functions
├── requirements.txt     # Python dependencies
├── schema.sql           # Database schema
└── tiffin_orders.db     # SQLite database file (development only, will be ignored later)
```

## Security

- Password hashing for stored passwords
- Session-based authentication for logged-in users

> Note: This project is intended for learning and local/demo use. Additional security features like CSRF protection, rate limiting, and production-ready session hardening are not fully implemented yet.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

For support, please open an issue in the GitHub repository.
