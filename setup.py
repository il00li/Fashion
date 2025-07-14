from setuptools import setup, find_packages

setup(
    name="yemen-fashion-store",
    version="1.0.0",
    description="متجر الأزياء اليمني - موقع تجارة إلكترونية",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.1.1",
        "Flask-SQLAlchemy>=3.1.1",
        "gunicorn>=23.0.0",
        "psycopg2-binary>=2.9.10",
        "SQLAlchemy>=2.0.41",
        "Werkzeug>=3.1.3",
        "email-validator>=2.2.0",
    ],
    python_requires=">=3.11",
)