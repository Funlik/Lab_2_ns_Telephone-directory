FROM python:latest

WORKDIR /app
COPY * /app/telephone_directory.py

CMD ["python", "telephone_directory.py"]
