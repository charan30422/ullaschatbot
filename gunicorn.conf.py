"""
Gunicorn configuration for Render deployment.
"""
import os

# Bind to the PORT env variable that Render sets
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# 2 sync workers is optimal for Render free tier (1 vCPU)
workers = 2

# Keep connections alive between requests — reduces TLS handshake overhead
keepalive = 5

# Timeout — generous for Twilio API calls
timeout = 60

# Only log warnings and above in production (reduces I/O overhead)
loglevel = "warning"
accesslog = "-"
errorlog  = "-"
