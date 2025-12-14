# Tiffin Tracker

A modern web application for managing tiffin orders with real-time tracking and admin dashboard.

## Features

- **User Authentication**
  - Secure login/logout
  - User registration
  - Admin dashboard
  - Password hashing with bcrypt

- **Order Management**
  - Place new orders
  - Track order status
  - View order history
  - Update delivery status

- **Admin Features**
  - View all orders
  - Manage users
  - Update order status
  - Generate reports

- **Responsive Design**
  - Mobile-friendly
  - Clean interface
  - Built with Tailwind CSS

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Authentication**: Session-based
- **Styling**: Tailwind CSS
- **Deployment**: Waitress (production WSGI server)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tiffin-tracker.git
   cd tiffin-tracker

### Setup & Installation

1. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   # This will create the database with all necessary tables
   python init_db.py
   ```

4. **Run the application**
   ```bash
   # Development server
   flask run
   
   # Or for production
   waitress-serve --port=5000 app:app
   ```
   The application will be available at `http://localhost:5000`

## Screenshots

### Login Page
![Login Page](screenshots/login.png)

### User Dashboard
![User Dashboard](screenshots/dashboard.png)

### Admin Panel
![Admin Panel](screenshots/admin.png)
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

## Running the Application

### Development Mode
```bash
# Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

# Run the application
flask run
```

### Production Mode
```bash
# Using Waitress
waitress-serve --port=5000 app:app
```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
tiffin-tracker/
├── app.py                # Main application
├── requirements.txt      # Python dependencies
├── static/              # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   └── register.html    # Registration page
└── tiffin_orders.db     # SQLite database file
```

## Security

- Password hashing with PBKDF2
- CSRF protection
- Rate limiting on authentication endpoints
- Secure session management

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

For support, please open an issue in the GitHub repository.
