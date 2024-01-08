FROM python:3.11

WORKDIR /transfer

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.prod.txt requirements.txt
COPY docker/launch.sh launch.sh
COPY docker/wait-for-it.sh wait-for-it.sh

RUN  pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir
    
COPY . .

ENTRYPOINT ["/transfer/launch.sh"]
