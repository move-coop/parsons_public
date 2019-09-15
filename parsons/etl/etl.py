import petl
import logging

logger = logging.getLogger(__name__)


class ETL(object):

    def __init__(self):

        pass

    def add_column(self, column, value=None, index=None):
        """
        Add a column to your table

        `Args:`
            column: str
                Name of column to add
            value:
                A fixed or calculated value
            index: int
                The position of the new column in the table
        `Returns:`
            `Parsons Table` and also updates self
        """

        if column in self.columns:
            raise ValueError(f"Column {column} already exists")

        self.table = self.table.addfield(column, value, index)

        return self

    def remove_column(self, *columns):
        """
        Remove a column from your table

        `Args:`
            \*columns: str
                Column names
        `Returns:`
            `Parsons Table` and also updates self
        """ # noqa: W605

        self.table = petl.cutout(self.table, *columns)

        return self

    def rename_column(self, column_name, new_column_name):
        """
        Rename a column

        `Args:`
            column_name: str
                The current column name
            new_column_name: str
                The new column name
        `Returns:`
            `Parsons Table` and also updates self
        """

        if new_column_name in self.columns:
            raise ValueError(f"Column {new_column_name} already exists")

        self.table = petl.rename(self.table, column_name, new_column_name)

        return self

    def fill_column(self, column_name, fill_value):
        """
        Fill a column in a table

        `Args:`
            column_name: str
                The column to fill
            fill_value:
                A fixed or calculated value
        `Returns:`
            `Parsons Table` and also updates self
        """

        self.add_column(column_name + '_column_fill_temp', fill_value)
        self.remove_column(column_name)
        self.rename_column(column_name + '_column_fill_temp', column_name)

        return self

    def fillna_column(self, column_name, fill_value):
        """
        Fill None values in a column in a table

        `Args:`
            column_name: str
                The column to fill
            fill_value:
                Fixed value only
        `Returns:`
            `Parsons Table` and also updates self
        """

        self.fill_column(column_name, lambda x: x[column_name] if x[column_name] else fill_value)

        return self

    def move_column(self, column, index):
        """
        Move a column

        `Args:`
            column: str
                The column name to move
            index:
                The new index for the column
        `Returns:`
            `Parsons Table` and also updates existing object.
        """

        self.table = petl.movefield(self.table, column, index)

        return self

    def convert_column(self, *column, **kwargs):
        """
        Transform values under one or more fields via arbitrary functions, method
        invocations or dictionary translations. This leverages the petl ``convert()``
        method. Example usage can be found `here` <https://petl.readthedocs.io/en/v0.24/transform.html#petl.convert>`_

        `Args:`
            \*column: str
                A single column or multiple columns passed as a list
            \**kwargs: str, method or variable
                The update function, method, or variable to process the update
        `Returns:`
            `Parsons Table` and also updates self
        """ # noqa: E501,E261

        self.table = petl.convert(self.table, *column, **kwargs)

        return self

    def convert_columns_to_str(self):
        """
        Convenience function to convert all non-string or mixed columns in a
        Parsons table to string (e.g. for comparison)

        `Returns:`
            `Parsons Table` and also updates self
        """

        cols = self.get_columns_type_stats()

        for col in cols:
            if len(col['type']) > 1 or col['type'][0] != 'str':
                self.convert_column(col['name'], str)

        return self

    def coalesce_columns(self, dest_column, source_columns, remove_source_columns=True):
        """
        Coalesces values from one or more source columns into a destination column, by selecting
        the first non-empty value. If the destination column doesn't exist, it will be added.

        `Args:`
            dest_column: str
                Name of destination column
            source_columns: list
                List of source column names
            remove_source_columns: bool
                Whether to remove the source columns after the coalesce. If the destination
                column is also one of the source columns, it will not be removed.
        `Returns:`
            `Parsons Table` and also updates self
        """

        if dest_column in self.columns:
            def convert_fn(value, row):
                for source_col in source_columns:
                    if row.get(source_col):
                        return row[source_col]

            logger.debug(f"Coalescing {source_columns} into {dest_column}")
            self.convert_column(dest_column, convert_fn, pass_row=True)

        else:
            def add_fn(row):
                for source_col in source_columns:
                    if row.get(source_col):
                        return row[source_col]

            logger.debug(f"Creating new column {dest_column} from {source_columns}")
            self.add_column(dest_column, add_fn)

        if remove_source_columns:
            for source_col in source_columns:
                if source_col != dest_column:
                    self.remove_column(source_col)

        return self

    def get_column_types(self, column):
        """
        Return all of the Python types for values in a given column

        `Args:`
            column: str
                Name of the column to analyze
        `Returns:`
            list
                A list of Python types
        """

        return list(petl.typeset(self.table, column))

    def get_columns_type_stats(self):
        """
        Return descriptive stats for all columns

        `Returns:`
            list
                A list of dicts
        `Returns:`
            list
                A list of dicts, each containing a column 'name' and a 'type' list
        """

        return [{'name': col, 'type': self.get_column_types(col)}
                for col in self.table.columns()]

    def convert_table(self, *args):
        """
        Transform all cells in a table via arbitrary functions, method invocations or dictionary
        translations. This method is useful for cleaning fields and data hygiene functions such
        as regex. This method leverages the petl ``convert()`` method. Example usage can be
        found `here` <https://petl.readthedocs.io/en/v0.24/transform.html#petl.convert>`_.

        `Args:`
            \*args: str, method or variable
                The update function, method, or variable to process the update. Can also
        `Returns:`
            `Parsons Table` and also updates self
        """ # noqa: W605

        self.convert_column(self.columns, *args)

        return self

    def unpack_dict(self, column, keys=None, include_original=False,
                    sample_size=1000, missing=None, prepend=True,
                    prepend_value=None):
        """
        Unpack dictionary values from one column into separate columns

        `Args:`
            column: str
                The column name to unpack
            keys: list
                The dict keys in the column to unpack. If ``None`` will unpack
                all.
            include_original: boolean
                Retain original column after unpacking
            sample_size: int
                Number of rows to sample before determining columns
            missing: str
                If a value is missing, the value to fill it with
            prepend:
                Prepend the column name of the unpacked values. Useful for
                avoiding duplicate column names
            prepend_value:
                Value to prepend new columns if ``prepend=True``. If None, will
                set to column name.
        """

        if prepend:
            if prepend_value is None:
                prepend_value = column

            self.table = petl.convert(
                self.table,
                column,
                lambda v: self._prepend_dict(v, prepend_value))

        self.table = petl.unpackdict(
            self.table, column, keys=keys, includeoriginal=include_original,
            samplesize=sample_size, missing=missing)

        return self

    def unpack_list(self, column, include_original=False, missing=None, replace=False,
                    max_columns=None):
        """
        Unpack list values from one column into separate columns. Numbers the
        columns.

        .. code-block:: python

          # Begin with a list in column
          json = [{'id': '5421',
                   'name': 'Jane Green',
                   'phones': ['512-699-3334', '512-222-5478']
                  }
                 ]

          tbl = Table(json)
          print (tbl)
          >>> {'id': '5421', 'name': 'Jane Green', 'phones': ['512-699-3334', '512-222-5478']}

          tbl.unpack_list('phones', replace=True)
          print (tbl)
          >>> {'id': '5421', 'name': 'Jane Green', 'phones_0': '512-699-3334', 'phones_1': '512-222-5478'} # noqa: E501

        `Args:`
            column: str
                The column name to unpack
            include_original: boolean
                Retain original column after unpacking
            sample_size: int
                Number of rows to sample before determining columns
            missing: str
                If a value is missing, the value to fill it with
            replace: boolean
                Return new table or replace existing
            max_columns: int
                The maximum number of columns to unpack
        `Returns:`
            None
        """

        # Convert all column values to list to avoid unpack errors
        self.table = petl.convert(
            self.table, column, lambda v: [v] if not isinstance(v, list) else v
        )

        # Find the max number of values in list for all rows
        col_count = 0
        for row in self.cut(column):
            if len(row[column]) > col_count:
                col_count = len(row[column])

        # If max columns provided, set max columns
        if col_count > 0 and max_columns:
            col_count = max_columns

        # Create new column names "COL_01, COL_02"
        new_cols = []
        for i in range(col_count):
            new_cols.append(column + '_' + str(i))

        tbl = petl.unpack(self.table, column, new_cols,
                          include_original=include_original, missing=missing)

        if replace:
            self.table = tbl

        else:
            return tbl

    def unpack_nested_columns_as_rows(self, column, key='id', expand_original=False):
        """
        Unpack list or dict values from one column into separate rows.
        Not recommended for JSON columns (i.e. lists of dicts), but can handle columns
        with any mix of types. Makes use of PETL's `melt()` method.

        `Args:`
            column: str
                The column name to unpack
            key: str
                The column to use as a key when unpacking. Defaults to `id`
            expand_original: boolean or int
                If `True`: Add resulting unpacked rows (with all other columns) to original
                If `int`: Add to original unless the max added per key is above the given number
                If `False` (default): Return unpacked rows (with `key` column only) as standalone
                Removes packed list and dict rows from original either way.
        `Returns:`
            If `expand_original`, original table with packed rows replaced by unpacked rows
            Otherwise, standalone table with key column and unpacked values only
        """

        if isinstance(expand_original, int) and expand_original is not True:
            lengths = {len(row[column]) for row in self if isinstance(row[column], (dict, list))}
            max_len = sorted(lengths, reverse=True)[0]
            if max_len > expand_original:
                expand_original = False

        if expand_original:
            # Include all columns and filter out other non-dict types in table_list
            table = self
            table_list = table.select_rows(lambda row: isinstance(row[column], list))
        else:
            # Otherwise, include only key and column, but keep all non-dict types in table_list
            table = self.cut(key, column)
            table_list = table.select_rows(lambda row: not isinstance(row[column], dict))

        # All the columns other than column to ignore while melting
        ignore_cols = table.columns
        ignore_cols.remove(column)

        # Unpack lists as separate columns
        table_list.unpack_list(column, replace=True)

        # Rename the columns to retain only the number
        for col in table_list.columns:
            if f'{column}_' in col:
                table_list.rename_column(col, col.replace(f'{column}_', ""))

        # Filter dicts and unpack as separate columns
        table_dict = table.select_rows(lambda row: isinstance(row[column], dict))
        table_dict.unpack_dict(column, prepend=False)

        from parsons.etl.table import Table

        # Use melt to pivot both sets of columns into their own Tables and clean out None values
        melted_list = Table(petl.melt(table_list.table, ignore_cols))
        melted_dict = Table(petl.melt(table_dict.table, ignore_cols))

        melted_list.remove_null_rows('value')
        melted_dict.remove_null_rows('value')

        melted_list.rename_column('variable', column)
        melted_dict.rename_column('variable', column)

        # Combine the list and dict Tables
        melted_list.concat(melted_dict)

        import hashlib

        if expand_original:
            # Add unpacked rows to the original table (minus packed rows)
            orig = self.select_rows(lambda row: not isinstance(row[column], (dict, list)))
            orig.concat(melted_list)
            # Add unique id column by hashing all the other fields
            if 'uid' not in self.columns:
                orig.add_column('uid', lambda row: hashlib.md5(
                    str.encode(
                        ''.join([str(x) for x in row])
                        )
                    ).hexdigest())
                orig.move_column('uid', 0)

            # Rename value column in case this is done again to this Table
            orig.rename_column('value', f'{column}_value')

            # Keep column next to column_value
            orig.move_column(column, -1)
            output = orig
        else:
            orig = self.remove_column(column)
            # Add unique id column by hashing all the other fields
            melted_list.add_column('uid', lambda row: hashlib.md5(
                str.encode(
                    ''.join([str(x) for x in row])
                    )
                ).hexdigest())
            melted_list.move_column('uid', 0)
            output = melted_list

        self = orig
        return output

    def long_table(self, key, column, key_rename=None, retain_original=False,
                   prepend=True, prepend_value=None):
        """
        Create a new long parsons table from a column, including the foreign
        key.

        .. code-block:: python

           # Begin with nested dicts in a column
           json = [{'id': '5421',
                    'name': 'Jane Green',
                    'emails': [{'home': 'jane@gmail.com'},
                               {'work': 'jane@mywork.com'}
                              ]
                   }
                  ]
           tbl = Table(json)
           print (tbl)
           >>> {'id': '5421', 'name': 'Jane Green', 'emails': [{'home': 'jane@gmail.com'}, {'work': 'jane@mywork.com'}]} # noqa: E501
           >>> {'id': '5421', 'name': 'Jane Green', 'emails': [{'home': 'jane@gmail.com'}, {'work': 'jane@mywork.com'}]} # noqa: E501

           # Create skinny table of just the nested dicts
           email_skinny = tbl.long_table(['id'], 'emails')

           print (email_skinny)
           >>> {'id': '5421', 'emails_home': 'jane@gmail.com', 'emails_work': None}
           >>> {'id': '5421', 'emails_home': None, 'emails_work': 'jane@mywork.com'}

        `Args:`
            key: lst
                The columns to retain in the long table (e.g. foreign keys)
            column: str
                The column name to make long
            key_rename: dict
                The new name for the foreign key to better identify it. For
                example, you might want to rename ``id`` to ``person_id``.
                Ex. {'KEY_NAME': 'NEW_KEY_NAME'}
            retain_original: boolean
                Retain the original column from the source table.
            prepend:
                Prepend the column name of the unpacked values. Useful for
                avoiding duplicate column names
            prepend_value:
                Value to prepend new columns if ``prepend=True``. If None, will
                set to column name.
        `Returns:`
            Parsons Table
                The new long table
        """

        if type(key) == str:
            key = [key]

        lt = self.cut(*key, column)  # Create a table of key and column
        lt.unpack_list(column, replace=True)  # Unpack the list
        lt.table = petl.melt(lt.table, key)  # Melt into a long table
        lt = lt.cut(*key, 'value')  # Get rid of column names created in unpack
        lt.rename_column('value', column)  # Rename 'value' to old column name
        lt.remove_null_rows(column)  # Remove null values

        # If a new key name is specified, rename
        if key_rename:
            for k, v in key_rename.items():
                lt.rename_column(k, v)

        # If there is a nested dict in the column, unpack it
        if lt.num_rows > 0 and isinstance(lt.table[column][0], dict):
            lt.unpack_dict(column, prepend=prepend, prepend_value=prepend_value)

        if not retain_original:
            self.remove_column(column)

        return lt

    def cut(self, *columns):
        """
        Return a table of selection of columns

        `Args:`
            \*columns: str
                Columns in the parsons table
        `Returns:`
            A new parsons table containing the selected columnns
        """

        from parsons.etl.table import Table

        return Table(petl.cut(self.table, *columns))

    def select_rows(self, *filters):
        """
        Select specific rows from a Parsons table based on the passed
        filters.

        Example filters:
        .. code-block:: python
            tbl = Table([['foo', 'bar', 'baz'],
                         ['c', 4, 9.3],
                         ['a', 2, 88.2],
                         ['b', 1, 23.3],])

            # You can structure the filter in multiple wayss

            # Lambda Function
            tbl2 = tbl.select_rows(lambda row: row.foo == 'a' and row.baz > 88.1)
            tbl2
            >>> {foo: 'a', 'bar': 2, 'baz': 88.1}

            # Expression String
            tbl3 = tbl.select_rows("{foo} == 'a' and {baz} > 88.1")
            tbl3
            >>> {foo: 'a', 'bar': 2, 'baz': 88.1}

        `Args:`
            \*filters: function or str
        `Returns:`
            A new parsons table containing the selected rows
        """

        from parsons.etl.table import Table

        return Table(petl.select(self.table, *filters))

    def remove_null_rows(self, columns):
        """
        Remove rows if the values in a column are ``None``. If multiple columns
        are passed as list, it will remove all rows with null values in any
        of the passed columns.

        `Args:`
            column: str or list
                The column or columns to analyze
        `Returns:`
            ``None``
        """
        if isinstance(columns, str):
            columns = [columns]

        for col in columns:
            self.table = petl.selectisnot(self.table, col, None)

        return self

    def _prepend_dict(self, dict_obj, prepend):
        # Internal method to rename dict keys

        new_dict = {}

        for k, v in dict_obj.items():

            new_dict[prepend + '_' + k] = v

        return new_dict

    def stack(self, *tables, missing=None):
        """
        Stack Parsons tables on top of one another.

        Similar to ``table.concat()``, except no attempt is made to align fields from
        different tables.

        `Args:`
            tables: Parsons Table or list
                A single table, or a list of tables
            missing: bool
                The value to use when padding missing values
        `Returns:`
            ``None``
        """

        if type(tables) not in [list, tuple]:
            tables = [tables]
        petl_tables = [tbl.table for tbl in tables]

        self.table = petl.stack(self.table, *petl_tables, missing=missing)

    def concat(self, *tables, missing=None):
        """
        Concatenates one or more tables onto this one.

        Note that the tables do not need to share exactly the same fields.
        Any missing fields will be padded with None, or whatever is provided via the
        ``missing`` keyword argument.

        `Args:`
            tables: Parsons Table or list
                A single table, or a list of tables
            missing: bool
                The value to use when padding missing values
        `Returns:`
            ``None``
        """

        if type(tables) not in [list, tuple]:
            tables = [tables]
        petl_tables = [tbl.table for tbl in tables]

        self.table = petl.cat(self.table, *petl_tables, missing=missing)

    def chunk(self, rows):
        """
        Divides a Parsons table into smaller tables of a specified row count. If the table
        cannot be divided evenly, then the final table will only include the remainder.

        `Args:`
            rows: int
                The number of rows of each new Parsons table
        `Returns:`
            List of Parsons tables
        """

        from parsons import Table  # Just trying to avoid recursive imports.
        return [Table(petl.rowslice(self.table, i, i+rows)) for i in range(0, self.num_rows, rows)]

    @staticmethod
    def get_normalized_column_name(column_name):
        """
        Returns a column name with whitespace removed, non-alphanumeric characters removed, and
        everything lowercased.

        `Returns:`
            str
                Normalized column name
        """

        column_name = column_name.lower().strip()
        return ''.join(c for c in column_name if c.isalnum())

    def match_columns(self, desired_columns, fuzzy_match=True, if_extra_columns='remove',
                      if_missing_columns='add'):
        """
        Changes the column names and ordering in this Table to match a list of desired column
        names.

        `Args:`
            desired_columns: list
                Ordered list of desired column names
            fuzzy_match: bool
                Whether to normalize column names when matching against the desired column names,
                removing whitespace and non-alphanumeric characters, and lowercasing everything.
                Eg. With this flag set, "FIRST NAME" would match "first_name".
                If the Table has two columns that normalize to the same string (eg. "FIRST NAME"
                and "first_name"), the latter will be considered an extra column.
            if_extra_columns: string
                If the Table has columns that don't match any desired columns, either 'remove'
                them, 'ignore' them, or 'fail' (raising an error).
            if_missing_columns: string
                If the Table is missing some of the desired columns, either 'add' them (with a
                value of None), 'ignore' them, or 'fail' (raising an error).

        `Returns:`
            `Parsons Table` and also updates self
        """

        from parsons import Table  # Just trying to avoid recursive imports.

        normalize_fn = Table.get_normalized_column_name if fuzzy_match else (lambda s: s)

        desired_columns_normalized = {
            normalize_fn(col): col for col in desired_columns
        }

        # Check for extra columns in the Table.
        for orig_col in self.columns:
            normalized_col = normalize_fn(orig_col)
            if normalized_col not in desired_columns_normalized:
                if if_extra_columns == 'fail':
                    raise TypeError(f"Table has extra column {orig_col}")
                elif if_extra_columns == 'remove':
                    self.remove_column(orig_col)
                elif if_extra_columns != 'ignore':
                    raise TypeError(f"Invalid option {if_extra_columns} for "
                                    "argument `if_extra_columns`")
            else:
                # We matched a desired column. Remove it from our list, so if there is another
                # column in our Table that has the same normalized name, we consider it an
                # extra column.
                desired_columns_normalized.pop(normalized_col)

        # Regenerate the desired columns normalized dict, since we removed any matches
        # from it above.
        # Note we reverse the desired columns here, to make reordering easier later.
        # Cast desired_columns to a list in case someone gave us a dict or other iterable
        # that can't be reversed.
        desired_columns_normalized = {
            normalize_fn(col): col for col in reversed(list(desired_columns))
        }

        tbl_columns_normalized = {
            normalize_fn(col): col for col in self.columns
        }

        # Check for missing columns
        for normalized_col, orig_col in desired_columns_normalized.items():
            if normalized_col not in tbl_columns_normalized:
                if if_missing_columns == 'fail':
                    raise TypeError(f"Table is missing column {orig_col}")
                elif if_missing_columns == 'add':
                    self.add_column(orig_col)
                    tbl_columns_normalized[normalized_col] = orig_col
                elif if_missing_columns != 'ignore':
                    raise TypeError(f"Invalid option {if_missing_columns} for "
                                    "argument `if_missing_columns`")

        # Change column ordering and names to match the desired columns
        for desired_normalized_col, desired_orig_col in desired_columns_normalized.items():
            # Note that we ignore any desired columns still not in the Table, given
            # that we already checked what the caller wanted to do above.
            if desired_normalized_col in tbl_columns_normalized:
                tbl_orig_col = tbl_columns_normalized[desired_normalized_col]
                if tbl_orig_col != desired_orig_col:
                    self.rename_column(tbl_orig_col, desired_orig_col)
                self.move_column(desired_orig_col, 0)

        return self

    def reduce_rows(self, columns, reduce_func, headers, presorted=False,
                    **kwargs):
        """
        Group rows by a column or columns, then reduce the groups to a single row.

        Based on the `rowreduce` petl function - https://petl.readthedocs.io/en/stable/transform.html#petl.transform.reductions.rowreduce # noqa

        For example, the output from the query to get a table's definition is
        returned as one component per row. The `reduce_rows` method can be used
        to reduce all those to a single row containg the entire query.

        .. code-block:: python

            >>> ddl = rs.query(sql_to_get_table_ddl)
            >>> ddl.table

            +--------------+--------------+----------------------------------------------------+
            | schemaname   | tablename    | ddl                                                |
            +==============+==============+====================================================+
            | 'db_scratch' | 'state_fips' | '--DROP TABLE db_scratch.state_fips;'              |
            +--------------+--------------+----------------------------------------------------+
            | 'db_scratch' | 'state_fips' | 'CREATE TABLE IF NOT EXISTS db_scratch.state_fips' |
            +--------------+--------------+----------------------------------------------------+
            | 'db_scratch' | 'state_fips' | '('                                                |
            +--------------+--------------+----------------------------------------------------+
            | 'db_scratch' | 'state_fips' | '\tstate VARCHAR(1024)   ENCODE RAW'              |
            +--------------+--------------+----------------------------------------------------+
            | 'db_scratch' | 'state_fips' | '\t,stusab VARCHAR(1024)   ENCODE RAW'            |
            +--------------+--------------+----------------------------------------------------+

            >>> reducer_fn = lambda columns, rows: [
            ...     f"{columns[0]}.{columns[1]}",
            ...     '\n'.join([row[2] for row in rows])]
            >>> ddl.reduce_rows(
            ...     ['schemaname', 'tablename'],
            ...     reducer_fn,
            ...     ['tablename', 'ddl'],
            ...     presorted=True)
            >>> ddl.table

            +-------------------------+------------------------------------------------------------------+
            | tablename               | ddl                                                              |
            +=========================+==================================================================+
            | 'db_scratch.state_fips' | '--DROP TABLE db_scratch.state_fips;\nCREATE TABLE IF NOT EXISTS |
            |                         | db_scratch.state_fips\n(\n\tstate VARCHAR(1024)   ENCODE RAW\n\t |
            |                         | ,db_scratch.state_fips\n(\n\tstate VARCHAR(1024)   ENCODE RAW    |
            |                         | \n\t,stusab VARCHAR(1024)   ENCODE RAW\n\t,state_name            |
            |                         | VARCHAR(1024)   ENCODE RAW\n\t,statens VARCHAR(1024)   ENCODE    |
            |                         | RAW\n)\nDISTSTYLE EVEN\n;'                                       |
            +-------------------------+------------------------------------------------------------------+

        `Args:`
            columns: list
                The column(s) by which to group the rows.
            reduce_func: fun
                The function by which to reduce the rows. Should take the 2
                arguments, the columns list and the rows list and return a list.
                `reducer(columns: list, rows: list) -> list;`
            headers: list
                The list of headers for modified table. The length of `headers`
                should match the length of the list returned by the reduce
                function.
            presorted: bool
                If false, the row will be sorted.
        `Returns:`
            `Parsons Table` and also updates self

        """

        self.table = petl.rowreduce(
            self.table,
            columns,
            reduce_func,
            header=headers,
            presorted=presorted,
            **kwargs)

        return self
