ARG TAG="master"
FROM python:3.7

ENV FLASK_APP=art_to_ftp.py
ENV APP_PORT=${APP_PORT:-5700}

RUN python3 -m pip install flask gunicorn oc-cdtapi

WORKDIR /app
COPY . /app

#HEALTHCHECK --interval=300s --timeout=3s CMD ./healthcheck.sh ${APP_PORT} || exit 1

CMD gunicorn -b 0.0.0.0:${APP_PORT} wsgi:app
