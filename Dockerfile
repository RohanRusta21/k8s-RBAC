# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Create and set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure the .kube directory exists and copy the kubeconfig file
RUN mkdir -p /root/.kube

# Copy kubeconfig from the build context to the image
COPY kubeconfig /root/.kube/config

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run"]
