FROM python:3.5

RUN apt update
Run apt install -y python3
RUN apt install -y python3-pip
COPY . .
RUN pip3 install -r requirements.txt
ENV SECRET_KEY = ${SECRET_KEY}
ENV DATABASE_URI = ${DATABASE_URI}
EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/python", "app.py"]
