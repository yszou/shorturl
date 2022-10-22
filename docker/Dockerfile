FROM ubuntu:20.04
MAINTAINER YS.Zou <yeshengzou@gmail.com>
 
ADD install.sh /root/install.sh

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y systemd

RUN bash /root/install.sh

# CMD ["/home/app/shorturl/bin/shorturl_docker.sh", "start"]
CMD ["/usr/local/bin/supervisord", "-c", "/home/app/shorturl/app/supervisord.conf"]

