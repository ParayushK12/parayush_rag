"""
Vercel serverless function entry point for Flask app.
This file is required for Vercel to properly deploy the Flask backend.
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

# This is required for Vercel
handler = app
