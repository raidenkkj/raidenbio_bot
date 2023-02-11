FROM python:3.5-alpine
MAINTAINER RaidenIshigami <contact.raidenishigami69@gmail.com>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
RUN py.test -m 'A vida é dura mas meu pau é mais'

ENV APP_ID ''
ENV API_HASH ''
ENV BOT_TOKEN ''
ENV SCAN_DALAY_SEC 60
ENV STATSD_HOST ''
ENV STATSD_PORT 8125

CMD [ "python", "main.py" ]
