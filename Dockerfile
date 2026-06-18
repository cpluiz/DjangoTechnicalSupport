FROM python:3.13.14-trixie

RUN groupadd -g 10001 apigroup && \
    useradd -u 10000 -g apigroup -m -s /bin/bash apiuser

ENV PYTHONBUFFERED 1

USER apiuser

WORKDIR /app

RUN chown apiuser:apigroup /app

COPY --chown=apiuser:apigroup requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=apiuser:apigroup . .

USER root

RUN chown -R apiuser:apigroup /app

USER apiuser

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"]