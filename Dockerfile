FROM python:3.6

WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

ADD setup.py README.md LICENSE /usr/src/app/
ADD loolmonitor /usr/src/app/loolmonitor/

RUN	python setup.py install

EXPOSE 8765/tcp

ADD logging.conf .
ADD entrypoint.sh /opt/
ENTRYPOINT ["/opt/entrypoint.sh"]