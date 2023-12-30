# Use the official Python image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Command to run the Python script
CMD ["python", "Scripts/main.py"]
