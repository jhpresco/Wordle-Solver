import nltk
import pymongo
from tqdm import tqdm
from Solver import Solver

def createDatabase():
    mydb = myclient["5_letter_words"]
    mycol = mydb["words"]
    nltk.download('words')
    english_words = nltk.corpus.words.words()
    five_letter_words = [word.lower() for word in english_words if len(word) == 5]
    for word in tqdm(five_letter_words, desc = "Creating Database", colour = "WHITE"):
        mycol.insert_one({"word": word})

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydatabases = myclient.list_database_names()
    if "5_letter_words" not in mydatabases:
        createDatabase()
    solver = Solver()
    print("There are now", len(solver.possible_words), "possible words!")

    #main loop    
    while True:
        guess = input("What word would you like to guess?\n>")
        key = input("How did it do?\n>") #a string of 5 characters consisting of b for black g for green and y for yellow
        for i in range(len(key)):
            if key[i] == 'b':
                solver.add_blacks(guess[i])
            if key[i] == 'y':
                solver.add_yellows(guess[i], i)
            if key[i] == 'g':
                solver.add_greens(guess[i], i)
        solver.get_possible_words()
        print("There are now", len(solver.possible_words), "possible words!")
        if len(solver.possible_words) <= 10000:
            solver.print_possible_words()
        if len(solver.possible_words) == 1:
            print("You win!")
            break
        if len(solver.possible_words) <= 0:
            print("Error: No possible words. Something went wrong")
            break
        #solver.print_all()