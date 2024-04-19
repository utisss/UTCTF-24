FROM ubuntu:20.04

RUN apt-get update
RUN apt-get update && apt-get install -y build-essential socat libseccomp-dev

ARG FLAG
ARG USER
ENV USER $USER
ENV FLAG $FLAG

RUN useradd -m $USER

WORKDIR /
COPY start.sh /start.sh

RUN chmod 755 /start.sh && \
    echo "$FLAG" > /home/$USER/flag.txt && \
    chown root:root /home/$USER/flag.txt && \
    chmod 644 /home/$USER/flag.txt

EXPOSE 9000

WORKDIR /home/$USER
COPY src/. ./src/.
COPY Makefile .
RUN make
COPY server-data/ .

WORKDIR /
RUN rm -rf /build/src

CMD ["/start.sh"]
