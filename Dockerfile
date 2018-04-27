FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py /usr/src/app/

EXPOSE 8765/tcp

CMD [ "python", "./main.py" ]
