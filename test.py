import nltk
from nltk.corpus import words, brown
from collections import Counter

nltk.download('words')
nltk.download('brown')

# Get all English words
english_words = words.words()

# Filter five-letter words
five_letter_words = [word.lower() for word in english_words if len(word) == 5]

# Get word frequencies from the Brown corpus
brown_words = brown.words()
brown_freq = Counter(word.lower() for word in brown_words)
print(type(brown_freq))

# Create a dictionary with five-letter words and their frequencies
five_letter_word_freq = {word: brown_freq[word] for word in five_letter_words}

# Sort words by frequency
sorted_words = sorted(five_letter_word_freq.items(), key=lambda item: item[1], reverse=True)

# Display the top 10 most common five-letter words
for word, freq in sorted_words[:10]:
    print(f"{word}: {freq}")
