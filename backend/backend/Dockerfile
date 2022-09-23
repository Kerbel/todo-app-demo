FROM python:3.9.1

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

CMD python main.py
