FROM python:3.9.13-alpine3.14


ENV USER_ID=1000
ENV GROUP_ID=1000
ENV USER_NAME=api

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN addgroup \
    --gid ${GROUP_ID} \
    --system ${USER_NAME} && \
    adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup ${USER_NAME} \
    --no-create-home \
    --uid ${USER_ID} \
    ${USER_NAME}

RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    postgresql-client \
    g++ \
    python3-dev \
    musl-dev \
    build-base \
    linux-headers \
    pcre-dev \
    libpq \
    libffi-dev \
    openssl-dev \
    cargo

COPY --chown=${USER_ID}:${GROUP_ID} ./surl/requirements/local.lock.txt /requirements/

RUN pip install -U pip && \
    pip install -r /requirements/local.lock.txt
# pip install sqlalchemy==2.0.15


COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/api/entrypoint /entrypoint
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/api/start /start
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/api/start-test /start-test

RUN chmod +x /entrypoint && \
    chmod +x /start && \
    chmod +x /start-test

WORKDIR /surl/
USER ${USER_NAME}

ENTRYPOINT [ "/entrypoint" ]
