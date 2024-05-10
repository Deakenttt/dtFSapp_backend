# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# FFmpeg installation
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /main

# Add current directory files to /main in container
ADD . /main

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Install necessary packages, Flask and ffmpeg-python
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
# EXPOSE 5000

# Run main.py (Flask server) when the container launches
CMD gunicorn --bind 0.0.0.0:$PORT main:app