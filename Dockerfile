FROM python:3.6.4-jessie
MAINTAINER "jeffrey77918@gmail.com"

COPY . /crawler

WORKDIR /crawler

RUN pip install -r requirements.txt

CMD python crawler.py
