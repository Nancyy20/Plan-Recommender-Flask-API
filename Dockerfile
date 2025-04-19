# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variable for Java (you can adjust the version if needed)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Java (if not already available in the base image)
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code
COPY . /app

# Set the working directory to the app
WORKDIR /app

# Expose the port the app will run on
EXPOSE 5000

# Run your app using gunicorn
CMD ["gunicorn", "app:app", "--workers", "4", "--bind", "0.0.0.0:$PORT"]
