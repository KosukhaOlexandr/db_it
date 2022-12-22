import copy
import pickle


class Char(str):
    def __new__(cls, string):
        if len(string) > 1:
            raise ValueError('Value should have length of 1 or 0')
        instance = super().__new__(cls, string)
        return instance


class Column:
    _types = [int, str, float, complex, Char]
    _str_types = ['int', 'str', 'float', 'complex', 'char']
    _str_to_type = dict(zip(_str_types, _types))

    def __init__(self, name, coltype):
        self._name = name
        self.ctype = coltype

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(str(value)) == 0:
            raise ValueError('Name can\'t be empty')

    @property
    def ctype(self):
        return self._ctype

    @ctype.setter
    def ctype(self, coltype):
        if coltype in Column._types:
            self._ctype = coltype
        elif coltype in Column._str_to_type:
            self._ctype = Column._str_to_type[coltype]
        else:
            raise NotImplementedError(f'Type {coltype} can\'t be entered')

    def __eq__(self, other):
        if type(other) == Column:
            if other.name == self.name and other.ctype == self.ctype:
                return True
            return False
        raise ValueError('Comparing column to not a column')

    def __hash__(self):
        primes = [3, 5, 7, 11, 13, 17, 19]
        pr_types = {Column._types[i]: primes[i] for i in range(len(Column._types))}

        return hash(self.name) * pr_types[self.ctype]

    def __repr__(self):
        return f'Column(Name: {self.name}, Type: {self.ctype})'


class Row:
    __next_id = 1

    def __init__(self, col_val):
        self._col_val = {}
        for key, val in col_val.items():
            self.add_col_val(key, val)
        self._id = Row.__next_id
        Row.__next_id += 1

    @property
    def id(self):
        return self._id

    @property
    def col_val(self):
        return copy.deepcopy(self._col_val)

    def add_col_val(self, col, val):
        if col.name in [cl.name for cl in self._col_val.keys()]:
            raise ValueError(f'Column with name {col.name} is already present in the row')
        else:
            try:
                col_cp = copy.deepcopy(col)
                val_cp = col.ctype(val)
                self._col_val[col_cp] = val_cp
            except ValueError:
                raise TypeError(f'val should have type {col.ctype}')

    def remove_col(self, col):
        if type(col) == str:
            if col in (d := {cl.name: cl for cl in self._col_val.keys()}):
                col = d[col]
            else:
                raise ValueError('There is no column with this name in the table')
        if col in self._col_val.keys():
            self._col_val.pop(col)
        else:
            raise ValueError('No such column')

    def edit(self, col, val):
        if type(col) == str:
            if col in (d := {cl.name: cl for cl in self._col_val.keys()}):
                col = d[col]
            else:
                raise ValueError('There is no column with this name in the table')
        if col in self._col_val.keys():
            try:
                val_cp = col.ctype(val)
                self._col_val[col] = val_cp
            except ValueError:
                raise ValueError(f'val should have type {col.ctype}')
        else:
            raise ValueError('No such column')

    def __repr__(self):
        return f'Row(Id: {self.id}, Values:{str(self._col_val)})'


