from parsons import Postgres
from parsons.etl.table import Table
from test.utils import assert_matching_tables
import unittest
import os
import re
import warnings
import datetime
from test.utils import validate_list

# The name of the schema and will be temporarily created for the tests
TEMP_SCHEMA = 'parsons_test'

# These tests do not interact with the Postgres Database directly, and don't need real credentials


class TestPostgres(unittest.TestCase):

    def setUp(self):

        self.pg = Postgres(username='test', password='test', host='test', db='test', port=123)

        self.tbl = Table([['ID', 'Name'],
                          [1, 'Jim'],
                          [2, 'John'],
                          [3, 'Sarah']])

        self.mapping = self.pg.generate_data_types(self.tbl)

    def test_data_type(self):

        # Test smallint
        self.assertEqual(self.pg.data_type(1, ''), 'smallint')
        # Test int
        self.assertEqual(self.pg.data_type(32769, ''), 'int')
        # Test bigint
        self.assertEqual(self.pg.data_type(2147483648, ''), 'bigint')
        # Test varchar that looks like an int
        self.assertEqual(self.pg.data_type('00001', ''), 'varchar')
        # Test a float as a decimal
        self.assertEqual(self.pg.data_type(5.001, ''), 'decimal')
        # Test varchar
        self.assertEqual(self.pg.data_type('word', ''), 'varchar')
        # Test int with underscore
        self.assertEqual(self.pg.data_type('1_2', ''), 'varchar')
        # Test int with leading zero
        self.assertEqual(self.pg.data_type('01', ''), 'varchar')

    def test_generate_data_types(self):

        # Test correct header labels
        self.assertEqual(self.mapping['headers'], ['ID', 'Name'])
        # Test correct data types
        self.assertEqual(self.mapping['type_list'], ['smallint', 'varchar'])
        # Test correct lengths
        self.assertEqual(self.mapping['longest'], [1, 5])

    def test_vc_padding(self):

        # Test padding calculated correctly
        self.assertEqual(self.pg.vc_padding(self.mapping, .2), [1, 6])

    def test_vc_max(self):

        # Test max sets it to the max
        self.assertEqual(self.pg.vc_max(self.mapping, ['Name']), [1, 65535])

        # Test raises when can't find column
        # To Do

    def test_vc_validate(self):

        # Test that a column with a width of 0 is set to 1
        self.mapping['longest'][0] = 0
        self.mapping = self.pg.vc_validate(self.mapping)
        self.assertEqual(self.mapping, [1, 5])

    def test_create_sql(self):

        # Test the the statement is expected
        sql = self.pg.create_sql('tmc.test', self.mapping, distkey='ID')
        exp_sql = "create table tmc.test (\n  id smallint,\n  name varchar(5)) \ndistkey(ID) ;"
        self.assertEqual(sql, exp_sql)

    def test_column_validate(self):

        bad_cols = ['', 'SELECT', 'asdfjkasjdfklasjdfklajskdfljaskldfjaklsdfjlaksdfjklasjdfklasjdkfljaskldfljkasjdkfasjlkdfjklasdfjklakjsfasjkdfljaslkdfjklasdfjklasjkldfakljsdfjalsdkfjklasjdfklasjdfklasdkljf'] # noqa: E501
        fixed_cols = ['col_0', 'col_1', 'asdfjkasjdfklasjdfklajskdfljaskldfjaklsdfjlaksdfjklasjdfklasjdkfljaskldfljkasjdkfasjlkdfjklasdfjklakjsfasjkdfljaslkdfjkl'] # noqa: E501
        self.assertEqual(self.pg.column_name_validate(bad_cols), fixed_cols)

    def test_create_statement(self):

        # Assert that copy statement is expected
        sql = self.pg.create_statement(self.tbl, 'tmc.test', distkey='ID')
        exp_sql = """create table tmc.test (\n  "id" smallint,\n  "name" varchar(5)) \ndistkey(ID) ;"""  # noqa: E501
        self.assertEqual(sql, exp_sql)

        # Assert that an error is raised by an empty table
        empty_table = Table([['Col_1', 'Col_2']])
        self.assertRaises(ValueError, self.pg.create_statement, empty_table, 'tmc.test')

# These tests interact directly with the Postgres database

@unittest.skipIf(not os.environ.get('LIVE_TEST'), 'Skipping because not running live test')
class TestPostgresDB(unittest.TestCase):

    def setUp(self):

        self.temp_schema = TEMP_SCHEMA

        self.pg = Postgres()

        self.tbl = Table([['ID', 'Name'],
                          [1, 'Jim'],
                          [2, 'John'],
                          [3, 'Sarah']])

        # Create a schema, create a table, create a view
        setup_sql = f"""
                    drop schema if exists {self.temp_schema} cascade;
                    create schema {self.temp_schema};
                    """

        other_sql = f"""
                    create table {self.temp_schema}.test (id smallint,name varchar(5));
                    create view {self.temp_schema}.test_view as (select * from {self.temp_schema}.test);
                    """ # noqa: E501

        self.pg.query(setup_sql)

        self.pg.query(other_sql)

    def tearDown(self):

        # Drop the view, the table and the schema
        teardown_sql = f"""
                       drop schema if exists {self.temp_schema} cascade;
                       """
        self.pg.query(teardown_sql)

    def test_query(self):

        # Check that query sending back expected result
        r = self.pg.query('select 1')
        self.assertEqual(r[0]['?column?'], 1)

    def test_query_with_parameters(self):
        table_name = f"{self.temp_schema}.test"
        self.pg.copy(self.tbl, f"{self.temp_schema}.test", if_exists='append')

        sql = f"select * from {table_name} where name = %s"
        name = 'Sarah'
        r = self.pg.query(sql, parameters=[name])
        self.assertEqual(r[0]['name'], name)

        sql = f"select * from {table_name} where name in (%s, %s)"
        names = ['Sarah', 'John']
        r = self.pg.query(sql, parameters=names)
        self.assertEqual(r.num_rows, 2)

    def test_copy(self):

        # Copy a table
        self.pg.copy(self.tbl, f'{self.temp_schema}.test_copy', if_exists='drop')

        # Test that file exists
        r = self.pg.query(f"select * from {self.temp_schema}.test_copy where name='Jim'")
        self.assertEqual(r[0]['id'], 1)

        # Copy to the same table, to verify that the "truncate" flag works.
        self.pg.copy(self.tbl, f'{self.temp_schema}.test_copy', if_exists='truncate')
        rows = self.pg.query(f"select count(*) from {self.temp_schema}.test_copy")
        self.assertEqual(rows[0]['count'], 3)

        # Copy to the same table, to verify that the "drop" flag works.
        self.pg.copy(self.tbl, f'{self.temp_schema}.test_copy', if_exists='drop')

if __name__ == "__main__":
    unittest.main()
