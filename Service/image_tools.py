from PIL import Image, ImageOps
import io
import os
from typing import Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ImageCompressor:
    """Handle image compression with quality and aspect ratio controls"""
    
    # Quality settings mapping
    QUALITY_SETTINGS = {
        'high': 85,
        'medium': 65,
        'low': 45
    }
    
    # Aspect ratio mappings
    ASPECT_RATIOS = {
        '4:3': (4, 3),
        '16:9': (16, 9),
        '1:1': (1, 1),
        'original': None
    }
    
    def __init__(self):
        pass
    
    def compress_image(self, image_file, quality: str = 'medium', aspect_ratio: str = 'original', 
                      max_size: Optional[int] = None) -> Tuple[bytes, dict]:
        """
        Compress an image with specified quality and aspect ratio
        
        Args:
            image_file: File object or file path
            quality: Quality level ('high', 'medium', 'low')
            aspect_ratio: Aspect ratio ('4:3', '16:9', '1:1', 'original')
            max_size: Maximum file size in bytes (optional)
        
        Returns:
            Tuple of (compressed_image_bytes, metadata_dict)
        """
        # Open and process the image
        if hasattr(image_file, 'read'):
            image_file.seek(0)
            img = Image.open(image_file)
            original_size = len(image_file.read())
            image_file.seek(0)
        else:
            img = Image.open(image_file)
            original_size = os.path.getsize(image_file)
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        original_dimensions = img.size
        
        # Apply aspect ratio transformation if specified
        if aspect_ratio != 'original' and aspect_ratio in self.ASPECT_RATIOS:
            img = self._apply_aspect_ratio(img, aspect_ratio)
        
        # Get quality setting
        jpeg_quality = self.QUALITY_SETTINGS.get(quality, 65)
        
        # Compress image
        compressed_bytes = self._compress_to_bytes(img, jpeg_quality, max_size)
        
        # Prepare metadata
        metadata = {
            'original_dimensions': original_dimensions,
            'final_dimensions': img.size,
            'original_size': original_size,
            'compressed_size': len(compressed_bytes),
            'quality_setting': quality,
            'jpeg_quality': jpeg_quality,
            'aspect_ratio': aspect_ratio,
            'compression_ratio': round((1 - len(compressed_bytes) / original_size) * 100, 2) if original_size > 0 else 0
        }
        
        return compressed_bytes, metadata
    
    def _apply_aspect_ratio(self, img: Image.Image, aspect_ratio: str) -> Image.Image:
        """Apply specified aspect ratio to image"""
        target_width, target_height = self.ASPECT_RATIOS[aspect_ratio]
        current_width, current_height = img.size
        
        # Calculate target dimensions maintaining the aspect ratio
        current_aspect = current_width / current_height
        target_aspect = target_width / target_height
        
        if current_aspect > target_aspect:
            # Image is wider than target aspect ratio - crop width
            new_width = int(current_height * target_aspect)
            new_height = current_height
            left = (current_width - new_width) // 2
            top = 0
            right = left + new_width
            bottom = current_height
        else:
            # Image is taller than target aspect ratio - crop height
            new_width = current_width
            new_height = int(current_width / target_aspect)
            left = 0
            top = (current_height - new_height) // 2
            right = current_width
            bottom = top + new_height
        
        # Crop the image to the target aspect ratio
        cropped_img = img.crop((left, top, right, bottom))
        
        return cropped_img
    
    def _compress_to_bytes(self, img: Image.Image, quality: int, max_size: Optional[int] = None) -> bytes:
        """Compress image to bytes with specified quality"""
        # Initial compression
        img_bytes_io = io.BytesIO()
        img.save(img_bytes_io, format='JPEG', quality=quality, optimize=True)
        compressed_bytes = img_bytes_io.getvalue()
        
        # If max_size is specified and exceeded, reduce quality iteratively
        if max_size and len(compressed_bytes) > max_size:
            current_quality = quality
            while len(compressed_bytes) > max_size and current_quality > 10:
                current_quality -= 5
                img_bytes_io = io.BytesIO()
                img.save(img_bytes_io, format='JPEG', quality=current_quality, optimize=True)
                compressed_bytes = img_bytes_io.getvalue()
        
        return compressed_bytes
    
    def get_supported_formats(self) -> list:
        """Get list of supported image formats"""
        # Get formats from environment variable or use defaults
        formats_str = os.getenv('SUPPORTED_IMAGE_FORMATS', '.jpg,.jpeg,.png,.bmp,.tiff,.webp')
        return [fmt.strip() for fmt in formats_str.split(',')]
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported"""
        _, ext = os.path.splitext(filename.lower())
        return ext in self.get_supported_formats()
    
    def resize_image(self, img: Image.Image, max_width: int = 1920, max_height: int = 1080) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        return img
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"