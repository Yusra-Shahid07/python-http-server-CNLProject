


class HTTPParser:
    """HTTP Request Parser"""
    
    @staticmethod
    def parse_request(request_data):
        """
        Parse HTTP request
        
        Args:
            request_data (bytes): Raw HTTP request data
            
        Returns:
            dict: Parsed request with method, path, version, headers, and body
        """
        try:
            # Decode request
            request_text = request_data.decode('utf-8', errors='ignore')
            
            # Split headers and body
            parts = request_text.split('\r\n\r\n', 1)
            header_section = parts[0]
            body = parts[1] if len(parts) > 1 else ''
            
            # Split into lines
            lines = header_section.split('\r\n')
            
            # Parse request line
            request_line = lines[0]
            method, path, version = HTTPParser._parse_request_line(request_line)
            
            # Parse headers
            headers = HTTPParser._parse_headers(lines[1:])
            
            return {
                'method': method,
                'path': path,
                'version': version,
                'headers': headers,
                'body': body
            }
            
        except Exception as e:
            print(f"❌ Error parsing request: {e}")
            return None
    
    @staticmethod
    def _parse_request_line(line):
        """
        Parse HTTP request line
        
        Args:
            line (str): Request line (e.g., "GET /index.html HTTP/1.1")
            
        Returns:
            tuple: (method, path, version)
        """
        parts = line.split(' ')
        if len(parts) != 3:
            raise ValueError(f"Invalid request line: {line}")
        
        method = parts[0].upper()
        path = parts[1]
        version = parts[2]
        
        return method, path, version
    
    @staticmethod
    def _parse_headers(lines):
        """
        Parse HTTP headers
        
        Args:
            lines (list): List of header lines
            
        Returns:
            dict: Dictionary of headers
        """
        headers = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        return headers
    
    @staticmethod
    def build_response(status_code, status_text, headers=None, body=b''):
        """
        Build HTTP response
        
        Args:
            status_code (int): HTTP status code
            status_text (str): HTTP status text
            headers (dict): Response headers
            body (bytes): Response body
            
        Returns:
            bytes: Complete HTTP response
        """
        if headers is None:
            headers = {}
        
        # Status line
        response = f"HTTP/1.1 {status_code} {status_text}\r\n"
        
        # Add Content-Length if not present
        if 'content-length' not in [k.lower() for k in headers.keys()]:
            headers['Content-Length'] = len(body)
        
        # Add headers
        for key, value in headers.items():
            response += f"{key}: {value}\r\n"
        
        # End of headers
        response += "\r\n"
        
        # Convert to bytes and add body
        response_bytes = response.encode('utf-8')
        if isinstance(body, str):
            body = body.encode('utf-8')
        
        return response_bytes + body
