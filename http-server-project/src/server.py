import socket
import threading
import os
from parser import HTTPParser
from connection import ConnectionHandler


class HTTPServer:
    """Main HTTP Server class"""
    
    def __init__(self, host='127.0.0.1', port=8080, www_dir='www'):
        """
        Initialize the HTTP server
        
        Args:
            host (str): Host address to bind to
            port (int): Port number to listen on
            www_dir (str): Directory to serve files from
        """
        self.host = host
        self.port = port
        self.www_dir = os.path.abspath(www_dir)
        self.server_socket = None
        self.running = False
        
    def start(self):
        """Start the HTTP server"""
        try:
            # Create socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind and listen
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"🚀 HTTP Server started on http://{self.host}:{self.port}")
            print(f"📁 Serving files from: {self.www_dir}")
            print("Press Ctrl+C to stop the server\n")
            
            # Accept connections
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"📥 Connection from {client_address[0]}:{client_address[1]}", flush=True)
                    
                    # Handle connection in a new thread
                    handler = ConnectionHandler(client_socket, client_address, self.www_dir)
                    thread = threading.Thread(target=handler.handle)
                    thread.daemon = True
                    thread.start()
                    
                except KeyboardInterrupt:
                    print("\n\n⏹️  Shutting down server...")
                    break
                except Exception as e:
                    if self.running:
                        print(f"❌ Error accepting connection: {e}")
                    
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Stop the HTTP server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("✅ Server stopped")


def main():
    """Main entry point"""
    # Create www directory if it doesn't exist
    www_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'www')
    if not os.path.exists(www_dir):
        os.makedirs(www_dir)
    
    # Start server
    server = HTTPServer(host='127.0.0.1', port=8080, www_dir=www_dir)
    server.start()


if __name__ == '__main__':
    main()
