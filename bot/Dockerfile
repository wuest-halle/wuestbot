FROM python:3

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8443

CMD exec gunicorn wuestbot:app -b 0.0.0.0:8443 -w 1 --access-logfile -