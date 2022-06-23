FROM python:3.8.10-slim

RUN apt-get update -y && apt-get install -y vim gettext apt-utils libpq-dev python3-dev python3-pip

WORKDIR /srv/

COPY ./data-app/ ./requirements.txt ./

RUN pip install -r requirements.txt && python3 database.py

ENTRYPOINT [ "bash", "-c", "python3 app.py" ]