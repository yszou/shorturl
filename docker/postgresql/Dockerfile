FROM postgres:latest
MAINTAINER YS.Zou <yeshengzou@gmail.com>
 
RUN mkdir -p /docker-entrypoint-initdb.d

RUN apt-get update -y
RUN apt-get install -y git
RUN cd /root && git clone https://github.com/yszou/shorturl.git

RUN cp /root/shorturl/app/sql/000.sql /docker-entrypoint-initdb.d
RUN cp /root/shorturl/app/sql/001.sql /docker-entrypoint-initdb.d

