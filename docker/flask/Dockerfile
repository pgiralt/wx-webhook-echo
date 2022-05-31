FROM alpine

RUN apk update \
    && apk add --no-cache python3 build-base libstdc++ python3-dbg python3-dev git bash \
    && apk add zlib-dev jpeg-dev freetype-dev py3-gunicorn gcc libxslt-dev libxml2-dev libffi-dev openssl-dev supervisor \
    && python3 -m ensurepip

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

