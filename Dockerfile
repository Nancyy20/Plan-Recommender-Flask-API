# Base image
FROM python:3.8

ENV JAVA_HOME=/usr/local/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install Python dependencies
RUN pip install  -r requirements.txt


# Set the entrypoint command
ENTRYPOINT ["python"]
CMD [ "app.py" ]
