
# Development Envrionment

- install Postgresql and create a DB by yourself.
- copy or link `conf/config-dev.conf` to `app/config.conf`.
- modify the `app/config.conf` according to your environment.
    - [general]/root, is the dir location of the project in your machine.
    - [database], fill the Postgresql information.
    - [log:filelog]/dir , the dir of where you want to the logs save to.

then install the requirements:

`pip3 install -r requirements.txt`

init the DB by running sqls in the `sql` dir in order.

Lastly, run the server:

`python server.py`


# Run tests

create a user (test:test) with `bin/create_super.py`, execute it and input `test` username and `test` password.

when the server is running on localhost:8888, chdir to test, then:

`python all_run.py`


# Codes Structure

- [bin] tools for project management.
- [test] test cases.
- [app] main logic.
- [conf] configurations for different envrionments.


the `app` tree:

- `server.py`: start point
- `config.py`: parse config and init the DB connection
- `url.py`: mapping path to Handlers
- [handler]: main logic by handlers
- [model]: data models
- [sql]: ordered sqls
- [static]: static resources from frontend
- [template]: page templates, only one now
- [lib]: standalone libraries 
- [timer]: special mechanism supplied by Tornado, for example dump logs per 10 secs



