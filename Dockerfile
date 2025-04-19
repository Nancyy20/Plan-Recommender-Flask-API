# Use a base image with both Python and OpenJDK preinstalled
FROM openjdk:11-jdk-slim

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the application port
EXPOSE 8080

# Command to run your Flask app
CMD ["gunicorn", "app:app", "--workers", "4", "--bind", "0.0.0.0:$PORT"]
