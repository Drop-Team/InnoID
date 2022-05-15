FROM python:3.10

WORKDIR /innoid-longpoll
COPY requirements.txt /innoid-longpoll

RUN pip install -r requirements.txt

ENV PROMETHEUS_MULTIPROC_DIR=prometheus-multiproc

COPY . /innoid-longpoll

CMD ["gunicorn", "-c", "gunicorn_config.py", "--worker-class=gthread", "longpoll:create_app()"]
