import xml.etree.ElementTree as ET #Element Tree XML parsing library
import re #Regex library
import yaml
from collections import OrderedDict
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import os

# @params
#   root: root of an ElementTree
#   columns: empty array to store column names
# Fills the columns array with column names
def dfs(root, columns):
    if list(root) == []:
        columns.append(root)
    for child in list(root):
        dfs(child, columns)

# @param root: root of the tree
# Outputs the node containing the 'instance' tag which is the start of the data form
def findInstanceTag(root):
    results = []
    if ('instance' in root.tag):
        return root
    for child in list(root):
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


#Parses through a single XML file
def xmlParse(fileName):
    inputFile = fileName #insert xml file name
    parser = ET.parse(inputFile) #initialize the ElementTree parser
    root = parser.getroot() #Find the root of the tree, the <html> tag
    form = findInstanceTag(root) #find the instances tag - this is the start of the data
    columns = [] #initialize empty array to store the column names
    dfs(form, columns) #extract column names with DFS
    return cleanColumnNames(columns) #clean the columns and return

#Generates YAML through a single XML file
def yaml_creator(filename, path = "../xml-files/", destination="../yaml-files/"):   
    assert '.xml' in filename[-4:]
    if os.getcwd()[-7:] != "scripts":
        path = "xml-files"
    parsed_fields = xmlParse(path + filename)
    
    #pairs = [(field, {'constraints': None, 'distribution': None, 'type': None}) for field in parsed_fields]
    keyvalue_pairs = {}
    for field in parsed_fields:
        keyvalue_pairs[field] = {'constraints': None, 'distribution': None, 'type': None}
    output = yaml.dump(keyvalue_pairs, explicit_start=True, default_flow_style=False, sort_keys=False)
    output = "\n".join(output.split("\n",2)[1:])
    
    try:
        file_test = open(destination + filename[:-4] + ".yaml", "r") # attempt to read the directory first
    
    except FileNotFoundError: # if there is no file with the given filename, then proceed
        file_object = open(destination + filename[:-4] + ".yaml", "w+") # w+ means read and write
        file_object.write("---\nrows:\n")
        file_object.write(output) # write to file
        file_object.close() # close file
        return

    file_test.close() # if we get here, there was already a file
    raise MemoryError(path + 'File ' + filename[:-4] + '''.yaml already exists in the current working directory. To avoid overwriting, aborting process.''')

def dirIterator(directory = "../xml-files"):
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            yaml_creator(filename)
        else:
            continue

if __name__ == '__main__':
    #print(xmlParse('../xml-files/delivery.xml'))
    #print(xmlParse('../xml-files/death_report.xml'))
    dirIterator()
