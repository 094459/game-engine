"""WSGI entry point for production (gunicorn)."""
from src.app import create_app

app = create_app("production")
