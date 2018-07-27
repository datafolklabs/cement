FROM python:3.6-alpine
MAINTAINER BJ Dierkes <derks@datafolklabs.com>
WORKDIR /app
COPY . /app
RUN python setup.py install \
    && rm -rf /app
WORKDIR /
ENTRYPOINT ["/usr/local/bin/cement"]
