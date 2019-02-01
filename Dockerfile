FROM python:3.6-slim
COPY . /ProxyPool
WORKDIR /ProxyPool
RUN pip3 install -r requirements.txt
CMD ["python", "run.py"]