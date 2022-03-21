FROM python:3.10

WORKDIR /innoid-api
COPY requirements.txt /innoid-api

RUN pip install -r requirements.txt

ENV PROMETHEUS_MULTIPROC_DIR=prometheus-multiproc

COPY . /innoid-api

CMD ["gunicorn", "-c", "gunicorn_config.py", "--worker-class=gthread", "api:create_app()"]
