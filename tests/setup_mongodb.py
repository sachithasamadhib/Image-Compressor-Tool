#!/usr/bin/env python3
"""
Setup MongoDB for Image Compressor Tool
This script helps set up MongoDB for the history database
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def create_env_file():
    """Create .env file with MongoDB configuration"""
    env_content = """# MongoDB Configuration
MONGODB_CONNECTION_STRING=mongodb://localhost:27017/
MONGODB_DATABASE_NAME=image_compressor
MONGODB_COLLECTION_NAME=compression_history

# Optional: MongoDB Atlas (cloud) configuration
# MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
# MONGODB_DATABASE_NAME=image_compressor
# MONGODB_COLLECTION_NAME=compression_history
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with MongoDB configuration")
    else:
        print("ℹ️  .env file already exists")

def check_mongodb_installation():
    """Check if MongoDB is installed"""
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ MongoDB is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ MongoDB is not installed")
    return False

def install_mongodb_windows():
    """Install MongoDB on Windows using chocolatey or manual instructions"""
    print("\n📦 MongoDB Installation Options for Windows:")
    print("1. Using Chocolatey (recommended):")
    print("   choco install mongodb")
    print("\n2. Manual installation:")
    print("   Download from: https://www.mongodb.com/try/download/community")
    print("   Follow the installation wizard")
    print("\n3. Using winget:")
    print("   winget install MongoDB.Server")
    
    # Try chocolatey
    try:
        result = subprocess.run(['choco', '--version'], 
                              capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print("\n🔧 Attempting to install MongoDB with Chocolatey...")
            subprocess.run(['choco', 'install', 'mongodb', '-y'], check=True)
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return False

def start_mongodb_service():
    """Start MongoDB service"""
    try:
        # Try to start MongoDB service
        subprocess.run(['net', 'start', 'MongoDB'], check=True, capture_output=True)
        print("✅ MongoDB service started")
        return True
    except subprocess.CalledProcessError:
        try:
            # Try to start mongod directly
            subprocess.Popen(['mongod', '--dbpath', './data/db'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ MongoDB started in background")
            return True
        except FileNotFoundError:
            print("❌ Could not start MongoDB")
            return False

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def main():
    print("=" * 60)
    print("MongoDB Setup for Image Compressor Tool")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Check if MongoDB is installed
    if check_mongodb_installation():
        # Try to start MongoDB
        if start_mongodb_service():
            # Test connection
            if test_mongodb_connection():
                print("\n🎉 MongoDB is ready to use!")
                print("The Image Compressor Tool will now use MongoDB for history storage.")
            else:
                print("\n⚠️  MongoDB is installed but not running.")
                print("Please start MongoDB manually and run this script again.")
        else:
            print("\n⚠️  Could not start MongoDB service.")
            print("Please start MongoDB manually.")
    else:
        print("\n📦 Installing MongoDB...")
        if install_mongodb_windows():
            print("✅ MongoDB installed successfully")
            if start_mongodb_service() and test_mongodb_connection():
                print("\n🎉 MongoDB setup complete!")
            else:
                print("\n⚠️  MongoDB installed but not running. Please start it manually.")
        else:
            print("\n⚠️  Could not install MongoDB automatically.")
            print("Please install MongoDB manually and run this script again.")
            print("\nThe application will work with JSON fallback until MongoDB is available.")
    
    print("\n" + "=" * 60)
    print("Setup complete! You can now run the Image Compressor Tool.")
    print("=" * 60)

if __name__ == "__main__":
    main()
