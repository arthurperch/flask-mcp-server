#!/usr/bin/env python3
"""
Quick Flask App Starter - Test the Flask app directly
"""

import os
import subprocess
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

def start_flask_app():
    """Start the Flask application"""
    load_dotenv()
    
    flask_app_path = os.getenv('FLASK_APP_PATH', 'C:/Users/olegp/OneDrive/Apps/MCP-AWS-Claude/Cloud-Infrastructure-Flask-App/app')
    host = '127.0.0.1'
    port = 5000
    
    print(f"🚀 Starting Flask app from: {flask_app_path}")
    
    # Check if the path exists
    if not os.path.exists(flask_app_path):
        print(f"❌ Flask app path not found: {flask_app_path}")
        return False
    
    # Set up environment
    env = os.environ.copy()
    env['FLASK_APP'] = os.path.join(flask_app_path, 'app.py')
    env['FLASK_ENV'] = 'development'
    
    # Start Flask
    try:
        print(f"📡 Starting Flask on http://{host}:{port}")
        print("🔧 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run Flask
        subprocess.run([
            sys.executable, '-m', 'flask', 'run',
            '--host', host,
            '--port', str(port),
            '--debug'
        ], cwd=flask_app_path, env=env)
        
    except KeyboardInterrupt:
        print("\n🛑 Flask server stopped by user")
    except Exception as e:
        print(f"❌ Error starting Flask: {e}")
        return False
    
    return True

def check_flask_status():
    """Check if Flask is running"""
    url = "http://127.0.0.1:5000"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ Flask is running at {url}")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response Preview: {response.text[:200]}...")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Flask is not running at {url}")
        return False
    except Exception as e:
        print(f"❌ Error checking Flask: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_flask_status()
    else:
        start_flask_app()