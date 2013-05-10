import string

# Functions adapted from ProgrammingHistorian (updated to Python3)
# http://niche.uwo.ca/programming-historian/index.php/Tag_clouds

# Take one long string of words and put them in an HTML box.
# If desired, width, background color & border can be changed in the function
# This function stuffs the "body" string into the the HTML formatting string.
def make_HTML_box(body):
    box_str = """<div style=\"
    width: 560px;
    background-color: rgb(250,250,250);
    border: 1px grey solid;
    text-align: center\" >{:s}</div>
    """
    return box_str.format(body)

def make_HTML_word(word,cnt,high,low):
    ''' make a word with a font size to be placed in the box. Font size is scaled
    between htmlBig and htmlLittle (to be user set). high and low represent the high 
    and low counts in the document. cnt is the cnt of the word 
    '''
    htmlBig = 96
    htmlLittle = 14
    ratio = (cnt-low)/float(high-low)
    fontsize = htmlBig*ratio + (1-ratio)*htmlLittle
    fontsize = int(fontsize)
    word_str = '<span style=\"font-size:{:s}px;\">{:s}</span>'
    return word_str.format(str(fontsize), word)

def print_HTML_file(body,title):
    ''' create a standard html page with titles, header etc.
    and add the body (an html box) to that page. File created is title+'.html'
    '''
    fd = open(title+'.html','w')
    theStr="""
    <html> <head>
    <title>"""+title+"""</title>
    </head>

    <body>
    <h1>"""+title+'</h1>'+'\n'+body+'\n'+"""<hr>
    </body> </html>
    """
    fd.write(theStr)
    fd.close()

def clean_str(aStr):
    aStr = aStr.strip()
    aStr = aStr.lower()
    for char in aStr:
        if char in string.punctuation:
            aStr = aStr.replace(char,'')
    return aStr

def extract_top_x(theDict,num):
    lst = [(value,key) for key,value in theDict.items()]
    lst.sort()
    lst = lst[-num:]
    lst = [(word,cnt) for cnt,word in lst]
    return lst

def print_frequency(my_dict,num,name):
    #pairs_list = [(value,key) for key,value in my_dict.items()]
    pairs_list = []
    for key,value in my_dict.items():
        pairs_list.append((value,key))
    print()
    print( '+'*12)
    print( name, ': words in frequency order as count:word pairs')
    pairs_list.sort(reverse=True)
    pairs_list = pairs_list[:num+1]
    print_cols = 0
    for cnt,word in pairs_list:
        print ('{:3d}:{:<13s}'.format(cnt,word),end = ' ')
        if print_cols == 3:
            print()
            print_cols = 0
        else:
            print_cols += 1

def display(D,name):
    l=extract_top_x(D,40)
    print_frequency(D,40,name)
    least = l[0][1]
    most =l[-1][1]
    l.sort()
    body = [make_HTML_word(w,cnt,most,least) for w,cnt in l]
    body=' '.join(body)
    body = make_HTML_box(body)
    print_HTML_file(body,name)

def parse_file(gregDict):
    fd = open('stopWords.txt')
    stopList = [line.strip() for line in fd]
    fd.close()
    
    fd = open('greg.txt')
    
    for line in fd:
        
        #skip lines not written by greg
        if line[0] == ">":
            continue
        
        fields = line.strip().split()
        if not fields:
            continue

        for f in fields:
            f = clean_str(f)
            if f not in stopList and f:
                    gregList.append(f)
                    try:
                        gregDict[f]+=1
                    except KeyError:
                        gregDict[f]=1
    fd.close()


gregDict={}

gregList=[]

parse_file(gregDict)

print(gregList[:100])

display(gregDict,'Gregory')

f_out = open('out.txt','w')
for item in gregList:
    f_out.write(item + ", ")
f_out.close()

print(len(gregList))



