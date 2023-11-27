ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
   build-essential \
   libpq-dev

COPY ./pyproject.toml ./

RUN pip install poetry && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt && \
    pip uninstall -y poetry

RUN pip wheel --wheel-dir /usr/src/app/wheels \
   -r requirements.txt

FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/apps
ENV PYTHONPATH /apps

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/

# Inicialização do serviço de comunicação com o chat.
COPY ./.docker/services/chat_api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./backend/services/chat_api ${APP_HOME}

ENTRYPOINT ["/start"]
