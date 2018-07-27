FROM python:3.6-alpine
MAINTAINER {{ creator }} <{{ creator_email }}>
WORKDIR /app
COPY . /app
RUN apk update \
    && apk add git \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -f /usr/local/lib/python3.6/site-packages/cement.egg-link \
    && cd src/cement \
    && python setup.py install \
    && cd /app \
    && python setup.py install \
    && rm -rf /app
WORKDIR /
ENTRYPOINT ["{{ label }}"]
