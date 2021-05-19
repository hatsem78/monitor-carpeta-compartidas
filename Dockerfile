FROM gitlab.ar.bsch:4567/santander-tecnologia/dockerbaseimages/python:v3.8

ENV HTTP_PROXY "http://proxy.ar.bsch:8080"
ENV HTTPS_PROXY "http://proxy.ar.bsch:8080"
ENV NO_PROXY "localhost,.ar.bsch"

USER root

RUN wget http://nexus.iaas.ar.bsch/repository/plataforma-digital-python/oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm

RUN yum -y install oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm

RUN yum -y install libaio

WORKDIR /home/app

COPY app /home/app

# COPY app/.env /home/app/.env

COPY requirements.txt /home/app/

RUN pip install --upgrade pip

RUN pip3 --default-timeout=2000 install -r requirements.txt

COPY app/ /home/app/

ENV PYTHONPATH="${PYTHONPATH}:/home/app:/home"

USER default

COPY app/ /home/app/

ENTRYPOINT ["python3", "/home/app/main.py"]
