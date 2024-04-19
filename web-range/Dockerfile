FROM python:3-alpine

RUN adduser -D range

EXPOSE 3000

WORKDIR /var/www
COPY www /var/www
COPY server.py /server.py
COPY flag.txt /setup/flag.txt
RUN chown -R range /setup
USER range

CMD ["python3", "/server.py"]
