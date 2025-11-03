FROM python:3.14-alpine
LABEL MAINTAINER="BJ Dierkes <derks@datafolklabs.com>"
ENV PS1="\[\e[0;33m\]|> cement <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
ENV PATH="${PATH}:/root/.local/bin"
WORKDIR /src
COPY . /src
COPY docker/vimrc /root/.vimrc
COPY docker/bashrc /root/.bashrc

RUN apk update \
    && apk add pipx vim \
    && ln -sf /usr/bin/vim /usr/bin/vi \
    && pipx install pdm
RUN pdm build
RUN pip install `ls dist/cement-*.tar.gz`[cli]

WORKDIR /
ENTRYPOINT ["/usr/local/bin/cement"]
