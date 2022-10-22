FROM ubuntu:20.04
MAINTAINER YS.Zou <yeshengzou@gmail.com>
 
ADD install.sh /root/install.sh
RUN bash /root/install.sh

CMD ["/home/app/shorturl/bin/shorturl_docker.sh", "start"]


