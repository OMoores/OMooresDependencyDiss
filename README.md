# Dissertation
 
-- REQUIREMENTS --
To run this project the following are needed:
Python 3.10.0 -> Download: https://www.python.org/downloads/release/python-3100/
Z3 solver -> pip install z3-solver
numpy -> pip install numpy

-- RECOMMEND ORDER --
The recommend order feature allows the set of selected material to be ordered. 
For it to work effectivly the user must create a hierarchy of relationships and resolvers can be added to decide how OR clauses are handled.

-- QUERIES --
A query is composed of a set of clauses which are in turn
composed of a set of variables and a set of dependencies. 
For a query to select a material the material must fulfil any of the clauses in the query
For a material to fulfil a clause the material must fulfil all of the variables in the clause and also be linked by the dependency specified in the clause
For a material to fulfil a variable the material must have any of the tags that are present in the variables.

A diagram of the internal structure of queries can be found through the link below 
https://www.dropbox.com/scl/fi/9bnmcf39bvghb72mj0r0r/QueryStructure.PNG?rlkey=62es2ih12hf2fspazw8a57nsx&dl=0

The query dependency page can be used to create queries and execute them on any set of material that has been imported.

-- RESOLVERS --
When using a query or the recommend order functionality there are boxes that allow you to add resolvers. These dicate how OR clauses are treated. If no resolvers are input then OR clauses are treated like 2 sets of dependencies and both will be returned.
If a resolver is input it will check to see if either of the clauses use the tags or names of the resolvers input. If one does but not the other the one that uses resolvers will be returned, if both do the one with the first unique resolver in the resolver list will be returned. e.g. requires A OR B. If the resolvers [isLetter,isA,isB] are used A will be the side returned. A and B are letters so the resolver is not unique to either side, the next resolver isA only applies to A.


--- XML FILE ---
XML Files can be written to represent a set of materials and show their characteristics and dependencies. There is an XSD file in the directory "TestMaterial/schema.xsd" showing the layout of one of these files, as well as several example files containing sets of material e.g. MathsAndPhys1.xml. The XmlHandler.py file will be able to import these files so a program can query an imported set of material.
The material creator in the tool can be used to create basic material files.

The structure of an XML file is as follows:
<materials> # The root tag
    <material> # Each material is in one of these tags
        <fileName></fileName>
        <tags>
            <tag></tag> Each characteristic goes in one of these
        </tags>
        <dependencies>
            <relationship> # Each relationship can have whatever name the user deciedes
                <OR> # An Or clause, must have 2 materials or other clauses
                    <material>materialName</material> 
                    <material>material2Name</material>
                </OR>
            </relationship>
            <relationship2>
                <AND> # And clauses, created to be used in OR clauses, must have 2 materials or other clauses
                    <material>materialName</material> 
                    <material>material2Name</material>
                </AND>
            </relationship2>
            <relationship>
               <material>material2Name</material>
            </relationship>
        </dependencies>
    </material>
</materials>

--- TESTS ---
There are a large set of tests in the path "TestMaterial/tests/" that I have written using unittest and can be run with the command 'python -m unittest discover "tests"'. As of the writing of this readme all tests should be successful.

python -m unittest discover "tests" # Runs all tests
python -m unittest tests.file # Runs all tests in a file