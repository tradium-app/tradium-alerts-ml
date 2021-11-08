FROM python:3.11.0a1-slim-bullseye

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# RUN apt-get -y install python3-pip

# COPY . /app
# WORKDIR /app

RUN pip install --upgrade pip

RUN python3 -m pip install fbprophet

# RUN pip install fbprophet
# RUN pip3 install -r requirements.txt

CMD ["python3", "job_runner.py"]
