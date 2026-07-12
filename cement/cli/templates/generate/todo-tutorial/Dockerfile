FROM python:3.10-alpine
LABEL MAINTAINER="Your Name <you@yourdomain.com>"
ENV PS1="\[\e[0;33m\]|> todo <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir .
WORKDIR /
ENTRYPOINT ["todo"]
