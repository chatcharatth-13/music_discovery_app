# Use an official lightweight Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the web application file into the container
COPY index.html .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run a simple web server when the container launches
# This command serves the files in the current directory ( /app ) on port 8000
CMD [ "python", "-m", "http.server", "8000" ]
