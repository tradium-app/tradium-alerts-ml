FROM python:3.8.12-bullseye

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN apt-get -y install python3-pip

# COPY . /app
# WORKDIR /app

# RUN pip install --upgrade pip
RUN pip3 install fbprophet
# RUN pip install fbprophet
# RUN pip3 install -r requirements.txt

CMD ["python3", "job_runner.py"]
