import os
import tempfile
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        
    yield app
    
    # Clean up the database file
    with app.app_context():
        db.session.remove()
        db.drop_all()
    os.close(db_fd)
    try:
        os.unlink(db_path)
    except PermissionError:
        # Windows can be slow to release file handles
        pass

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with an authenticated user."""
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    return client
