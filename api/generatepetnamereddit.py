import re
import nltk
import emoji
import spacy
import nltk
import praw
from collections import Counter
from better_profanity import profanity
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

subreddits = ["aww", "Pets", "cats", "dogs", "PetsareAmazing", "Catswithjobs", "dogswithjobs"]
catsubreddits = ["aww", "Pets", "cats", "Catswithjobs"]
dogsubreddits = ["aww", "Pets", "dogs", "dogswithjobs"]

reddit = praw.Reddit(
    client_id='z_yeSt_azbvYgHBAeATnDw',
    client_secret='hFUlPqA13eu9QGSYuWTxl6UAkCHXKg',
    user_agent='script:petname generator:v1.0 (by u/YogurtclosetSharp745)',
    username='YogurtclosetSharp745 ',
    password='Auras123!'
)

def preprocess_text(text):

    # Eliminate emojis and other non-alphabetic characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Eliminate emojis
    emoji.demojize(text)

    # Convert numbers to words
    text = re.sub(r'\b\d+\b', lambda x: num2words(x.group()), text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|@\S+|#\S+', '', text)

    # Tokenize while preserving punctuation
    tokens = nltk.word_tokenize(text)

    # Optionally, remove stopwords and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    processed_tokens = []
    for word in tokens:
        # Check if the token is a punctuation or a useful word
        if word.isalpha():
            if word not in stop_words:
                # Lemmatize the word
                word = lemmatizer.lemmatize(word)
                processed_tokens.append(word)
        else:
            # Directly append punctuations and other non-alphabetic tokens
            processed_tokens.append(word)

    # Reconstruct the text
    preprocessed_text = ' '.join(processed_tokens)

    return preprocessed_text

def is_name(word, pos=False):
    if pos:
        pos_tag = nltk.pos_tag([word])
        #print(pos_tag)
        return pos_tag[0][1] == 'NNP'
    potential_name = nlp(word)
    if potential_name.ents:
        return "PERSON" in [ent.label_ for ent in potential_name.ents]
    else:
        return False


def find_popular_pet_names(reddit, pet_color1, pet_color2, pet_type="pet", two_colors=False, limit=100, pos=True):
    names_counter = Counter()

    chosen_subreddits = subreddits

    if pet_type == "cat":
        chosen_subreddits = catsubreddits
    elif pet_type == "dog":
        chosen_subreddits = dogsubreddits

    for subreddit_name in chosen_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        search_query = f"{pet_color1} {pet_color2}" if two_colors else f"{pet_color1}"
        for submission in subreddit.search(search_query, limit=limit):
            title = submission.title
            title = preprocess_text(title)
            words = title.split()
            for word in words:
                if is_name(word, pos=pos):
                    names_counter[word] += 1

    return names_counter


def get_pet_names(pet_color1, pet_color2, pet_type="pet", two_colors=False, limit=100, pos=True):
    popular_pet_names = find_popular_pet_names(reddit, pet_color1, pet_color2, pet_type=pet_type ,two_colors=two_colors, limit=limit, pos=pos)

    illegal_chars = ".,/;'[]{}|<>?:\"\\=+_)(*&^%$#@!`~-"

    for name in list(popular_pet_names.keys()):
        if any(char in name for char in illegal_chars):
            popular_pet_names.pop(name)

    popular_pet_names.pop("OC", None)
    popular_pet_names.pop("Idiot", None)

    names = []

    for name in list(popular_pet_names.keys()):
        if profanity.contains_profanity(name):
            popular_pet_names.pop(name)
        else:
            names.append(name.title())

    print(pet_type)

    print(names)

    return list(names)


if __name__ == '__main__':
    pet_color1 = "white"
    pet_color2 = "black"
    popular_pet_names = get_pet_names(pet_color1, pet_color2, pet_type="dog", two_colors=True, limit=100, pos=False)
    print(popular_pet_names)
    print(len(popular_pet_names))
    print("Done!")

    