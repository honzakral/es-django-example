Stack
=====

Example application in Django using Elasticsearch DSL for search.

It uses data from StackExchange dumps
(https://archive.org/details/stackexchange) - download the torrent and just
point the ``load_dump`` command to an unpacked data directory for a stack
exchange server.

To install::

    # install requirements
    pip install -r requirements.txt

    # create database
    python manage.py migrate

    # load SE dump into the DB
    python manage.py load_dump DIR

    # index all data into elasticsearch
    python manage.py index_data

To perform search just go to ``http://localhost:8000/search/?tags=flavor&tags=beans&q=bitterness``.


Docker workflow
---------------

To develop on this project make sure you Docker an Docker Compose installed. 

To get started just run::
	
	docker-compose up -d

wait till the elastic cluster is healthy::

	$ docker ps
	CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS                 PORTS                       NAMES
	d25832cf31db        e62bf4ebda11                "python manage.py ..."   About an hour ago   Up About an hour       0.0.0.0:80->80/tcp          esdjangoexample_web_1
	98a60d2d200c        fxdgear/elasticsearch:5.4   "/docker-entrypoin..."   2 hours ago         Up 2 hours (healthy)   9200/tcp, 9300/tcp          esdjangoexample_elasticsearch_1



Once healthy you can access the web container by running::

	docker exec --it esdjangoexample_web_1 ash


Then you can create the database by running::

	python manage.py migrate


Then you can load the SE dump into the data base::

	python manage.py load_dump DIR


Then you can index the data::

	python manage.py index_data


Now you can naviaget to http://localhost


Deploying with docker swarm
----------------------------

Build and push the image to the repository::

	docker-compose build
	docker-compose push


To deploy this with docker swarm. Make sure you have access to a swarm cluster and simply run::


	docker stack deploy --compose-file docker-compose.prod.yml es-django-example


