FROM python:3.7-slim

COPY ./docker/local/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

WORKDIR /{{params['project_name']}}

COPY ./{{params['project_name']}}/requirements /{{params['project_name']}}/requirements

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r requirements/local_requirements.txt

COPY ./{{params['project_name']}} /{{params['project_name']}}

ENTRYPOINT ["/entrypoint.sh"]
