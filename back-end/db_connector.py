from db_utilities import *

# NULL in field value is returned as None

# CHAR field is retrieved without the 'padded' characcters, i.e., data is not returned with 'fixed-length'


# connect to the database
try:
	mycon = connect()

# catch all the exceptions
except Exception as e:
	print(e)


else:
	print("Connected to the database")
	curs = mycon.cursor()

	with open("Institutes_Added_to_Check_via_Program (copy)", "r") as fi:
		for s in fi.readlines():
			s = s.split(",")

			name = s[:-1]
			name = ",".join(name)

			if s[-1][-1] == '\n':
				hpg = s[-1][:-1]
			else:
				hpg = s[-1]

			query = 'INSERT INTO records (name, home_page) values(\"'+name+'\",\"'+hpg+'\")'

			try:
				curs.execute(query)
				mycon.commit()
			except Exception as e:
				print(e)
				print(name, hpg)

			# print(name, hpg)

	print("All records added to the database")
	curs.close()
	mycon.close()

