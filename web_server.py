import socket
import threading

# Function to handle client connections and respond with an HTML page
def handle_client(client_socket):
    try:
        # Receive the HTTP request from the client
        request = client_socket.recv(1024).decode('utf-8')
        
        # Print the HTTP request to the server console
        print(f"Received HTTP request:\n{request}")
        
        # Prepare the HTTP response (static HTML content)
        response = """HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: 61

<html>
  <body>
    <h1>Welcome to my Dockerized server!</h1>
  </body>
</html>
"""
        
        # Send the HTTP response to the client
        client_socket.sendall(response.encode('utf-8'))
        
        # Close the connection
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

# Function to start the server
def start_server(host, port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow the socket to be reused quickly
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the provided address and port
    server_socket.bind((host, port))
    
    # Enable the server to accept connections (maximum 5 in the queue)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")
    
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        
        # Handle the client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Main entry point
if __name__ == "__main__":
    # Host and port configuration
    HOST = '0.0.0.0'  # Listen on all available network interfaces
    PORT = 6789        # The port you want to listen on
    
    # Start the server
    start_server(HOST, PORT)

