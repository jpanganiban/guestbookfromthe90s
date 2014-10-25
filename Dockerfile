FROM infoshift/python

RUN apt-get update && \
  apt-get install -y git-core

ADD requirements.txt /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt

WORKDIR /opt/app
