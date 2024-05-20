FROM python:3.11-alpine
LABEL MAINTAINER="BJ Dierkes <derks@datafolklabs.com>"
ENV PS1="\[\e[0;33m\]|> cement <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
WORKDIR /src
COPY . /src
ENV PDM_BUILD_SCM_VERSION=0.0.0.dev
# RUN pip install . \
#     && rm -rf /src
RUN pip install .
WORKDIR /
ENTRYPOINT ["/usr/local/bin/cement"]
