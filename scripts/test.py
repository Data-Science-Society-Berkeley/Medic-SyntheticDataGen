# import xml.etree.ElementTree as ET #Element Tree XML parsing library
# import re #Regex library
# import yaml
# from collections import OrderedDict
# from yaml import load, dump
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper

# @params
#   root: root of an ElementTree
#   columns: empty array to store column names
# Fills the columns array with column names
def dfs(root, columns):
    if root.getchildren() == []:
        columns.append(root)
    for child in root.getchildren():
        dfs(child, columns)

# @param root: root of the tree
# Outputs the node containing the 'instance' tag which is the start of the data form
def findInstanceTag(root):
    results = []
    if ('instance' in root.tag):
        return root
    for child in root.getchildren():
        tagElement = root.find(child.tag)
        results.append(findInstanceTag(tagElement))
        for node in results:
            if node is not None:
                return node
    
# @param columns: array of column names
# Outputs a new array of column names stripped of their xmlns tags 
def cleanColumnNames(columns):
    xmlns_re = "({.+})"
    cleaned_columns = [re.sub(xmlns_re, '', name.tag) for name in columns]
    return cleaned_columns

def xmlParse(fileName):
    inputFile = fileName #insert xml file name
    parser = ET.parse(inputFile) #initialize the ElementTree parser
    root = parser.getroot() #Find the root of the tree, the <html> tag
    form = findInstanceTag(root) #find the instances tag - this is the start of the data
    columns = [] #initialize empty array to store the column names
    dfs(form, columns) #extract column names with DFS
    return cleanColumnNames(columns) #clean the columns and return

if __name__ == '__main__':
    print(xmlParse('../xml-files/death_report.xml'))
