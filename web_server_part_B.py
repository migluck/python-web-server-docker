"""
SIT540_51FA24
Michael Gluck
Program Assignment 1

File: web_server_part_B.py 
"""
import socket
import threading
import os

# Define CRLF (Carriage Return Line Feed) to comply with HTTP response format
CRLF = "\r\n"

# MIME types for different file extensions
MIME_TYPES = {
    '.html': 'text/html',
    '.htm': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.png': 'image/png',
    '.txt': 'text/plain',
}

# HttpRequest Class to handle each incoming HTTP request in a separate thread
class HttpRequest(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)  # Initialize the threading.Thread class
        self.client_socket = client_socket

    def process_request(self):
        # Receive the HTTP request (GET request line)
        request = self.client_socket.recv(1024).decode('utf-8')
        print(f"Request received: {request}")

        # Extract the filename from the request (GET /index.html HTTP/1.1)
        try:
            request_line = request.splitlines()[0]
            tokens = request_line.split(" ")
            if len(tokens) < 2:
                self.send_error("400 Bad Request")
                return

            file_name = tokens[1]
            if file_name == '/':
                file_name = '/index.html'  # Default to index.html if no file is requested

            # Prepend the dot to make the path relative to the current directory
            file_name = '.' + file_name

            # Check if the file exists
            if os.path.exists(file_name) and os.path.isfile(file_name):
                self.send_response(file_name)
            else:
                self.send_error("404 Not Found")
        except Exception as e:
            self.send_error("500 Internal Server Error")
            print(f"Error processing request: {e}")

    def send_response(self, file_name):
        """Send the requested file content with the appropriate headers."""
        try:
            # Determine the MIME type
            content_type = self.get_content_type(file_name)

            # Open the file to send its content
            with open(file_name, 'rb') as file:
                content = file.read()
            
            # Prepare the response for HTTP/1.0
            status_line = "HTTP/1.0 200 OK" + CRLF
            content_type_line = f"Content-Type: {content_type}" + CRLF
            content_length_line = f"Content-Length: {len(content)}" + CRLF
            connection_close_line = "Connection: close" + CRLF  # HTTP/1.0 closes connection by default

            # Send the HTTP response
            self.client_socket.sendall(status_line.encode('utf-8'))
            self.client_socket.sendall(content_type_line.encode('utf-8'))
            self.client_socket.sendall(content_length_line.encode('utf-8'))
            self.client_socket.sendall(connection_close_line.encode('utf-8'))  # Explicit close
            self.client_socket.sendall(CRLF.encode('utf-8'))  # Blank line to end headers
            self.client_socket.sendall(content)  # Send the file content

        except Exception as e:
            print(f"Error sending file: {e}")
            self.send_error("500 Internal Server Error")

    def send_error(self, error_message):
        """Send an error message when a file is not found or another error occurs."""
        if error_message == "404 Not Found":
            entity_body = "<html><body><h1>404 Not Found</h1></body></html>"
            status_line = "HTTP/1.0 404 Not Found" + CRLF
        elif error_message == "400 Bad Request":
            entity_body = "<html><body><h1>400 Bad Request</h1></body></html>"
            status_line = "HTTP/1.0 400 Bad Request" + CRLF
        else:
            entity_body = "<html><body><h1>500 Internal Server Error</h1></body></html>"
            status_line = "HTTP/1.0 500 Internal Server Error" + CRLF

        content_type_line = "Content-Type: text/html" + CRLF
        content_length_line = f"Content-Length: {len(entity_body)}" + CRLF
        connection_close_line = "Connection: close" + CRLF  # Ensure connection is closed for HTTP/1.0

        self.client_socket.sendall(status_line.encode('utf-8'))
        self.client_socket.sendall(content_type_line.encode('utf-8'))
        self.client_socket.sendall(content_length_line.encode('utf-8'))
        self.client_socket.sendall(connection_close_line.encode('utf-8'))  # Explicit close
        self.client_socket.sendall(CRLF.encode('utf-8'))  # Blank line to end headers
        self.client_socket.sendall(entity_body.encode('utf-8'))  # Send the error message

        self.client_socket.close()

    def get_content_type(self, file_name):
        """Determine the MIME type based on the file extension."""
        _, extension = os.path.splitext(file_name)
        return MIME_TYPES.get(extension, "application/octet-stream")

    def run(self):
        try:
            self.process_request()  # Process the request and send a response
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error("500 Internal Server Error")


# Main WebServer class
def start_server(host, port):
    # Create a TCP socket and bind it to the given host and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # The server will allow up to 5 simultaneous connections

    print(f"Server listening on {host}:{port}...")

    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Create an HttpRequest object to handle the request
        request_handler = HttpRequest(client_socket)

        # Create a new thread to handle the request concurrently
        thread = threading.Thread(target=request_handler.run)
        thread.start()

if __name__ == "__main__":
    HOST = '0.0.0.0'  # Listen on all available network interfaces
    PORT = 6789        # Define the port to listen on

    start_server(HOST, PORT)

