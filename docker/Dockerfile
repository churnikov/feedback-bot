FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry==1.*

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY ./feedback_bot /code/feedback_bot
COPY ./data/replies /replies

ENV PYTHONPATH "${PYTHONPATH}:/code/feedback_bot"

ENTRYPOINT /bin/bash -c "python3 feedback_bot/main.py"
