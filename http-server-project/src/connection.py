import os
import socket
from parser import HTTPParser
from mime import MIMETypes


class ConnectionHandler:
    """Handles individual HTTP connections"""
    
    def __init__(self, client_socket, client_address, www_dir):
        """
        Initialize connection handler
        
        Args:
            client_socket: Client socket object
            client_address: Client address tuple
            www_dir (str): Directory to serve files from
        """
        self.client_socket = client_socket
        self.client_address = client_address
        self.www_dir = www_dir
        
    def handle(self):
        """Handle the client connection with Keep-Alive support"""
        try:
            # Set timeout for keep-alive
            self.client_socket.settimeout(5)
            
            # Counter for requests on this single connection
            request_count = 0
            
            while True:
                try:
                    # Receive request
                    request_data = self.client_socket.recv(4096)
                    
                    if not request_data:
                        break
                    
                    request_count += 1
                    
                    # Parse request
                    request = HTTPParser.parse_request(request_data)
                    
                    if not request:
                        self._send_error(400, "Bad Request")
                        break
                    
                    # Explicit proof for demo
                    if request_count > 1:
                        print(f"🔄 [PERSISTENCE] Reusing connection for request #{request_count}", flush=True)
                    
                    # Log request
                    print(f"📨 {request['method']} {request['path']}", flush=True)
                    
                    # Check for Connection: close header
                    connection_header = request['headers'].get('connection', '').lower()
                    should_close = connection_header == 'close'
                    
                    # Handle request based on method
                    if request['method'] == 'GET':
                        self._handle_get(request, not should_close)
                    elif request['method'] == 'HEAD':
                        self._handle_head(request, not should_close)
                    else:
                        self._send_error(405, "Method Not Allowed")
                        should_close = True
                        
                    if should_close:
                        break
                        
                except socket.timeout:
                    # Connection timed out
                    break
                    
        except Exception as e:
            print(f"❌ Error handling connection: {e}")
        finally:
            self.client_socket.close()
    
    def _handle_get(self, request, keep_alive=True):
        """Handle GET request"""
        file_path = self._get_file_path(request['path'])
        
        if not file_path:
            self._send_error(404, "Not Found")
            return
        
        try:
            # Read file
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Get MIME type
            mime_type = MIMETypes.get_mime_type(file_path)
            
            # Build response
            headers = {
                'Content-Type': mime_type,
                'Content-Length': len(content),
                'Server': 'Python-HTTP-Server/1.0',
                'Connection': 'keep-alive' if keep_alive else 'close'
            }
            
            if keep_alive:
                headers['Keep-Alive'] = 'timeout=5'
            
            response = HTTPParser.build_response(200, "OK", headers, content)
            self.client_socket.sendall(response)
            
            print(f"✅ 200 OK - {request['path']} ({len(content)} bytes)", flush=True)
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            self._send_error(500, "Internal Server Error")
    
    def _handle_head(self, request, keep_alive=True):
        """Handle HEAD request"""
        file_path = self._get_file_path(request['path'])
        
        if not file_path:
            self._send_error(404, "Not Found")
            return
        
        try:
            # Get file size
            file_size = os.path.getsize(file_path)
            mime_type = MIMETypes.get_mime_type(file_path)
            
            # Build response (no body)
            headers = {
                'Content-Type': mime_type,
                'Content-Length': file_size,
                'Server': 'Python-HTTP-Server/1.0',
                'Connection': 'keep-alive' if keep_alive else 'close'
            }

            if keep_alive:
                headers['Keep-Alive'] = 'timeout=5'
            
            response = HTTPParser.build_response(200, "OK", headers, b'')
            self.client_socket.sendall(response)
            
            print(f"✅ 200 OK - {request['path']} (HEAD)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self._send_error(500, "Internal Server Error")
    
    def _get_file_path(self, url_path):
        """
        Get file system path from URL path
        
        Args:
            url_path (str): URL path
            
        Returns:
            str: File system path or None if invalid
        """
        # Remove query string
        if '?' in url_path:
            url_path = url_path.split('?')[0]
        
        # Default to index.html for root
        if url_path == '/':
            url_path = '/index.html'
        
        # Remove leading slash
        url_path = url_path.lstrip('/')
        
        # Build full path
        file_path = os.path.join(self.www_dir, url_path)
        file_path = os.path.abspath(file_path)
        
        # Security check: ensure path is within www_dir
        if not file_path.startswith(self.www_dir):
            print(f"⚠️  Security: Attempted access outside www directory: {url_path}")
            return None
        
        # Check if file exists
        if not os.path.isfile(file_path):
            return None
        
        return file_path
    
    def _send_error(self, status_code, status_text):
        """
        Send error response
        
        Args:
            status_code (int): HTTP status code
            status_text (str): HTTP status text
        """
        body = f"""<!DOCTYPE html>
<html>
<head>
    <title>{status_code} {status_text}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 100px auto;
            text-align: center;
        }}
        h1 {{
            color: #e74c3c;
            font-size: 72px;
            margin: 0;
        }}
        h2 {{
            color: #333;
            font-weight: normal;
        }}
    </style>
</head>
<body>
    <h1>{status_code}</h1>
    <h2>{status_text}</h2>
    <p>Python HTTP Server</p>
</body>
</html>"""
        
        headers = {
            'Content-Type': 'text/html',
            'Server': 'Python-HTTP-Server/1.0'
        }
        
        response = HTTPParser.build_response(status_code, status_text, headers, body.encode('utf-8'))
        self.client_socket.sendall(response)
        
        print(f"⚠️  {status_code} {status_text}")
