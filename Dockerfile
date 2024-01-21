FROM python:3.11-alpine3.18

RUN apk add curl

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app/

HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

CMD ["python3", "/app/main.py"]