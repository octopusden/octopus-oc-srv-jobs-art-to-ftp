FROM python:3.7

RUN python3 -m pip install requests flask gunicorn coverage 

COPY . /local/art_to_ftp
WORKDIR /local/art_to_ftp

#RUN python3 -m coverage run -m unittest discover test && \
#    mkdir -p /build/reports && \
#    python3 -m coverage xml --include=./app/* -o /build/reports/art_to_ftp_coverage.xml

RUN python3 -m unittest discover

HEALTHCHECK --interval=1m --timeout=30s --start-period=15s --retries=3 \
    CMD curl -v --silent http://localhost:5700/ping 2>&1 | grep '< HTTP/1.1 200'

CMD /usr/local/bin/gunicorn wsgi:app --log-level=debug -b 0.0.0.0:5700

