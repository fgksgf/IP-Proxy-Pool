FROM python:3.6-slim
COPY . /code
WORKDIR /code
EXPOSE 5000
RUN pip3 install -r requirements.txt
CMD ["python", "run.py"]