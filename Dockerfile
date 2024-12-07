# Use a Python base image
FROM python:3.12-slim

# Install Tesseract and required dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libxrender-dev

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . /app/

# Set the entrypoint for the Streamlit app
CMD ["streamlit", "run", "app.py"]
