from Crawler import *



# 'Data' class inherits from 'Crawler' class

class Data(Crawler):       # Changing 'show tables;logo' to 'log' ???

    # constructor function
    def __init__(self, homepage, verbose=False, browser=False):

        # initialize the base part
        super().__init__(homepage, verbose, browser)

        # initialize the derived part
        self.tsites=list()


    # for filtering target sites based on filters provided
    def get_tsites(self, a, b=[]):

        # examining every link ('half' link) present in the urls[]
        for link in self.urls:

            for i in b:    # Negative filter
                if bool( re.search(i, link, re.IGNORECASE) ) == True:
                    # passed the negative filter
                    break

            # all negative filters failed, now check for positive filters
            else:
                for j in a:
                    if bool( re.search(j, link, re.IGNORECASE) ) == True:
                        # positive filter matched
                        self.tsites.append(link)
                        break



    # funcion that returns URL of the logo of an institute
    def get_logo(self):

        # a local function
        def img_to_hpage(tag):

            if tag.name != 'a':
                return False

            if tag.has_attr('href') == False:
                # <a> tag has no href attribute
                return False

            c = tag.find('img')
            if c is None:  # no <img> tag inside the given <a> tag
                return False


            p = tag['href']     # href attribute of the tag

            if bool(re.search(r'index|default', p, re.IGNORECASE)) == True:
                # 'index', 'default' keywords there in the href attribute - very likely that it is link to the home-page
                return True

            q = url_normalize(self.home_page, p)

            if q != self.home_page:
                return False

            return True


        # a local function
        def src_or_alt(tag):
            if tag.name != 'img':
                # not an <img> tag
                return False

            # some sites have 'logs' and similar keywords
            if tag.has_attr('src'):
                if bool(re.search(r'logo', tag['src'], re.IGNORECASE)) == True:
                    return True

            if tag.has_attr('alt'):
                if bool(re.search(r'logo', tag['alt'], re.IGNORECASE)) == True:
                    return True

            return False


        # load the home-page
        ht = load_page(self.home_page)

        # get only the <a> and <img> tags from the home-page
        soup = BeautifulSoup(ht, features='lxml', parse_only=SoupStrainer(['img', 'a']))

        # attributes to be examined
        a = ['title', 'id', 'class']

        # for storing the URL of the logo
        t = None

        if t is None:
            # link to the home-page heuristic
            t = soup.find(img_to_hpage)

        if t is None:
            # 'src' and 'alt' are at the highest priority level
            t = soup.find(src_or_alt)



        if t is None:
            # searching for appropriate <img> tag with 'logo' keyword
            for key in a:
                t = soup.find('img', attrs={key : re.compile('logo', re.IGNORECASE)})
                if t is not None:
                    # appropriate <img> tag found
                    break

        if t is None:
            # searching for appropriate <img> tag with 'banner' keyword
            for key in a:
                t = soup.find('img', attrs={key : re.compile('banner', re.IGNORECASE)})
                # appropriate <img> tag found
                if t is not None:
                    break

        if t is None:
            # searching for appropriate <img> tag with 'header' keyword ------>   EXPERIMENTAL
            for key in a:
                t = soup.find('img', attrs={key : re.compile('header', re.IGNORECASE)})
                if t is not None:
                    # appropriate <img> tag found
                    break

        # 'image' keyword can also be tried but is too generous

        if t is None:
            # URL of the logo couldn't be found
            return None

        # else, URL of the logo found
        u = None

        if t.name == 'img':
            u = url_normalize(self.home_page, t['src'])
            if u is None:   # still None, some heuristics to be tried

                # some sites have 'data-src' attribute present instead
                if t.has_attr('data-src'):
                    u = url_normalize(self.home_page, t['data-src'])

        else:
            t = t.find('img')
            u = url_normalize(self.home_page, t['src'])

        if u is None:
            u = t['src']
            u = url_normalize(u, u)    # normalizing 'u' just in case it contains some control characters

        # print(u)
        # print("Logo Found")
        return u



    def __get_from_table(self, tag, cur_url):
        if tag is None:
            return

        for row in tag.find_all('tr'):       # examining every row
            a = row.find('a')

            if a is None or a.has_attr('href') == False:
                continue

            link = url_normalize(cur_url, a['href'])
            if link is None:
                continue

            ht = load_page(link)
            res_headers = ht.info()
            l_modified = res_headers.get_all('last-modified')

            if self.check_for_download(a['href']):  # good for downloading

                if cmp_date(l_modified, 120):  # recent document found -> save it
                    name = a.stripped_strings.replace('/', ' ')  # substituting '/' with ' '
                    with open(name, "wb") as fi:  # any type of file (simple text or binary) saved through 'wb' mode
                        fi.write(ht.read())

            else:     # not good for downloading -> some link to other page or other thing
                with open('additional_links', 'a') as fi:          # last-modified not checked - assuming it won't be very useful in this case (REVIEW LATER)
                    fi.write(name+' ')
                    fi.write(link+'\n')




    def __get_from_form(self, tag, cur_url):
        if tag is None:
            return
        pass

    def download_data(self, url):
        soup = BeautifulSoup(load_page(url), features='lxml')

        tag=None
        tag = soup.find('table')   # searching for <table> tag
        self.__get_from_table(tag, url)

        tag = None
        tag = soup.find('form')      # searching for <form> tag
        self.__get_from_form(tag, url)

                                    # check_for_download only checks on the basis of the url ; 'content-type' header should also be used


    def check_for_download(self, s):    # if the file can be downloaded (image, pdf, doc, sheet, etc.)

                                        # checking the complete 'href' attribute
        a = mimetypes.guess_type(s)
        a = a[0]

        if a is not None:
            if a.startswith('application/'):
                appli = ['pdf', 'csv', 'json', 'msword', 'vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'vnd.ms-excel', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         'vnd.oasis.opendocument.text', 'vnd.oasis.opendocument.presentation', 'vnd.oasis.opendocument.spreadsheet']
                # types = [.pdf .csv .json .doc .docx .xls .xlsx .odt .odp .ods ]

                if a[12:] in appli:
                    return True

            if a == 'text/plain':
                return True

            if a.startswith('image'):
                return True
                                # checking the path part of the 'href' attribute
        s = up.urlparse(s)
        s = s[2]

        if s == '':
            return False

        a = mimetypes.guess_type(s)
        a = a[0]

        if a is None:
            return False

        if a.startswith('application/'):
            appli = ['pdf', 'csv', 'json', 'msword', 'vnd.openxmlformats-officedocument.wordprocessingml.document',
                     'vnd.ms-excel', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     'vnd.oasis.opendocument.text', 'vnd.oasis.opendocument.presentation',
                     'vnd.oasis.opendocument.spreadsheet']
            # types = [.pdf .csv .json .doc .docx .xls .xlsx .odt .odp .ods ]

            if a[12:] in appli:
                return True

        if a == 'text/plain':
            return True

        if a.startswith('image'):
            return True

        return False






if __name__ == '__main__':

    # a = input("Enter URL address: ")
    # b = float(input("Input delay: "))
    url = 'http://www.macet.net.in/'

    web = Data(url)


    print(web.get_logo())


    # print("\nNo. of URLs =", len(web.urls))
    # print("No. of pages examined =", web.counter)
    #
    # s, p = get_filters()
    #
    # web.get_tsites(s, p)
    #
    # for i in web.tsites:
    #     print(i)


