import sqlite3
from numpy import divide as div
from numpy import mean
from functools import reduce

# establish connection
conn = sqlite3.connect('rpg_db.sqlite3')

# function that establishes the connection and cursor
# Also executes the query


def query_fetch(query):
    curs = conn.cursor()

    curs.execute(query)

    return curs.fetchall()


# a list with the character classes
classes = ['cleric', 'fighter', 'mage', 'thief']

# function that selects from a dataset


def sel_count(tab):
    def q(s): return f'SELECT COUNT(*) FROM charactercreator_{s};'
    return q(tab)


# all queries for the AssignmentÍ
queries = {
    1: sel_count('character'),
    2: '''SELECT 'mages' as class, COUNT(*) as amount
        FROM charactercreator_mage
        UNION
        SELECT 'clerics', COUNT(*)
        FROM charactercreator_cleric
        UNION
        SELECT 'fighters', COUNT(*)
        FROM charactercreator_fighter
        UNION
        SELECT 'thieves', COUNT(*)
        FROM charactercreator_thief;''',
    3: 'SELECT COUNT(*) FROM armory_item;',
    4: 'SELECT COUNT(*) FROM armory_weapon',
    5: '''SELECT AVG(items) FROM (SELECT COUNT(item_id) as items
        FROM charactercreator_character_inventory GROUP BY character_id);''',
    6: '''SELECT AVG(items) FROM (
        SELECT COUNT(item_id) as items
        FROM charactercreator_character_inventory as invs
        JOIN armory_weapon as weap
        ON weap.item_ptr_id = invs.item_id
        GROUP BY character_id);'''}

# select and get the total # of characters
total_characters = query_fetch(queries[1])[0][0]

# select and get total # of characters in each individual class
count_each_subclass = [query_fetch(sel_count(spec))[0][0] for spec in classes]

assert total_characters == sum(count_each_subclass)

# total items
total_items = query_fetch(queries[3])[0][0]

# weapon count
weapons_count = query_fetch(queries[4])[0][0]

# average items a character has
items_avg = query_fetch(queries[5])

# average weapons a character has
weaps_avg = query_fetch(queries[6])

# total number of characters
print(f'there are {total_characters} characters. ')

# number of characters in each individual class
# Lambda used to apply the 'sel_count'(s) function to an arguement(t)
print(reduce(lambda s,
             t: s + t,
             [f'there are {num} {cla}s. ' for num,
              cla in zip(count_each_subclass,
                         classes)]))

# total number of items
print(f'there are {total_items} total items')

# total number of non-weapons
print(f'{total_items-weapons_count} is the number of non-weapon items. ')

# average number of items a character has
print(
    f'The mean number of items each character carries is {mean(items_avg):.3}')

# average number of weapons a character has
print(
    f'The mean number of weapons carried by a character is {mean(weaps_avg):.3}')
