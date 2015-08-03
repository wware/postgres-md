import time

from helper import engine, set_schema, get_table

set_schema("./example_schema.sql")


class TestExampleSchema:

    def test_example(self, engine):
        users = get_table('users', columns=['id', 'name', 'age', 'password'])
        start = time.time()
        i = users.insert()
        i.execute(name='Mary', age=30, password='secret')
        i.execute({'name': 'John', 'age': 42},
                  {'name': 'Susan', 'age': 57},
                  {'name': 'Carl', 'age': 33})

        s = users.select()    # SELECT * FROM users
        rs = s.execute()

        row = rs.fetchone()
        assert row.id == 1
        assert row['name'] == 'Mary'
        assert row.age == 30
        assert row[users.c.password] == 'secret'

        stuff = [(row.name, row.age) for row in rs]
        assert stuff == [('John', 42), ('Susan', 57), ('Carl', 33)]

        # row = db.engine.execute('select sum_of_ages()').fetchone()
        row = engine.execute('select sum_of_ages()').fetchone()
        assert row[0] == 162

        # make sure this stuff is performant
        test_time = time.time() - start
        assert test_time < 0.1, test_time

    def test_example_2(self, engine):
        """
        Confirm that we get a fresh database each time.
        No rows from the previous test should appear here.
        """
        users = get_table('users')
        i = users.insert()
        i.execute(name='Margo', age=29, password='broccoli')

        s = users.select()
        rs = s.execute()

        row = rs.fetchone()
        assert row.id == 1
        assert row['name'] == 'Margo'
        assert row.age == 29
        assert row[users.c.password] == 'broccoli'
        # no more after the first row
        assert rs.fetchall() == []
