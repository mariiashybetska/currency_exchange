FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /currency_exchange
WORKDIR /currency_exchange
COPY requirements.txt /currency_exchange
RUN pip install -r requirements.txt
COPY . /currency_exchange