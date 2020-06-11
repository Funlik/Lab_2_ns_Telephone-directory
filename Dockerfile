FROM python:3-alpine

COPY * /apps/subredditfetcher/
WORKDIR /apps/subredditfetcher/

CMD ["python", "telephone dorectory.py"]
