# Dissertation
 
python3 -m unittest discover "tests" # Runs all tests
python3 -m unittest tests.file # Runs all tests in a file

--- DEMO FILE ---
A demo file called Demo.py can be run using the command "python ./Demo.py" whilst in the Dissertation directory

This files uses a set of materials found in the folder "TestMaterial/MathsAndPhysics/MathsAndPhys1.xml"

A diagram of the materials, their attributes and relationships can be found through the link below
https://www.dropbox.com/scl/fi/6mwx8lxcbutlfiil2soyr/DemoMats.PNG?rlkey=8d6rdjgyf422xaggnu0hr7hmd&dl=0

The file creates several queries and runs them on the set of material to demonstrate how queries are constructed and executed on a material

--- QUERIES ---
The function queryDependencies is used to select a materials dependencies based on a query that can be constructed. A query is composed of a set of clauses which are in turn
composed of a set of variables and a set of dependencies. 
For a query to select a material the material must fulfil any of the clauses in the query
For a material to fulfil a clause the material must fulfil all of the variables in the clause and also be linked by the dependency specified in the clause
For a material to fulfil a variable the material must have any of the tags that are present in the variables

A diagram of the internal structure of queries can be found through the link below 
https://www.dropbox.com/scl/fi/9bnmcf39bvghb72mj0r0r/QueryStructure.PNG?rlkey=62es2ih12hf2fspazw8a57nsx&dl=0

To set up a query you need to create a query object and a clause object. You use the method addVariable to add a variable to a clause (A list of strings) and the method addDependencyLevel to add a dependency to a clause. 
After creating one or more clause you use the addClause method on the Query and pass it the queries you want to add.
Then you can call the function queryDependencies and pass it one or more materials and the query it will find the dependencies of the materials passed to it.

You can also use queries with the function searchMaterials. This function takes a set of materials and a query then finds all materials that fulfil the query (it does not take into account dependency levels, it can be used to do things like select all workshops in the set of materials passed to it)


--- XML FILE ---
XML Files can be written to represent a set of materials and show their characteristics and dependencies. There is an XSD file in the directory "TestMaterial/schema.xsd" showing the layout of one of these files, as well as several example files containing sets of material e.g. MathsAndPhys1.xml. The XmlHandler.py file will be able to import these files so a program can query an imported set of material. At the time of writing this readme an XML must be written with its attributes in a certain order or the XmlHandler module will not be able to read it properly, I will change this eventually but it is not the top of my priority list.

--- TESTS ---
There are a large set of tests in the path "TestMaterial/tests/" that I have written using unittest and can be run with the command 'python -m unittest discover "tests"'. As of the writing of this readme all tests should be successful.