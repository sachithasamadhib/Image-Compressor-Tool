#!/usr/bin/env python3
"""
Debug test to see what's happening with quality levels and aspect ratios
"""

import requests
import time
from PIL import Image
import io

def debug_quality_test():
    """Debug quality level issues"""
    print("🔍 Debugging Quality Levels...")
    
    quality_levels = ['high', 'medium', 'low']
    
    for quality in quality_levels:
        print(f"\n   Testing {quality} quality...")
        try:
            # Create a fresh test image for each request
            img = Image.new('RGB', (200, 200), color='red')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(f'http://127.0.0.1:5000/upload-images/{quality}/5000000/original/jpeg', files=files)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Response keys: {list(data.keys())}")
                if 'processed_files' in data and data['processed_files']:
                    file_data = data['processed_files'][0]
                    print(f"   File data keys: {list(file_data.keys())}")
                    if 'compression_ratio' in file_data:
                        print(f"   Compression ratio: {file_data['compression_ratio']}")
                    else:
                        print(f"   Missing compression_ratio in: {file_data}")
                else:
                    print(f"   No processed files: {data}")
            else:
                print(f"   Error response: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")

def debug_aspect_test():
    """Debug aspect ratio issues"""
    print("\n🔍 Debugging Aspect Ratios...")
    
    aspect_ratios = ['original', '4:3', '16:9', '1:1']
    
    for aspect in aspect_ratios:
        print(f"\n   Testing {aspect} aspect ratio...")
        try:
            # Create a fresh test image for each request
            img = Image.new('RGB', (400, 300), color='blue')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            files = {'images': ('test.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(f'http://127.0.0.1:5000/upload-images/medium/5000000/{aspect}/jpeg', files=files)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Response keys: {list(data.keys())}")
                if 'processed_files' in data and data['processed_files']:
                    file_data = data['processed_files'][0]
                    print(f"   File data keys: {list(file_data.keys())}")
                    if 'original_dimensions' in file_data:
                        print(f"   Original dimensions: {file_data['original_dimensions']}")
                        print(f"   Final dimensions: {file_data['final_dimensions']}")
                    else:
                        print(f"   Missing dimensions in: {file_data}")
                else:
                    print(f"   No processed files: {data}")
            else:
                print(f"   Error response: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")

if __name__ == "__main__":
    debug_quality_test()
    debug_aspect_test()
