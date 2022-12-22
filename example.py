# an example of usage

from db_cust import *

t = Table('t1')
c1 = Column('c', int)
c2 = Column('c1', 'int')
print(c2.__dict__)

t.add_column(c1)
t.add_column(c2)
t.add_row(Row({c1: 1, c2: 4}))
t.add_row(Row({c1: 4}))

print(t)

t.delete_row(1)
print(t)
t.add_row(Row({c2: 4}))
print(dict(t.__dict__))
print(t)
t.delete_column('c')

db = Database('db')
db.add_table(t)
print(db)

Database.save_pickle(db)
db_1 = Database.load_pickle()
print(db_1)
