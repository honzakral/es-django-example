Stack
=====

Example application in Django using Elasticsearch DSL for search.

It uses data from StackExchange dumps
(https://archive.org/details/stackexchange) - download the torrend and just
point the ``load_dump`` command to an unpacked data directory for a stack
exchange server.

To install::

    # install requirements
    pip install -r requirements.txt

    # create dabatase
    python manage.py migrate

    # load SE dump into the DB
    python manage.py load_dump DIR

Sample data can be downloaded from https://www.dropbox.com/s/eeocipgw6y6pk89/coffee.zip?dl=0
