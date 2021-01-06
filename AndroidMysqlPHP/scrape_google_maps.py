''' Program that scrapes institutes' data from Google Maps website '''



# search in order - colleges, universities, educational institutions, research institutions, schools, ...,
# coaching institutions, ..., programming institutes, acting, fine arts, language schools, teacher training
#
# industrial training institutes,
# beauty training, painting, dance, singing, sketching, academy


from selenium import webdriver
from db_utilities import connect
from url_utilities import *


print(datetime.now(), "->", __file__)      # Some utility function to print data-time of run NEEDED

# query = input("Enter keyword: ")
# clean 'query' if required

target = 'https://www.google.com/maps/search/schools+in+patna/@25.5574686,84.9633204,12z'

driver = webdriver.Firefox()
# driver.minimize_window()
driver.get(target)


names = set()


# process page by page
while True:
    # explicit wait of 1 minute to ensure that everything gets loaded
    time.sleep(60)

    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # process tile by tile (tile here shows info about a institute)
        for tag in soup.find_all('div', attrs={'class': 'section-result'}):

            # extract data from the tile
            try:
                title = tag.find('h3', attrs={'class': 'section-result-title'}).find('span').text
                website = tag.find('a', attrs={'class': 'section-result-action section-result-action-wide'})

                print(title, website)

                if website is not None:     # if it has a website
                    website = website['href']
                    # add to result set
                    names.add((title, website))

            # catch all exceptions
            except Exception as e:
                print(e)

        # find the 'next' button
        # a = driver.find_element_by_class_name('n7lv7yjyC35__button-next-icon')
        a = driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next')
        # click it
        a.click()

        break


    # catch all exceprtions
    except Exception as e:
        print(e)
        break



# save screenshot of the last page
driver.save_screenshot("./last.png")
driver.close()


print("Total links found =", len(names))
print()


# connect to database
mycon = connect()
# get cursor instance
curs = mycon.cursor()


for row in names:
    name = row[0]       # name of the institute
    home = row[1]       # home-page URL of the institute

    print(name, home)

    # normalize the URL
    try:
        if home.startswith('/'):
            home = "https://www.google.com" + home

        ht = load_page(home)
        home = ht.geturl()

        # ???? Avoiding jusdial based home pages ????
        # if bool(re.search('justdial', home, re.IGNORECASE)) == True:
        #     continue

    # catch all exceptions
    except Exception as e:
        print(e)
        print()

    # insert into a tempoarry table; it will be transferred to the main table by a different function
    query = "INSERT INTO temp (name, home) VALUES ('%s', '%s')" %(name, home)

    # execute query and commit
    try:
        curs.execute(query)
        mycon.commit()
    # catch all exceptions - (sometimes, home-page url may be too large, or some error may occur)
    except Exception as e:
        print(e)



curs.close()    # close the cursor instance
mycon.close()   # close the connection

print()

