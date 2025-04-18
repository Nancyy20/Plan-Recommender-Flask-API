# Base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install Python dependencies
RUN pip install  -r requirements.txt


# Set the entrypoint command
ENTRYPOINT ["python"]
CMD [ "app.py" ]
