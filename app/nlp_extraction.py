# importing libraries
# https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
import nltk

from nltk import pos_tag
from rake_nltk import Rake
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from gensim.summarization import keywords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


 ########################################################################
#    Functions extracting sentences with importance above a threshold    #
 ########################################################################

def _create_dictionary_table(text_string) -> dict:
    # removing stop words
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(text_string)

    # reducing words to their root form
    stem = PorterStemmer()

    # creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    # algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> int:
    # calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


def _run_article_summary(article):
    """
    Function that extract sentences above a calculated threshold.
    Parameters:
        - article: string with your text
    """
    # creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(article)

    # tokenizing the sentences
    sentences = sent_tokenize(article)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    # getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, threshold)

    return article_summary


 ######################
#    Using Rake Lib    #
 ######################

def extract_kw_rake(article, n=5):
    """
    Function that extract keywords from some text
    Parameters:
        - article: string with your text
        - n (optional int): number of keywords extracted
    """
    r = Rake()
    r.extract_keywords_from_text(article)
    return "\\n".join(r.get_ranked_phrases()[0:n])


 #######################
#    Using gensim lib   #
 #######################

def keywords_gensim(article, ratio=False, n=5):
    """
    Function that extract keywords from some text
    Parameters:
        - article: string with your text
        - ratio (optional bool): if true, the function will return 20% of the keywords
        - n (optional int): number of keywords extracted
    """
    if ratio:
        return keywords(article, ratio, lemmatize=True)
    return keywords(article, words=n, lemmatize=True)


 ###################################
#    Using nltk and sklearn libs    #
 ###################################

def extract_nltk_sklearn(article):
    """
    Function that extract keywords from some text
    Parameters:
        - article: string with your text
    """
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    text = tokenizer.tokenize(article.lower())
    stopWords = stopwords.words('english')
    text = [w for w in text if not w in stopWords]
    tag_map = defaultdict(lambda: wordnet.NOUN)
    tag_map['J'] = wordnet.ADJ
    tag_map['V'] = wordnet.VERB
    tag_map['R'] = wordnet.ADV

    lemmatizer = WordNetLemmatizer()
    words = []

    for token, tag in pos_tag(text):
        words.append(lemmatizer.lemmatize(token, tag_map[tag[0]]))

    text = words
    vectorizer = TfidfVectorizer()

    vectorizer.fit_transform(text)
    return "\\n".join(vectorizer.get_feature_names())
