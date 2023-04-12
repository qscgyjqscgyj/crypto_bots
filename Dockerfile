FROM python:3.9-slim

COPY reqs.txt .
RUN pip install -r reqs.txt

WORKDIR /app

COPY . .

EXPOSE 8000

CMD python ./main.py
