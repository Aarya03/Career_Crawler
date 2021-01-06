from modules import *
import mysql.connector as sqltor
from url_utilities import load_page


def connect():
    return sqltor.connect(host='localhost', user='fred', passwd='zap', database='misc')


            # keywords like 'institutiton', 'academy', etc. should be used in name-based search

def institution_type(name):    #  Returns the type of institution based on its name


    # cue-word to type of institution mapping
    fields = {
            "play|pre|kid|montessori|kindergarten":"play", "primary":"primary", "secondary":"secondary", "high":"high", "school":"school",
            "engineer": "engineering", "tech": "technology", "polytechni|iti|i\.t\.i\.": "polytechnic",
            "medical": "medical", "dent":"dental","pharma":"pharmacy", r'nurs(e|ing)\b':"nurse",
            "research": "research", "scien": "science",
            "college": "college", "universit": "university",
            r"\bart": "arts", "manag": "management", "social": "social", "humanit": "humanities", "market":"marketing",
            "music":"music", "act":"acting", r'\bsing':"singing", "danc":"dance", "film":"filmography", "television|tv|t\.v\.":"television",
            "train": "training", "teach":"teacher",
            r"comput|program(m)?|cod|web|cyb": "computer", "digital":"digital",
            "design": "designing", "(fashion)|(nift)|(n.i.f.t)|(n\.i\.f\.t)": "fashion", "animat":"animation", "graphic":"graphics",
            "professio":"professional",
            "journali":"journalism", r"mass|(\bmedia\b)":"media",
            "law":"law",
            "meteorolog":"meteorology",
            "beaut":"beauty",
            "langua":"language",
            # "hotel":"hotel"

            "women|girl|lad(y|i)|mahila":"women", r"(\bboy)|(\bmen)":"men",  # Problem here

            "yoga":"yoga", "fitness":"fitness", "physical":"physical",

            }

    res = ''    # result to be returned

    for i in fields:
        if bool(re.search(i, name, re.IGNORECASE)):
            res += fields[i] + ' '

    return res[:-1]     # return the result (last space character removed)



# function that finds and updates the type of an institution from the table
def set_type():
    print(datetime.now(), "->", set_type.__name__)

    # connect to the database
    try:
        mycon = connect()

    # catch all exceptions
    except Exception as e:
        print("Error connecting to database ->", e)


    else:
        # get ccursor instance
        curs = mycon.cursor()

        # basic query
        curs.execute("SELECT id, name FROM records ")

        # process one row at a time
        for row in curs.fetchall():
            name = row[1]       # name of the institution
            res = institution_type(name)

            if res != '':
                query = "UPDATE records SET type = \"" + res + "\" WHERE id = " + str(row[0])
                curs.execute(query)
                mycon.commit()

        curs.close()        # close the cursor instance
        mycon.close()       # close the connection
        print()


# a function that opens home-page and update the value with the redirected one
def home_page_normalizer():
    print(datetime.now(), "->", home_page_normalizer.__name__)

    # connect to database
    try:
        mycon = connect()

    # catch all exceptions
    except Exception as e:
        print("Error connecting to database")


    else:
        # get cursor instance
        curs = mycon.cursor()

        # basic query
        query = "SELECT id, home_page FROM records";
        curs.execute(query)

        # process row by row
        for row in curs.fetchall():
            id = row[0]
            link = row[1]

            # open the home-page
            try:
                ht = load_page(link)

            # catch all exceptions
            except Exception as e:
                print(id, link)
                print(e)
                print()


            else:
                new_link = ht.geturl()
                if link == new_link:
                    # no redirection
                    continue

                # else, redirection happened
                try:
                    query = "UPDATE records SET home_page = " + "\'" + new_link + "\'" + " WHERE id = " + str(id) ;
                    print(query)
                    # execute query and commit
                    curs.execute(query)
                    mycon.commit()

                # catch all exceptions
                except Exception as e:
                    print(id, link)
                    print(e)
                    print()


        curs.close()        # close the cursor instance
        mycon.close()       # close the connection




# a function that tries to resolve home-page URLs that have no protocol; tries to prefix them with 'https://' or 'http://'
def protocol_resolver():

    # connect to database
    try:
        mycon = connect()

    # catch all exceptions
    except Exception as e:
        print("Error connecting to the database ->", e)


    else:
        # get cursor instance
        curs = mycon.cursor()

        # basic query
        query = ''' SELECT id, home_page FROM records WHERE home_page NOT LIKE \'http%\'  '''

        curs.execute(query)

        # process row by row
        for row in curs.fetchall():
            id = row[0]
            link = row[1]
            print(id)

            url = ''

            # try with 'https'
            try:
                ht = load_page('https://' + link)
                url = ht.geturl()

            # catch all exceptions
            except Exception as e:
                print(e)

                # try with 'http'
                try:
                    ht = load_page('http://' + link)
                    url = ht.geturl()

                # catch all exceptions
                except Exception as f:
                    print(f)


            if url == '':
                # couldn't be resolved
                continue

            # update query
            query = "  UPDATE records SET home_page = " + "\'" + url + "\' " + "WHERE id = " + str(id);
            print(query)
            print()

            # execute query and commit
            curs.execute(query)
            mycon.commit()


        curs.close()        # close cursor instance
        mycon.close()       # close the connection



