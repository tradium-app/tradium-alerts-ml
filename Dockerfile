FROM tensorflow/tensorflow

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY . /app

WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "job_runner.py"]
