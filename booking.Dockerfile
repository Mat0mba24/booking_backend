FROM python:3.11-slim

WORKDIR /booking_project

COPY requirements.txt .

RUN pip install -r /booking_project/requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000", "--forwarded-allow-ips='*'", "--proxy-headers"]