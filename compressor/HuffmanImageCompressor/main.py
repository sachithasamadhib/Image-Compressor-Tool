import file_handling
import huffman_coding
import os

# --- Get image path ---
image_path = input("Enter Image Path: ")
print(f"Compressing: {image_path}")

# --- Read image ---
image_bit_string = file_handling.read_image_bit_string(image_path)
print(f"Original size: {len(image_bit_string)} bits")

# --- Compress with Huffman coding ---
compressed_image_bit_string = huffman_coding.compress(image_bit_string)
print(f"Compressed size: {len(compressed_image_bit_string)} bits")

# --- Save compressed file ---
input_filename = os.path.splitext(os.path.basename(image_path))[0]
output_path = f"IO/Outputs/{input_filename}_compressed.bin"
file_handling.write_image(compressed_image_bit_string, output_path)

# --- Show results ---
compression_ratio = len(image_bit_string) / len(compressed_image_bit_string)
space_saved = len(image_bit_string) - len(compressed_image_bit_string)

print(f"\nCompression Complete!")
print(f"Compressed file: {output_path}")
print(f"Compression ratio: {compression_ratio:.2f}")
print(f"Space saved: {space_saved} bits")
