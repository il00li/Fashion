from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(200), nullable=False, default="متجر الأزياء اليمني")
    site_description = db.Column(db.Text, default="متجر الأزياء اليمني الأول في اليمن")
    whatsapp_number = db.Column(db.String(20), nullable=False, default="967XXXXXXXX")
    admin_code = db.Column(db.String(50), nullable=False, default="F-S-YA76")
    logo_url = db.Column(db.String(500), default="/static/images/logo.svg")
    primary_color = db.Column(db.String(7), default="#14213D")
    secondary_color = db.Column(db.String(7), default="#5BC0EB")
    text_color = db.Column(db.String(7), default="#FFFFFF")
    font_family = db.Column(db.String(100), default="Cairo")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    sizes = db.Column(db.String(200))  # JSON string: ["صغير", "متوسط", "كبير"]
    colors = db.Column(db.String(200))  # JSON string: ["أحمر", "أزرق", "أسود"]
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='product', lazy=True)
    ratings = db.relationship('Rating', backref='product', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def get_average_rating(self):
        if self.ratings:
            return sum(r.stars for r in self.ratings) / len(self.ratings)
        return 0
    
    def get_sizes_list(self):
        if self.sizes:
            import json
            try:
                return json.loads(self.sizes)
            except:
                return []
        return []
    
    def get_colors_list(self):
        if self.colors:
            import json
            try:
                return json.loads(self.colors)
            except:
                return []
        return []

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    delivery_fee = db.Column(db.Float, nullable=False)
    estimated_time = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    orders = db.relationship('Order', backref='region', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="جديد")  # جديد، قيد التجهيز، تم الإرسال، تم التسليم، ملغي
    whatsapp_sent = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)  # 1-5 stars
    customer_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
