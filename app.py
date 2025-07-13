import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "F-S-YA76-secret-key"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///yemen_fashion_store.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to create tables
    import models
    db.create_all()
    
    # Create default admin settings if not exists
    from models import SiteSettings
    if not SiteSettings.query.first():
        default_settings = SiteSettings(
            site_name="متجر الأزياء اليمني",
            site_description="متجر الأزياء اليمني الأول في اليمن",
            whatsapp_number="967XXXXXXXX",
            admin_code="F-S-YA76"
        )
        db.session.add(default_settings)
        db.session.commit()
    
    # Create default regions if not exists
    from models import Region, Category, Product
    if not Region.query.first():
        regions = [
            Region(name="الحديدة - المدينة", delivery_fee=500, estimated_time="يوم واحد", is_active=True),
            Region(name="صنعاء - التحرير", delivery_fee=1000, estimated_time="يومان", is_active=True),
            Region(name="عدن - الشيخ عثمان", delivery_fee=1200, estimated_time="3 أيام", is_active=True)
        ]
        for region in regions:
            db.session.add(region)
        db.session.commit()
    
    # Create default categories if not exists
    if not Category.query.first():
        categories = [
            Category(name="أزياء رجالية", description="ملابس وأزياء للرجال", is_active=True, sort_order=1),
            Category(name="أزياء نسائية", description="ملابس وأزياء للنساء", is_active=True, sort_order=2),
            Category(name="ملابس أطفال", description="ملابس وأزياء للأطفال", is_active=True, sort_order=3),
            Category(name="إكسسوارات", description="إكسسوارات ومجوهرات", is_active=True, sort_order=4)
        ]
        for category in categories:
            db.session.add(category)
        db.session.commit()
    
    # Create sample products if not exists
    if not Product.query.first():
        import json
        sample_products = [
            Product(
                name="ثوب يمني تقليدي",
                description="ثوب يمني تقليدي عالي الجودة مصنوع من أفضل الخامات",
                price=2500.0,
                category_id=1,
                image_url="https://images.unsplash.com/photo-1583391733956-6c78526d362e?w=400",
                sizes=json.dumps(["صغير", "متوسط", "كبير", "كبير جداً"]),
                colors=json.dumps(["أبيض", "بيج", "رمادي"]),
                is_active=True,
                sort_order=1
            ),
            Product(
                name="فستان يمني مطرز",
                description="فستان يمني جميل مطرز بالطريقة التقليدية",
                price=3200.0,
                category_id=2,
                image_url="https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400",
                sizes=json.dumps(["صغير", "متوسط", "كبير"]),
                colors=json.dumps(["أحمر", "أزرق", "أخضر", "ذهبي"]),
                is_active=True,
                sort_order=2
            ),
            Product(
                name="جلابية أطفال",
                description="جلابية جميلة للأطفال مريحة وعملية",
                price=800.0,
                category_id=3,
                image_url="https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400",
                sizes=json.dumps(["2-3 سنوات", "4-5 سنوات", "6-7 سنوات", "8-9 سنوات"]),
                colors=json.dumps(["أزرق", "وردي", "أصفر"]),
                is_active=True,
                sort_order=3
            ),
            Product(
                name="خنجر يمني تقليدي",
                description="خنجر يمني أصيل صناعة حرفية تقليدية",
                price=15000.0,
                category_id=4,
                image_url="https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
                sizes=json.dumps([]),
                colors=json.dumps(["فضي", "ذهبي"]),
                is_active=True,
                sort_order=4
            )
        ]
        for product in sample_products:
            db.session.add(product)
        db.session.commit()

# Import routes
from routes import *
