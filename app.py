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
    from models import Region
    if not Region.query.first():
        regions = [
            Region(name="الحديدة - المدينة", delivery_fee=500, estimated_time="يوم واحد", is_active=True),
            Region(name="صنعاء - التحرير", delivery_fee=1000, estimated_time="يومان", is_active=True),
            Region(name="عدن - الشيخ عثمان", delivery_fee=1200, estimated_time="3 أيام", is_active=True)
        ]
        for region in regions:
            db.session.add(region)
        db.session.commit()

# Import routes
from routes import *
