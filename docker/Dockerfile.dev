FROM python:3.6-alpine
MAINTAINER BJ Dierkes <derks@datafolklabs.com>
WORKDIR /app
COPY requirements-dev.txt /app/
RUN apk update \
    && apk add libmemcached-dev \
        gcc \
        musl-dev \
        cyrus-sasl-dev \
        zlib-dev \
        make \
    && pip install --no-cache-dir -r requirements-dev.txt
COPY . /app
CMD ["/bin/ash"]
