import json
import os
from datetime import datetime
from pymongo import MongoClient
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self):
        """Initialize history manager with both JSON fallback and MongoDB support"""
        self.json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'history.json')
        self.use_mongodb = True
        self.client = None
        self.db = None
        self.collection = None
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
        
        # Try to connect to MongoDB
        try:
            self._connect_mongodb()
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}. Using JSON fallback.")
            self.use_mongodb = False
    
    def _connect_mongodb(self):
        """Connect to MongoDB using environment variables"""
        connection_string = os.getenv('MONGODB_CONNECTION_STRING')
        database_name = os.getenv('MONGODB_DATABASE_NAME', 'image_compressor')
        collection_name = os.getenv('MONGODB_COLLECTION_NAME', 'compression_history')
        
        if not connection_string:
            raise Exception("MONGODB_CONNECTION_STRING not found in environment variables")
        
        self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        # Test connection
        self.client.admin.command('ping')
        
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        logger.info("Successfully connected to MongoDB")
    
    def add_compression_record(self, filename: str, original_size: int, compressed_size: int, 
                             quality: str, aspect_ratio: str) -> Dict[str, Any]:
        """Add a new compression record to history"""
        record = {
            'filename': filename,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round((1 - compressed_size / original_size) * 100, 2) if original_size > 0 else 0,
            'quality': quality,
            'aspect_ratio': aspect_ratio,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if self.use_mongodb:
            try:
                result = self.collection.insert_one(record)
                record['_id'] = str(result.inserted_id)
                logger.info(f"Record added to MongoDB: {filename}")
            except Exception as e:
                logger.error(f"Failed to add record to MongoDB: {e}")
                self._add_to_json(record)
        else:
            self._add_to_json(record)
        
        return record
    
    def _add_to_json(self, record: Dict[str, Any]):
        """Add record to JSON file as fallback"""
        try:
            history = self._load_json_history()
            record['_id'] = len(history) + 1
            history.append(record)
            
            with open(self.json_file_path, 'w') as f:
                json.dump(history, f, indent=2, default=str)
            logger.info(f"Record added to JSON: {record['filename']}")
        except Exception as e:
            logger.error(f"Failed to add record to JSON: {e}")
    
    def _load_json_history(self) -> List[Dict[str, Any]]:
        """Load history from JSON file"""
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON history: {e}")
        return []
    
    def get_all_history(self) -> List[Dict[str, Any]]:
        """Get all compression history records"""
        if self.use_mongodb:
            try:
                records = list(self.collection.find({}))
                # Convert ObjectId to string
                for record in records:
                    record['_id'] = str(record['_id'])
                return records
            except Exception as e:
                logger.error(f"Failed to fetch from MongoDB: {e}")
                return self._load_json_history()
        else:
            return self._load_json_history()
    
    def get_history_sorted_by_date(self, ascending: bool = False) -> List[Dict[str, Any]]:
        """Get history sorted by date"""
        history = self.get_all_history()
        return sorted(history, key=lambda x: x['timestamp'], reverse=not ascending)
    
    def get_history_sorted_by_size(self, ascending: bool = True) -> List[Dict[str, Any]]:
        """Get history sorted by original file size"""
        history = self.get_all_history()
        return sorted(history, key=lambda x: x['original_size'], reverse=not ascending)
    
    def clear_history(self):
        """Clear all history records"""
        if self.use_mongodb:
            try:
                self.collection.delete_many({})
                logger.info("MongoDB history cleared")
            except Exception as e:
                logger.error(f"Failed to clear MongoDB history: {e}")
        
        # Also clear JSON file
        try:
            with open(self.json_file_path, 'w') as f:
                json.dump([], f)
            logger.info("JSON history cleared")
        except Exception as e:
            logger.error(f"Failed to clear JSON history: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get compression statistics"""
        history = self.get_all_history()
        
        if not history:
            return {
                'total_files': 0,
                'total_original_size': 0,
                'total_compressed_size': 0,
                'average_compression_ratio': 0,
                'best_compression_ratio': 0
            }
        
        total_original = sum(record['original_size'] for record in history)
        total_compressed = sum(record['compressed_size'] for record in history)
        ratios = [record['compression_ratio'] for record in history]
        
        return {
            'total_files': len(history),
            'total_original_size': total_original,
            'total_compressed_size': total_compressed,
            'average_compression_ratio': round(sum(ratios) / len(ratios), 2),
            'best_compression_ratio': max(ratios) if ratios else 0
        }