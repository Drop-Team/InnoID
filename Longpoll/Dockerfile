FROM python:3.10

WORKDIR /longpoll
COPY requirements.txt /longpoll

RUN pip install -r requirements.txt

ENV PROMETHEUS_MULTIPROC_DIR=prometheus-multiproc

COPY . /longpoll

CMD ["gunicorn", "-c", "gunicorn_config.py", "--worker-class=gthread", "longpoll:create_app()"]
