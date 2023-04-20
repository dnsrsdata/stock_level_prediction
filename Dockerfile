FROM python:3.9.13-buster

WORKDIR /projeto_estoque

RUN apt-get update

RUN apt-get install build-essential

COPY Makefile /projeto_estoque/

COPY requirements.txt /projeto_estoque/

RUN make setup

COPY . /projeto_estoque/

CMD [ "Make", "predictions"]



