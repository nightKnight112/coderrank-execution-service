FROM python:3.11-slim

RUN apt-get update && apt-get install -y default-jdk

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /home/codes

CMD ["python", "./app.py"]