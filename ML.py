import pandas as pd
from sklearn.model_selection import train_test_split
import nltk
import string
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score, precision_recall_curve
from matplotlib import pyplot as plt
from sklearn.metrics import plot_precision_recall_curve
import numpy as np
from sklearn.model_selection import GridSearchCV
import json

chosen_id = []

def Maximazer(role):
    with open("marked_news_{0}.json".format(role), encoding="utf-8") as file:
        all_marked_news = json.load(file)

    with open("news.json", encoding="utf-8") as file:
        news = json.load(file)

    important_1 = 0
    important_2 = 0
    important_3 = 0
    index_1 = 0
    index_2 = 0
    index_3 = 0
    for index7 in range(0, len(all_marked_news)):
        if important_1 <= all_marked_news[index7] and index7 not in chosen_id:
            important_3 = important_2
            index_3 = index_2
            important_2 = important_1
            index_2 = index_1
            important_1 = all_marked_news[index7]
            index_1 = index7

    chosen_id.append(index_1)
    chosen_id.append(index_2)
    chosen_id.append(index_3)
    important_news = [news[index_1], news[index_2], news[index_3]]
    with open("{0}.json".format(role), "w", encoding="utf-8") as file:
        json.dump(important_news, file, indent=4, ensure_ascii=False)
    


optimizer = 'adam'

def MLY(role):
    df = pd.read_csv("newsTitles_director.csv", sep=",", encoding="utf-8")



    df["value"] = df["value"].apply(int)

    if role == "accountant":
        train_df, test_df = train_test_split(df, test_size=400)

    if role == "director":
        train_df, test_df = train_test_split(df, test_size=700)



    sentence_example = df.iloc[1]["news"]

    snowball = SnowballStemmer(language="russian")
    russian_stop_words = stopwords.words("russian")


    def tokenize_sentence(sentence: str, remove_stop_words: bool = True):
        tokens = word_tokenize(sentence, language="russian")
        tokens = [i for i in tokens if i not in string.punctuation]
        if remove_stop_words:
            tokens = [i for i in tokens if i not in russian_stop_words]
        tokens = [snowball.stem(i) for i in tokens]
        return tokens



    vectorizer = TfidfVectorizer(tokenizer=lambda x: tokenize_sentence(x, remove_stop_words=True))

    features = vectorizer.fit_transform(train_df["news"])

    model = LogisticRegression(random_state=0)
    model.fit(features, train_df["value"])



    model_pipeline = Pipeline([
        ("vectorizer", TfidfVectorizer(tokenizer=lambda x: tokenize_sentence(x, remove_stop_words=True))),
        ("model", LogisticRegression(random_state=0))
    ]
    )


    with open("newsTitles.json", encoding="utf-8") as file:
        all_news = json.load(file)

    model_pipeline.fit(train_df["news"], train_df["value"])



    marked_news = []
    for x in all_news:
        rr = int(model_pipeline.predict([x])[0])
        marked_news.append(rr)

    with open("marked_news_{0}.json".format(role), "w", encoding="utf-8") as file:
        json.dump(marked_news, file, indent=4, ensure_ascii=False)

    Maximazer(role)


if __name__ == '__main__':
    MLY("director")
    MLY("accountant")


