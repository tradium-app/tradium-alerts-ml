FROM python:3.8.12-bullseye

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY . /app
WORKDIR /app

# RUN pip install --upgrade pip
RUN pip install numpy pystan pandas fbprophet
# RUN pip install fbprophet
# RUN pip3 install -r requirements.txt

CMD ["python3", "job_runner.py"]
