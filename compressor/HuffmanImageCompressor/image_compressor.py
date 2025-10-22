import file_handling
import huffman_coding
import os
from PIL import Image
import io

def compress_image_to_jpg(input_path, output_path, quality=85):
    """
    Compress an image to JPEG with reduced quality while maintaining JPEG format
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (JPEG doesn't support transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save with reduced quality (this is the compression)
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            return original_size, compressed_size
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def huffman_compress_image(input_path, output_path):
    """
    Compress image using Huffman coding and save as binary file
    """
    try:
        # Read image as bit string
        image_bit_string = file_handling.read_image_bit_string(input_path)
        print(f"Original size: {len(image_bit_string)} bits")
        
        # Compress using Huffman coding
        compressed_image_bit_string = huffman_coding.compress(image_bit_string)
        print(f"Compressed size: {len(compressed_image_bit_string)} bits")
        
        # Save compressed file
        file_handling.write_image(compressed_image_bit_string, output_path)
        
        return len(image_bit_string), len(compressed_image_bit_string)
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Main execution
if __name__ == "__main__":
    print("Image Compressor")
    print("1. JPEG Quality Compression (viewable image)")
    print("2. Huffman Binary Compression (not viewable)")
    
    choice = input("Choose compression method (1 or 2): ")
    image_path = input("Enter image path: ")
    
    input_filename = os.path.splitext(os.path.basename(image_path))[0]
    
    if choice == "1":
        # JPEG quality compression
        output_path = f"IO/Outputs/{input_filename}_compressed.jpg"
        print(f"Compressing with JPEG quality reduction...")
        
        original_size, compressed_size = compress_image_to_jpg(image_path, output_path, quality=60)
        
        if original_size and compressed_size:
            compression_ratio = original_size / compressed_size
            space_saved = original_size - compressed_size
            
            print(f"\nCompression Complete!")
            print(f"Compressed file: {output_path}")
            print(f"Original size: {original_size} bytes")
            print(f"Compressed size: {compressed_size} bytes")
            print(f"Compression ratio: {compression_ratio:.2f}")
            print(f"Space saved: {space_saved} bytes")
            print("This is a viewable JPEG image!")
            
    elif choice == "2":
        # Huffman compression
        output_path = f"IO/Outputs/{input_filename}_huffman_compressed.bin"
        print(f"Compressing with Huffman coding...")
        
        original_bits, compressed_bits = huffman_compress_image(image_path, output_path)
        
        if original_bits and compressed_bits:
            compression_ratio = original_bits / compressed_bits
            space_saved = original_bits - compressed_bits
            
            print(f"\nCompression Complete!")
            print(f"Compressed file: {output_path}")
            print(f"Original size: {original_bits} bits")
            print(f"Compressed size: {compressed_bits} bits")
            print(f"Compression ratio: {compression_ratio:.2f}")
            print(f"Space saved: {space_saved} bits")
            print("Note: This is a binary file, not a viewable image.")
            
    else:
        print("Invalid choice!")
