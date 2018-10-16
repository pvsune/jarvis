FROM python:3.7-slim

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY . /jarvis
WORKDIR /jarvis

EXPOSE 8000
CMD gunicorn jarvis:app -b 0.0.0.0:8000
