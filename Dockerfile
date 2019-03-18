FROM python:3
MAINTAINER jonachanboi@hamtyskeren.ru


RUN mkdir -p /src/shitbot
WORKDIR /src/shitbot


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

