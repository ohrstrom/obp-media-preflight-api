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
    && pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c 'pip install --no-cache-dir -r /requirements.txt' \
    && apk del .build-deps

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /app/
WORKDIR /app/
ADD . /app/

COPY docker-entrypoint.sh /app/


# wsgi port
EXPOSE 8000

# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=app.settings

# entrypoint (contains migration/static handling)
# ENTRYPOINT ['/app/docker-entrypoint.sh']

CMD ['gunicorn', 'app.wsgi', '--bind 0.0.0.0:$PORT']
