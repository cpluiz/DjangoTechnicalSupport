FROM python:3.13.14-trixie

RUN groupadd -g 10001 apigroup && \
    useradd -u 10000 -g apigroup -m -s /bin/bash apiuser

ENV PYTHONBUFFERED 1

WORKDIR /app

RUN chown apiuser:apigroup /app

COPY requirements.txt .

USER apiuser

RUN pip install -r requirements.txt

USER root

COPY . /app

RUN chown -R apiuser:apigroup /app

USER apiuser

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"]