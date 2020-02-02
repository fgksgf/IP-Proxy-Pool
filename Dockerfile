FROM python:3.6-slim
COPY . /code
WORKDIR /code
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "run.py"]