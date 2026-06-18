FROM python:3.13.14-trixie

ENV PYTHONBUFFERED 1

WORKDIR /app

RUN python3 -m venv /opt/apienv

ENV PATH="/opt/apienv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"]