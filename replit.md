# Yemen Fashion Store - replit.md

## Overview

This is a Flask-based e-commerce web application for a Yemeni fashion store. The application is built with a focus on Arabic language support (RTL) and includes a complete admin dashboard for managing products, orders, and site settings. The app uses a glassmorphism design aesthetic with modern UI components.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: HTML templates with Jinja2 templating engine
- **CSS Framework**: Bootstrap 5 with custom glassmorphism styling
- **JavaScript**: Vanilla JavaScript for interactive features
- **Typography**: Arabic fonts (Cairo, Noto Kufi Arabic)
- **Design Pattern**: Responsive design with RTL (right-to-left) support

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Session Management**: Flask sessions for admin authentication
- **Template Engine**: Jinja2 (integrated with Flask)

### Database Architecture
- **Primary Database**: SQLite (with PostgreSQL support planned)
- **ORM**: SQLAlchemy with DeclarativeBase
- **Migration Strategy**: Direct table creation via `db.create_all()`

## Key Components

### Models (Database Schema)
- **SiteSettings**: Store configuration, branding, and contact information
- **Category**: Product categorization system
- **Product**: Main product catalog with pricing, images, and specifications
- **Order**: Customer orders with delivery details
- **Region**: Delivery areas with shipping fees
- **Rating**: Product rating system
- **Comment**: Product reviews and feedback
- **AdminLog**: Admin activity tracking

### Authentication System
- **Admin Authentication**: Code-based authentication system
- **Access Control**: Session-based admin access control
- **Security**: Password hashing for sensitive data

### Admin Dashboard
- **Dashboard**: Statistics overview and system monitoring
- **Product Management**: CRUD operations for products and categories
- **Order Management**: Order tracking and status updates
- **Settings Management**: Site configuration and customization
- **Region Management**: Delivery areas and shipping fees

### Customer Features
- **Product Catalog**: Browse products by category
- **Product Details**: Detailed product views with ratings
- **Order System**: WhatsApp-based ordering system
- **Reviews**: Customer rating and comment system

## Data Flow

### Customer Journey
1. Browse products on homepage or by category
2. View product details with ratings and specifications
3. Select size, color, and quantity
4. Fill order form with delivery details
5. Submit order (redirects to WhatsApp for completion)

### Admin Workflow
1. Access admin panel via secret code authentication
2. Manage products, categories, and inventory
3. Process and track customer orders
4. Configure site settings and branding
5. Monitor system activity through admin logs

### Order Processing
1. Customer submits order form
2. Order saved to database with "جديد" (New) status
3. Admin receives order notification
4. Admin processes order through dashboard
5. Order status updated throughout fulfillment

## External Dependencies

### Frontend Libraries
- **Bootstrap 5**: UI framework and responsive design
- **Font Awesome 6**: Icon library
- **Google Fonts**: Arabic typography (Cairo, Noto Kufi Arabic)

### Backend Dependencies
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Werkzeug**: Security utilities and middleware

### Third-party Integrations
- **WhatsApp Business**: Order completion and customer communication
- **Image Hosting**: External image URLs for product photos

## Deployment Strategy

### Environment Configuration
- **Database**: Environment variable `DATABASE_URL` (defaults to SQLite)
- **Session Security**: Environment variable `SESSION_SECRET`
- **Admin Access**: Configurable admin code in database

### Production Considerations
- **Proxy Support**: ProxyFix middleware for reverse proxy deployment
- **Database Pooling**: Connection pool configuration for production
- **Static Files**: CDN-ready static asset structure

### Development Setup
- **Debug Mode**: Enabled in development environment
- **Hot Reload**: Flask development server with auto-reload
- **Database Initialization**: Automatic table creation and default data seeding

## Additional Notes

### Arabic Language Support
- Full RTL (right-to-left) layout support
- Arabic fonts and typography optimization
- Arabic text content throughout the application

### Security Features
- Admin authentication with session management
- Input validation and form security
- Activity logging for admin actions

### Mobile Responsiveness
- Bootstrap-based responsive design
- Touch-friendly interface elements
- Mobile-optimized order forms

### Future Enhancements
- The application is structured to easily migrate from SQLite to PostgreSQL
- Extensible model structure for additional features
- Modular template system for easy customization