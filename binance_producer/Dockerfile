FROM python:3.8-slim

RUN mkdir ./producer

ENV INDEX 1

COPY . ./producer

WORKDIR producer

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD ["python3", "producer.py"]