# Dockerfile relative to docker-compose.yml

FROM postgres:14-alpine

RUN apk update && apk add git build-base make postgresql-pg_cron

RUN git clone https://github.com/citusdata/pg_cron.git
RUN cd pg_cron && make


# export PATH=/usr/pgsql-14/bin:$PATH
