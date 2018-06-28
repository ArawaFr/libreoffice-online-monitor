FROM python:3

WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

ADD *.py /usr/src/app/

EXPOSE 8765/tcp

CMD [ "python", "./main.py" ]
