FROM python:3.10

WORKDIR /api
COPY requirements.txt /api

RUN pip install -r requirements.txt

ENV PROMETHEUS_MULTIPROC_DIR=prometheus-multiproc

COPY . /api

CMD ["gunicorn", "-c", "gunicorn_config.py", "--worker-class=gthread", "api:create_app()", "--access-logfile", "guni.log"]
