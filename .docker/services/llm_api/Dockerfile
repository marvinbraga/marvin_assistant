ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
   build-essential \
   libpq-dev \
   libgirepository1.0-dev \
   libcairo2-dev pkg-config python3-dev \
   python3-pyaudio portaudio19-dev

RUN apt-get update -y && apt-get upgrade -y

COPY ./pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry && \
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

# Inicialização do serviço de comunicação com o llm.
COPY ./.docker/services/llm_api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./backend ${APP_HOME}/backend

ENTRYPOINT ["/start"]
