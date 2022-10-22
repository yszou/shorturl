apt-get update -y 
apt-get upgrade -y
apt-get install -y \
    language-pack-en-base \
    man \
    sudo \
    gcc \
    g++ \
    systemd \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libgif-dev \
    libfreetype6-dev \
    libtiff-dev \
    libwebp-dev \
    libxml2-dev \
    libxslt1-dev \
    libsqlite3-dev \
    libmysqlclient-dev \
    libpq-dev \
    libyaml-dev \
    libffi-dev \
    libreadline6-dev \
    libpython3-dev \
    python3-dev \
    python3-pip \
    vim \
    git \
    curl \
    wget \
    sqlite3 \
    postgresql-client \
    mysql-client \
    axel \
    ctags \
    zsh \
    locate \
    telnet \
    dnsutils \
    libmemcached-dev \
    libpcre3-dev \
    unzip \
    cmake \
    libncurses5-dev \
    dpkg-dev \
    net-tools


pip3 install supervisor


cd /root
wget https://nginx.org/download/nginx-1.22.1.tar.gz
tar xzf nginx-1.22.1.tar.gz
cd nginx-1.22.1
./configure --prefix=/opt/nginx
make
make install

useradd -m app
mkdir /var/log/shorturl
chown -R app:app /var/log/shorturl
chown -R app:app /opt/nginx

