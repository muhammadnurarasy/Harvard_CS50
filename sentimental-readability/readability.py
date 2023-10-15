# TODO
def count_letters(text):
    return sum(c.isalpha() for c in text)

def count_words(text):
    return sum(c.isspace() for c in text) + 1 if text else 0

def count_sentences(text):
    return sum(c in ".!?" for c in text)

text = input("Text: ")
letter = count_letters(text)
word = count_words(text)
sentence = count_sentences(text)

if word == 0:  # Handle empty string edge case
    print("Before Grade 1")
else:
    L = (letter / word) * 100
    S = (sentence / word) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")
