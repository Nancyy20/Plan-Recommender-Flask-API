# Base image
# FROM python:3.9

FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-11-jre-headless
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"
ENV TF_ENABLE_ONEDNN_OPTS = 0

# ENV JAVA_HOME=/usr/local/lib/jvm/java-11-openjdk-amd64
# ENV PATH=$JAVA_HOME/bin:$PATH
# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install Python dependencies
RUN pip install  -r requirements.txt


# Set the entrypoint command
ENTRYPOINT ["python"]
CMD [ "app.py" ]
