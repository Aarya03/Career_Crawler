from Data import *
from db_utilities import connect
import json
import sys

def generate_JSON(about, links, errors):

    # name of the JSON file = id_timestamp.json
    name = str(about['ID']) + '_' + datetime.now().strftime("%Y-%m-%d__%H:%M:%S") + '.json'

    with open("Out.json", 'w') as fi:
        info = {"about": about, "links": links, "errors": errors}
        json.dump(info, fi)



if __name__=='__main__':

    # enter id of the Institute to be crawled
    institute_id = sys.argv[1];

    # will be written to a JSON file
    about = dict()
    links = list()
    errors = list()

    about['ID'] = institute_id

    # connect to the database
    try:
        mycon = connect()

    # catch all exceptions
    except Exception as e:
        errors.append(e)
        # call function to generate JSON file
        generate_JSON(about, links, errors)

    else:

        # get an cursor instance
        curs = mycon.cursor()
        # basic select query
        query = " SELECT home_page, name, type FROM records WHERE id = " + str(institute_id)
        # execute the query
        curs.execute(query)

        row = curs.fetchall()

        if row != []:
            # store basic information about the institute
            about['Name'] = row[0][1]
            about['Home-Page'] = row[0][0]
            about['Type'] = row[0][2]

            # initialise a web crawler
            web = Data(row[0][0])

            # only 20 pages from the site will be crawled
            pages_to_crawl = 20

            clock_start = time.time()
            web.crawl(0, pages_to_crawl)
            clock_end = time.time()
            # calculate time taken for crawling
            time_taken = clock_end - clock_start

            about['Pages crawled'] = pages_to_crawl
            about['Time taken'] = time_taken

            s, p = get_filters()
            # filter out job-related sites
            web.get_tsites(s, p)
            for li in web.tsites:
                print(web.scheme_dom+li,end='#')
            # put the result in 'links' list
            links = [ web.scheme_dom + li for li in web.tsites ]

            # update info of the institute in the 'records' table
            comp_crawl = ''
            if web.index == len(web.urls):
                # whole website crawled
                comp_crawl = 'y'
            else:
                # only partial website crawled
                comp_crawl = 'n'

            # update query
            query = "UPDATE records SET examined_pages = " + str(web.index) + ", complete_crawl = '" + comp_crawl + "' WHERE id = " + str(institute_id)
            curs.execute(query)

        else:
            # invalid 'id' entered
            errors.append("Invalid ID entered")

        # generate the JSON file
        generate_JSON(about, links, errors)

        for li in links:
            try:
                query = "INSERT INTO sites (id, link) VALUES (%s, '%s')" % (institute_id, li)
                # execute the query
                curs.execute(query)
            # catch the exceptions
            except Exception as e:
                pass


        mycon.commit()

        curs.close()
        mycon.close()



