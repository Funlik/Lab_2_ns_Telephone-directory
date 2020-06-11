FROM python:latest

WORKDIR /app
COPY * /app

CMD ["python", "telephone_directory.py"]
