FROM python:3.7-alpine
MAINTAINER BJ Dierkes <derks@datafolklabs.com>
ENV PS1="\[\e[0;33m\]|> cement-py37 <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY requirements-dev.txt /src/
RUN apk update \
    && apk add libmemcached-dev \
        gcc \
        musl-dev \
        cyrus-sasl-dev \
        zlib-dev \
        make \
        vim \
        bash \
        git \
        libffi \
        libffi-dev \
    && ln -sf /usr/bin/vim /usr/bin/vi \
    && pip install --no-cache-dir -r requirements-dev.txt
COPY . /src
COPY docker/vimrc /root/.vimrc
RUN python setup.py develop
CMD ["/bin/bash"]
