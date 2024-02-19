# Dissertation
 
python -m unittest discover "tests" # Runs all tests
python -m unittest tests.file # Runs all tests in a file

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
For a material to fulfil a variable the material must have any of the tags that are present in the variable

A diagram of the internal structure of queries can be found through the link below 
https://www.dropbox.com/scl/fi/9bnmcf39bvghb72mj0r0r/QueryStructure.PNG?rlkey=62es2ih12hf2fspazw8a57nsx&dl=0
