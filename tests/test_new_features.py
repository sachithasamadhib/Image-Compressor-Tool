#!/usr/bin/env python3
"""
Test all new features: folder selection, quality levels, size filters, MongoDB
"""

import requests
import time
import os
import tempfile
from PIL import Image
import io

def test_backend_connection():
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

def test_quality_levels():
    """Test different quality levels"""
    print("\n🧪 Testing Quality Levels...")
    
    quality_levels = ['high', 'medium', 'low']
    results = {}
    
    for quality in quality_levels:
        try:
            # Create a fresh test image for each request
            img = Image.new('RGB', (200, 200), color='red')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(f'http://127.0.0.1:5000/upload-images/{quality}/5000000/original/jpeg', files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data['processed_files']:
                    file_data = data['processed_files'][0]
                    results[quality] = {
                        'compression_ratio': file_data['compression_ratio'],
                        'compressed_size': file_data['compressed_size']
                    }
                    print(f"   ✅ {quality}: {file_data['compression_ratio']}% compression")
                else:
                    print(f"   ❌ {quality}: No processed files")
            else:
                print(f"   ❌ {quality}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {quality}: {e}")
    
    return results

def test_aspect_ratios():
    """Test different aspect ratios"""
    print("\n🧪 Testing Aspect Ratios...")
    
    aspect_ratios = ['original', '4:3', '16:9', '1:1']
    results = {}
    
    for aspect in aspect_ratios:
        try:
            # Create a fresh test image for each request
            img = Image.new('RGB', (400, 300), color='blue')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(f'http://127.0.0.1:5000/upload-images/medium/5000000/{aspect}/jpeg', files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data['processed_files']:
                    file_data = data['processed_files'][0]
                    results[aspect] = {
                        'original_dimensions': file_data['original_dimensions'],
                        'final_dimensions': file_data['final_dimensions']
                    }
                    print(f"   ✅ {aspect}: {file_data['original_dimensions']} → {file_data['final_dimensions']}")
                else:
                    print(f"   ❌ {aspect}: No processed files")
            else:
                print(f"   ❌ {aspect}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {aspect}: {e}")
    
    return results

def test_custom_output_folder():
    """Test custom output folder functionality"""
    print("\n🧪 Testing Custom Output Folder...")
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"   Using temp directory: {temp_dir}")
    
    try:
        # Create a test image
        img = Image.new('RGB', (100, 100), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Test with custom output folder
        files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
        headers = {'X-Output-Folder': temp_dir}
        response = requests.post('http://127.0.0.1:5000/upload-images/medium/5000000/original/jpeg', 
                               files=files, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Custom folder request successful")
            
            # Check if files were created in the custom folder
            files_in_temp = os.listdir(temp_dir)
            if files_in_temp:
                print(f"   ✅ Files created in custom folder: {files_in_temp}")
                return True
            else:
                print(f"   ❌ No files found in custom folder")
                return False
        else:
            print(f"   ❌ Custom folder request failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Custom folder test failed: {e}")
        return False
    finally:
        # Clean up temp directory
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass

def test_huffman_compression():
    """Test Huffman compression with new features"""
    print("\n🧪 Testing Huffman Compression...")
    
    try:
        # Create a test image
        img = Image.new('RGB', (150, 150), color='purple')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post('http://127.0.0.1:5000/compress-huffman', files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data['processed_files']:
                file_data = data['processed_files'][0]
                print(f"   ✅ Huffman compression: {file_data['compression_ratio']}% compression")
                print(f"   ✅ Output file: {file_data.get('output_path', 'N/A')}")
                return True
            else:
                print(f"   ❌ Huffman: No processed files")
                return False
        else:
            print(f"   ❌ Huffman: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Huffman test failed: {e}")
        return False

def test_mongodb_history():
    """Test MongoDB history functionality"""
    print("\n🧪 Testing MongoDB History...")
    
    try:
        # Test history endpoint
        response = requests.get('http://127.0.0.1:5000/history')
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ History endpoint working: {len(data.get('history', []))} records")
            
            # Test statistics endpoint
            stats_response = requests.get('http://127.0.0.1:5000/history/statistics')
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                print(f"   ✅ Statistics endpoint working")
                print(f"   📊 Total files: {stats_data.get('total_files', 0)}")
                print(f"   📊 Average compression: {stats_data.get('average_compression_ratio', 0)}%")
                return True
            else:
                print(f"   ❌ Statistics endpoint failed: HTTP {stats_response.status_code}")
                return False
        else:
            print(f"   ❌ History endpoint failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ History test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Testing New Features - Image Compressor Tool")
    print("=" * 60)
    
    # Test backend connection
    if not test_backend_connection():
        print("\n❌ Backend not running. Please start it first.")
        return
    
    # Test all features
    quality_results = test_quality_levels()
    aspect_results = test_aspect_ratios()
    custom_folder_ok = test_custom_output_folder()
    huffman_ok = test_huffman_compression()
    mongodb_ok = test_mongodb_history()
    
    # Summary
    print("\n" + "=" * 60)
    print("FEATURE TEST SUMMARY:")
    print("=" * 60)
    
    print(f"✅ Quality Levels: {len(quality_results)} working")
    print(f"✅ Aspect Ratios: {len(aspect_results)} working")
    print(f"{'✅' if custom_folder_ok else '❌'} Custom Output Folder")
    print(f"{'✅' if huffman_ok else '❌'} Huffman Compression")
    print(f"{'✅' if mongodb_ok else '❌'} MongoDB History")
    
    total_features = 5
    working_features = len(quality_results) + len(aspect_results) + (1 if custom_folder_ok else 0) + (1 if huffman_ok else 0) + (1 if mongodb_ok else 0)
    
    print(f"\n🎯 Overall: {working_features}/{total_features} features working")
    
    if working_features == total_features:
        print("🎉 All new features are working perfectly!")
    else:
        print("⚠️  Some features need attention. Check the output above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
