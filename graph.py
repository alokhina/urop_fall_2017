import re
import scr_parser

class MovieScript:

    def __init__(self, filename):

        self.title = "title"
        self.characters = []
       ## self.frames
        self.interactions = []


    def analyze(self):
        scr_parser.parse()
        scenes = scr_parser.divide_into_scenes()
        set_characters = scr_parser.get_characters()
        number_of_scenes = 0

        for scene in scenes:
            number_of_scenes += 1
            phrases = scr_parser.create_phrases(scene)
            characters_in_scene = set()
            for phrase in phrases:
                characters_in_scene.add(phrase[0])
            ##print (number_of_scenes, characters_in_scene)
            for character1 in characters_in_scene:
                for character2 in characters_in_scene:
                    if character1 != character2:
                        scene_str = "#"+str(number_of_scenes)
                        ##dialogue_str = "dialogue #"+scene(3
                        self.interactions.append((character1, character2, "same scene",  scene_str ))

            for char_phrase in phrases:
                print(char_phrase)
                phrase = char_phrase[1]
                character1 = char_phrase[0]
                scene_str = "scene #"+str(number_of_scenes)+" dial #" + str(char_phrase[2])
                for character2 in set_characters:
                    print(character1, character2)
                    if scr_parser.isMentioned(phrase, character2):
                        self.interactions.append((character1, character2, "mentioned", scene_str))







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



movie = MovieScript("filename")
movie.analyze()
print(movie.interactions)