""" contains various utility functions related to URL parsing and processing """

from modules import *

# load the URL and return the opened page
def load_page(url, ref='https://www.google.com/'):

    # SSL certificate_verify_failed error to be resolved, happens SOMETIMES only

    # artificial header to look humanly
    headers={'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
             'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             'Connection':"keep-alive",
             'Referer': ref
             }

            # Accept header to be reviewed !!

    # text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8   ->  from FIREFOX
    # test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8  ->  googlebot

    req = ur.Request(url=url, headers=headers)

    # tries to open a page for at max 1 minute
    return ur.urlopen(req, timeout=60)



# function that normalizes a given URL and a given path
def url_normalize(cur_page, path):

    #cur_page=cur_page.strip() # may have spaces at the end, but not necessary now

    # remove trailing and leading spaces
    path = path.strip()

    # encode the path
    path = encode_url(path)

    # cur_page argument parsed into components
    a = list(up.urlparse(cur_page))
    # path argument parsed into components
    b = list(up.urlparse(path))


    if b[0] not in ['', 'http', 'https']:
        # some other scheme, like, mailto, javascript, etc., present
        return None


    if b[2] == '' and b[3] == '' and b[4] == '':      # b[1] to be checked???
        # if b[5]=='':    # Everything is empty; probably an internal link to the same page
        #     return None
        # else:           # Some internal link; may reveal something new
        #     a[5]=b[5]
        #     return up.urlunparse(a)

        # internal link with complete path name (to the same page) to be excluded
        return None


    if b[1] != '' and b[1] != a[1]:   # sub-domain or external site
        # s1=extract_domain(a[1])
        # s2=extract_domain(b[1])
        #
        # if s1==s2:     #sub-domain
        #     if b[0]=='':
        #         b[0]='http://'
        #     return up.urlunparse(b)
        #
        # else:        #external site
        #     return None
        return None


    else:
        # link belonging to the same domain

        # set the scheme of 'a' in 'b' (they belong to the same domain)
        b[0] = a[0]

        if b[1] == a[1]:    # complete link already present
            if a[2] == b[2] and a[3] == b[3] and a[4] == b[4]:
                # all components same except possibly the last one -> internal link to the same page-IGNORE
                return None
            # a = up.urlunparse(a)
            # b = up.urlunparse(b)
            #
            # i, j = 0, 0
            # while i < len(a) and j < len(b):
            #     if a[i] == b[j]:
            #         i += 1
            #         j += 1
            #     else:
            #         break
            #
            # if j == len(b):
            #     return None
            # if b[j] == '#':
            #     return None
            # if j+1 == len(a):
            #     return None
            # if b[j+1] == '#':
            #     return None
            #
            # b = up.urlparse(b)

            return encode_url(up.urlunparse(b).strip())



        b[1] = a[1]

        if b[2] == '':      # path component is empty- other components may be present
            b[2] = a[2]
            return up.urlunparse(b)

        if b[2][0] == '/':
            # search in the 'root' directory
            if a[2] == b[2] and a[3] == b[3] and a[4] == b[4]:
                # all components same except possibly the last one
                return None

            return up.urlunparse(b)

        if a[2] != '' and a[2][-1] == '/':
            # removing the last '/' if present -> to be REVIEWED
            a[2] = a[2][:-1]

        # code for moving up the directory levels
        if b[2][:3] == '../' or b[2][:5] == './../':
            i = 0
            n = len(b[2])
            if b[2][:2] == './':
                i += 2

            a[2] = remove_fname(a[2])

            while i+2 <= n and b[2][i:i+2] == '..':
                a[2] = remove_fname(a[2])
                i += 3

            b[2] = '/' + b[2][i:]
            b[2] = a[2]+b[2]

            return up.urlunparse(b)


        if b[2][0:2] == './' or (b[2][0] not in ['/', '.']):
            # search in the same directory
            a[2] = remove_fname(a[2])

            if b[2][0] == '.':
                b[2] = b[2][1:]

            if b[2][0] != '/':
                b[2] = '/' + b[2]

            b[2] = a[2] + b[2]

            return up.urlunparse(b)

        # case not found
        print("**** From url_normalize() - CASE NOT FOUND ->", cur_page, path, file=sys.stderr)
        return None




# function to extract domain part
def extract_domain(s):

    i = len(s)-1

    while i >= 0 and s[i] != '.':
        i -= 1

    j = 0

    while j < i and s[j] != '.':
        j += 1

    if j == i or i == -1:
        return s

    else:
        return s[j+1:]


# function that removes 'filename' from the string
def remove_fname(s):
    if s == '':
        return ''

    i = len(s)-1

    # search for the index of last occurrence of '/'
    while i >= 0 and s[i] != '/':
        i -= 1

    if i == -1:
        # '/' not present in argument s
        return ''

    else:
        # return the string after removing last '/' and following substring
        return s[:i]



def encode_url(s):
    res = ''
    for i in s:

        if i == '\\':   # encoding \ character (used in some Windows servers)
            res = res + '/'

        # elif i == ' ':      # encoding the space character
        #     res = res + '%20'

        # elif i == '\u2019':   # encoding the character (’) (decimal value 146; escape sequence \u2019)
        #     res = res + '%E2%80%99'

        elif i in ('\t', '\v', '\f', '\r', '\0', '\n', '\b'):
            # do nothing - just skip the character which is in the form of escape sequence
            pass

        else:
            res = res + i

    res = up.quote(res, safe='`~!@#$%^&*()-_=+[]{};:\'\"\\|,./<>?*')

    return res



def cmp_date(l_modified, days_passed=-1):

    if l_modified is None:
        return False

    if days_passed == -1:
        return True

    a = date.today()

    l_modified = list(l_modified[0].split(' '))
    month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

    b = date(int(l_modified[3]), int(month[l_modified[2]]), int(l_modified[1]))

    if (a-b).days <= days_passed:
        return True

    return False



# function to return the filters required to get the target URLs
def get_filters():
    s = []      # positive filter list
    p = []      # negative filter list

    s.append('vacanc')
    s.append('job')
    s.append('career')
    s.append('opportunit')
    # s.append('notice')         # Very generous filter
    # s.append('announcement')
    s.append('recruit(?!er)')
    s.append('[^a-zA-Z]position')
    # s.append('role')     # dangerous
    s.append('walk(%20)?(-)?(%20)?in')
    s.append('interview')

    p.append('result')
    p.append('select(ed|ion)')
    p.append('tender')

    return (s, p)



if __name__ == '__main__':

    print(url_normalize('http://www.marywardkinder.in/path', 'http://www.marywardkinder.in/path/#comment'))
    print()

