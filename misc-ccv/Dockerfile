FROM ubuntu:20.04

RUN apt-get update
RUN apt-get update && apt-get install -y python3 python3-pip socat
RUN pip install numpy pycryptodome

COPY . /usr/src/app
RUN chmod +x /usr/src/app/server.py
RUN chmod +x /usr/src/app/app.py

COPY start.sh /start.sh
RUN chmod 755 /start.sh

WORKDIR /usr/src/app

EXPOSE 9000

CMD ["/start.sh"]