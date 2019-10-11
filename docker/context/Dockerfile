FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y openssh-server  && \
    mkdir /var/run/sshd  && \
    echo 'root:root' |chpasswd
    #sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    #sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN apt-get install -y unzip
RUN add-apt-repository ppa:jonathonf/firefox-esr
RUN apt update
RUN apt-get install -y vim firefox-esr


COPY sshd_config /etc/ssh/sshd_config
RUN mkdir /app
COPY dockerdist/*.* /app/
RUN mkdir /app/lib
COPY dockerdist/lib /app/lib

RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN  apt-get -y autoclean && apt-get -y autoremove && \
     apt-get -y purge $(dpkg --get-selections | grep deinstall | sed s/deinstall//g) && \
     rm -rf /var/lib/apt/lists/*

RUN chmod 755 ./app/entrypoint.sh

ENTRYPOINT ["./app/entrypoint.sh"]

EXPOSE 2223
