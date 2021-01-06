''' Program that downloads logos of the institutions '''

from Data import *
from db_utilities import *
from selenium import webdriver

# make the data in the folder and the database consistent
logo_field_checker()

# connect to database
mycon = connect()
# get cursor instance
curs = mycon.cursor()

# basic query
query = "SELECT id, home_page FROM records WHERE logo_found = 'n' "
curs.execute(query)


# process row by row
for row in curs.fetchall():
    id = row[0]
    hp = row[1]

    print()
    print(id, hp)

    # address of the folder where images qill be saved
    store = "/home/saumya/Desktop/logos/"
    # change current working directory to that location
    os.chdir(store)

    # get url of the logo
    try:
        web = Data(hp)
        u = web.get_logo()
    # catch all exceptions
    except Exception as e:
        print(e)
        print()


    else:
        if u is not None and u != '':
            # load the image page
            try:
                image = load_page(u, hp)
            # catch all exceptions
            except Exception as e:
                print(e)
                print("Error in opening logo's URL - ",u)


            else:
                # save the image
                print("Logo found and saved.")
                print(u)
                with open('x'+str(id), 'wb') as fi:
                    fi.write(image.read())

                # update query
                query = " UPDATE records SET logo_found = \'y\' WHERE ID = " + str(id)
                # execute query and commit
                curs.execute(query)
                mycon.commit()


curs.close()    # close the cursor
mycon.close()   # close the connection


