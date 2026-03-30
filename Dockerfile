# Use official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory for the app
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the generated directory and give it wide-open permissions
RUN mkdir -p generated && chmod 777 generated

# Change to the backend directory to run the server
WORKDIR /app

# Expose the ports
EXPOSE 8000
EXPOSE 8501

# Command to run the application using Uvicorn
CMD ["bash", "./startup.sh"]