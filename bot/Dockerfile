FROM python:3

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python wuestbot.py