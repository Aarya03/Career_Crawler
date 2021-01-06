from Data import *
from db_utilities import *

# required delay of websites may be stored in database -> some may not support 0 delay

try:
    # connect to the MySQL database
    mycon = connect()

# catch all the exceptions
except Exception as e:
    print(e)

else:
    # get a cursor instance
    curs = mycon.cursor()

    # basic selection query
    query = " SELECT id, home_page, examined_pages, complete_crawl FROM records where link_found = 'n' order by id  desc limit 150"   # not in (28, 1, 3, 4, 6, 9, 21, 32, 56) "
    curs.execute(query)

    a = curs.fetchall()
    curs.close()
    mycon.close()   # close the connection for now

    timestamped_log = datetime.now().strftime("%Y-%m-%d__%H:%M:%S.log")

    fi = open(timestamped_log, "w")    # open a log file
    # set the error stream to the log file
    sys.stderr = fi

    stats = []

    # start crawling websites one by one
    for row in a:
        # get the required info about the institution
        id = row[0]
        link = row[1]
        epages = row[2]
        ccrawl = row[3]

        print(id, link)
        print(id, link, file=fi)

        # crawl the site
        try:
            web = Data(link)
            web.crawl(0.0, 3*epages+50)     # Setting limit as a function of number of pages crawled previously

        # catch all the exceptions
        except Exception as e:
            print("**** From TESTER ->", e, file=sys.stderr)
            print(file=sys.stderr)

        # get the requied filters - s is positive, p is negative
        s, p = get_filters()
        # filter sites using filters s and p
        web.get_tsites(s, p)

        print()
        # for i in web.tsites:
        #     print(web.scheme_dom + i)
        # print()

        tmp = []    # will later be appended to stats
        tmp.append(id)

        if web.counter <= epages:
            # less pages cralwed than what earlier had been crawled
            tmp.append(epages)
            tmp.append(ccrawl)

        else:
            # morepages crawled than what earlier has been crawled
            tmp.append(web.counter)
            if web.index == len(web.urls):
                tmp.append('y')
            else:
                tmp.append('n')


        tmp2 = []      # 'sites' will be stored in this

        try:
            for li in web.tsites:
                # pdf, ppt, doc, etc. not to be stored -> Ooly webpagesational institution database
                # are to be stored
                if web.url_file_check(li) == True:
                    tmp2.append(web.scheme_dom+li)


        except Exception as e:
            print("**From crawl_and_find.py**", li)
            print(e, file=sys.stderr)

        if len(tmp2) != 0:
            # some target link found
            link_found = 'y'
        else:
            link_found = 'n'

        tmp.append(link_found)
        tmp.append(tmp2)

        stats.append(tmp)

    # connect to the MySQL database
    mycon = connect()
    # get a cursor instance
    curs = mycon.cursor()

    # update the records for each institution
    for row in stats:
        id = row[0]
        cnt = row[1]
        comple = row[2]
        link_found = row[3]

        query = "UPDATE records SET examined_pages = %s, complete_crawl = '%s', link_found = '%s' WHERE id = %s " %(cnt, comple, link_found, id)
        print(query)

        # execute and commit the query
        try:
            curs.execute(query)
            mycon.commit()

        # catch all the exceptions
        except Exception as e:
            print(query)
            print(e, file=sys.stderr)


        links = row[4]     # for storing in the 'sites' table

        for li in links:
            query = "INSERT INTO sites (id, link) VALUES (%s, '%s')" %(id, li)
            print(query)
            # execute and commit the query
            try:
                curs.execute(query)
                mycon.commit()

            # catch all the exceptions
            except Exception as e:
                print(query)
                print(e, file=sys.stderr)


    fi.close()      #close the log file
    curs.close()    # close the cursor instance
    mycon.close()   # close the database connection



