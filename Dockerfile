# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python web server script into the container
COPY web_server.py /app/web_server.py

# Expose the port that the server will run on
EXPOSE 6789

# Install necessary dependencies (no external dependencies needed for this server)
RUN apt-get update && apt-get install -y python3 && apt-get clean

# Run the Python script when the container starts
CMD ["python", "web_server.py"]

