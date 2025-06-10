FROM python:3.10-slim
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libffi-dev python3-dev build-essential
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 10000
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
