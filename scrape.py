from bs4 import BeautifulSoup as BS
import requests
from builtins import type
from bs4.element import NavigableString
from bs4.element import Tag

replace = {
    'a' : '"link"',
    'h3' : '"heading"',
    'p' : '"text"',
    'strong' : '"bold"',
    'h1': '"title"',
    'li': '"bullet"'
    #'div': 'CONTAINER'
}

class Scrape(object):
    """docstring for ClassName"""
    def __init__(self, URL, count):
        self.indent = 0
        self.outfile = open('out/url' + str(count) + '.txt', 'w')
        self.count = count
        self.URL = URL

    def Solve(self):
        print('scraping URL' + str(self.count) + ': ' + self.URL + '\n')
        scrape = self.URL.strip('\n')
        
        page = requests.get(scrape)
        soup = BS(page.content, "html.parser")    
            
        root = soup.find(id = 'region')

        try :
            self.write_tree_into_JSON(root)

        except Exception as ex:
            print(ex)
            file = open('errog.txt', 'a')
            file.write('error with URL ' + str(self.count) + '\n')
            file.close()

        self.outfile.close()
        return self.count + 1
        
    def ParseNavStr(self,elt):
        toConvert = str(elt.string)
        return str(toConvert.encode('ascii', 'replace').decode("utf-8"))

    def quoteWrap(self,str):
        return '"' + str + '"'

    def write_Indent(self,text):
        self.outfile.write('\t' * self.indent + text)

    def write_tree_into_JSON(self,node):
        #basecase: if no tag children just print and return, dont recurse

        recurseNeeded = False
        #first find out if leaf
        child_list = []
        for child in node.contents:
            if type(child) == Tag:
                child_list.append(child)

        if child_list: 
            recurseNeeded = True

        #now we can check if we hit base case or not
        if not recurseNeeded:
            #just iterate thru and print text
            for child in node.contents:
                parsed = self.ParseNavStr(child)
                self.outfile.write(parsed + '\n')

        #means we have tags to explore
        else:
            self.write_Indent('{\n')
            self.indent = self.indent + 1
            for child in child_list:
                tagType = child.name
                replaceString = ''
                if tagType in replace:
                    replaceString = replace[tagType] + ': '
                self.write_Indent(replaceString)
                self.write_tree_into_JSON(child)
            self.indent = self.indent - 1
            self.write_Indent('\n}')


    
        
        
    

if __name__ == '__main__':
    count = 0
    #clear error log
    file = open('errog.txt', 'w')
    file.write('')
    file.close()
    file = open('urls.txt','r')
    for URL in file:
        if count == 1: break
        '''if count != 17: 
            count = count + 1
            continue'''
        
        if URL == '\n': continue #in case '\n' at end of file
        scrape = Scrape(URL, count)
        count = scrape.Solve()