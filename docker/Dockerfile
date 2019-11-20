FROM python:3.7-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry \
    && poetry config settings.virtualenvs.create false

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY ./feedback_bot /code/feedback_bot

ENTRYPOINT /bin/bash -c "python3 feedback_bot/main.py"
