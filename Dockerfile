# Use the official Python image
FROM python:latest

# Set the working directory in the container
WORKDIR /DatasetFinder

# Copy the current directory contents into the container at /app
COPY . /DatasetFinder

# Install dependencies
RUN pip install requests

# Command to run the Python script
CMD ["python", "Scripts/main.py"]
