# Getting smarter with PostgreSQL

Originally I intended this project to be a means to document a schema using Markdown. I'd like to expand the scope to also include recording some [best practices](http://c2.com/cgi/wiki?DatabaseBestPractices) for schema design and general database usage, some thoughts on incrementally improving an entrenched bad schema design, and some ideas on how one might unit-test a database design (including table layout, queries, views, functions, and triggers). My quick guess is that fixing a bad design incrementally is probably a matter of identifying a collection of mutually orthogonal bugs, for which patches to the schema and the application code can be created, along with data migration scripts, and tested thoroughly before they are moved to production. (Here are [more thoughts](http://c2.com/cgi/wiki?ContinuousDatabaseRefactoring) on schema changes, which I have glanced at but not studied yet.)

I have some thoughts on unit testing, based on the needs of my current job. We are building an automated test framework using [pytest](http://pytest.org/latest/) and we usually talk to our DB using [SQLAlchemy](http://www.sqlalchemy.org/). I observe that Docker has a [PostgreSQL image](https://registry.hub.docker.com/_/postgres/) available, and like all Docker images, you can probably instantiate it very fast. My thought is that the unit test setup function should bring up a Docker Postgres instance and populate it with the intended schema. The teardown function should kill the instance, so that each test is running with a fresh empty database. Each test is responsible for populating the DB with any data required, and then it runs whatever functions or selects or whatnot and confirms the answer is correct. The setup and teardown functions and the tests will be written in Python using SQLAlchemy.

## Testing SQL

Here are some relevant links that I need to spend more time with, picking out what's good and what's meh.

* [Best way to test SQL queries - Stack Overflow](http://stackoverflow.com/questions/754527/best-way-to-test-sql-queries)
* [How to do database unit testing? - StackOverflow](http://stackoverflow.com/questions/3772093/how-to-do-database-unit-testing)
* [Close Those Loopholes: Lessons learned from Unit Testing T-SQL](https://www.simple-talk.com/sql/database-administration/close-those-loopholes-lessons-learned-from-unit-testing-t-sql/)
* [Unit testing of stored procedures - Database Administrators Stack Exchange](http://dba.stackexchange.com/questions/21065/unit-testing-of-stored-procedures)
* [How to unit test databases](http://blog.pluralsight.com/how-to-unit-test-databases)
* [What are the best practices for testing long SQL queries? - Quora](http://www.quora.com/What-are-the-best-practices-for-testing-long-SQL-queries)

### Avoid IP address space conflict with AWS

If there is no danger of IP address space collision with AWS instances, skip this section.

Docker wants to use a 172.17.x.x address space, and this bumps into the 172.16.x.x address space used by AWS. So we need to fiddle around with the Docker daemon to make things work.

Find the docker daemon process on your machine and kill it. Now do this as root.
```bash
ip link set docker0 down
apt-get install bridge-utils
brctl delbr docker0
```
Finally, restart the daemon with an IP address space that won't bother AWS.
```bash
docker -d --bip 192.168.0.1/16
```
This allows you to painlessly talk to AWS servers while Docker is running.

### Docker client stuff to run the test

First make sure you've installed [docker-py](https://docker-py.readthedocs.org/en/latest/) and pulled the Docker Postgres image. More info about the Postgres image [here](https://docs.docker.com/examples/postgresql_service/).
```bash
docker pull postgres
sudo pip install docker-py
```

An example unit test appears in `test_this.py`. When you finish running your unit tests, you can blow away all Docker containers with this command.
```bash
docker rm -f $(docker ps -a | tail --lines=+2 | cut -c -8)
```
NOTE, this will also blow away any Docker containers *not* involved in your testing. Use caution.

## Documenting schemas

> Show me your flowchart and conceal your tables, and I shall continue to be mystified.
> Show me your tables, and I won't usually need your flowchart; it'll be obvious.
> -- Fred Brooks, The Mythical Man-Month

This is hopefully going to be a useful way to add commentary to a PostgreSQL schema. The commentary will be in standard Markdown as it is understood by [Python's Markdown module](https://pythonhosted.org/Markdown/index.html) and [Google's Github-Flavored Markdown extension](https://github.com/google/py-gfm). The [official Markdown reference](http://daringfireball.net/projects/markdown/syntax) is helpful, and [GFM extends that syntax](https://help.github.com/articles/github-flavored-markdown/) in handy ways. The schema and commentary are pre-processed to produce a Markdown file which can then be processed into HTML and then into a [PDF](http://weasyprint.org/).

As I look at it, there isn't a lot here that is terribly PostgreSQL-specific. It should be possible to pretty easily adapt it to MySQL, Oracle, or other RDBMSes.

### Identifying SQL objects in the schema

Using the schema in `schema.sql` as an example, here is how SQL objects are referenced.

#### Tables

    ## command_set

Because it matches the name of a table in the schema and is a "##" level heading, this is recognized as a reference to that table. What would follow would be the Markdown telling what this table is all about and how it's used in the system. You can reference this elsewhere in your commentary by writing

    Now I will talk about the [command_set table](#command_set).

#### Columns

    ### command_set:command_set_type

This is a reference to a column, the `command_set_type` column in the `command_set` table.Likewise, the following Markdown text would describe it in whatever way is helpful.

#### Functions

There aren't any functions in this schema, but if there were, they would be indentified
like this.

    ## hello_world_function

Anything before the first marker is presumed to be a preamble.

Tables, columns and functions become headers in the generated Markdown, in the order in
which they appear in the schema.

Tables and functions will become sections and columns will become subsections.

### Adding additional sections and subsections

This can be done in the conventional way using "##" and "###" at the beginning of the line. As long as these don't match objects found in the schema, they will be treated as additional sections, and will be placed after all the database stuff.

### Basic workflow

```bash
pip install markdown
git clone git@github.com:google/py-gfm.git
(cd py-gfm; sudo python setup.py install)

pg_dump <params> <dbname> > schema.sql
python this_script.py schema.sql commentary.md > schema_doc.md
python -m markdown -x gfm schema_doc.md > README.html
```

### Named anchors

These aren't part of this project, they are a standard feature of Markdown, but so useful that they're worthy of mention here.

```
* [Chapter 1](#chapter-1)
* [Chapter 2](#chapter-2)
* [Chapter 3](#chapter-3)
```

will jump to these sections:

```
## Chapter 1 <a id="chapter-1"></a>
Content for chapter one.

## Chapter 2 <a id="chapter-2"></a>
Content for chapter two.

## Chapter 3 <a id="chapter-3"></a>
Content for chapter three.
```

### Table of contents? Index?

It might be good to automatically generate these things. I'll think about that.
