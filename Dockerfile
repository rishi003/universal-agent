# Use Python 3.13 as the base image
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && apt-get clean

ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install the dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the application
CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0"]
