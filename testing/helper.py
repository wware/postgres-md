from docker import Client
import os
import pytest
import time
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy_utils.functions import (
    database_exists,
    create_database,
    drop_database
)

cli = Client(base_url='unix://var/run/docker.sock')
container = cli.create_container(image='postgres')
cli.start(container=container)
ip_addr = ip_addr = cli.inspect_container(
    container
)['NetworkSettings']['IPAddress']
url = 'postgresql://postgres:@{0}:5432/test'.format(ip_addr)

# It takes several seconds for Postgres to warm up.
while True:
    if "5432/tcp open" in os.popen("nmap -p 5432 " + ip_addr).read():
        break
    time.sleep(1)


_schema = None


def set_schema(fname):
    global _schema
    _schema = fname


def get_table(tname, columns=None):
    "import table info from the database"
    db = create_engine(url)
    metadata = MetaData(db)
    table = Table(tname, metadata, autoload=True, autoload_with=db)
    if columns is not None:
        assert [c.name for c in table.columns] == columns
    return table


@pytest.fixture
def engine(request, url=url):
    assert _schema is not None, "Please call set_schema(filename) first"
    def fin():
        drop_database(url)
    request.addfinalizer(fin)
    create_database(url)
    cmd = "cat {0} | psql -h {1} -U postgres test".format(_schema, ip_addr)
    os.system(cmd)
    return create_engine(url)
