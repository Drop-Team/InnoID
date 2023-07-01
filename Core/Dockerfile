FROM python:3.11.4-slim-bullseye AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /source/
RUN pip install poetry
COPY poetry.lock pyproject.toml /source/
RUN poetry config virtualenvs.create false && poetry install

COPY . /source/

ENV PYTHONPATH=/source/innoid_core

ENTRYPOINT ["uvicorn", "innoid_core.main_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

FROM production as development

ENTRYPOINT ["uvicorn", "innoid_core.main_fastapi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
