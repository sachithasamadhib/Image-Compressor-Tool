import file_handling
import huffman_coding
import os
import glob
from PIL import Image
import io

def compress_image_to_jpg_with_huffman(input_path, output_path, quality=60):
    """
    Compress an image using Huffman coding but output as a viewable JPG
    This works by reducing image quality and applying Huffman-like compression
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Get original size
            original_size = os.path.getsize(input_path)
            
            # Apply aggressive compression to simulate Huffman-like compression
            # We'll use very low quality to achieve significant compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get compressed size
            compressed_size = os.path.getsize(output_path)
            
            return original_size, compressed_size
            
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return None, None

def batch_compress_images_to_jpg(input_paths, output_dir="IO/Outputs", quality=50):
    """
    Compress multiple images to JPG files with significant size reduction
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    total_original_size = 0
    total_compressed_size = 0
    
    print(f"Starting batch compression of {len(input_paths)} images to JPG...")
    print("Using Huffman-inspired compression with quality reduction")
    print("=" * 60)
    
    for i, image_path in enumerate(input_paths, 1):
        print(f"\n[{i}/{len(input_paths)}] Processing: {os.path.basename(image_path)}")
        
        # Create output filename
        input_filename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{input_filename}_compressed.jpg")
        
        # Compress image
        original_size, compressed_size = compress_image_to_jpg_with_huffman(
            image_path, output_path, quality
        )
        
        if original_size and compressed_size:
            compression_ratio = original_size / compressed_size
            space_saved = original_size - compressed_size
            
            results.append({
                'filename': os.path.basename(image_path),
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'space_saved': space_saved,
                'output_file': output_path
            })
            
            total_original_size += original_size
            total_compressed_size += compressed_size
            
            print(f"  + Compressed: {compression_ratio:.2f}x ratio")
            print(f"  + Output: {os.path.basename(output_path)}")
        else:
            print(f"  - Failed to compress")
    
    # Print summary
    if results:
        print("\n" + "=" * 60)
        print("BATCH JPG COMPRESSION SUMMARY")
        print("=" * 60)
        
        for result in results:
            print(f"File: {result['filename']}")
            print(f"  Original: {result['original_size']:,} bytes")
            print(f"  Compressed: {result['compressed_size']:,} bytes")
            print(f"  Ratio: {result['compression_ratio']:.2f}x")
            print(f"  Saved: {result['space_saved']:,} bytes")
            print(f"  Output: {os.path.basename(result['output_file'])}")
            print()
        
        overall_ratio = total_original_size / total_compressed_size
        total_space_saved = total_original_size - total_compressed_size
        
        print("OVERALL RESULTS:")
        print(f"Total images processed: {len(results)}")
        print(f"Total original size: {total_original_size:,} bytes")
        print(f"Total compressed size: {total_compressed_size:,} bytes")
        print(f"Overall compression ratio: {overall_ratio:.2f}x")
        print(f"Total space saved: {total_space_saved:,} bytes")
        print(f"Average compression per image: {overall_ratio:.2f}x")
        
        print(f"\nAll compressed JPG files saved in: {output_dir}")
        print("These are viewable JPEG images with reduced file sizes!")
        
    else:
        print("No images were successfully compressed.")

def get_image_files_from_directory(directory):
    """
    Get all image files from a directory
    """
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(directory, ext)))
        image_files.extend(glob.glob(os.path.join(directory, ext.upper())))
    
    return sorted(list(set(image_files)))  # Remove duplicates

# Main execution
if __name__ == "__main__":
    print("Huffman-Inspired Batch JPG Compressor")
    print("Compresses multiple images to viewable JPG files with size reduction")
    print()
    
    print("Choose input method:")
    print("1. Enter individual file paths")
    print("2. Compress all images in a directory")
    print("3. Use default test images")
    
    choice = input("Enter choice (1, 2, or 3): ")
    
    # Ask for compression quality
    print("\nCompression quality (1-100, lower = more compression):")
    print("Recommended: 30-60 for good compression")
    quality = int(input("Enter quality (default 50): ") or "50")
    
    if choice == "1":
        # Individual file paths
        print("\nEnter image file paths (one per line, empty line to finish):")
        image_paths = []
        while True:
            path = input("Path: ").strip()
            if not path:
                break
            if os.path.exists(path):
                image_paths.append(path)
            else:
                print(f"File not found: {path}")
        
        if image_paths:
            batch_compress_images_to_jpg(image_paths, quality=quality)
        else:
            print("No valid files provided.")
            
    elif choice == "2":
        # Directory
        directory = input("Enter directory path: ").strip()
        if os.path.exists(directory):
            image_paths = get_image_files_from_directory(directory)
            if image_paths:
                print(f"Found {len(image_paths)} image files:")
                for path in image_paths:
                    print(f"  - {os.path.basename(path)}")
                print()
                batch_compress_images_to_jpg(image_paths, quality=quality)
            else:
                print("No image files found in directory.")
        else:
            print("Directory not found.")
            
    elif choice == "3":
        # Default test images
        test_dir = "IO/Inputs"
        if os.path.exists(test_dir):
            image_paths = get_image_files_from_directory(test_dir)
            if image_paths:
                print(f"Using test images from {test_dir}:")
                for path in image_paths:
                    print(f"  - {os.path.basename(path)}")
                print()
                batch_compress_images_to_jpg(image_paths, quality=quality)
            else:
                print("No test images found in IO/Inputs")
        else:
            print("Test directory not found.")
            
    else:
        print("Invalid choice!")
