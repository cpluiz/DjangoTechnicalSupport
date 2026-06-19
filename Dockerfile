FROM python:3.13.14-trixie

RUN groupadd -g 10001 apigroup && \
    useradd -u 10000 -g apigroup -m -s /bin/bash apiuser

ENV PYTHONUNBUFFERED=1 
ENV PATH="/home/apiuser/.local/bin:${PATH}"

WORKDIR /app

RUN chown apiuser:apigroup /app

COPY requirements.txt .

USER apiuser

RUN pip install -r requirements.txt

USER root

COPY . .

RUN chmod +x ./django.sh

RUN chown -R apiuser:apigroup /app

USER apiuser

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"]