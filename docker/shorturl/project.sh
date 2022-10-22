cd /root
git clone https://github.com/yszou/shorturl.git

cd /root/shorturl/app
rm -f config.conf
ln -s ../conf/config-docker.conf ./config.conf
ln -s ../conf/nginx-docker.conf ./nginx.conf
ln -s ../conf/supervisord-docker.conf ./supervisord.conf

cd /root/shorturl/
pip3 install -r requirements.txt

cd /home/app
cp -r /root/shorturl /home/app/shorturl
chown -R app:app /home/app/shorturl
cd /home/app/shorturl/bin
chmod +x shorturl_docker.sh



