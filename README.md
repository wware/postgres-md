# Documenting PostgreSQL schemas in Markdown

> Show me your flowchart and conceal your tables, and I shall continue to be mystified.
> Show me your tables, and I won't usually need your flowchart; it'll be obvious.
> -- Fred Brooks, The Mythical Man-Month

This is hopefully going to be a useful way to add commentary to a PostgreSQL schema. The commentary will be in standard Markdown as it is understood by [Python's Markdown module](https://pythonhosted.org/Markdown/index.html) and [Google's Github-Flavored Markdown extension](https://github.com/google/py-gfm). The [official Markdown reference](http://daringfireball.net/projects/markdown/syntax) is helpful, and [GFM extends that syntax](https://help.github.com/articles/github-flavored-markdown/) in handy ways. The schema and commentary are pre-processed to produce a Markdown file which can then be processed into HTML and then into a [PDF](http://weasyprint.org/).

As I look at it, there isn't a lot here that is terribly PostgreSQL-specific. It should be possible to pretty easily adapt it to MySQL, Oracle, or other RDBMSes.

## Identifying SQL objects in the schema

Using the schema in `schema.sql` as an example, here is how SQL objects are referenced.

### Tables

    ## command_set

Because it matches the name of a table in the schema and is a "##" level heading, this is recognized as a reference to that table. What would follow would be the Markdown telling what this table is all about and how it's used in the system. You can reference this elsewhere in your commentary by writing

    Now I will talk about the [command_set table](#command_set).

### Columns

    ### command_set:command_set_type

This is a reference to a column, the `command_set_type` column in the `command_set` table.Likewise, the following Markdown text would describe it in whatever way is helpful.

### Functions

There aren't any functions in this schema, but if there were, they would be indentified
like this.

    ## hello_world_function

Anything before the first marker is presumed to be a preamble.

Tables, columns and functions become headers in the generated Markdown, in the order in
which they appear in the schema.

Tables and functions will become sections and columns will become subsections.

## Adding additional sections and subsections

This can be done in the conventional way using "##" and "###" at the beginning of the line. As long as these don't match objects found in the schema, they will be treated as additional sections, and will be placed after all the database stuff.

## Basic workflow

```bash
pip install markdown
git clone git@github.com:google/py-gfm.git
(cd py-gfm; sudo python setup.py install)

pg_dump <params> <dbname> > schema.sql
python this_script.py schema.sql commentary.md > schema_doc.md
python -m markdown -x gfm schema_doc.md > README.html
```

## Named anchors

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

## Table of contents? Index?

It might be good to automatically generate these things. I'll think about that.