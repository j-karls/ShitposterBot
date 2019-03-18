FROM python:3
MAINTAINER jonachanboi@hamtyskeren.ru


RUN mkdir -p /src/shitbot
WORKDIR /src/shitbot


COPY requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY . .

RUN python main.py