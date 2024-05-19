# Stage 1: Build stage
FROM python:3.9-slim AS builder

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pkg-config \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source $VIRTUAL_ENV/bin/activate

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.9-slim

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create the virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source $VIRTUAL_ENV/bin/activate

# Copy the virtual environment from the builder stage
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# Set the working directory in the container
WORKDIR /app

# Copy the application's code into the container
COPY . .

# Start your Flask application
CMD ["flask", "run", "--host=0.0.0.0"]


#docker run -v $(pwd):/app my_image_name

#sudo docker run  -v $(pwd):/app -p 5000:5000 slim_py:latest

#docker build --no-cache -t slim_py .
