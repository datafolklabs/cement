FROM python:3.6-alpine
MAINTAINER BJ Dierkes <derks@datafolklabs.com>
ENV PS1="\[\e[0;33m\]|> cement <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
WORKDIR /src
COPY . /src
RUN python setup.py install \
    && rm -rf /src
WORKDIR /
ENTRYPOINT ["/usr/local/bin/cement"]
