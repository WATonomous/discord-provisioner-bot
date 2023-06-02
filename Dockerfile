FROM python:3.11-alpine3.18

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r /app/requirements.txt

CMD ["python3", "/app/main.py"]