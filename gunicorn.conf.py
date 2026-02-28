"""
Gunicorn configuration for Render deployment.
"""
import os

# Bind to the PORT env variable that Render sets
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# Workers
workers = 2

# Timeout (seconds) — increase to avoid worker kills on free tier cold starts
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
