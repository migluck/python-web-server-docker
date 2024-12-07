import threading
import socket

# HttpRequest class handles individual requests in separate threads
class HttpRequest(threading.Thread):
    def __init__(self, client_socket, client_address):
        # Initialize the thread and pass the client socket and address
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        # Handle the HTTP request and send the HTTP response
        try:
            request = self.client_socket.recv(1024).decode('utf-8')
            print(f"Received request from {self.client_address}:\n{request}")
            
            # Prepare the HTTP response
            response = """HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: 61

<html>
  <body>
    <h1>Welcome to my multi-threaded server!</h1>
  </body>
</html>
"""
            
            # Send the HTTP response to the client
            self.client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            # Close the client socket
            self.client_socket.close()

# The main server function
def start_server(host, port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Enable the server to accept connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Create a new HttpRequest thread to handle the client request
        request_handler = HttpRequest(client_socket, client_address)

        # Start the thread to process the request
        request_handler.start()

# Main entry point
if __name__ == "__main__":
    HOST = '0.0.0.0'  # Listen on all available network interfaces
    PORT = 6789        # The port you want to listen on
    
    # Start the server
    start_server(HOST, PORT)

