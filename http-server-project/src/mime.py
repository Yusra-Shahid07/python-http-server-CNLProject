

import os


class MIMETypes:
    """MIME type handler"""
    
    # Common MIME types mapping
    TYPES = {
        # Text
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.txt': 'text/plain',
        
        # Images
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.webp': 'image/webp',
        
        # Fonts
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.ttf': 'font/ttf',
        '.otf': 'font/otf',
        
        # Audio/Video
        '.mp3': 'audio/mpeg',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.ogg': 'audio/ogg',
        
        # Documents
        '.pdf': 'application/pdf',
        '.zip': 'application/zip',
        '.tar': 'application/x-tar',
        '.gz': 'application/gzip',
        
        # Other
        '.wasm': 'application/wasm',
    }
    
    @staticmethod
    def get_mime_type(file_path):
        """
        Get MIME type for a file based on its extension
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: MIME type string
        """
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Return MIME type or default
        return MIMETypes.TYPES.get(ext, 'application/octet-stream')
    
    @staticmethod
    def is_text_type(mime_type):
        """
        Check if MIME type is text-based
        
        Args:
            mime_type (str): MIME type string
            
        Returns:
            bool: True if text-based, False otherwise
        """
        text_types = ['text/', 'application/javascript', 'application/json', 'application/xml']
        return any(mime_type.startswith(t) for t in text_types)
