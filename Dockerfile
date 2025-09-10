# Use an official Python runtime as a parent image
FROM python:3.13.0b3-slim

LABEL authors="YOUSSEF-BOUTALEB"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it by setting the PATH
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install libGL.so.1 for OpenCV and other dependencies
# Combine update, install, and cleanup into a single RUN to reduce layers and image size
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get purge -y --auto-remove nvidia-common \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
# These commands will use the binaries from the virtual environment
# Upgrade pip and install dependencies in a single RUN to reduce layers
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
# This will also use the binaries from the virtual environment
CMD ["python", "main.py"]
