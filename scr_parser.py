import re

def delete_whitespaces(line):
    i=0
    if line == "":
        return line
    clear_line = line
    while clear_line[0] == ' ' or clear_line[0] == '\n':

        clear_line = clear_line[1:]
        if len(clear_line) == 0:
            return ""

    i = len(clear_line)-1
    while clear_line[i] == ' ' or clear_line[i] == '\n':
        clear_line = clear_line[0:i]
        if len(clear_line) == 0:
            return ""
        i -= 1
    return clear_line



def delete_whitespaces_and_punctuation_marks(line):
    i=0

    if line == "":
        return line
    clear_line = line
    while clear_line[0] == ' ':
        clear_line = clear_line[1:]
        if clear_line == "":
            return line

    i = len(clear_line)-1
    while clear_line[i] == ' ' or clear_line[i] == '\n' or clear_line[i] == '.' or clear_line[i] == '!' or clear_line[i] == '\r' and clear_line[i] == '\t':
        clear_line = clear_line[0:i]
        if clear_line == "":
            return line
        i -= 1
    if clear_line[-1] == ' ':
        clear_line = clear_line[:len(clear_line)-2]
    return clear_line




def isSubsrting(s, subs):
    for i in range(len(s) - len(subs)+1):
        if s[i: i+len(subs)] == subs:
            return True

    return False


def parse():
    originalLine = "     "

    def clearLine(line):
        newline = re.sub(r'\s+', ' ', line)
        if len(newline) == 0:
            return ""
        if newline[0] == ' ':
            newline = newline[1:]



        if len(newline) == 0:
            return ""
        if newline[-1] == ' ':
            newline = newline[0: -1]
        return (newline)

    def lineType(line, prevType):

        def isCharacterName():
            line1 = line
            line2 = delete_whitespaces(line)
            b0 = not line2[0].isdigit();
            b1 =  (line1.upper() == line and re.sub(r'\s*', '', line1) == line)
            b2 = isSubsrting(line, "(CONT\'D)")
            b6 = isSubsrting(line, "(CONT.)")
            b3 = isSubsrting(line, "(V.O.)")
            b4 = not isSubsrting(line, "CUT")
            b5 = line == line.upper()
            return b0 and (b1 or b2 or b3 or b6) and len(line)>2 and b4 and b5

        def isBetweenDialogue():
            line1 =  delete_whitespaces(line)
            return line1[0].isdigit() and line1[-1].isdigit()

        def isMetaData():
            line1 = line
            b1 = (line[0] == "(" or isSubsrting(line, "INT.") or isSubsrting(line, "EXT."))
            b2 = isSubsrting(line, ":")
            b3 = len(line) < 3
            b4 = prevType != "N"
            b5 = line.upper() == line
            b6 = isSubsrting(line, "FADE OUT")
            b7 = isSubsrting(line, "FADE INTO")
            return (b1 or b2 or b3 or b6 or b7) and b4 and b5

        def isDialogue():
            b1 = (prevType == "D") or (prevType == "C")
            b2 = line[0] == "\""
            return b1 or b2

        def isSceneDescription():
            b1 = line.upper() != line
            return (b1 and prevType=="E") or prevType == "N"

        if line is None:
            return "E"
        if line == "":
            return "E"

        if isCharacterName():
            return "C"

        if isBetweenDialogue():
            return "X"

        if isMetaData():
            return "M"

        if isDialogue():
            return "D"

        if isSceneDescription():
            return  "N"

        return "M"

    file_in = open("ex_in.txt", "r")
    file_out = open("ex_out.txt", "w")

    prevType = "X"

    while (originalLine != ""):
        originalLine = file_in.readline()
        clear = clearLine(originalLine)

        type = lineType(clear, prevType)
        ##if type == 'M':
        ##    number_of_M += 1
        ##    file_out.write(type+str(number_of_M) + "|||  " + clear + "\n")
        ##else:
        if type != "X":
            file_out.write(type + "  |||  " + clear+"\n")
            prevType = type

    file_out.close()
    file_in.close()



def divide_into_scenes():
    scenes = []
    file_in = open("ex_out.txt", "r")
    ##file_out = open("ex_.txt", "w")
    number_of_scenes = 0
    current_scene = ""
    line = " "
    while (line != ""):
        line = file_in.readline()
        if (len(line)>0  and line[0] == 'M'):
            if number_of_scenes>0:
                scenes.append(current_scene)
            current_scene = line
            number_of_scenes += 1
        else:
            current_scene += line
    return scenes

def create_phrases(scene):
    lines = scene.split('\n')
    curr_character = None
    curr_phrase = ""
    characters = set()
    characters_phrases = []
    number = 0
    name = None
    number_of_d = 0
    is_new_dialogue = 1
    for line in lines:
        if (len(line) > 0 and line[0] == 'C'):
            number += 1
            if name is not None:
                characters_phrases.append((name, curr_phrase, number_of_d))
            name = extract_name(line)
            curr_phrase = ""
            is_new_dialogue = 1
        elif (len(line) > 0):
            if line[0] == 'D':
                number_of_d += is_new_dialogue
                is_new_dialogue = 0
                curr_phrase += line[7:]
    if name is not None:
        characters_phrases.append((name, curr_phrase, number_of_d))
    return characters_phrases

def isMentioned(phrase, name):
    return isSubsrting(phrase.lower(), name.lower())


def extract_name(line):
    clear_line = delete_whitespaces_and_punctuation_marks(line[7:])
    i = 0
    while (i < len(clear_line) and clear_line[i] != '('):
        i += 1
    name = clear_line[0:i]
    return name



def get_characters():
    characters = set()
    file_in = open("ex_out.txt", "r")
    line = None
    while (line != ""):
        line = file_in.readline()
        delete_whitespaces(line)

        if (len(line)>4  and line[0] == 'C'):

            name = extract_name(line)
            if len(name)>0:
                if name[-1] == ' ':
                    name = name[:len(name)-1]
                characters.add(name.upper())
            ##print("###", name.upper())
    for c in characters:
        if c[-1] == ' ':
            print("FUCK")
    print(characters)
    return characters



parse()
get_characters()
scenes = divide_into_scenes()
arr = create_phrases(scenes[9])
