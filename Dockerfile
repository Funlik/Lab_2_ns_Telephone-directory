FROM python:latest

WORKDIR /app
COPY ./telephone_directory.py .

CMD ["python", "telephone_directory.py"]
