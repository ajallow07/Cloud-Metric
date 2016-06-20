FROM python:2.7
ADD . /Cloud-Metric
WORKDIR /Cloud-Metric

RUN pip install -r requirements.txt
