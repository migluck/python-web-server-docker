# Use Python 3.10 image as base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY web_server.py /app/
COPY index.html /app/

# Install any Python dependencies if you have a requirements.txt
# COPY requirements.txt /app/
# RUN pip install -r requirements.txt

# Expose port 6789 to access the server
EXPOSE 6789

# Command to run the Python web server
CMD ["python", "web_server.py"]

