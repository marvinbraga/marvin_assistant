ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
   build-essential \
   libpq-dev \
   libgirepository1.0-dev \
   libcairo2-dev pkg-config python3-dev \
   python3-pyaudio portaudio19-dev \
   libportaudio2

COPY ./pyproject.toml ./

RUN apt-get update -y && apt-get upgrade -y

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
ENV LD_LIBRARY_PATH /usr/lib:/usr/local/lib:$LD_LIBRARY_PATH

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --upgrade pip \
   && pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/ \
   && pip install pyaudio

# Inicialização do frontend com o pygame.
COPY ./.docker/frontend/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./frontend ${APP_HOME}/frontend

ENTRYPOINT ["/start"]
