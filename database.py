import sqlite3

# Creating table
tables = {
"economy" : """ CREATE TABLE economy (
			id INTEGER(25) NOT NULL,
			balance INTEGER(25)
		); """,
}
def ch_del(s, i):
	s = s[:i] + s[i+1:]
	return s

def recreate_table(table_name):
	abdb = sqlite3.connect('apobotdb.db')
	cursor = abdb.cursor()
	cursor.execute("DROP TABLE IF EXISTS {0}".format(table_name))
	cursor.execute(tables[table_name])
	cursor.close()
	abdb.close()

def insert_eco_table(member_id, balance):
	abdb = sqlite3.connect('apobotdb.db')
	cursor = abdb.cursor()
	cursor.execute("""INSERT INTO economy (id, balance)
				VALUES ('{0}', '{1}');""".format(member_id, balance))
	abdb.commit()
	abdb.close()

def get_eco_table(member_id):
	abdb = sqlite3.connect('apobotdb.db')
	cursor = abdb.cursor()
	cursor.execute("""SELECT * FROM economy""")
	output = cursor.fetchall()
	return(output)
	cursor.close()
	abdb.close()

def update_eco_table(member_id, balance):
	abdb = sqlite3.connect('apobotdb.db')
	cursor = abdb.cursor()
	cursor.execute("""UPDATE economy SET balance = {0} WHERE id={1};""".format(balance, member_id))
	abdb.commit()
	abdb.close()

recreate_table("economy")
insert_eco_table(1, 1)
print(get_eco_table(1))
update_eco_table(1, 20)
print(get_eco_table(1))
