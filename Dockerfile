FROM python:3.6.8-alpine3.9

LABEL maintainer="roy luo <royluoliang@163.com>"

ENV CA_EXPORTER_VERSION 1.0

COPY pip.conf /etc/pip.conf
COPY ca_exporter /usr/local/bin/

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update \
    && apk add gcc linux-headers libffi-dev libc-dev libressl-dev \
    && pip install pyopenssl prometheus_client \
    && rm -rf /var/cache/apk/* /root/.cache /tmp/*

CMD ["ca_exporter"]
