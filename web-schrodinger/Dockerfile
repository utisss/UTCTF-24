FROM ubuntu:latest

# install dependencies
RUN apt update
RUN apt install -y unzip python3 python3-pip openssh-server
RUN pip3 install --upgrade pip
RUN pip3 install flask Flask-WTF

# make new user
RUN useradd -m copenhagen

# setup files for website
WORKDIR /app
COPY . /app
RUN rm /app/Dockerfile
RUN chown -R copenhagen /app
RUN chgrp -R copenhagen /app
RUN chmod +x ./src/main.py

# expose website port
EXPOSE 9000

# setup user and flag
USER copenhagen
RUN echo "utflag{No_Observable_Cats_Were_Harmed}" > /home/copenhagen/flag.txt

CMD ["python3", "src/main.py"]
