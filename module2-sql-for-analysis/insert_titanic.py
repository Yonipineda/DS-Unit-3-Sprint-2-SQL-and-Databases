import psycopg2 as psy
import pandas as pd
import numpy as np
from functools import reduce
from dotenv import load_dotenv
import os

"""
Note on reduce from functools: Its applying two arguments(s, t) cumulatively
to the items of iterable, from left to right, to reduc the iterable to a
single value.
"""
load_dotenv()

dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")

conn = psy.connect(dbname=dbname, user=user, password=password, host=host)
curs = conn.cursor()
# function for strings/cleaning


def f(x):
    if isinstance(x, str):
        return(x.replace(' ', '_')
                .replace('/', '_')
                .replace('(', '')
                .replace(')', '')
                .replace(".", "")
                .replace("'", ""))
    else:
        return x


# read in file
# apply previous function to columns in the df
# fix dtypes
name = 'titanic'  # saved titanic in name for reusability
df = pd.read_csv(name+'.csv').rename(columns=f).applymap(f)
D = df.shape[0]
d_ty = df.dtypes.replace(
    {'int64': 'INT', 'object': 'TEXT', 'float64': 'FLOAT'})


tab_feats_name = '{0} ({1})'.format(name, reduce(
    lambda s, t: s + ', ' + t, [' '.join(t) for t in zip(d_ty.index,
                                                         [x.__str__() for x in d_ty.values])]))

Create_t = f'CREATE TABLE {tab_feats_name};'

insert_prefix = f'INSERT INTO' + name

insert_multir = ' VALUES {0};'.format(reduce(
    lambda s, t: s + ", " + t,
    ["('" + "', '".join(map(str, df.loc[k].values)) + "')" for k in df.index]))


def inserts(q, DDD=D):
    curs.execute('SELECT COUNT(*) FROM ' + name)
    if curs.fetchall()[0][0] < DDD:
        try:
            curs.execute(q)
        except psy.ProgrammingError as e:
            print(e)
        else:
            print("inserted now")
        finally:
            print("exiting")
            pass
    else:
        print("items already inserted")
        pass

    try:
        curs.execute(create)
    except psy.ProgrammingError as e:
        print(e)
    else:
        inserts(insert_prefix + insert_multir)
    finally:
        conn.commit()


"""
This was an attempt to automate much of the process, it does its job but it is
quite dificult to read. Probably not a good idea to write it this way when
working with a team.

Initially, it did not load the query into ElephantSQL but, after rewatching them
lecture video, it turns out doing conn.close() was the problem.
"""
