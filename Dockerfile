# Use an Anaconda base image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the environment.yml file to the container
COPY base_environment.yml /app/base_environment.yml

# Create the environment using the environment.yml file
RUN conda env create -f /app/base_environment.yml --force

# Make port 80 available to the world outside this container
EXPOSE 80

# Use the environment created above
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# The command to run the app
ENTRYPOINT ["conda", "run", "-n", "myenv", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
