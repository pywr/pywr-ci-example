FROM python:3.7-slim-stretch

RUN pip install pipenv
COPY Pipfile* ./
RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile

COPY . /app
WORKDIR /app

CMD ["python", "app/thames.py"]
