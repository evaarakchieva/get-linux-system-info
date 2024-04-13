FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

EXPOSE 80

CMD ["python3", "generate_output.py"]
