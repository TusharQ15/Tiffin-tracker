from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
import os
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Security configurations
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max upload size
)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Database configuration
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiffin_orders.db')

# Admin credentials (in production, use a proper user database)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', 
    generate_password_hash('admin123', method='pbkdf2:sha256:600000'))

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

# Security middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page.', 'warning')
            session['next'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def home():
    return render_template('index.html')

@limiter.limit('10 per minute')
@app.route('/order', methods=['POST'])
def place_order():
    try:
        # Input validation
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        meal = request.form.get('meal', '').strip()
        quantity = request.form.get('quantity', '1').strip()
        
        # Validate inputs
        if not all([name, phone, meal, quantity]):
            flash('All fields are required', 'error')
            return redirect(url_for('home'))
            
        if not phone.isdigit() or len(phone) < 10:
            flash('Please enter a valid phone number', 'error')
            return redirect(url_for('home'))
            
        try:
            quantity = int(quantity)
            if quantity < 1 or quantity > 10:  # Reasonable limit
                raise ValueError
        except ValueError:
            flash('Please enter a valid quantity', 'error')
            return redirect(url_for('home'))
        
        # Sanitize inputs
        name = name[:100]  # Limit name length
        phone = phone[:15]  # Limit phone length
        meal = meal[:50]   # Limit meal length
        
        # Save to database with parameterized query
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO orders (name, phone, meal, quantity, date, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                name,
                phone,
                meal,
                quantity,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                request.remote_addr
            ))
            conn.commit()
            flash('Order placed successfully!', 'success')
        except sqlite3.Error as e:
            app.logger.error(f'Database error: {str(e)}')
            flash('An error occurred while processing your order.', 'error')
        finally:
            conn.close()
            
        return redirect(url_for('home'))
        
    except Exception as e:
        app.logger.error(f'Unexpected error: {str(e)}')
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('home'))

@limiter.limit('5 per minute')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('register'))
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
            
        # Create new user
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                     (username, hashed_password, False))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@limiter.limit('5 per minute')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            session['logged_in'] = True
            
            if user['is_admin']:
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
            next_page = session.pop('next', None) or url_for('admin')
            return redirect(next_page)
        else:
            # Simulate password verification delay to prevent timing attacks
            check_password_hash(ADMIN_PASSWORD_HASH, secrets.token_hex(16))
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Create a new session to prevent session fixation
    session.regenerate()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY date DESC")
    orders = c.fetchall()
    conn.close()
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    # For development
    # app.run(debug=True)
    
    # For production with Waitress
    from waitress import serve
    print("Server is running at http://127.0.0.1:5000")
    print("Admin panel: http://127.0.0.1:5000/admin")
    serve(app, host='0.0.0.0', port=5000)
