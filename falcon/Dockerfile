FROM python:3.5

RUN apt-get update && \
    apt-get install -y supervisor

ADD supervisor.conf /etc/supervisor/supervisord.conf

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /code/

EXPOSE 80
CMD ["supervisord", "-n"]
