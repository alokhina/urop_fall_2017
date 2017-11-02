import re

class MovieScript:

    def __init__(self, filename):

        self.title = "title"
        self.characters = []
        self.frames
        self.characters
        self.interactions


    def pprint(self):
        print (self.characters)

    def parse(self, filename):

        def clearLine(line):
            line.replace(" ", "")

        def lineType(line):
            if line == "":
                return "E"
            if line[0] == "(" or line[0:3]=="INT." or line[0:3] == "EXT.":
                return "M"
            line1 = line
            if line1.upper() == line and line1.replace("\\s+", " ") == line:
                return "N"
            return "D"

        file_in = open("ex_in.txt", "r")
        file_out = open("ex_out.txt", "w")

        while (line != ""):
            line = (file.readline())
            line = clearLine(line)

            type = lineType(line)

            file_out.write(type + "  |||  " + line)

        file_out.close()
        file_in.close()


    class Frame:
        def __init__(self):
            self.time = 0
            self.type = "type"






class GraphOfInteractions:

    def __init__ (self):
        characters = []
        interactions = []



    class Character:

        def __init__ (self, name):
            self.name = name
            self.interactions = []




