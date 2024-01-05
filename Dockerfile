FROM python:3.11

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.prod.txt requirements.txt
COPY movies_admin/uwsgi/uwsgi.ini uwsgi.ini
COPY movies_admin/docker/scripts/migrations.sh migrations.sh
COPY movies_admin/docker/scripts/index_creation.sh index_creation.sh
COPY movies_admin/docker/scripts/wait-for-it.sh wait-for-it.sh
COPY movies_admin/docker/scripts/launch.sh launch.sh

RUN  apt-get update \
     && apt-get -y install netcat-traditional \
     && mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY movies_admin .
COPY etl etl

EXPOSE 8000

ENTRYPOINT ["/opt/app/launch.sh"]
