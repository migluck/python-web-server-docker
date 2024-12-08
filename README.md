CSIT540_51FA25
Michael Gluck
Program Assignment 1

# Python Multi-Threaded Web Server with Docker

## Description

This is a simple Python-based web server that listens on a specified port, accepts incoming HTTP requests, processes them in separate threads, and serves static HTML content. The server supports **HTTP/1.0** and responds with a basic HTML page. It uses **Docker** to create a containerized environment for easy deployment.

## Features

- Multi-threaded HTTP server that handles multiple client requests simultaneously.
- Basic support for **HTTP/1.0** with `GET` requests.
- Serves static HTML files from the current directory.
- Returns a **404 Not Found** response if the requested file is missing.
- Runs inside a Docker container for easy deployment.

## Prerequisites

Before running the Docker container, ensure that you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.x**: Required for building and running the Python web server.

## Instructions

- docker build -t python-web-server .
- docker run -p 6789:6789 python-web-server
