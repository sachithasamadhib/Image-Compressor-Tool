#!/usr/bin/env python3
"""
Test script to verify the integration between frontend and compression logic
"""

import requests
import json
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_backend_connection():
    """Test if the backend is running and accessible"""
    try:
        response = requests.get('http://127.0.0.1:5000/test-connection', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend connection successful!")
            print(f"   Status: {data['status']}")
            print(f"   Message: {data['message']}")
            print(f"   Huffman available: {data['huffman_available']}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure Flask server is running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error testing backend connection: {e}")
        return False

def test_compression_methods():
    """Test compression methods endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/compression-methods', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Compression methods endpoint working!")
            print("   Available methods:")
            for method, details in data['compression_methods'].items():
                status = "✅" if details['available'] else "❌"
                print(f"     {status} {method}: {details['name']}")
            return True
        else:
            print(f"❌ Compression methods endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing compression methods: {e}")
        return False

def test_huffman_compression():
    """Test Huffman compression endpoint"""
    try:
        # Create a simple test image file
        test_image_path = project_root / "compressor" / "HuffmanImageCompressor" / "IO" / "Inputs" / "test1.jpg"
        
        if not test_image_path.exists():
            print("❌ Test image not found. Skipping Huffman compression test.")
            return False
        
        with open(test_image_path, 'rb') as f:
            files = {'images': f}
            response = requests.post('http://127.0.0.1:5000/compress-huffman', files=files, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Huffman compression endpoint working!")
            print(f"   Processed {data['total_files']} files")
            for file_data in data['processed_files']:
                if 'error' not in file_data:
                    print(f"     ✅ {file_data['filename']}: {file_data['compression_ratio']}% compression")
                else:
                    print(f"     ❌ {file_data['filename']}: {file_data['error']}")
            return True
        else:
            print(f"❌ Huffman compression endpoint returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing Huffman compression: {e}")
        return False

def test_jpeg_compression():
    """Test JPEG compression endpoint"""
    try:
        # Create a simple test image file
        test_image_path = project_root / "compressor" / "HuffmanImageCompressor" / "IO" / "Inputs" / "test1.jpg"
        
        if not test_image_path.exists():
            print("❌ Test image not found. Skipping JPEG compression test.")
            return False
        
        with open(test_image_path, 'rb') as f:
            files = {'images': f}
            response = requests.post('http://127.0.0.1:5000/upload-images/medium/5000000/original/jpeg', files=files, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ JPEG compression endpoint working!")
            print(f"   Processed {data['total_files']} files")
            for file_data in data['processed_files']:
                if 'error' not in file_data:
                    print(f"     ✅ {file_data['filename']}: {file_data['compression_ratio']}% compression")
                else:
                    print(f"     ❌ {file_data['filename']}: {file_data['error']}")
            return True
        else:
            print(f"❌ JPEG compression endpoint returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing JPEG compression: {e}")
        return False

def main():
    """Run all integration tests"""
    print("=" * 60)
    print("Image Compressor Integration Test")
    print("=" * 60)
    
    tests = [
        ("Backend Connection", test_backend_connection),
        ("Compression Methods", test_compression_methods),
        ("JPEG Compression", test_jpeg_compression),
        ("Huffman Compression", test_huffman_compression),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  {test_name} test failed")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
