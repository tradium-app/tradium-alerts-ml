FROM python:3.8.12-bullseye

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pystan
RUN pip3 install -r requirements.txt

CMD ["python3", "job_runner.py"]
