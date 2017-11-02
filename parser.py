class Movies:
    def __init__(self, year, name, country, character):
        self.year = year
        self.name = name
        self.country = country
        self.character= character

    def getName(self):
        return self.name

    def getYear(self):
        return self.year

    def getCharacter(self):
        return self.character

    def getCountry(self):
        return self.country


file = open("list.txt", "r")

all_movies = []


year ="begin"

while (year != ""):

    year=(file.readline())
    if  (year != "" and (ord(year[0]) >= ord('0') and  ord(year[0]) <= ord('9') )) :

        name = (file.readline())
        country = (file.readline())
        character = (file.readline())
        all_movies.append(Movies(year, name, country, character))


print(all_movies[12].getCountry())

