from tkinter import *

class Operation:
    """
    The UI for constructing an operation -> Packs to the left
    """

    def __init__(self, root):
        self.root = root
        self.frame = Frame(root) # Holds all operations
        self.widgetDict = {}

        self.initialiseButton("addMatButton","Add material",self.addMaterial)
        self.initialiseButton("addAndButton","Add AND",self.addAND)
        self.initialiseButton("addOrButton","Add OR",self.addOr)

        self.frame.pack(side="left")

    def destroy(self):
        """
        Destroys this operation and replaces it with a new empty one
        """

        self.clearLabels()
        self.frame.destroy()
        self.__init__(self.root) # Calls the objects constructor, effectivly resetting it
        
    def clearLabels(self):

        for widget in list(self.widgetDict.values()):
            widget.destroy()


    def initialiseButton(self, name, text : str, command):
        """
        Creates a button and packs it into the root
        """
        
        if self.widgetDict.get(name) is None:
            self.widgetDict[name] = Button(self.frame,text=text,command=lambda:command())
            self.widgetDict[name].pack()

    def initialiseEntry(self, name : str):
        """
        Create an entry using the inputed name
        """

        if self.widgetDict.get(name) is not None:
            del self.dict[name]
        self.widgetDict[name] = Entry(self.frame)
        self.widgetDict[name].pack()

    
    def initialiseLabel(self, name : str, text : str):
        """
        Creates a label using the inputed name and text
        """

        if self.widgetDict.get(name) is not None:
            del self.dict[name]
        self.widgetDict[name] = Label(self.frame, text=text)
        self.widgetDict[name].pack()


    def addMaterial(self):
        """
        Replaces widgets with an entry for a material
        """
        self.clearLabels()

        self.initialiseLabel("addMatLabel","Enter material name:")
        self.initialiseEntry("materialEntry")
        self.initialiseButton("deleteMaterial","Delete material",self.destroy)

    def addOr(self):
        """
        Replaces widgets with an OR operation 
        """
        self.clearLabels()
        self.widgetDict["ORLEFTBRACKET"] = Label(self.frame,text="(")
        self.widgetDict["ORLEFTBRACKET"].pack(side="left")
        self.widgetDict["ORLEFT"] = Operation(self.frame)
        
        self.widgetDict["ORLABELFRAME"] = Frame(self.frame)
        self.widgetDict["ORLABEL"] = Label(self.widgetDict["ORLABELFRAME"],text="OR")
        self.widgetDict["ORLABEL"].pack()
        self.widgetDict["ORDELETEBUTTON"] = Button(self.widgetDict["ORLABELFRAME"],text="Delete OR",command=lambda:self.destroy())
        self.widgetDict["ORDELETEBUTTON"].pack()
        self.widgetDict["ORLABELFRAME"].pack(side="left")

        self.widgetDict["ORRIGHT"] = Operation(self.frame)
        self.widgetDict["ORRIGHTBRACKET"] = Label(self.frame,text=")")
        self.widgetDict["ORRIGHTBRACKET"].pack(side="right")

    def addAND(self):
        """
        Replaces widgets with an AND operation
        """

        self.clearLabels()
        
        self.widgetDict["ANDLEFTBRACKET"] = Label(self.frame,text="(")
        self.widgetDict["ANDLEFTBRACKET"].pack(side="left")
        self.widgetDict["ANDLEFT"] = Operation(self.frame)
        
        self.widgetDict["ANDLABELFRAME"] = Frame(self.frame)
        self.widgetDict["ANDLABEL"] = Label(self.widgetDict["ANDLABELFRAME"],text="AND")
        self.widgetDict["ANDLABEL"].pack()
        self.widgetDict["ANDDELETEBUTTON"] = Button(self.widgetDict["ANDLABELFRAME"],text="Delete AND",command=lambda:self.destroy())
        self.widgetDict["ANDDELETEBUTTON"].pack()
        self.widgetDict["ANDLABELFRAME"].pack(side="left")

        self.widgetDict["ANDRIGHT"] = Operation(self.frame)
        self.widgetDict["ANDRIGHTBRACKET"] = Label(self.frame,text=")")
        self.widgetDict["ANDRIGHTBRACKET"].pack(side="right")
        
        