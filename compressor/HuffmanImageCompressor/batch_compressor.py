import file_handling
import huffman_coding
import os
import glob
from pathlib import Path

def compress_single_image(image_path, output_dir):
    """
    Compress a single image using Huffman coding
    """
    try:
        print(f"Processing: {os.path.basename(image_path)}")
        
        # Read image as bit string
        image_bit_string = file_handling.read_image_bit_string(image_path)
        original_size = len(image_bit_string)
        
        # Compress using Huffman coding
        compressed_image_bit_string = huffman_coding.compress(image_bit_string)
        compressed_size = len(compressed_image_bit_string)
        
        # Save compressed file
        input_filename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{input_filename}_compressed.bin")
        file_handling.write_image(compressed_image_bit_string, output_path)
        
        # Save Huffman codes for this image
        codes_path = os.path.join(output_dir, f"{input_filename}_huffman_codes.txt")
        file_handling.write_dictionary_file(huffman_coding.huffman_codes, codes_path)
        
        compression_ratio = original_size / compressed_size
        space_saved = original_size - compressed_size
        
        return {
            'filename': os.path.basename(image_path),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'space_saved': space_saved,
            'output_file': output_path,
            'codes_file': codes_path
        }
        
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")
        return None

def batch_compress_images(input_paths, output_dir="IO/Outputs"):
    """
    Compress multiple images using Huffman coding
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    total_original_size = 0
    total_compressed_size = 0
    
    print(f"Starting batch compression of {len(input_paths)} images...")
    print("=" * 50)
    
    for i, image_path in enumerate(input_paths, 1):
        print(f"\n[{i}/{len(input_paths)}] Compressing: {os.path.basename(image_path)}")
        
        result = compress_single_image(image_path, output_dir)
        if result:
            results.append(result)
            total_original_size += result['original_size']
            total_compressed_size += result['compressed_size']
            print(f"  + Compressed: {result['compression_ratio']:.2f}x ratio")
        else:
            print(f"  - Failed to compress")
    
    # Print summary
    if results:
        print("\n" + "=" * 50)
        print("BATCH COMPRESSION SUMMARY")
        print("=" * 50)
        
        for result in results:
            print(f"File: {result['filename']}")
            print(f"  Original: {result['original_size']:,} bits")
            print(f"  Compressed: {result['compressed_size']:,} bits")
            print(f"  Ratio: {result['compression_ratio']:.2f}x")
            print(f"  Saved: {result['space_saved']:,} bits")
            print(f"  Output: {os.path.basename(result['output_file'])}")
            print()
        
        overall_ratio = total_original_size / total_compressed_size
        total_space_saved = total_original_size - total_compressed_size
        
        print("OVERALL RESULTS:")
        print(f"Total images processed: {len(results)}")
        print(f"Total original size: {total_original_size:,} bits")
        print(f"Total compressed size: {total_compressed_size:,} bits")
        print(f"Overall compression ratio: {overall_ratio:.2f}x")
        print(f"Total space saved: {total_space_saved:,} bits")
        print(f"Average compression per image: {overall_ratio:.2f}x")
        
        print(f"\nAll compressed files saved in: {output_dir}")
        print("Note: These are binary files, not viewable images.")
        
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
    
    return sorted(image_files)

# Main execution
if __name__ == "__main__":
    print("Huffman Batch Image Compressor")
    print("Compresses multiple images at once using Huffman coding")
    print()
    
    print("Choose input method:")
    print("1. Enter individual file paths")
    print("2. Compress all images in a directory")
    print("3. Use default test images")
    
    choice = input("Enter choice (1, 2, or 3): ")
    
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
            batch_compress_images(image_paths)
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
                batch_compress_images(image_paths)
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
                batch_compress_images(image_paths)
            else:
                print("No test images found in IO/Inputs")
        else:
            print("Test directory not found.")
            
    else:
        print("Invalid choice!")
