FROM python:3.6-slim
COPY . /ProxyPool
WORKDIR /ProxyPool
RUN apt-get update \
    && apt-get install vim \
    && pip3 install -r requirements.txt
