#!/usr/bin/env python3
"""
Pest Tracker Application Launcher
Run this script to start the pest tracking web application.
"""

import os
import sys
from main import app

def get_local_ip():
    """Get the local IP address of this computer"""
    import socket
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "localhost"

def main():
    local_ip = get_local_ip()
    
    print("🐛 Starting Pest Tracker Application...")
    print("=" * 60)
    print("📱 MOBILE ACCESS:")
    print(f"   On your phone, go to: http://{local_ip}:5000")
    print("💻 COMPUTER ACCESS:")
    print("   On this computer: http://localhost:5000")
    print("=" * 60)
    print("🔧 Press Ctrl+C to stop the server")
    print("📶 Make sure your phone is on the same WiFi network!")
    print("-" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Pest Tracker stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()