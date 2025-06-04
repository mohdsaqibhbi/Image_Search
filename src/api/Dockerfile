FROM python:3.10-slim

WORKDIR /server

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ca-certificates nginx curl supervisor

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying Source
COPY nginx.conf /etc/nginx/conf.d/
COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["supervisord", "-c", "supervisord.conf", "-n"]