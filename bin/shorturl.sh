#!/bin/bash  
SV=/usr/bin/supervisord
SVC=/usr/bin/supervisorctl
LOG_DIR=/var/log/shorturl
SVPID=$LOG_DIR/supervisord.pid
DIR_NAME=/home/app/shorturl/app
SVCONF=$DIR_NAME/supervisord.conf

function usage(){
	echo "Usage: /bin/bash ${DIR_NAME}/shorturl start|stop|restart";
}

function start(){
    echo 'CONFIG IS' $SVCONF;
    echo 'STARTING...';
    if [ -f $SVPID ]; then
        stop;
    fi;
    $SV -c $SVCONF;
    echo 'OK';
}

function stop(){
    echo 'STOPING...';
    $SVC -c $SVCONF stop all;
    kill -s SIGTERM `cat $SVPID`;
    pkill chrome;
    echo 'OK';
}

function restart(){
    echo 'RESTARTING...'
    if [ -f $SVPID ]; then
        stop;
    fi;
    $SV -c $SVCONF;
    echo 'OK';
}

if test $# -eq 0; then
	usage;
	exit 0;
fi;

case $1 in 
	start)
		start;
		;;
	stop)
		stop;
		;;
	restart)
		restart;
		;;
	*)
		usage;
		;;
esac
