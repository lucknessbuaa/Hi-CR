host:=0.0.0.0
port:=9003
activate_venv=source venv/bin/activate

debug:
	$(activate_venv) && ./manage.py runserver $(host):$(port)

start-uwsgi:
	$(activate_venv) \
	&& uwsgi --socket 127.0.0.1:$(port) \
          --chdir $(shell pwd) \
          --wsgi-file baidu/wsgi.py \
          --master \
          --process 4 \
          --daemonize $(shell pwd)/logs/uwsgi.log \
          --pidfile $(shell pwd)/uwsgi.pid  

stop-uwsgi:
	$(activate_venv) && uwsgi --stop uwsgi.pid

reload-uwsgi: 
	$(activate_venv) && uwsgi --reload uwsgi.pid

collectstatic:
	$(activate_venv) \
	&& ./manage.py collectstatic --noinput

database:=HiCR
password:=
db:
	-mysql -u root --password=$(password) -e \
		"drop database $(database)"
	mysql -u root --password=$(password) -e \
		"create database $(database)"
	$(activate_venv) && ./manage.py syncdb --noinput && ./manage.py load_universities


deps:
	$(activate_venv) && \
	pip install -r requirements.txt && \
	npm install && \
	bower install


.PHONY: debug \
	db \
	deps \
	collectstatic \
	reload-uwsgi \
	start-uwsgi \
	stop-uwsgi
