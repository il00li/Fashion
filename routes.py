from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import *
import json
from urllib.parse import quote
from datetime import datetime
import logging

# Helper function to check admin authentication
def is_admin_authenticated():
    return session.get('admin_authenticated', False)

# Helper function to log admin actions
def log_admin_action(action, details=""):
    if is_admin_authenticated():
        log_entry = AdminLog(
            action=action,
            details=details,
            ip_address=request.remote_addr
        )
        db.session.add(log_entry)
        db.session.commit()

@app.route('/')
def index():
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    products = Product.query.filter_by(is_active=True).order_by(Product.sort_order).all()
    settings = SiteSettings.query.first()
    return render_template('index.html', categories=categories, products=products, settings=settings)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    ratings = Rating.query.filter_by(product_id=product_id).order_by(Rating.created_at.desc()).all()
    comments = Comment.query.filter_by(product_id=product_id, is_approved=True).order_by(Comment.created_at.desc()).all()
    regions = Region.query.filter_by(is_active=True).all()
    settings = SiteSettings.query.first()
    return render_template('product.html', product=product, ratings=ratings, comments=comments, regions=regions, settings=settings)

@app.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id, is_active=True).order_by(Product.sort_order).all()
    settings = SiteSettings.query.first()
    return render_template('index.html', products=products, selected_category=category, settings=settings)

@app.route('/add_rating/<int:product_id>', methods=['POST'])
def add_rating(product_id):
    stars = int(request.form.get('stars'))
    customer_name = request.form.get('customer_name', 'مجهول')
    
    rating = Rating(
        product_id=product_id,
        stars=stars,
        customer_name=customer_name
    )
    db.session.add(rating)
    db.session.commit()
    
    flash('تم إضافة تقييمك بنجاح!')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/add_comment/<int:product_id>', methods=['POST'])
def add_comment(product_id):
    user_name = request.form.get('user_name')
    text = request.form.get('text')
    
    comment = Comment(
        product_id=product_id,
        user_name=user_name,
        text=text
    )
    db.session.add(comment)
    db.session.commit()
    
    flash('تم إضافة تعليقك وسيتم مراجعته قريباً!')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        # Get form data
        customer_name = request.form.get('customer_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        product_id = int(request.form.get('product_id'))
        region_id = int(request.form.get('region_id'))
        size = request.form.get('size')
        color = request.form.get('color')
        quantity = int(request.form.get('quantity', 1))
        
        # Get product and region
        product = Product.query.get(product_id)
        region = Region.query.get(region_id)
        
        if not product or not region:
            flash('خطأ في البيانات!')
            return redirect(url_for('index'))
        
        # Calculate total amount
        total_amount = (product.price * quantity) + region.delivery_fee
        
        # Create order
        order = Order(
            customer_name=customer_name,
            phone=phone,
            address=address,
            product_id=product_id,
            region_id=region_id,
            size=size,
            color=color,
            quantity=quantity,
            total_amount=total_amount
        )
        db.session.add(order)
        db.session.commit()
        
        # Prepare WhatsApp message
        settings = SiteSettings.query.first()
        whatsapp_number = settings.whatsapp_number if settings else "967XXXXXXXX"
        
        message = f"""طلب جديد من {settings.site_name if settings else 'متجر الأزياء اليمني'}

الاسم: {customer_name}
الهاتف: {phone}
العنوان: {address}
المنطقة: {region.name}

المنتج: {product.name}
المقاس: {size}
اللون: {color}
الكمية: {quantity}

سعر المنتج: {product.price} ريال
رسوم التوصيل: {region.delivery_fee} ريال
المبلغ الإجمالي: {total_amount} ريال

رقم الطلب: {order.id}
التاريخ: {order.created_at.strftime('%Y-%m-%d %H:%M')}"""
        
        # Encode message for WhatsApp URL
        encoded_message = quote(message)
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
        
        # Mark order as WhatsApp sent
        order.whatsapp_sent = True
        db.session.commit()
        
        flash('تم إنشاء الطلب بنجاح! سيتم تحويلك إلى واتساب لإكمال الطلب.')
        return redirect(whatsapp_url)
        
    except Exception as e:
        logging.error(f"Error placing order: {str(e)}")
        flash('حدث خطأ أثناء إنشاء الطلب. يرجى المحاولة مرة أخرى.')
        return redirect(url_for('index'))

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        code = request.form.get('admin_code')
        settings = SiteSettings.query.first()
        correct_code = settings.admin_code if settings else "F-S-YA76"
        
        if code == correct_code:
            session['admin_authenticated'] = True
            log_admin_action("دخول المدير", f"تم الدخول من IP: {request.remote_addr}")
            return redirect(url_for('admin_dashboard'))
        else:
            log_admin_action("محاولة دخول فاشلة", f"كود خاطئ: {code} من IP: {request.remote_addr}")
            return render_template('access_denied.html')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    if is_admin_authenticated():
        log_admin_action("خروج المدير")
    session.pop('admin_authenticated', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    # Get statistics
    total_products = Product.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='جديد').count()
    total_comments = Comment.query.count()
    pending_comments = Comment.query.filter_by(is_approved=False).count()
    
    # Top rated products
    top_products = db.session.query(Product).join(Rating).group_by(Product.id).order_by(db.func.avg(Rating.stars).desc()).limit(5).all()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_comments=total_comments,
                         pending_comments=pending_comments,
                         top_products=top_products,
                         recent_orders=recent_orders)

