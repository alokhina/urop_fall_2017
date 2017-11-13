import re
import scr_parser

class MovieScript:

    class Phrase:
        def __init__(self, phrase, character, scene_number, dialogue_number):
            self.character = character
            self.text = phrase
            self.mentioned_characters = []
            self.negative_words = {}
            self.positive_words = {}
            self.scene_number = scene_number
            self.dialogue_number = dialogue_number

        def __str__(self):
            return (self.character + ": " + self.text)

        def analyse(self, set_of_characters):
            ##print(set_of_characters)
            for character in set_of_characters:
                if scr_parser.isMentioned(self.text, character):
                    self.mentioned_characters.append(character)
            ##print(">>>>")
            ##print(self.character)
            ##print(self.text)
            ##print(self.mentioned_characters)
            ##print("<<<<")
            ##all features

    class Dialogue:
        def __init__(self, ):
            self.character1 = "SOMEONE"
            self.character2 = "SOMEONE ELSE"
            self.positive_words_char1 = []
            self.positive_words_char2 = []
            self.negative_words_char1 = []
            self.negative_words_char2 = []
            self.behaviour_of_char1
            self.behaviour_of_char2

    class Scene:
        def __init__(self, text, number):
            self.characters_set = set()
            self.characters_list = []
            self.phrases = []
            self.text = text
            self.dialogues = []
            self.negative_words = {}
            self.positive_words = {}
            self.scene_number = number

        def __str__(self):
            if (len(self.characters_set) == 0):
                return "SCENE #"+str(self.scene_number)+" has no characters\n"
            result  = "________________________\n"
            result += "SCENE #"+str(self.scene_number)+"\n\n"
            result += "CHARACTERS IN SCENE:\n"
            result += str(self.characters_set)
            result += "\n"
            for p in self.phrases:
                if len(p.mentioned_characters) >0:
                    result += p.character + " mentions " + str(p.mentioned_characters)+":\n"
                    result += ">>>  " + p.text +"  <<<\n"

            result += "\n"
            result += "DIALOGUES IN SCENE:\n"
            for d in self.dialogues:
                result += "****"
                for p in d:
                    result += str(p)
                    result += "\n"
            result += "________________________\n"
            return result


        def analyse(self, set_of_characters):
            characters_phrases = scr_parser.create_phrases(self.text)
            for phrase in characters_phrases:
                self.characters_list.append(phrase[0])
                self.characters_set.add(phrase[0])
                curr_phrase = MovieScript.Phrase(phrase[1], phrase[0], self.scene_number, phrase[2])
                curr_phrase.analyse(set_of_characters)
                self.phrases.append(curr_phrase)
            self.find_dialogues()
            ##print('####', self.scene_number, self.characters_set)


        def find_dialogues(self):
            length_of_dialogue = 5

            previous_character_phrase = None
            current_character_phrase = None
            current_length = 0
            current_dialogue = []

            for phrase in self.phrases:

                if current_character_phrase is None:
                    current_character_phrase = phrase
                    current_length += 1
                    current_dialogue.append(phrase)
                    continue
                if previous_character_phrase is None:
                    previous_character_phrase = current_character_phrase
                    current_character_phrase = phrase
                    current_length += 1
                    current_dialogue.append(phrase)
                    continue

                next_character_phrase = phrase

                if next_character_phrase.character == current_character_phrase.character:
                    current_dialogue.append(phrase)
                    current_length +=1


                else:
                    if next_character_phrase.character == previous_character_phrase.character:
                        current_dialogue.append(phrase)
                        current_length += 1
                    else:
                        if current_length >= length_of_dialogue:
                            self.dialogues.append(current_dialogue)
                        current_dialogue = [previous_character_phrase, current_character_phrase]
                        current_length=2
                    previous_character_phrase = current_character_phrase
                    current_character_phrase = next_character_phrase
            if current_length >= length_of_dialogue:
                self.dialogues.append(current_dialogue)


    def __init__(self, filename):

        self.title = "title"
        self.characters = []
       ## self.frames
        self.interactions = []
        self.scenes = []


    def analyze(self):
        scr_parser.parse()
        scenes = scr_parser.divide_into_scenes()
        set_characters = scr_parser.get_characters()


        number_of_scenes = 0


        for scene_text in scenes:
            ##print("****************************************************************")
            ##print(scene)
            number_of_scenes += 1
            current_scene = MovieScript.Scene(scene_text, number_of_scenes)
            current_scene.analyse(set_characters)
            self.scenes.append(current_scene)
            print(str(current_scene))

            #phrases = scr_parser.create_phrases(scene)
            #characters_in_scene = set()

            # for phrase in phrases:
            #     characters_in_scene.add(phrase[0])
            # ##print (number_of_scenes, characters_in_scene)
            # for character1 in characters_in_scene:
            #     for character2 in characters_in_scene:
            #         if character1 != character2:
            #             scene_str = "#"+str(number_of_scenes)
            #             ##dialogue_str = "dialogue #"+scene(3
            #             self.interactions.append((character1, character2, "same scene",  scene_str ))
            #
            # for char_phrase in phrases:
            #     phrase = char_phrase[1]
            #     character1 = char_phrase[0]
            #     ##print(character1, phrase)
            #     scene_str = "scene #"+str(number_of_scenes)+" dial #" + str(char_phrase[2])
            #     for character2 in set_characters:
            #         if scr_parser.isMentioned(phrase, character2):
            #             self.interactions.append((character1, character2, "mentioned", scene_str))








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

