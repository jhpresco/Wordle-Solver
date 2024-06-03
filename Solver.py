import pymongo

def indexesOf(word: str, letter: chr) -> list:
    indexes = []
    for let in word:
        if let == letter:
            indexes.append(let)
    return indexes
    

class Solver:
    def __init__(self):
        self.blacks = []
        self.yellows = {}
        self.greens = {}
        self.possible_words = []
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["5_letter_words"]  
        self.collection = self.db["words"]  

        for document in self.collection.find():
            word = document.get("word")  # Extract the word field
            if word:
                self.possible_words.append(word)
            else:
                print("Warning: Document does not contain 'word' field:", document)

        #print(self.possible_words)

    def add_blacks(self, letter: str) -> None:
        self.blacks.append(letter)

    def add_yellows(self, letter: str, index: int) -> None:
        if letter in self.yellows:
            self.yellows[letter].append(index)
        else:
            self.yellows[letter] = [index];

    def add_greens(self, letter: str, index: int) -> None:
        if letter in self.yellows:
            del self.yellows[letter]
        self.greens[index] = letter

    def get_possible_words(self):
        new_possible_words = []
        for word in self.possible_words:
            black_flag = False
            yellow_flag = True
            green_flag = True

            #filter blacks
            if self.blacks:
                contains_black_letter = False
                for letter in self.blacks:
                    if letter in word: #word contains a black charater, do not add
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

            #add word if all 3 flags are true
            if black_flag and green_flag and yellow_flag:
                new_possible_words.append(word)
            

        self.possible_words = new_possible_words
                    

    def print_all(self):
        print("blacks: ", self.blacks)
        print("yellows: ", self.yellows)
        print("greens: ", self.greens)

    def print_possible_words(self):
        print(self.possible_words)