@app.route('/admin/products')
def admin_products():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    products = Product.query.order_by(Product.sort_order).all()
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('admin_products.html', products=products, categories=categories)

@app.route('/admin/products/add', methods=['POST'])
def admin_add_product():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category_id = int(request.form.get('category_id'))
        image_url = request.form.get('image_url')
        sizes = request.form.getlist('sizes')
        colors = request.form.getlist('colors')
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image_url=image_url,
            sizes=json.dumps(sizes),
            colors=json.dumps(colors)
        )
        db.session.add(product)
        db.session.commit()
        
        log_admin_action("إضافة منتج", f"تم إضافة منتج: {name}")
        flash('تم إضافة المنتج بنجاح!')
        
    except Exception as e:
        logging.error(f"Error adding product: {str(e)}")
        flash('حدث خطأ أثناء إضافة المنتج.')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
def admin_edit_product(product_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    product = Product.query.get_or_404(product_id)
    
    try:
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category_id = int(request.form.get('category_id'))
        product.image_url = request.form.get('image_url')
        product.sizes = json.dumps(request.form.getlist('sizes'))
        product.colors = json.dumps(request.form.getlist('colors'))
        product.is_active = 'is_active' in request.form
        
        db.session.commit()
        
        log_admin_action("تعديل منتج", f"تم تعديل منتج: {product.name}")
        flash('تم تعديل المنتج بنجاح!')
        
    except Exception as e:
        logging.error(f"Error editing product: {str(e)}")
        flash('حدث خطأ أثناء تعديل المنتج.')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/products/delete/<int:product_id>')
def admin_delete_product(product_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    product = Product.query.get_or_404(product_id)
    product_name = product.name
    
    try:
        db.session.delete(product)
        db.session.commit()
        
        log_admin_action("حذف منتج", f"تم حذف منتج: {product_name}")
        flash('تم حذف المنتج بنجاح!')
        
    except Exception as e:
        logging.error(f"Error deleting product: {str(e)}")
        flash('حدث خطأ أثناء حذف المنتج.')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/products/get/<int:product_id>')
def admin_get_product(product_id):
    if not is_admin_authenticated():
        return jsonify({'error': 'Unauthorized'}), 401
    
    product = Product.query.get_or_404(product_id)
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
        'category_id': product.category_id,
        'sizes': product.get_sizes_list(),
        'colors': product.get_colors_list(),
        'is_active': product.is_active
    })

