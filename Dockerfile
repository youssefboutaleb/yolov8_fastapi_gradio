# Use an official Python runtime as a parent image
FROM python:3.9-slim
LABEL authors="YOUSSEF-BOUTALEB"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it by setting the PATH
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install libGL.so.1 for OpenCV and other dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get purge -y nvidia-common \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
# These commands will use the binaries from the virtual environment
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
# This will also use the binaries from the virtual environment
CMD ["python", "main.py"]
