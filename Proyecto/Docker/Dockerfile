FROM ubuntu:22.04
COPY . /app
WORKDIR /app
RUN apt update
RUN apt install python3.10 -y
RUN apt install python3-pip -y
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD [ "python3.10", "app.py" ]
