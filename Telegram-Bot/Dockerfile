FROM python:3.10

WORKDIR /innoid-tg-bot
COPY requirements.txt /innoid-tg-bot

RUN pip install -r requirements.txt

COPY . /innoid-tg-bot

CMD ["python", "run.py"]
