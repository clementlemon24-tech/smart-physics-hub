#!/usr/bin/env python3
"""
Smart Physics Hub - Quick Start Script
Run this to start your physics learning platform locally
"""

import os
import sys
from main import app

def main():
    print("🚀 Starting Smart Physics Hub...")
    print("📚 Features Available:")
    print("   ✅ AI Tutor (Engineer Clement Ekelemchi)")
    print("   ✅ Interactive Classroom")
    print("   ✅ Virtual Laboratory")
    print("   ✅ Physics Encyclopedia")
    print("   ✅ Nanophysics & AI Topics")
    print("   ✅ JAMB/WAEC/NECO Preparation")
    print()
    
    # Set environment variables for local development
    os.environ['FLASK_ENV'] = 'development'
    if 'SECRET_KEY' not in os.environ:
        os.environ['SECRET_KEY'] = 'smart-physics-hub-dev-key'
    
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🌐 Starting server on:")
    print(f"   📱 Local: http://localhost:{port}")
    print(f"   📱 Network: http://0.0.0.0:{port}")
    print()
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 Smart Physics Hub stopped. Thanks for learning!")
        sys.exit(0)

if __name__ == '__main__':
    main()