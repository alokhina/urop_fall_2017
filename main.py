import re

def delete_whitespaces(line):
    i=0
    if line == "":
        return line
    clear_line = line
    while clear_line[i] == ' ':
        clear_line = clear_line[1:]
        i += 1
    i = len(clear_line)-1
    while clear_line[i] == ' ':
        clear_line = clear_line[0:i]
        i -= 1
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
            b1 =  (line1.upper() == line and re.sub(r'\s*', '', line1) == line)
            b2 = isSubsrting(line, "(CONT\'D)")
            b3 = isSubsrting(line, "(V.O.)")
            return (b1 or b2 or b3) and len(line)>3

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

        if isMetaData():
            return "M"

        if isDialogue():
            return "D"

        if isSceneDescription():
            return  "N"

        return "C"

    file_in = open("ex_in.txt", "r")
    file_out = open("ex_out.txt", "w")

    prevType = "X"
    number_of_M = 0
    while (originalLine != ""):
        originalLine = file_in.readline()
        clear = clearLine(originalLine)

        type = lineType(clear, prevType)
        ##if type == 'M':
        ##    number_of_M += 1
        ##    file_out.write(type+str(number_of_M) + "|||  " + clear + "\n")
        ##else:
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

def create_communications(scene):
    lines = scene.split('\n')
    curr_character = None
    curr_phrase = None
    characters = set()
    characters_phrases = []
    number = 0
    name = None
    for line in lines:
        print(line)
        if (len(line) > 0 and line[0] == 'C'):
            number += 1
            if name is not None:
                characters_phrases.append((name, curr_phrase))
            name = delete_whitespaces(line[7:])
            curr_phrase = ""
        elif (len(line) > 0):
            if line[0] == 'D':
                curr_phrase += line[7:]
    characters_phrases.append((name, curr_phrase))


    return characters_phrases






parse()
scenes = divide_into_scenes()
arr = create_communications(scenes[9])
print(scenes[9])
print(arr)



