from flask import Flask, jsonify, request, send_file
import os
import io
import base64
from datetime import datetime
from dotenv import load_dotenv

from Service.arrangeFiles import create_deque
from Service.quicksort import quickSort
from Service.history_db import HistoryManager
from Service.image_tools import ImageCompressor
from Service.merge_sort import merge_sort_by_date, merge_sort_by_size, merge_sort_by_compression_ratio

# Load environment variables
load_dotenv()

app = Flask(__name__)
history_manager = HistoryManager()
image_compressor = ImageCompressor()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to my Flask API!"})

@app.route('/hello/<name>', methods=['GET'])
def hello(name):
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/upload-images/<quality>/<maxSize>/<resize>', methods=['POST'])
def upload_images(quality,maxSize,resize):
    if 'images' not in request.files:
        return jsonify({'error' : 'No images part in the request'}), 400
    
    image_files = request.files.getlist('images')
    if not image_files:
        return jsonify({'error' : 'No images selected for upload'}), 400
    
    uploaded_fileSize = []
    for file in image_files:
        size = len(file.read())
        file.seek(0)  # reset pointer
        uploaded_fileSize.append(size)
        
    uploaded_files = []
    for fileAll in image_files:
          uploaded_files.append(fileAll)
    
    quickSort(uploaded_files,uploaded_fileSize,0,len(uploaded_fileSize) - 1)  
    created_dequeue = create_deque(uploaded_files)   
    fileNameDequeue = create_deque(uploaded_fileSize) 
    # return jsonify({
    #     'message ': uploaded_fileSize,
    #     'quality ': quality,
    #     'max ': maxSize
    #     }),200
    
    # Process each image with compression and history tracking
    processed_files = []
    for i, file in enumerate(uploaded_files):
        try:
            # Compress image with specified quality and aspect ratio
            compressed_bytes, metadata = image_compressor.compress_image(
                file, quality=quality, aspect_ratio=resize
            )
            
            # Add to history
            history_record = history_manager.add_compression_record(
                filename=file.filename,
                original_size=metadata['original_size'],
                compressed_size=metadata['compressed_size'],
                quality=quality,
                aspect_ratio=resize
            )
            
            # Prepare response data
            processed_files.append({
                'filename': file.filename,
                'original_size': metadata['original_size'],
                'compressed_size': metadata['compressed_size'],
                'compression_ratio': metadata['compression_ratio'],
                'original_dimensions': metadata['original_dimensions'],
                'final_dimensions': metadata['final_dimensions'],
                'compressed_data': base64.b64encode(compressed_bytes).decode('utf-8')
            })
            
        except Exception as e:
            processed_files.append({
                'filename': file.filename,
                'error': f'Processing failed: {str(e)}'
            })
    
    return jsonify({
        "message": "Images processed successfully",
        "processed_files": processed_files,
        "total_files": len(processed_files)
    }), 200

@app.route('/history', methods=['GET'])
def get_history():
    """Get compression history with optional sorting"""
    sort_by = request.args.get('sort_by', 'date')  # date, size, compression_ratio
    order = request.args.get('order', 'desc')  # asc, desc
    
    try:
        history = history_manager.get_all_history()
        
        # Apply merge sort based on sort criteria
        ascending = order == 'asc'
        if sort_by == 'date':
            sorted_history = merge_sort_by_date(history, ascending)
        elif sort_by == 'size':
            sorted_history = merge_sort_by_size(history, ascending)
        elif sort_by == 'compression_ratio':
            sorted_history = merge_sort_by_compression_ratio(history, ascending)
        else:
            sorted_history = history
        
        return jsonify({
            "history": sorted_history,
            "total_records": len(sorted_history),
            "sort_by": sort_by,
            "order": order
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve history: {str(e)}"}), 500

@app.route('/history/statistics', methods=['GET'])
def get_history_statistics():
    """Get compression statistics"""
    try:
        stats = history_manager.get_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get statistics: {str(e)}"}), 500

@app.route('/history/clear', methods=['DELETE'])
def clear_history():
    """Clear all compression history"""
    try:
        history_manager.clear_history()
        return jsonify({"message": "History cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to clear history: {str(e)}"}), 500

@app.route('/quality-options', methods=['GET'])
def get_quality_options():
    """Get available quality options"""
    return jsonify({
        "quality_options": list(ImageCompressor.QUALITY_SETTINGS.keys()),
        "quality_settings": ImageCompressor.QUALITY_SETTINGS
    }), 200

@app.route('/aspect-ratios', methods=['GET'])
def get_aspect_ratios():
    """Get available aspect ratio options"""
    ratios = {k: v for k, v in ImageCompressor.ASPECT_RATIOS.items() if v is not None}
    ratios['original'] = 'Keep original aspect ratio'
    
    return jsonify({
        "aspect_ratios": list(ImageCompressor.ASPECT_RATIOS.keys()),
        "aspect_ratio_details": ratios
    }), 200

@app.route('/supported-formats', methods=['GET'])
def get_supported_formats():
    """Get supported image formats"""
    return jsonify({
        "supported_formats": image_compressor.get_supported_formats()
    }), 200
    
    
if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
