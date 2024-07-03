import pymongo


class Solver:
    def __init__(self):
        self.blacks = set({})
        self.yellows = {}
        self.greens = {}
        self.possible_words = {}
        self.black_and_greens = set({})
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["5_letter_words_with_frequency"]  
        self.collection = self.db["words"]  

        for document in self.collection.find():
            word = document.get("word")  
            frequency = document.get("frequency")
            if word:
                self.possible_words[word] = frequency
            else:
                print("Warning: Document does not contain 'word' field:", document)


        #print(self.possible_words)

    def add_blacks(self, letter: str) -> None:
        self.blacks.add(letter)

    def add_yellows(self, letter: str, index: int) -> None:
        if letter in self.yellows:
            self.yellows[letter].append(index)
        else:
            self.yellows[letter] = [index];

    def add_greens(self, letter: str, index: int) -> None:
        if letter in self.yellows:
            del self.yellows[letter]
        self.greens[index] = letter

    def add_blacks_and_greens(self) -> None:
        # print("running add_blacks_and_greens!")
        # print("blacks at this time:", self.blacks)
        for letter in self.blacks:
            if letter in self.greens.values():
                self.black_and_greens.add(letter)

    def get_possible_words(self):
        new_possible_words = {}
        self.add_blacks_and_greens()
        for word in self.possible_words.keys():
            black_flag = False
            yellow_flag = True
            green_flag = True
            black_and_green_flag = False

            #filter blacks
            if self.blacks:
                contains_black_letter = False
                for letter in self.blacks:
                    if letter in word and letter not in self.black_and_greens: #word contains a black charater, do not add
                        contains_black_letter = True
                        break
                if not contains_black_letter:
                    black_flag = True
            else:
                black_flag = True

            #filter greens
            if self.greens:
                for index in self.greens:
                    try:
                        if word[index] != self.greens[index]:
                            green_flag = False
                            break
                    except KeyError:
                        pass


            #filter yellows
            if self.yellows:
                #make sure word contains yellow letter, but not in yellow position
                for letter, indices in self.yellows.items():
                    if letter not in word:
                        yellow_flag = False
                        break
                    for index in indices:
                        if word[index] == letter:
                            yellow_flag = False
                            break

            if self.black_and_greens:
                for letter in self.black_and_greens:
                    if word.count(letter) == list(self.greens.values()).count(letter):
                        black_and_green_flag = True

            #add word if all 4 flags are true
            if black_flag and green_flag and yellow_flag and black_and_green_flag:
                freq = self.possible_words[word]
                new_possible_words[word] = freq
            

        self.possible_words = new_possible_words
                    

    def print_all(self):
        print("blacks: ", self.blacks)
        print("yellows: ", self.yellows)
        print("greens: ", self.greens)
        print("blacks and greens: ", self.black_and_greens)

    def print_possible_words(self):
        print(self.possible_words)
