FROM python:3.8-slim

COPY . /api
WORKDIR /api

RUN python3 -m pip install -r requirements.txt
