# Use a lightweight Python base image
FROM python:3.10-slim

# Install system packages
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libffi-dev python3-dev build-essential

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port Render will use
EXPOSE 10000

# Run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
