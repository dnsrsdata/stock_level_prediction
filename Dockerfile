FROM python:3.9.13-buster

WORKDIR /projeto_estoque

COPY requirements.txt /projeto_estoque/

RUN pip install -r requirements.txt

COPY . /projeto_estoque/





