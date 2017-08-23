FROM python:3.6-alpine

ADD requirements.txt /requirements.txt

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        libffi-dev \
        linux-headers \
        git \
        postgresql-dev \
    && apk add --no-cache --virtual .run-deps \
        pcre-dev \
        postgresql-client \
        sox \
        ffmpeg \
        lame \
        flac \
    && python3.6 -m venv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r /requirements.txt" \
    && apk del .build-deps

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# uWSGI will listen on this port
EXPOSE 8000

# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=app.settings

# uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=app/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# entrypoint (contains migration/static handling)
ENTRYPOINT ["/code/docker-entrypoint.sh"]
# Start uWSGI
CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive"]
#CMD /venv/bin/uwsgi --http :$UWSGI_HTTP --module app.wsgi --virtualenv ~/srv/fprint-api
