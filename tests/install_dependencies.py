#!/usr/bin/env python3
"""
Install dependencies for the Image Compressor Tool
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Install all dependencies"""
    print("=" * 60)
    print("Installing Image Compressor Tool Dependencies")
    print("=" * 60)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  No virtual environment detected. Consider using a virtual environment.")
    
    # Upgrade pip first
    print("\n📦 Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Pip upgrade")
    
    # Install dependencies one by one to handle errors better
    dependencies = [
        "blinker==1.9.0",
        "click==8.3.0", 
        "colorama==0.4.6",
        "Flask==3.1.2",
        "Flask-CORS==4.0.0",
        "itsdangerous==2.2.0",
        "Jinja2==3.1.6",
        "MarkupSafe==3.0.2",
        "Werkzeug==3.1.3",
        "pymongo==4.6.0",
        "python-dotenv==1.0.0"
    ]
    
    # Install Pillow separately with specific options
    print("\n🖼️  Installing Pillow (this may take a while)...")
    pillow_success = run_command(
        f"{sys.executable} -m pip install Pillow --no-cache-dir", 
        "Pillow installation"
    )
    
    if not pillow_success:
        print("⚠️  Pillow installation failed. Trying alternative approach...")
        # Try installing a pre-compiled wheel
        run_command(
            f"{sys.executable} -m pip install Pillow --only-binary=all", 
            "Pillow installation (pre-compiled)"
        )
    
    # Install other dependencies
    print("\n📚 Installing other dependencies...")
    for dep in dependencies:
        run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}")
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    try:
        import flask
        import flask_cors
        from PIL import Image
        print("✅ Core dependencies verified successfully")
        
        # Test Flask-CORS
        from flask_cors import CORS
        print("✅ Flask-CORS verified successfully")
        
        # Test PIL
        img = Image.new('RGB', (10, 10))
        print("✅ Pillow verified successfully")
        
    except ImportError as e:
        print(f"❌ Verification failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Dependencies installation completed!")
    print("You can now run the application with: python app.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
