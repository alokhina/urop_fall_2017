import re
import scr_parser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def sum_polarity_scores(elements):
    pos = 0
    neu = 0
    neg = 0
    sum = 0
    for el in elements:
        if len(el.polarity_scores) == 0:
            continue
        print(str(el), el.polarity_scores)
        pos += el.polarity_scores['pos']
        neu += el.polarity_scores['neu']
        neg += el.polarity_scores['neg']
        sum += el.polarity_scores['pos'] + el.polarity_scores['neu'] + el.polarity_scores['neg']
    if (sum == 0):
        return {}
    pos = (pos + .0) / sum
    neu = (neu + .0) / sum
    neg = (neg + .0) / sum
    d = {'pos': pos, 'neu' : neu, 'neg' : neg}
    return d



class MovieScript:
    class Time:
        def __init__(self, scene_number, phrase_number = 0, sentence_number = 0):
            self.scene_number    = scene_number
            self.phrase_number   = phrase_number
            self.sentence_number = sentence_number

    class Sentence:
        def __init__(self, text):
            self.text = text
            self.words = nltk.tokenize.word_tokenize(text)
            self.tagged_words = nltk.pos_tag(self.words)
            sid = SentimentIntensityAnalyzer()
            self.polarity_scores = sid.polarity_scores(self.text)
            self.pos = self.polarity_scores['pos']
            self.neg = self.polarity_scores['neg']
            self.neu = self.polarity_scores['neu']

        def __str__(self):
            return self.text ##+"\nAnalysis: "+str(self.polarity_scores)

    class Phrase:
        def __init__(self, phrase, character, scene_number, dialogue_number):
            self.character = character
            self.text = phrase
            self.sentences = []
            self.mentioned_characters = []
            self.scene_number = scene_number
            self.dialogue_number = dialogue_number
            self.polarity_scores = {}

        def __str__(self):
            r = self.character + ": " + self.text+"\nSENTENCES:\n"
            for s in self.sentences:
                r += str(s) +"\n"
            return r

        def analyse(self, set_of_characters, graph):
            split_regex = re.compile(r'[.|!|?]')
            sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(self.text)])
            for s in sentences:
                self.sentences.append(MovieScript.Sentence(s))
            self.polarity_scores = sum_polarity_scores(self.sentences)
            for character2 in set_of_characters:
                if scr_parser.isMentioned(self.text, character2):
                    self.mentioned_characters.append(character2)
                    graph.add(Mentioning(self.character, character2, self))

    class Scene:
        def __init__(self, text, number):
            self.characters_set = set()
            self.phrases = []
            self.text = text
            self.dialogues = []
            self.scene_number = number
            self.polarity_scores = {}
            self.metadata = []

        def __str__(self):
            if (len(self.characters_set) == 0):
                return "SCENE #" + str(self.scene_number) + " has no characters\n"
            result = "________________________\n"
            result += "SCENE #" + str(self.scene_number) + "\n\n"
            result += "CHARACTERS IN SCENE:\n"
            result += str(self.characters_set)
            result += "\n"
            for p in self.phrases:
                if len(p.mentioned_characters) > 0:
                    result += p.character + " mentions " + str(p.mentioned_characters) + ":\n"
                    result += ">>>  " + p.text + "  <<<\n"

            result += "\n"
            result += "DIALOGUES IN SCENE:\n"
            for d in self.dialogues:
                result += "****"
                for p in d:
                    result += str(p)
                    result += "\n"
            result += "________________________\n"
            return result

        def analyse(self, set_of_characters, graph):
            characters_phrases = scr_parser.create_phrases(self.text)

            for phrase in characters_phrases:
                self.characters_set.add(phrase[0])
                curr_phrase = MovieScript.Phrase(phrase[1], phrase[0], self.scene_number, phrase[2])
                curr_phrase.analyse(set_of_characters, graph)
                self.phrases.append(curr_phrase)
            self.find_dialogues()

            for c1 in self.characters_set:
                for c2 in self.characters_set:
                    if c1 != c2:
                        graph.add(SameScene(c1, c2, self))

            self.polarity_scores = sum_polarity_scores(self.phrases)

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
                    current_length += 1


                else:
                    if next_character_phrase.character == previous_character_phrase.character:
                        current_dialogue.append(phrase)
                        current_length += 1
                    else:
                        if current_length >= length_of_dialogue:
                            self.dialogues.append(current_dialogue)
                        current_dialogue = [previous_character_phrase, current_character_phrase]
                        current_length = 2
                    previous_character_phrase = current_character_phrase
                    current_character_phrase = next_character_phrase
            if current_length >= length_of_dialogue:
                self.dialogues.append(current_dialogue)

    def __init__(self, filename):
        self.title = "title"
        self.characters = []
        self.interactions = []
        self.scenes = []
        self.graph = None

    def analyze(self):
        scr_parser.parse()
        scenes = scr_parser.divide_into_scenes()
        set_characters = scr_parser.get_characters()
        self.graph = GraphOfInteractions(set_characters)

        number_of_scenes = 0

        for scene_text in scenes:
            number_of_scenes += 1
            current_scene = MovieScript.Scene(scene_text, number_of_scenes)
            current_scene.analyse(set_characters, self.graph)
            self.scenes.append(current_scene)
            #print(str(current_scene))

    #def pprint(self):
        #print(self.characters)

    def parse(self, filename):

        def clearLine(line):
            line.replace(" ", "")

        def lineType(line):
            if line == "":
                return "E"
            if line[0] == "(" or line[0:3] == "INT." or line[0:3] == "EXT.":
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



class Interaction(object):
    def __init__(self, c1, c2):
        self.polarity_scores = {}
        self.c1 = 0
        self.c2 = 0
        self.symmetry = None

class Dialogue(Interaction):
    def __init__(self, c1, c2, phrases):
        super(Dialogue, self).__init__(c1, c2)
        self.phrases = phrases
        self.symmetry = True
        self.polarity_scores = sum_polarity_scores(phrases)

class SameScene(Interaction):
    def __init__(self, c1, c2, scene):
        super(SameScene, self).__init__(c1, c2)
        self.scene = scene
        self.symmetry = True
        self.polarity_scores = scene.polarity_scores

class Mentioning(Interaction):
    def __init__(self, c1, c2, phrase):
        super(Mentioning, self).__init__(c1, c2)
        self.phrase = phrase
        self.symmetry = False
        self.polarity_scores = phrase.polarity_scores

class GraphOfInteractions:
    def __init__(self, characters):
        self.characters = characters
        self.relationships = {}
        for c1 in characters:
            for c2 in characters:
                if c1 != c2:
                    self.relationships[(c1, c2)] = []

    def add(self, interaction):
        if interaction.c1 == interaction.c2:
            return
        self.relationships[(interaction.c1, interaction.c2)].append(interaction)
        self.relationships[(interaction.c2, interaction.c1)].append(interaction)


movie = MovieScript("filename")
movie.analyze()
#print(movie.graph.interactions)
