from datetime import datetime
from app import db

class Order(db.Model):
    """Order model for tiffin orders."""
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, confirmed, delivered, cancelled
    delivery_address = db.Column(db.Text, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_time = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id}>'
    
    def calculate_total(self):
        """Calculate the total amount for the order."""
        self.total_amount = sum(item.quantity * item.meal.price for item in self.items)
        return self.total_amount
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'delivery_address': self.delivery_address,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'delivery_time': self.delivery_time,
            'total_amount': self.total_amount,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    """Order items model for individual items in an order."""
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationships
    meal = db.relationship('Meal')
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
    
    def to_dict(self):
        """Convert order item to dictionary."""
        return {
            'id': self.id,
            'meal_id': self.meal_id,
            'meal_name': self.meal.name if self.meal else None,
            'quantity': self.quantity,
            'unit_price': self.meal.price if self.meal else 0,
            'total_price': self.meal.price * self.quantity if self.meal else 0
        }
