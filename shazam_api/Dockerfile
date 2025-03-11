FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rfv /var/lib/apt/lists/*

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
