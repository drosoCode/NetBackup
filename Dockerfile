FROM python:3

WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y git tzdata && pip3 install -r requirements.txt
COPY . .
RUN chmod +x main.py && git config --global user.email "" && git config --global user.name "NetBackup"

CMD ["/app/main.py"]