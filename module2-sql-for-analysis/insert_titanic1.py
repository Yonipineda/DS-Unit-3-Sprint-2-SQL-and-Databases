import psycopg2 as psy
import os
import pandas as pd
from dotenv import load_dotenv

"""
Trying it the 'standard' way.
"""

load_dotenv()
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")

conn = psy.connect(dbname=dbname, user=user, password=password, host=host)
curs = conn.cursor()


query = """
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived bool,
    pclass int,
    name varchar,
    sex varchar,
    age int,
    sib_spouse_count int,
    parent_child_count int,
    fare float8
);
"""
curs.execute(query)
conn.commit()  # actually update the database

df = pd.read_csv(
    'https://raw.githubusercontent.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv')
df['Survived'] = df['Survived'].astype(bool)
df.rename(columns={'Siblings/Spouses Aboard': 'sibs_spouses'}, inplace=True)
df.rename(
    columns={'Parents/Children Aboard': 'parents_children'}, inplace=True)
df.rename(
    columns={'Parents/Children Aboard': 'parents_children'}, inplace=True)
df['Age'] = df['Age'].astype(int)
df['Name'] = df['Name'].str.replace("'", '')

for row in df.itertuples():
    insert_rows = """
    INSERT INTO passengers
    (survived, pclass, name, sex, age, sib_spouse_count, parent_child_count, fare)
    VALUES """ + '(' + str(row.Survived) + ', ' + str(row.Pclass) + ', ' + "'" + str(row.Name) + "'" + ", '" + str(row.Sex) + "', " + str(row.Age) + ', ' + str(row.sibs_spouses) + ', ' + str(row.parents_children) + ', ' + str(row.Fare) + ');'
    curs.execute(insert_rows)

conn.commit()
