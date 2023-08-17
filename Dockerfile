FROM fedora:38

ENV APP_PORT=${APP_PORT:-5700}

RUN dnf --assumeyes makecache && \
    dnf --assumeyes install \
        python3 \
        python3-pip \
        python3-pysvn \
        ftp

RUN rm -rf /build
COPY --chown=root:root . /build
WORKDIR /build
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install $(pwd) && \
    python3 -m unittest discover -v && \
    python3 setup.py bdist_wheel

HEALTHCHECK --interval=300s --timeout=3s CMD ./healthcheck.sh ${APP_PORT} || exit 1

ENTRYPOINT "python3" "-m" "gunicorn" "-t" "600" "oc_art_to_ftp.wsgi:app" "-b" "0.0.0.0:${APP_PORT}"
