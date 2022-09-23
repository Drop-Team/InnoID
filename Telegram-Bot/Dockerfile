FROM python:3.10

WORKDIR /tg-bot
COPY requirements.txt /tg-bot

RUN pip install -r requirements.txt

COPY . /tg-bot

CMD ["python", "-u", "run.py"]
