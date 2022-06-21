FROM python:3.9.5-slim-buster
ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1
COPY ./app /opt/app
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /opt/app
CMD ["python", "-m", "api_v1"]