class Table:
    def __init__(self, name):
        self._name = name
        self._rows = []
        self._columns = []

    @property
    def rows(self):
        return copy.deepcopy(self._rows)

    @property
    def columns(self):
        return copy.deepcopy(self._columns)

    def _col_in_table(self, col):
        res = col
        if type(col) == str:
            if col in (d := {cl.name: cl for cl in self._columns}):
                res = d[col]
            else:
                res = None
        elif type(col) != Column:
            raise TypeError('Column argument should be of type str of Column')
        elif col.name not in (cl.name for cl in self._columns):
            res = None

        return res

    def _row_in_table(self, row):
        res = row
        if type(row) == int:  # id
            if row in (d := {r.id: r for r in self._rows}):
                res = d[row]
            else:
                res = None
        elif type(row) != Row:
            raise TypeError('Row argument should have type str or Row')
        elif row.id not in (r.id for r in self._rows):
            res = None

        return res

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if len(str(new_name)) < 1:
            raise ValueError('Name should not be empty')

    def add_column(self, col):
        if self._col_in_table(col) is None and type(col) == Column:
            col_copy = copy.deepcopy(col)
            self._columns.append(col_copy)
        else:
            raise ValueError(f'Column that have name {col.name} is already present in the table')
        return col

    def add_row(self, row):
        if self._row_in_table(row) is not None and type(row) == Row:
            raise ValueError(f'Row with id {row.id} is already in the table')

        for col in row.col_val.keys():
            if col not in self._columns:
                raise ValueError(f'Column {col} is not in the table')
        row_copy = copy.deepcopy(row)
        self._rows.append(row_copy)
        return row

    def delete_row(self, idd):
        deleted = False
        for row in self._rows:
            if row.id == idd:
                self._rows.remove(row)
                deleted = True
        if not deleted:
            raise ValueError(f'Row with id {idd} is not present in the table')

    def delete_column(self, name):
        column = self._col_in_table(name)
        if column is None:
            raise ValueError(f'Column {name} is not present in the table')

        for i, row in enumerate(self._rows):
            if column in row.col_val:
                self._rows[i].remove_col(column)
        can_delete = True
        while can_delete:
            can_delete = False
            for i, row in enumerate(self._rows):
                if self._rows[i].col_val == {}:
                    self.delete_row(row.id)
                    can_delete = True
        self._columns.remove(column)

    def edit_row_element(self, col, row_id, val):
        column = self._col_in_table(col)
        if column is None:
            raise ValueError('There is no such column in the table')

        row = self._row_in_table(row_id)
        if row is None:
            raise ValueError('There is no such row in the table')

        row.edit(col, val)

    def delete_duplicates(self):
        for i, i_row in enumerate(self._rows):
            for j, j_row in enumerate(self._rows):
                if i_row.id != j_row.id:
                    if i_row.col_val == j_row.col_val:
                        self._rows.remove(j_row)

    def __repr__(self):
        return f'Table(\nName: {self.name}\nColumns: {self._columns}\nRows: {self._rows}\n'

    """def __dict__(self):
        col_val_dict = []
        for row in self.rows:
            col_val_dict.append({'id': row.id, 'col_val': {col.__dict__(): val for col, val in row.col_val.items()}})
        return {'table_name': self.name, 'table_columns': [col.__dict__() for col in self._columns],
                'table_rows': col_val_dict}
    """

class Database:
    def __init__(self, name):
        self._name = name
        self._tables = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        try:
            new_name = str(new_name)
            if new_name == '':
                raise AttributeError('Name of a database can\'t be empty', '')
            self._name = new_name
        except ValueError:
            raise ValueError('Name of a database should be of type string')

    @property
    def tables(self):
        return self._tables

    def add_table(self, table):
        if table.name in [tbl.name for tbl in self._tables]:
            raise ValueError(f'The table with name {table.name} is already present in the database')
        else:
            table_copy = copy.deepcopy(table)
            self._tables.append(table_copy)

    def get_table(self, name):
        table = None
        for tbl in self._tables:
            if tbl.name == name:
                table = tbl

        # it will give a reference to the table - so that the changes to the object change table in the database
        if table is None:
            raise ValueError(f'The table with name {name} is not present in the database')
        else:
            return table

    def delete_table(self, name):
        table = None  # without it gives 'Local variable 'table' might be referenced before assignment' warning
        for tbl in self._tables:
            if tbl.name == name:
                table = tbl

        if table is None:
            raise ValueError(f'The table with name {name} is not present in the database')
        else:
            self._tables.remove(table)

    def __repr__(self):
        return f'Database(\nName: {self.name}\nColumns: {self.tables}\n'

    @staticmethod
    def save_pickle(db):
        with open(f'db.pkl', 'wb') as out:
            pickle.dump(db, out, -1)

    @staticmethod
    def load_pickle():
        with open(f'db.pkl', 'rb') as inp:
            return pickle.load(inp)

# every object added to the table or database is copied beforehand to
