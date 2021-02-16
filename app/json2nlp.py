import re
import gensim
import fileinput
import collections

from process_json import *
from nlp_extraction import *
from nlp_extraction import _run_article_summary
from operator import itemgetter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stopwords = stopwords.words('english')
model = gensim.models.Word2Vec.load("word2vec")
stemmer = PorterStemmer()


def tokenize(input_text):
    text = str(input_text).lower()
    text = re.sub('[^A-Za-z0-9\s]+', '', text)
    return text.split()


def remove_stopwords(input_text):
    text = [word for word in input_text if not (word in stopwords)]
    return text


def stemming(input_text):
    text = [stemmer.stem(word) for word in input_text]
    return text


def cleaning(input_text):
    text = stemming(remove_stopwords(tokenize(input_text)))
    return text


def frequency(text, n=5):
    text_ = cleaning(text)
    model.train(text_, total_examples=len(text_), epochs=model.epochs)
    freq = collections.Counter(text_)
    importance = {}
    for word in freq.keys():
        importance_ = freq[word]
        try:
            synonyms = model.wv.most_similar(word, topn=30)
            for synonym in synonyms:
                try:
                    importance_ += freq[synonym[0]]
                except:
                    pass
        except:
            pass
        importance[word] = importance_

    try:
        return '\\n'.join(dict(sorted(importance.items(), key=itemgetter(1), reverse=True)[:n]).keys())
    except:
        return '\\n'.join(dict(sorted(importance.items(), key=itemgetter(1), reverse=True)).keys())


def json2nlp(file_name, nlp_type="KeyConcept"):
    """
    Function that takes a json file as input and summarizes its plain_text content.
    Parameters:
        - filename: json file path that will be modified (a backup is also created)
    Right now there is only one function that summarizes but you can easily change with your own.
    """
    if nlp_type == "KeyConcept":
        nlp_func = frequency
    elif nlp_type == "KeySentence":
        nlp_func = _run_article_summary
    elif nlp_type == "KeyWord":
        nlp_func = extract_kw_rake


    with open(file_name) as f_json:
        data = json.load(f_json)

    # we don't care about the beginning of the file
    json_slides = data['document_content']

    # getting the slide elements
    slide_elements = []
    breakdown_json(json_slides, slide_elements)

    # here we will put the best nlp function (14/02 _run_article_summary)
    # just change with your function (str as input and nlp str as output)
    nlp_sentences = {}
    for item in retrieve_content(slide_elements):  # get only the plain_text from the slide elements
        nlp_sentences[item[0]] = nlp_func(item[0])  # perform nlp on the plain_text

    # write nlp sentences into the file
    # creates a backup file just in case
    for in_sentence, out_sentence in nlp_sentences.items():
        with fileinput.FileInput(file_name, inplace=True, backup='.bak', mode="r") as nlp_file:
            for line in nlp_file:
                if in_sentence in line:
                    print(line.replace(in_sentence, out_sentence), end='')
                else:
                    print(line, end='')

    return file_name
