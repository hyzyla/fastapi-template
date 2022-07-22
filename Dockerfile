FROM python:3.10-slim-bullseye as base

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.1.14

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

# Such as we don't need virtual environment in docker
# we can install requirements directly by pip
RUN poetry export --dev --without-hashes --output=requirements.txt
RUN pip install -r requirements.txt

COPY . /code

ENTRYPOINT ["scripts/start.sh"]
