import unittest
from importlib.machinery import SourceFileLoader
# Importing Index
IndexModule = SourceFileLoader("Index", "./Index.py").load_module()
Index = IndexModule.Index
# Importing XmlHandler
XmlHandler = SourceFileLoader(Index.xmlHandler["filename"], Index.xmlHandler["path"])

class TestParseXmlFiles(unittest.TestCase):

    def parseSingleXml():
        ...

    def parseMultipleXml():
        ...

    def parseSingleXmlWithDuplicates():
        ...

    def parseMultipleXmlWithDuplicates():
        ...
        
    def parseSingleEmptyXml():
        ...

    def parseXmlWithNoExistDep():
        ...
    
