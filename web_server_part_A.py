"""
SIT540_51FA24
Michael Gluck
Program Assignment 1

File: web_server_part_A.py 
"""
import threading
import socket
import os

class HttpRequest(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        try:
            request = self.client_socket.recv(1024).decode('utf-8')
            print(f"Received request from {self.client_address}:\n{request}")

            # Parse the request line
            lines = request.split("\r\n")
            request_line = lines[0]
            method, path, version = request_line.split(" ")

            if version != "HTTP/1.0":
                response = "HTTP/1.0 505 HTTP Version Not Supported\r\n\r\n"
                self.client_socket.sendall(response.encode('utf-8'))
                return

            # Extract the file name from the request (e.g., "/index.html")
            file_name = path.strip("/")
            if file_name == "":
                file_name = "index.html"

            # Try to open the requested file
            try:
                with open(file_name, 'r') as f:
                    file_content = f.read()
                    content_length = len(file_content)
                    response = f"""HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: {content_length}

{file_content}"""
            except FileNotFoundError:
                # If the file is not found, send a 404 response
                response = """HTTP/1.0 404 Not Found
Content-Type: text/html
Content-Length: 89

<html>
  <body>
    <h1>404 Not Found</h1>
    <p>The requested file could not be found.</p>
  </body>
</html>"""

            # Send the HTTP response to the client
            self.client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            # Close the client socket
            self.client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        request_handler = HttpRequest(client_socket, client_address)
        request_handler.start()

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 6789
    start_server(HOST, PORT)

