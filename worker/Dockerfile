FROM python:3.5
# RUN apt-get update -qq && apt-get install -y build-essential python3-dev
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