# function to check if the entries in database are consistent with the actual images saved in the folder
def logo_field_checker():

    print(datetime.now(), "->", logo_field_checker.__name__)

    # connect to database
    try:
        mycon = connect()

    # catch all exceptions
    except Exception as e:
        print("Error connecting to database ->", e)


    else:
        # get cursor instance
        curs = mycon.cursor()
        # basic query
        query = ''' SELECT id, logo_found FROM records  '''
        curs.execute(query)

        data = curs.fetchall()

        # process row by row
        for row in data:
            id = row[0]         # 'id' to be processed ahead
            logo_found = row[1]
            res = 'y'       # keeping default as 'y'

            # address of folder where images are stored
            store = "/home/saumya/Desktop/logos/"


            if os.path.isfile(store+'x'+str(id)) == False:
                # image not found in the folder
                res = 'n'

            if logo_found != res:
                # update query
                query = " UPDATE records SET logo_found = \'" + res + "\' " + "WHERE id = " + str(id)
                # execute query and commit
                curs.execute(query)
                mycon.commit()


        curs.close()
        mycon.close()


    # reverse check also required -> id not in the database but associated logo file still present -> delete such file
    files = os.listdir(store)

    for a in files:
        flag = 0
        for row in data:
            if a[1:] == str(row[0]):
                flag = 1
                break

        if flag == 0:     # id not in database
            os.remove(store+a)
            print(a, "deleted")

    print()





def table_transfer():
    try:
        mycon = connect()

    except Exception as e:
        print(e)

    else:
        curs = mycon.cursor()

        query = "SELECT name, home FROM temp"
        curs.execute(query)

        data = curs.fetchall()

        for row in data:
            name = row[0]
            home = row[1]

            query = "INSERT INTO records(name, home_page) VALUES ('%s', '%s')" % (name, home)
            try:
                curs.execute(query)
                mycon.commit()
            except Exception as e:
                print(e)
                print(query)
                print()

        query = "TRUNCATE temp"
        curs.execute(query)
        mycon.commit()

        curs.close()
        mycon.close()




def duplicate_name_remover():
    print(datetime.now(), "->", duplicate_name_remover.__name__)

    mycon = connect()
    curs = mycon.cursor()

    curs.execute("SELECT id, name from records where name in (select name from records group by name having count(name) > 1 ) order by name, id")

    data = curs.fetchall()
    n = len(data)

    if n == 0:        # no duplicate names present
        return

    i = 0
    row = data[i]
    i += 1
    delete = list()

    while i < n:
        tmp = data[i]
        if tmp[1].casefold() == row[1].casefold():    # name matches with the previous row
            delete.append(tmp[0])

        else:
            row = tmp

        i += 1

    num = ''
    for k in delete:
        num = str(k) + ","

    if num == '':
        return

    num = num[:-1]

    query = "DELETE FROM records where id IN (" + num + ")"

    curs.execute(query)
    mycon.commit()
    print(query)
    print()

    curs.close()
    mycon.close()


def similar_home_page_remover():
    print(datetime.now(), "->", similar_home_page_remover.__name__)

    mycon = connect()
    curs = mycon.cursor()

    curs.execute("SELECT id, home_page FROM records ORDER BY home_page")

    data = curs.fetchall()
    n = len(data)

    if n == 0:      # Nothing to do
        return

    delete = list()
    i = 0

    while i < n-1:
        row = data[i]
        hp = row[1]

        next_row = data[i+1]
        next_hp = next_row[1]

        if hp+'/' == next_hp:
            delete.append(next_row[0])
            i += 2

        else:
            i += 1

    num = ''
    for k in delete:
        num = str(k) + ","

    if num == '':
        return

    num = num[:-1]

    query = "DELETE FROM records WHERE id IN (" + num + ")"
    print(query)
    curs.execute(query)
    mycon.commit()

    print()

    curs.close()
    mycon.close()




def link_found_field_checker():    # Both 'y' and 'n' settter to be made in one query using case statement
    mycon = connect()
    curs = mycon.cursor()

    curs.execute("UPDATE records SET link_found = 'n'  where id NOT IN (select distinct(id) from sites) ")
    curs.execute("UPDATE records SET link_found = 'y'  where id IN (select distinct(id) from sites) ")
    mycon.commit()

    curs.close()
    mycon.close()




if __name__ == '__main__':

    # table_transfer()

    # duplicate_name_remover()
    # similar_home_page_remover()
    set_type()
    # logo_field_checker()
    # protocol_resolver()

    # home_page_normalizer()

    print()

# More database cleainng tasks left -> general prefix checking, difference in terms of http and https only