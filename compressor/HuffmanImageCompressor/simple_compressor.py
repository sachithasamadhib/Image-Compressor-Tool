import os
from PIL import Image

def compress_image(input_path, quality=60):
    """
    Compress an image to JPEG with reduced quality
    """
    # Get input filename
    input_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = f"IO/Outputs/{input_filename}_compressed.jpg"
    
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (JPEG doesn't support transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save with reduced quality (this compresses the image)
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            return output_path, original_size, compressed_size
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

# Main execution
if __name__ == "__main__":
    print("Simple Image Compressor")
    print("Compresses images to smaller JPEG files")
    
    image_path = input("Enter image path: ")
    print(f"Compressing: {image_path}")
    
    output_path, original_size, compressed_size = compress_image(image_path, quality=60)
    
    if output_path and original_size and compressed_size:
        compression_ratio = original_size / compressed_size
        space_saved = original_size - compressed_size
        
        print(f"\nCompression Complete!")
        print(f"Compressed file: {output_path}")
        print(f"Original size: {original_size:,} bytes")
        print(f"Compressed size: {compressed_size:,} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Space saved: {space_saved:,} bytes")
        print("This is a viewable JPEG image!")
    else:
        print("Compression failed!")
