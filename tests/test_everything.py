#!/usr/bin/env python3
"""
Test everything - backend, frontend connection, and file processing
"""

import requests
import time
import os

def test_backend():
    """Test if backend is running"""
    try:
        response = requests.get('http://127.0.0.1:5000/test-connection', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running")
            print(f"   Status: {data['status']}")
            print(f"   Huffman available: {data['huffman_available']}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_file_upload():
    """Test file upload and compression"""
    try:
        # Create a simple test image
        from PIL import Image
        import io
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Test upload
        files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post('http://127.0.0.1:5000/upload-images/medium/5000000/original/jpeg', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ File upload and compression working")
            print(f"   Processed {data['total_files']} files")
            return True
        else:
            print(f"❌ File upload failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        return False

def check_folders():
    """Check if files are being saved to correct folders"""
    inputs_dir = "compressor/HuffmanImageCompressor/IO/Inputs"
    outputs_dir = "compressor/HuffmanImageCompressor/IO/Outputs"
    
    print(f"📁 Checking folders...")
    print(f"   Inputs: {inputs_dir} - {len(os.listdir(inputs_dir)) if os.path.exists(inputs_dir) else 0} files")
    print(f"   Outputs: {outputs_dir} - {len(os.listdir(outputs_dir)) if os.path.exists(outputs_dir) else 0} files")
    
    return os.path.exists(inputs_dir) and os.path.exists(outputs_dir)

def main():
    print("=" * 60)
    print("Testing Everything - Backend, Frontend, File Processing")
    print("=" * 60)
    
    # Test backend
    print("\n🔧 Testing Backend...")
    backend_ok = test_backend()
    
    if not backend_ok:
        print("\n❌ Backend not running. Please start it with:")
        print("   python -c \"from Controller.AccessPoint import app; app.run(host='127.0.0.1', port=5000, debug=True)\"")
        return
    
    # Test file upload
    print("\n📤 Testing File Upload...")
    upload_ok = test_file_upload()
    
    # Check folders
    print("\n📁 Checking Folders...")
    folders_ok = check_folders()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Backend: {'✅ Working' if backend_ok else '❌ Not working'}")
    print(f"File Upload: {'✅ Working' if upload_ok else '❌ Not working'}")
    print(f"Folders: {'✅ Working' if folders_ok else '❌ Not working'}")
    
    if backend_ok and upload_ok and folders_ok:
        print("\n🎉 Everything is working! The frontend should be able to connect and process files.")
    else:
        print("\n⚠️  Some issues found. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
