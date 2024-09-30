FROM python:3.11-slim

WORKDIR /booking_project

COPY requirements.txt .

RUN pip install -r /booking_project/requirements.txt

COPY . .

RUN chmod a+x /booking_project/scripts/*.sh