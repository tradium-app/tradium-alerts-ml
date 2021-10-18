FROM python:3.8.12-bullseye

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "job_runner.py"]
