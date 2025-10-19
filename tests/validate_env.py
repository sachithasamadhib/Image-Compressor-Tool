#!/usr/bin/env python3
"""
Environment Configuration Validator
Validates that all required environment variables are properly set.
"""

import os
from dotenv import load_dotenv
import sys

def validate_environment():
    """Validate environment configuration"""
    
    # Load environment variables
    load_dotenv()
    
    # Required environment variables
    required_vars = [
        'MONGODB_CONNECTION_STRING',
        'MONGODB_DATABASE_NAME',
        'MONGODB_COLLECTION_NAME'
    ]
    
    # Optional environment variables with defaults
    optional_vars = {
        'FLASK_HOST': '127.0.0.1',
        'FLASK_PORT': '5000',
        'FLASK_DEBUG': 'True',
        'API_BASE_URL': 'http://127.0.0.1:5000',
        'MAX_FILE_SIZE_MB': '50',
        'SUPPORTED_IMAGE_FORMATS': '.jpg,.jpeg,.png,.bmp,.tiff,.webp',
        'APP_NAME': 'Image Compressor Tool',
        'APP_VERSION': '1.0.0'
    }
    
    print("🔍 Validating Environment Configuration...\n")
    
    # Check required variables
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * (len(value) - 10) + value[-10:] if len(value) > 10 else '*' * len(value)}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    print()
    
    # Check optional variables
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        print(f"📋 {var}: {value}")
    
    print()
    
    # Test MongoDB connection if credentials are provided
    if not missing_vars:
        print("🔗 Testing MongoDB Connection...")
        try:
            from pymongo import MongoClient
            connection_string = os.getenv('MONGODB_CONNECTION_STRING')
            client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            print("✅ MongoDB connection successful!")
            client.close()
        except Exception as e:
            print(f"⚠️  MongoDB connection failed: {e}")
            print("   Application will use JSON fallback storage.")
    
    print()
    
    # Summary
    if missing_vars:
        print(f"❌ Configuration INVALID - Missing required variables: {', '.join(missing_vars)}")
        print("\n📝 To fix:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env with your MongoDB credentials")
        print("3. Run this script again to validate")
        return False
    else:
        print("✅ Environment configuration is VALID!")
        print("🚀 You can now run the application with: python Controller/AccessPoint.py")
        return True

if __name__ == "__main__":
    success = validate_environment()
    sys.exit(0 if success else 1)