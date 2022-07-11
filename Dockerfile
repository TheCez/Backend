FROM python:3.10-slim

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y curl unzip
RUN curl https://rclone.org/install.sh | bash

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "35500"]