@app.route('/admin/orders')
def admin_orders():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/orders/update_status/<int:order_id>', methods=['POST'])
def admin_update_order_status(order_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    old_status = order.status
    order.status = new_status
    order.notes = request.form.get('notes', '')
    
    db.session.commit()
    
    log_admin_action("تحديث حالة الطلب", f"الطلب #{order_id}: {old_status} -> {new_status}")
    flash('تم تحديث حالة الطلب بنجاح!')
    
    return redirect(url_for('admin_orders'))

@app.route('/admin/regions')
def admin_regions():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    regions = Region.query.all()
    return render_template('admin_regions.html', regions=regions)

@app.route('/admin/regions/add', methods=['POST'])
def admin_add_region():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    try:
        name = request.form.get('name')
        delivery_fee = float(request.form.get('delivery_fee'))
        estimated_time = request.form.get('estimated_time')
        
        region = Region(
            name=name,
            delivery_fee=delivery_fee,
            estimated_time=estimated_time
        )
        db.session.add(region)
        db.session.commit()
        
        log_admin_action("إضافة منطقة", f"تم إضافة منطقة: {name}")
        flash('تم إضافة المنطقة بنجاح!')
        
    except Exception as e:
        logging.error(f"Error adding region: {str(e)}")
        flash('حدث خطأ أثناء إضافة المنطقة.')
    
    return redirect(url_for('admin_regions'))

@app.route('/admin/regions/edit/<int:region_id>', methods=['POST'])
def admin_edit_region(region_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    region = Region.query.get_or_404(region_id)
    
    try:
        region.name = request.form.get('name')
        region.delivery_fee = float(request.form.get('delivery_fee'))
        region.estimated_time = request.form.get('estimated_time')
        region.is_active = 'is_active' in request.form
        
        db.session.commit()
        
        log_admin_action("تعديل منطقة", f"تم تعديل منطقة: {region.name}")
        flash('تم تعديل المنطقة بنجاح!')
        
    except Exception as e:
        logging.error(f"Error editing region: {str(e)}")
        flash('حدث خطأ أثناء تعديل المنطقة.')
    
    return redirect(url_for('admin_regions'))

@app.route('/admin/settings')
def admin_settings():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    settings = SiteSettings.query.first()
    categories = Category.query.all()
    logs = AdminLog.query.order_by(AdminLog.created_at.desc()).limit(50).all()
    
    return render_template('admin_settings.html', settings=settings, categories=categories, logs=logs)

@app.route('/admin/settings/update', methods=['POST'])
def admin_update_settings():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
    
    try:
        settings.site_name = request.form.get('site_name')
        settings.site_description = request.form.get('site_description')
        settings.whatsapp_number = request.form.get('whatsapp_number')
        settings.logo_url = request.form.get('logo_url')
        settings.primary_color = request.form.get('primary_color')
        settings.secondary_color = request.form.get('secondary_color')
        settings.text_color = request.form.get('text_color')
        settings.whatsapp_channel = request.form.get('whatsapp_channel')
        settings.telegram_channel = request.form.get('telegram_channel')
        
        if request.form.get('new_admin_code'):
            settings.admin_code = request.form.get('new_admin_code')
        
        db.session.commit()
        
        log_admin_action("تحديث إعدادات الموقع")
        flash('تم تحديث إعدادات الموقع بنجاح!')
        
    except Exception as e:
        logging.error(f"Error updating settings: {str(e)}")
        flash('حدث خطأ أثناء تحديث الإعدادات.')
    
    return redirect(url_for('admin_settings'))

@app.route('/admin/comments')
def admin_comments():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin_comments.html', comments=comments)

@app.route('/admin/comments/approve/<int:comment_id>')
def admin_approve_comment(comment_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    
    log_admin_action("الموافقة على تعليق", f"تم الموافقة على تعليق من: {comment.user_name}")
    flash('تم الموافقة على التعليق!')
    
    return redirect(url_for('admin_comments'))

@app.route('/admin/comments/delete/<int:comment_id>')
def admin_delete_comment(comment_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    comment = Comment.query.get_or_404(comment_id)
    user_name = comment.user_name
    
    db.session.delete(comment)
    db.session.commit()
    
    log_admin_action("حذف تعليق", f"تم حذف تعليق من: {user_name}")
    flash('تم حذف التعليق!')
    
    return redirect(url_for('admin_comments'))

@app.route('/admin/categories/add', methods=['POST'])
def admin_add_category():
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        
        category = Category(
            name=name,
            description=description
        )
        db.session.add(category)
        db.session.commit()
        
        log_admin_action("إضافة تصنيف", f"تم إضافة تصنيف: {name}")
        flash('تم إضافة التصنيف بنجاح!')
        
    except Exception as e:
        logging.error(f"Error adding category: {str(e)}")
        flash('حدث خطأ أثناء إضافة التصنيف.')
    
    return redirect(url_for('admin_settings'))

@app.route('/admin/categories/edit/<int:category_id>', methods=['POST'])
def admin_edit_category(category_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    category = Category.query.get_or_404(category_id)
    
    try:
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        category.is_active = 'is_active' in request.form
        
        db.session.commit()
        
        log_admin_action("تعديل تصنيف", f"تم تعديل تصنيف: {category.name}")
        flash('تم تعديل التصنيف بنجاح!')
        
    except Exception as e:
        logging.error(f"Error editing category: {str(e)}")
        flash('حدث خطأ أثناء تعديل التصنيف.')
    
    return redirect(url_for('admin_settings'))

@app.route('/admin/categories/delete/<int:category_id>')
def admin_delete_category(category_id):
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    
    category = Category.query.get_or_404(category_id)
    category_name = category.name
    
    try:
        # Check if category has products
        if category.products:
            flash('لا يمكن حذف التصنيف لأنه يحتوي على منتجات!')
            return redirect(url_for('admin_settings'))
        
        db.session.delete(category)
        db.session.commit()
        
        log_admin_action("حذف تصنيف", f"تم حذف تصنيف: {category_name}")
        flash('تم حذف التصنيف بنجاح!')
        
    except Exception as e:
        logging.error(f"Error deleting category: {str(e)}")
        flash('حدث خطأ أثناء حذف التصنيف.')
    
    return redirect(url_for('admin_settings'))

# Context processor to make settings available in all templates
@app.context_processor
def inject_settings():
    settings = SiteSettings.query.first()
    return dict(site_settings=settings)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
