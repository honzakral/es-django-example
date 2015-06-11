Stack
=====

Example application in Django using Elasticsearch DSL for search.

It uses data from StackExchange dumps - download the xml filed for a SE site,
place it into DIR before installing.

To install::

    # install requirements
    pip install -r requirements.txt

    # create dabatase
    python manage.py migrate

    # load SE dump into the DB
    python manage.py load_dump DIR

    # index all data into elasticsearch
    python manage.py index_data

To perform search just go to ``http://localhost:8000/search/?tags=flavor&tags=beans&q=bitterness``.
